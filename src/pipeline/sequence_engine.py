
# #sequence_engine.py
# import time
# import queue
# import traceback
# from src.algorithms.ai_inference import AIInferenceEngine
# from src.algorithms.cv_processor import CVProcessor
# from src.communication.modbus_client import PLCModbusClient

# def flush_queue(q):
#     """Xả sạch frame rác/xung dội còn đọng lại trong queue."""
#     while True:
#         try:
#             q.get_nowait()
#         except (queue.Empty, Exception):
#             break

# def inspection_manager_process(q_cam1, q_cam2, res_queue, stop_event, cmd_cam1, timeout_sec=10.0):
#     ai_engine = AIInferenceEngine()
#     cv_proc = CVProcessor()
#     modbus = PLCModbusClient(ip="192.168.1.50", port=502)

#     current_step = 0
#     cycle_start_time = None
#     step_results = {}

#     def reset_fsm():
#         nonlocal current_step, cycle_start_time, step_results
#         current_step = 0
#         cycle_start_time = None
#         step_results = {}
#         flush_queue(q_cam1)
#         flush_queue(q_cam2)

#     print("🚀 [FSM] Sequence Engine đã sẵn sàng.")
#     reset_fsm()

#     while not stop_event.is_set():
#         # -------------------------------------------------------------
#         # 1. WATCHDOG TIMEOUT CHECK
#         # -------------------------------------------------------------
#         if current_step > 0 and cycle_start_time is not None:
#             if (time.time() - cycle_start_time) > timeout_sec:
#                 print(f"❌ [TIMEOUT] Quá {timeout_sec}s -> Phán định NG & Reset!")


#                 # print(f"❌ [TIMEOUT] Quá {timeout_sec}s -> Kích chân Line0 NG & Reset!")
#                 # # 👉 Kích chân Line0 sáng đèn trong 1s
#                 # cmd_cam1.put("PULSE_NG")


#                 modbus.send_inspection_result(result_code=3)  # 3: Timeout NG
#                 res_queue.put({"type": "RESULT", "status": "TIMEOUT_NG", "data": step_results})
#                 reset_fsm()
#                 continue

#         # -------------------------------------------------------------
#         # 2. BƯỚC 1: Cam 1 - Đèn 1 - AI 1
#         # -------------------------------------------------------------
#         if current_step == 0:
#             flush_queue(q_cam2)
#             try:
#                 data = q_cam1.get(timeout=0.05)
#                 cam_id, frame = data if isinstance(data, tuple) else (0, data)

#                 cycle_start_time = time.time()
#                 ok1, msg1, ann1 = ai_engine.run_ai_1(frame)
#                 step_results['step1'] = ok1

#                 res_queue.put({
#                     "type": "FRAME",
#                     "cam_id": 1,
#                     "image": ann1,
#                     "step": 0,
#                     "ok": ok1
#                 })
#                 current_step = 1

#             except queue.Empty:
#                 pass
#             except Exception as e:
#                 print(f"❌ [LỖI BƯỚC 1]: {e}")
#                 traceback.print_exc()


#         elif current_step == 1:
#             try:
#                 data = q_cam1.get(timeout=0.05)
#                 cam_id, frame = data if isinstance(data, tuple) else (0, data)

#                 print("-> Đã nhận ảnh Bước 2 từ q_cam1")

#                 # 1. Chạy AI 2 trên ảnh gốc
#                 ok2_ai, msg2_ai, ann2_ai = ai_engine.run_ai_2(frame)
                
#                 # 2. Chạy OpenCV kiểm tra độ nghiêng chữ với bộ tham số thực tế đã calibrate
#                 ok2_cv, ratio_val, deskew_annotated = CVProcessor.measure_alignment(
#                     frame=frame,
#                     thresh_rotate=174,
#                     blur_k=5,
#                     spacing=400,
#                     scan_dir=1,
#                     thresh_letters=154,
#                     min_char_area=2180,
#                     max_char_area=50000,
#                     min_char_h=15,
#                     max_ratio_limit=1.2
#                 )
                
