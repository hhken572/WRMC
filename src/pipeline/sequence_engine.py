# import time
# from src.algorithms.ai_inference import AIInferenceEngine
# from src.algorithms.cv_processor import CVProcessor
# from src.communication.modbus_client import PLCModbusClient
# import traceback
# import queue
# def inspection_manager_process(q_cam1, q_cam2, res_queue, stop_event, timeout_sec=3.0):
#     ai_engine = AIInferenceEngine()
#     cv_proc = CVProcessor()
#     modbus = PLCModbusClient(ip="192.168.1.50", port=502)

#     current_step = 0
#     cycle_start_time = None
#     step_results ={}
    
    
#     def reset_fsm():
#         nonlocal current_step, cycle_start_time, step_results
#         current_step = 0
#         cycle_start_time = None
#         step_results = {}

#     print("🚀 [FSM] Sequence Engine đã sẵn sàng.")

#     while not stop_event.is_set():
#         # Kiểm tra Timeout khi đang ở giữa các bước
#         if current_step > 0 and cycle_start_time is not None:
#             if (time.time() - cycle_start_time) > timeout_sec:
#                 print(f"❌ [TIMEOUT] Rớt bước quá {timeout_sec}s -> Phát định NG!")
#                 modbus.send_inspection_result(result_code=3)  # 3: Timeout NG
#                 res_queue.put({"type": "RESULT", "status": "TIMEOUT_NG", "data": step_results})
#                 reset_fsm()
#                 continue

#         # BƯỚC 1: Cam 1 - Đèn 1 - AI 1
#         if current_step == 0:
#             try:
#                 cam_id, frame = q_cam1.get(timeout=0.05)
#                 print("3 - Sequence Engine đã nhận ảnh Bước 1 từ q_cam1")
#                 cycle_start_time = time.time()
#                 ok1, msg1, ann1 = ai_engine.run_ai_1(frame)
#                 step_results['step1'] = ok1
#                 res_queue.put({"type": "FRAME", "cam_id": 1, "image": ann1, "step": 0, "ok": ok1})
#                 print("3.1 - Đã push FRAME Bước 1 vào res_queue")
#                 frame = None
#                 if q_cam1.empty():
#                     print("Queue đang rỗng, chưa có ảnh nào.")
#                 else:
#                     print("Trong queue đang có ảnh!")
#                 current_step = 1
#             except: pass

#         # BƯỚC 2: Cam 1 - Đèn 2 - AI 2 + OpenCV
#         elif current_step == 1:
#             try:
#                 data = q_cam1.get(timeout=0.05)
#                 if isinstance(data, tuple):
#                     cam_id, frame = data
#                 else:
#                     frame = data

#                 # 1. Chạy AI2
#                 ok2_ai, _, ann2 = ai_engine.run_ai_2(frame)
                
#                 # 2. Chạy OpenCV lấy cả ảnh kết quả và ảnh nhị phân
#                 ok2_cv, area_val, ann2_final, thresh_img = cv_proc.measure_area(ann2)
#                 step_results['step2'] = (ok2_ai and ok2_cv)

#                 # Gửi cả ảnh gốc đã vẽ và ảnh nhị phân lên GUI
#                 res_queue.put({
#                     "type": "FRAME",
#                     "step": 1,                     # Bước 2 (index 1)
#                     "image": ann2_final,          # Ảnh gốc + vẽ contour
#                     "thresh_image": thresh_img,   # Ảnh nhị phân (Grayscale/Binary)
#                     "ok": step_results['step2']
#                 })
#                 current_step = 2
#             except queue.Empty:
#                 pass
#             except Exception as e:
#                 print(f"❌ [LỖI TẠI BƯỚC 2]: {e}")

#         # BƯỚC 3: Cam 2 - Đèn 3 - AI 3
#         elif current_step == 2:
#             try:
#                 cam_id, frame = q_cam2.get(timeout=0.05)
#                 ok3, msg3, ann3 = ai_engine.run_ai_3(frame)
#                 step_results['step3'] = ok3
#                 res_queue.put({"type": "FRAME", "cam_id": 2, "image": ann3, "step": 3, "ok": ok3})