#                 step_results['step2'] = (ok2_ai and ok2_cv)

#                 # 3. Đẩy lên UI
#                 res_queue.put({
#                     "type": "FRAME",
#                     "cam_id": 1,
#                     "image": ann2_ai,
#                     "thresh_image": deskew_annotated,  # Ảnh đã xoay phẳng và vẽ kết quả đo h/L
#                     "step": 1,
#                     "ok": step_results['step2'],
#                     "ratio": ratio_val
#                 })
#                 current_step = 2

#             except queue.Empty:
#                 pass
#             except Exception as e:
#                 print(f"❌ [LỖI BƯỚC 2]: {e}")
#                 traceback.print_exc()

#         # -------------------------------------------------------------
#         # 4. BƯỚC 3: Cam 2 - Đèn 3 - AI 3 -> TỔNG HỢP PHÁN ĐỊNH
#         # -------------------------------------------------------------
#         elif current_step == 2:
#             try:
#                 data = q_cam2.get(timeout=0.05)
#                 cam_id, frame = data if isinstance(data, tuple) else (1, data)

#                 ok3, msg3, ann3 = ai_engine.run_ai_3(frame)
#                 step_results['step3'] = ok3

#                 res_queue.put({
#                     "type": "FRAME",
#                     "cam_id": 2,
#                     "image": ann3,
#                     "step": 2,
#                     "ok": ok3
#                 })

#                 # 👉 IN CHI TIẾT TỪNG BƯỚC ĐỂ BẮT ĐÍCH DANH BƯỚC NÀO BỊ FALSE:
#                 print(f"📊 [DEBUG TRẠNG THÁI] Step 1: {step_results.get('step1')} | Step 2: {step_results.get('step2')} | Step 3: {step_results.get('step3')}")

#                 # Tổng hợp kết quả toàn chu trình
#                 final_status = all(step_results.values())
#                 result_code = 1 if final_status else 2


#                 if final_status:
#                     print("✅ [RESULT: OK] -> Bắn xung kích chân Line0 1s!")
#                     if cmd_cam1 is not None:
#                         cmd_cam1.put("PULSE_NG")  # Lệnh này gọi trigger_ng_pulse (bật chân Line0 1s)
#                 else:
#                     print("⚠️ [RESULT: NG] -> Không kích Output.")


#                 modbus.send_inspection_result(result_code=result_code)

#                 res_queue.put({
#                     "type": "RESULT",
#                     "status": "OK" if final_status else "NG",
#                     "data": step_results
#                 })
#                 print(f"🏁 === KẾT QUẢ CHU KỲ: {'OK' if final_status else 'NG'} ===")

#                 # time.sleep(10000)
#                 reset_fsm()


#             except queue.Empty:
#                 pass
#             except Exception as e:
#                 print(f"❌ [LỖI BƯỚC 3]: {e}")
#                 traceback.print_exc()

#     modbus.close()

















import cv2
import time
import queue
import traceback
from src.algorithms.ai_inference import AIInferenceEngine
from src.algorithms.cv_processor import CVProcessor
from src.communication.modbus_client import PLCModbusClient

def flush_queue(q):
    """Xả sạch frame đọng lại trong queue."""
    while True:
        try:
            q.get_nowait()                                                                                                                                
        except (queue.Empty, Exception):
            break