#                 # TỔNG HỢP KẾT QUẢ
#                 final_status = all(step_results.values())
#                 result_code = 1 if final_status else 2
#                 modbus.send_inspection_result(result_code=result_code)

#                 res_queue.put({
#                     "type": "RESULT",
#                     "status": "OK" if final_status else "NG",
#                     "data": step_results
#                 })
#                 reset_fsm()
#             except: pass

#     modbus.close()
















import time
import queue
import traceback
from src.algorithms.ai_inference import AIInferenceEngine
from src.algorithms.cv_processor import CVProcessor
from src.communication.modbus_client import PLCModbusClient

def flush_queue(q):
    """Xả sạch frame rác/xung dội còn đọng lại trong queue."""
    while True:
        try:
            q.get_nowait()
        except (queue.Empty, Exception):
            break

def inspection_manager_process(q_cam1, q_cam2, res_queue, stop_event, cmd_cam1, timeout_sec=10.0):
    ai_engine = AIInferenceEngine()
    cv_proc = CVProcessor()
    modbus = PLCModbusClient(ip="192.168.1.50", port=502)

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

    print("🚀 [FSM] Sequence Engine đã sẵn sàng.")
    reset_fsm()

    while not stop_event.is_set():
        # -------------------------------------------------------------
        # 1. WATCHDOG TIMEOUT CHECK
        # -------------------------------------------------------------
        if current_step > 0 and cycle_start_time is not None:
            if (time.time() - cycle_start_time) > timeout_sec:
                print(f"❌ [TIMEOUT] Quá {timeout_sec}s -> Phán định NG & Reset!")


                # print(f"❌ [TIMEOUT] Quá {timeout_sec}s -> Kích chân Line0 NG & Reset!")
                # # 👉 Kích chân Line0 sáng đèn trong 1s
                # cmd_cam1.put("PULSE_NG")


                modbus.send_inspection_result(result_code=3)  # 3: Timeout NG
                res_queue.put({"type": "RESULT", "status": "TIMEOUT_NG", "data": step_results})
                reset_fsm()
                continue

        # -------------------------------------------------------------
        # 2. BƯỚC 1: Cam 1 - Đèn 1 - AI 1
        # -------------------------------------------------------------
        if current_step == 0:
            flush_queue(q_cam2)
            try:
                data = q_cam1.get(timeout=0.05)
                cam_id, frame = data if isinstance(data, tuple) else (0, data)

                cycle_start_time = time.time()
                ok1, msg1, ann1 = ai_engine.run_ai_1(frame)
                step_results['step1'] = ok1

                res_queue.put({
                    "type": "FRAME",
                    "cam_id": 1,
                    "image": ann1,
                    "step": 0,
                    "ok": ok1
                })
                current_step = 1

            except queue.Empty:
                pass
            except Exception as e:
                print(f"❌ [LỖI BƯỚC 1]: {e}")
                traceback.print_exc()

        # -------------------------------------------------------------
        # BƯỚC 2: Cam 1 - Đèn 2 - Tách biệt AI 2 và OpenCV
        # -------------------------------------------------------------
        # elif current_step == 1:
        #     try:
        #         data = q_cam1.get(timeout=0.05)
        #         cam_id, frame = data if isinstance(data, tuple) else (0, data)

        #         print("-> Đã nhận ảnh Bước 2 từ q_cam1")

        #         # 1. Chạy AI 2 trên ảnh gốc -> Ra ảnh ann2 có vẽ kết quả AI
        #         ok2_ai, msg2_ai, ann2_ai = ai_engine.run_ai_2(frame)
                
        #         # 2. Chạy OpenCV trên ảnh GỐC (frame) -> Trả về ảnh nhị phân đã vẽ kết quả CV
        #         ok2_cv, area_val, thresh_annotated = CVProcessor.measure_area(frame)
                
        #         step_results['step2'] = (ok2_ai and ok2_cv)

        #         # 3. Đẩy lên UI:
        #         # - 'image': Ảnh màu có kết quả AI2
        #         # - 'thresh_image': Ảnh nhị phân có vẽ contour và text kết quả CV
        #         res_queue.put({
        #             "type": "FRAME",
        #             "cam_id": 1,
        #             "image": ann2_ai,
        #             "thresh_image": thresh_annotated,
        #             "step": 1,
        #             "ok": step_results['step2']
        #         })
        #         current_step = 2

        elif current_step == 1:
            try:
                data = q_cam1.get(timeout=0.05)
                cam_id, frame = data if isinstance(data, tuple) else (0, data)

                print("-> Đã nhận ảnh Bước 2 từ q_cam1")

                # 1. Chạy AI 2 trên ảnh gốc
                ok2_ai, msg2_ai, ann2_ai = ai_engine.run_ai_2(frame)
                
                # 2. Chạy OpenCV kiểm tra độ nghiêng chữ với bộ tham số thực tế đã calibrate
                ok2_cv, ratio_val, deskew_annotated = CVProcessor.measure_alignment(
                    frame=frame,
                    thresh_rotate=174,
                    blur_k=5,
                    spacing=400,
                    scan_dir=1,
                    thresh_letters=154,
                    min_char_area=2180,
                    max_char_area=50000,
                    min_char_h=15,
                    max_ratio_limit=1.2
                )
                
                step_results['step2'] = (ok2_ai and ok2_cv)

                # 3. Đẩy lên UI
                res_queue.put({
                    "type": "FRAME",
                    "cam_id": 1,
                    "image": ann2_ai,
                    "thresh_image": deskew_annotated,  # Ảnh đã xoay phẳng và vẽ kết quả đo h/L
                    "step": 1,
                    "ok": step_results['step2'],
                    "ratio": ratio_val
                })
                current_step = 2

            except queue.Empty:
                pass
            except Exception as e:
                print(f"❌ [LỖI BƯỚC 2]: {e}")
                traceback.print_exc()

        # -------------------------------------------------------------
        # 4. BƯỚC 3: Cam 2 - Đèn 3 - AI 3 -> TỔNG HỢP PHÁN ĐỊNH
        # -------------------------------------------------------------
        elif current_step == 2:
            try:
                data = q_cam2.get(timeout=0.05)
                cam_id, frame = data if isinstance(data, tuple) else (1, data)

                ok3, msg3, ann3 = ai_engine.run_ai_3(frame)
                step_results['step3'] = ok3

                res_queue.put({
                    "type": "FRAME",
                    "cam_id": 2,
                    "image": ann3,
                    "step": 2,
                    "ok": ok3
                })

                # 👉 IN CHI TIẾT TỪNG BƯỚC ĐỂ BẮT ĐÍCH DANH BƯỚC NÀO BỊ FALSE:
                print(f"📊 [DEBUG TRẠNG THÁI] Step 1: {step_results.get('step1')} | Step 2: {step_results.get('step2')} | Step 3: {step_results.get('step3')}")

                # Tổng hợp kết quả toàn chu trình
                final_status = all(step_results.values())
                result_code = 1 if final_status else 2


                # # 👉 NẾU NG -> GỬI LỆNH KÍCH CHÂN LINE0 CAM 20MP TRONG 1S
                # if not final_status:
                #     print("⚠️ [RESULT: NG] -> Bắn xung kích chân Line0 1s!")
                #     cmd_cam1.put("PULSE_NG")
                # else:
                #     print("✅ [RESULT: OK]")


                # 👉 ĐẢO LOGIC: CHỈ KÍCH OUTPUT KHI TẤT CẢ ĐỀU OK
                if final_status:
                    print("✅ [RESULT: OK] -> Bắn xung kích chân Line0 1s!")
                    if cmd_cam1 is not None:
                        cmd_cam1.put("PULSE_NG")  # Lệnh này gọi trigger_ng_pulse (bật chân Line0 1s)
                else:
                    print("⚠️ [RESULT: NG] -> Không kích Output.")


                modbus.send_inspection_result(result_code=result_code)

                res_queue.put({
                    "type": "RESULT",
                    "status": "OK" if final_status else "NG",
                    "data": step_results
                })
                print(f"🏁 === KẾT QUẢ CHU KỲ: {'OK' if final_status else 'NG'} ===")

                # time.sleep(10000)
                reset_fsm()


            except queue.Empty:
                pass
            except Exception as e:
                print(f"❌ [LỖI BƯỚC 3]: {e}")
                traceback.print_exc()

    modbus.close()