def inspection_manager_process(q_cam1, q_cam2, res_queue, stop_event, cmd_cam1 ,rule_queue=None, timeout_sec=1.4):
    ai_engine = AIInferenceEngine()
    cv_proc = CVProcessor()
    modbus = PLCModbusClient(ip="192.168.1.100", port=502)

    current_step = 0
    cycle_start_time = None
    step_results = {}

    def reset_fsm():
        nonlocal current_step, cycle_start_time, step_results
        current_step = 0
        cycle_start_time = None
        step_results = {}
        flush_queue(q_cam1)
        flush_queue(q_cam2)

    print("🚀 [FSM] Sequence Engine (2 Shot Mode) đã sẵn sàng.")
    reset_fsm()

    while not stop_event.is_set():

        # Lấy bản tin mới nhất, bỏ qua các bản tin cũ nếu có nhiều
        latest_rules = None
        while rule_queue is not None and not rule_queue.empty():
            try:
                latest_rules = rule_queue.get_nowait()
            except queue.Empty:
                break
        
        # Chỉ cập nhật 1 lần duy nhất với giá trị cuối cùng
        if latest_rules is not None:
            ai_engine.update_rules_from_dict(latest_rules)
        # -------------------------------------------------------------
        # 1. WATCHDOG TIMEOUT CHECK
        # -------------------------------------------------------------
        if current_step > 0 and cycle_start_time is not None:
            if (time.time() - cycle_start_time) > timeout_sec:
                print(f"❌ [TIMEOUT] Quá {timeout_sec}s -> Phán định NG & Reset!")

                # 👉 Timeout cũng phán định là NG -> Ghi D138 = 2
                modbus.send_inspection_result(result_code=2, reg_addr=138)

                res_queue.put({"type": "RESULT", "status": "TIMEOUT_NG", "data": step_results})
                reset_fsm()
                continue

        # -------------------------------------------------------------
        # 2. CHỤP LẦN 1: CAM 1 -> Chạy AI 1 + Đo góc OpenCV
        # -------------------------------------------------------------
        if current_step == 0:
            flush_queue(q_cam2)
            try:
                data = q_cam1.get(timeout=0.05)
                cam_id, frame = data if isinstance(data, tuple) else (0, data)

                # #luu 1 anh vua chup vao folder, ten theo chuan the nay Image_20260922083847489.png
                # timestamp = time.strftime("%Y%m%d%H%M%S")
                # image_name = f"Image_{timestamp}.png"
                # cv2.imwrite(f"anh_them_c1/{image_name}", frame)


                cycle_start_time = time.time()

                # a. Chạy AI 1 (UNet lỗi bề mặt)
                ok1_ai, msg1_ai, ann1_ai = ai_engine.run_ai_1(frame)

                # Danh sách giới hạn pixel cho từng ký tự (hoặc để None để dùng CVProcessor.DEFAULT_CHAR_PIXEL_LIMITS)
                char_pixel_limits = [
                    (11000, 15000),  # Ký tự 1 ('S'): ~13.2k - 14.0k
                    (12000, 15200),  # Ký tự 2 ('A'): ~13.6k - 14.2k
                    (21000, 25200),  # Ký tự 3 ('M'): ~22.8k - 23.8k
                    (11000, 15200),  # Ký tự 4 ('S'): ~13.6k - 14.2k
                    (12000, 16200),  # Ký tự 5 ('U'): ~14.2k - 14.9k
                    (15000, 19200),  # Ký tự 6 ('N'): ~17.3k (NG lem sơn lên >20k)
                    (11000, 15200),  # Ký tự 7 ('G'): ~13.6k - 14.2k
                ]

                ok1_cv, ratio_val, deskew_annotated, char_inspect_img = CVProcessor.measure_alignment(
                    frame=frame,
                    thresh_rotate=50,       # Theo hình trackbar: 49
                    blur_k=5,               # Theo hình trackbar: 5
                    spacing=400,            # Theo hình trackbar: 170
                    thresh_letters=150,     # Theo hình trackbar: 150
                    min_char_area=10000,    # Ngưỡng pixel tối thiểu chung
                    max_char_area=24000,    # Ngưỡng pixel tối đa chung
                    min_char_h=15,          # Chiều cao ký tự tối thiểu
                    min_char_w=90,          # Chiều rộng tối thiểu của ký tự
                    max_char_w=210,         # Chiều rộng tối đa của ký tự (nhận đủ 7 ký tự)
                    max_ratio_limit=1.2,    # Tỉ lệ nghiêng tối đa (%)
                    expected_char_count=7,  # Số ký tự: 7 contours
                    char_pixel_limits=char_pixel_limits  # Tuỳ chỉnh khoảng pixel hợp lệ cho từng ký tự
                )

                step_results['step1'] = (ok1_ai and ok1_cv)
                print(f"📊 [LẦN 1 CHI TIẾT] AI 1: {'OK' if ok1_ai else 'NG'} ({msg1_ai}) | Đo góc & Ký tự CV: {'OK' if ok1_cv else 'NG'} (ratio={ratio_val}) => Lần 1: {'OK' if step_results['step1'] else 'NG'}")

                # Gửi toàn bộ dữ liệu lần 1 lên UI hiển thị vào 3 khung
                res_queue.put({
                    "type": "FRAME_STEP1",
                    "ai_image": ann1_ai,                  # Khung 1: Ảnh kết quả AI 1
                    "bin_vis_image": char_inspect_img,    # Khung 2: Ảnh kiểm tra 6 contour và pixel ký tự (thay cho ảnh binarization cũ)
                    "deskew_image": deskew_annotated,     # Khung 3: Ảnh gốc vẽ kết quả đo góc
                    "ratio": ratio_val,
                    "ok": step_results['step1']
                })

                current_step = 1

            except queue.Empty:
                pass
            except Exception as e:
                print(f"❌ [LỖI CHỤP LẦN 1]: {e}")
                traceback.print_exc()

        # -------------------------------------------------------------
        # 3. CHỤP LẦN 2: CAM 2 -> Chạy AI 3 & Tổng hợp toàn chu trình
        # -------------------------------------------------------------
        elif current_step == 1:
            try:
                data = q_cam2.get(timeout=0.05)
                cam_id, frame = data if isinstance(data, tuple) else (1, data)

                # #luu 1 anh vua chup vao folder, ten theo chuan the nay Image_20260922083847489.png
                # timestamp = time.strftime("%Y%m%d%H%M%S")
                # image_name = f"Image_{timestamp}.png"
                # cv2.imwrite(f"anh_them_c2/{image_name}", frame)

                # Chạy AI 3 (Model kiểm tra Cam 2)
                ok2_ai, msg2_ai, ann2_ai = ai_engine.run_ai_3(frame)
                step_results['step2'] = ok2_ai
                print(f"📊 [LẦN 2 CHI TIẾT] AI 3: {'OK' if ok2_ai else 'NG'} ({msg2_ai}) => Lần 2: {'OK' if ok2_ai else 'NG'}")

                # Gửi ảnh lần 2 lên UI (Khung 4)
                res_queue.put({
                    "type": "FRAME_STEP2",
                    "image": ann2_ai,
                    "ok": ok2_ai
                })

                # Tổng hợp kết quả
                final_status = all(step_results.values())

                # 👉 OK: D138 = 1 | NG: D138 = 2
                result_code = 1 if final_status else 2

                print(f"📊 [KẾT QUẢ] Lần 1 (AI1+Góc): {step_results.get('step1')} | Lần 2 (AI3): {step_results.get('step2')}")

                # Gửi kết quả vào D138 qua Modbus TCP
                modbus.send_inspection_result(result_code=result_code, reg_addr=138)

                res_queue.put({
                    "type": "RESULT",
                    "status": "OK" if final_status else "NG",
                    "data": step_results
                })
                print(f"🏁 === HOÀN THÀNH CHU KỲ: {'OK (D138=1)' if final_status else 'NG (D138=2)'} ===\n")

                reset_fsm()

            except queue.Empty:
                pass
            except Exception as e:
                print(f"❌ [LỖI CHỤP LẦN 2]: {e}")
                traceback.print_exc()
