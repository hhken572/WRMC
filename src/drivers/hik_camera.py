# import os
# import sys

# # Đường dẫn mặc định tới thư mục chứa MvCameraControl.dll (Windows 64-bit)
# mvs_dll_dir = r"C:\Program Files (x86)\MVS\Development\Samples\Python\MvImport"
# if not os.path.exists(mvs_dll_dir):
#     # Thư mục Runtime chính thức của MVS
#     mvs_dll_dir = r"C:\Program Files (x86)\Common Files\MVS\Runtime\Win64_x64"

# # Nạp thư mục DLL vào môi trường Python (bắt buộc cho Python 3.8+)
# if hasattr(os, 'add_dll_directory') and os.path.exists(mvs_dll_dir):
#     os.add_dll_directory(mvs_dll_dir)
# os.environ['PATH'] = mvs_dll_dir + ';' + os.environ.get('PATH', '')

# # Import các module từ thư mục MvImport của Hikrobot
# from MvImport.MvCameraControl_class import *
# import time
# import numpy as np
# import cv2
# from ctypes import *


# # def grabber_process(dev_index: int, frame_queue, stop_event, config: dict = None):
# #     if config is None:
# #         config = {"exposure": 20000}
        
# #     cam = MvCamera()
# #     deviceList = MV_CC_DEVICE_INFO_LIST()
# #     tlayerType = MV_GIGE_DEVICE

# #     ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
# #     if ret != 0 or deviceList.nDeviceNum <= dev_index:
# #         print(f"[Cam{dev_index}] Khong tim thay camera tai index {dev_index}")
# #         return
    
# #     stDeviceInfo = cast(deviceList.pDeviceInfo[dev_index], POINTER(MV_CC_DEVICE_INFO)).contents
# #     ret = cam.MV_CC_CreateHandle(stDeviceInfo)
# #     if ret != 0:
# #         print(f"[Cam{dev_index}] Khong the khoi tao camera: {ret}")
# #         return
    
# #     ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
# #     if ret != 0:
# #         print(f"[Cam{dev_index}] Khong the mo camera: {ret}")
# #         cam.MV_CC_DestroyHandle()
# #         return

# def grabber_process(cam_name: str, target_serial: str, frame_queue, stop_event, config: dict = None):
#     if config is None:
#         config = {"exposure": 20000}
        
#     cam = MvCamera()
#     deviceList = MV_CC_DEVICE_INFO_LIST()
#     tlayerType = MV_GIGE_DEVICE

#     ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
#     if ret != 0 or deviceList.nDeviceNum == 0:
#         print(f"[{cam_name}] Khong tim thay thiet bi nao tren mang!")
#         return

#     # Quét tìm camera có Serial Number khớp với target_serial
#     selected_device = None
#     for i in range(deviceList.nDeviceNum):
#         dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
#         if dev_info.nTLayerType == MV_GIGE_DEVICE:
#             # Lấy chuỗi Serial Number từ thông tin GigE
#             gige_info = dev_info.SpecialInfo.stGigEInfo
#             sn = "".join([chr(c) for c in gige_info.chSerialNumber if c != 0]).strip()
#             if sn == target_serial:
#                 selected_device = dev_info
#                 break

#     if selected_device is None:
#         print(f"[{cam_name}] Khong tim thay camera co SN: {target_serial}")
#         return

#     # Khởi tạo handle với thiết bị đã tìm thấy
#     ret = cam.MV_CC_CreateHandle(selected_device)
#     if ret != 0:
#         print(f"[{cam_name}] Khong the tao handle: {ret}")
#         return

#     ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
#     if ret != 0:
#         print(f"[{cam_name}] Khong the mo camera: {ret}")
#         cam.MV_CC_DestroyHandle()
#         return



    
#     # 1. Cấu hình ROI
#     if "width" in config and "height" in config:
#         cam.MV_CC_SetIntValue("OffsetX", 0)
#         cam.MV_CC_SetIntValue("OffsetY", 0)
#         cam.MV_CC_SetIntValue("Width", int(config["width"]))
#         cam.MV_CC_SetIntValue("Height", int(config["height"]))
#         if "offset_x" in config:
#             cam.MV_CC_SetIntValue("OffsetX", int(config["offset_x"]))
#         if "offset_y" in config:
#             cam.MV_CC_SetIntValue("OffsetY", int(config["offset_y"]))
        
#     # 2. Cấu hình Exposure Time (Dùng SetFloatValue và SetEnumValue)
#     if "exposure" in config:
#         cam.MV_CC_SetEnumValue("ExposureAuto", 0)
#         cam.MV_CC_SetFloatValue("ExposureTime", float(config["exposure"]))
    
#     # 3. Cấu hình Hardware Trigger & Lọc chống dội nút
#     cam.MV_CC_SetEnumValue("TriggerMode", 1)
#     cam.MV_CC_SetEnumValue("TriggerSource", 0)
#     cam.MV_CC_SetEnumValue("TriggerActivation", 0)
#     cam.MV_CC_SetIntValue("LineDebouncerTime", 20000)  # Lọc chống dội 20ms
    
#     nPacketSize = cam.MV_CC_GetOptimalPacketSize()
#     if nPacketSize > 0:
#         cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
#     cam.MV_CC_SetIntValue("GevSCPD", 0)

#     ret = cam.MV_CC_StartGrabbing()
#     if ret != 0:
#         print(f"[Cam{dev_index}] Khong the bat dau chup: {ret}")
#         cam.MV_CC_CloseDevice()
#         cam.MV_CC_DestroyHandle()
#         return

#     # print(f"[Cam ] Khoi dong thanh cong. Dang cho xung kich Line 0...")

#     stOutFrame = MV_FRAME_OUT()
#     memset(byref(stOutFrame), 0, sizeof(stOutFrame))

#     try:
#         while not stop_event.is_set():
#             # ret = cam.MV_CC_GetImageBuffer(stOutFrame, 100)
#             # if ret == 0:
#             #     width = stOutFrame.stFrameInfo.nWidth
#             #     height = stOutFrame.stFrameInfo.nHeight
#             #     frame_len = stOutFrame.stFrameInfo.nFrameLen

#             #     pData = (c_ubyte * frame_len)()
#             #     cdll.msvcrt.memcpy(byref(pData), stOutFrame.pBufAddr, frame_len)
#             #     raw_data = np.frombuffer(pData, dtype=np.uint8)

#             #     raw_img = raw_data.reshape((height, width))
#             #     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_BayerRG2BGR)

#             #     cam.MV_CC_FreeImageBuffer(stOutFrame)

#             #     # 👉 KIỂM TRA ĐẦY QUEUE TRƯỚC RỒI MỚI PUT DUY NHẤT 1 LẦN
#             #     if frame_queue.full():
#             #         try:
#             #             frame_queue.get_nowait()
#             #         except:
#             #             pass
                
#             #     frame_queue.put((dev_index, bgr_img))

#             # Lấy ảnh từ buffer
#             ret = cam.MV_CC_GetImageBuffer(stOutFrame, 100)
#             if ret == 0:
#                 width = stOutFrame.stFrameInfo.nWidth
#                 height = stOutFrame.stFrameInfo.nHeight
#                 pixel_type = stOutFrame.stFrameInfo.enPixelType

#                 # Lấy con trỏ dữ liệu trực tiếp, không dùng memcpy
#                 ptr = cast(stOutFrame.pBufAddr, POINTER(c_ubyte))

#                 # Xử lý theo từng loại pixel định dạng thực tế của cam gửi về
#                 if pixel_type == PixelType_Gvsp_BayerRG8:
#                     # Cam 1: Mảng BayerRG8 (1 kênh)
#                     raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
#                     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_BayerRG2BGR)

#                 elif pixel_type == PixelType_Gvsp_BayerGR8:
#                     # Cam 2: Mảng BayerGR8 (1 kênh - chú ý mã GR)
#                     raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
#                     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_BayerGR2BGR)

#                 elif pixel_type == PixelType_Gvsp_BGR8_Packed:
#                     # Cam 2 (nếu bạn để BGR 8): Mảng 3 kênh dùng luôn
#                     bgr_img = np.ctypeslib.as_array(ptr, shape=(height, width, 3)).copy()

#                 elif pixel_type == PixelType_Gvsp_RGB8_Packed:
#                     # Cam 2 (nếu bạn để RGB 8): Lỗi 15116544 byte trước đó rơi vào đây
#                     raw_img = np.ctypeslib.as_array(ptr, shape=(height, width, 3))
#                     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_RGB2BGR)

#                 elif pixel_type == PixelType_Gvsp_Mono8:
#                     raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
#                     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_GRAY2BGR)

#                 else:
#                     cam.MV_CC_FreeImageBuffer(stOutFrame)
#                     raise ValueError(f"Chưa hỗ trợ PixelType: {hex(pixel_type)}")

#                 cam.MV_CC_FreeImageBuffer(stOutFrame)

#                 # Đẩy bgr_img vào queue
#                 if frame_queue.full():
#                     try:
#                         frame_queue.get_nowait()
#                     except:
#                         pass
#                 frame_queue.put((dev_index, bgr_img))
#                 print(f"[Cam {dev_index}] Đã đẩy duy nhất 1 frame vào queue.")
    
#     finally:
#         cam.MV_CC_StopGrabbing()
#         cam.MV_CC_CloseDevice()
#         cam.MV_CC_DestroyHandle()
#         print(f"[Cam{dev_index}] Da dong camera an toan.")







# #hik_camera.py

# import os
# import sys
# import time
# from ctypes import *
# import numpy as np
# import cv2
# import queue


# # Nạp thư mục DLL của MVS
# mvs_dll_dir = r"C:\Program Files (x86)\MVS\Development\Samples\Python\MvImport"
# if not os.path.exists(mvs_dll_dir):
#     mvs_dll_dir = r"C:\Program Files (x86)\Common Files\MVS\Runtime\Win64_x64"

# if hasattr(os, 'add_dll_directory') and os.path.exists(mvs_dll_dir):
#     os.add_dll_directory(mvs_dll_dir)
# os.environ['PATH'] = mvs_dll_dir + ';' + os.environ.get('PATH', '')

# from MvImport.MvCameraControl_class import *


# def trigger_ng_pulse(cam, duration=1.0):
#     """Bật chân Line0 trong duration giây rồi tự động tắt (chạy ngầm)."""
#     def _pulse():
#         try:
#             cam.MV_CC_SetEnumValueByString("UserOutputSelector", "UserOutput0")
#             cam.MV_CC_SetBoolValue("UserOutputValue", True)
#             print("🚨 [GPIO Cam 20MP] Kích ON chân Line0 (NG Output)")
#             time.sleep(duration)
#             cam.MV_CC_SetBoolValue("UserOutputValue", False)
#             print("⚪ [GPIO Cam 20MP] Đã ngắt chân Line0 (OFF)")
#         except Exception as e:
#             print(f"❌ [GPIO Error] Lỗi kích chân Line0: {e}")

#     threading.Thread(target=_pulse, daemon=True).start()


# def grabber_process(cam_name: str, target_serial: str, frame_queue, stop_event, config: dict = None):
#     if config is None:
#         config = {"exposure": 20000}
        
#     cam = MvCamera()
#     deviceList = MV_CC_DEVICE_INFO_LIST()
#     tlayerType = MV_GIGE_DEVICE

#     ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
#     if ret != 0 or deviceList.nDeviceNum == 0:
#         print(f"[{cam_name}] Không tìm thấy bất kỳ camera nào trên mạng!")
#         return

#     # Quét danh sách tìm camera có Serial Number khớp với target_serial
#     selected_device = None
#     for i in range(deviceList.nDeviceNum):
#         dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
#         if dev_info.nTLayerType == MV_GIGE_DEVICE:
#             gige_info = dev_info.SpecialInfo.stGigEInfo
#             sn = "".join([chr(c) for c in gige_info.chSerialNumber if c != 0]).strip()
#             if sn == target_serial:
#                 selected_device = dev_info
#                 break

#     if selected_device is None:
#         print(f"[{cam_name}] Không tìm thấy camera có Serial Number: {target_serial}")
#         return

#     ret = cam.MV_CC_CreateHandle(selected_device)
#     if ret != 0:
#         print(f"[{cam_name}] Lỗi tạo handle: {ret}")
#         return

#     ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
#     if ret != 0:
#         print(f"[{cam_name}] Lỗi mở thiết bị: {ret}")
#         cam.MV_CC_DestroyHandle()
#         return

#     # 1. Cấu hình ROI
#     if "width" in config and "height" in config:
#         cam.MV_CC_SetIntValue("OffsetX", 0)
#         cam.MV_CC_SetIntValue("OffsetY", 0)
#         cam.MV_CC_SetIntValue("Width", int(config["width"]))
#         cam.MV_CC_SetIntValue("Height", int(config["height"]))
#         if "offset_x" in config:
#             cam.MV_CC_SetIntValue("OffsetX", int(config["offset_x"]))
#         if "offset_y" in config:
#             cam.MV_CC_SetIntValue("OffsetY", int(config["offset_y"]))
        
#     # 2. Cấu hình Exposure Time
#     if "exposure" in config:
#         cam.MV_CC_SetEnumValue("ExposureAuto", 0)
#         cam.MV_CC_SetFloatValue("ExposureTime", float(config["exposure"]))
    
#     # 3. Cấu hình Hardware Trigger & Chống rung phím
#     trigger_source = config.get("trigger_source", 0)
#     cam.MV_CC_SetEnumValue("TriggerMode", 1)                  # 1: Bật Trigger Mode
#     cam.MV_CC_SetEnumValue("TriggerSource", trigger_source)  # 0: Line 0, 1: Line 1
#     cam.MV_CC_SetEnumValue("TriggerActivation", 0)           # 0: Rising Edge
#     cam.MV_CC_SetIntValue("LineDebouncerTime", 20000)        # Lọc chống dội 20ms





#     # Thêm cấu hình chân Line0 làm Output nếu là Cam 20MP
#     if config.get('Cam1_20MP', False) or "Line0" in config.get('name', ''):
#         try:
#             cam.MV_CC_SetEnumValueByString("LineSelector", "Line0")
#             cam.MV_CC_SetEnumValueByString("LineSource", "UserOutput0")
#             cam.MV_CC_SetEnumValueByString("UserOutputSelector", "UserOutput0")
#             cam.MV_CC_SetBoolValue("UserOutputValue", False)  # Mặc định tắt
#             print("[Cam 20MP] Đã cấu hình chân Line0 làm UserOutput0.")
#         except Exception as e:
#             print(f"[Cam 20MP] Cảnh báo cấu hình Line0: {e}")

#     while not stop_event.is_set():
#         # 1. Kiểm tra lệnh kích chân Output từ sequence_engine gửi sang
#         try:
#             cmd = cmd_queue.get_nowait()
#             if cmd == "PULSE_NG":
#                 trigger_ng_pulse(cam, duration=1.0)
#         except queue.Empty:
#             pass




    
#     # Tối ưu gói mạng
#     nPacketSize = cam.MV_CC_GetOptimalPacketSize()
#     if nPacketSize > 0:
#         cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
#     cam.MV_CC_SetIntValue("GevSCPD", 0)

#     ret = cam.MV_CC_StartGrabbing()
#     if ret != 0:
#         print(f"[{cam_name}] Lỗi bắt đầu grab: {ret}")
#         cam.MV_CC_CloseDevice()
#         cam.MV_CC_DestroyHandle()
#         return

#     print(f"[{cam_name}] Sẵn sàng (SN: {target_serial}). Đang chờ xung Line {trigger_source}...")

#     stOutFrame = MV_FRAME_OUT()
#     memset(byref(stOutFrame), 0, sizeof(stOutFrame))

#     try:
#         while not stop_event.is_set():
#             ret = cam.MV_CC_GetImageBuffer(stOutFrame, 100)
#             if ret == 0:
#                 width = stOutFrame.stFrameInfo.nWidth
#                 height = stOutFrame.stFrameInfo.nHeight
#                 pixel_type = stOutFrame.stFrameInfo.enPixelType

#                 ptr = cast(stOutFrame.pBufAddr, POINTER(c_ubyte))

#                 if pixel_type == PixelType_Gvsp_BayerRG8:
#                     raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
#                     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_BayerRG2BGR)

#                 elif pixel_type == PixelType_Gvsp_BayerGR8:
#                     raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
#                     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_BayerGR2BGR)

#                 elif pixel_type == PixelType_Gvsp_BGR8_Packed:
#                     bgr_img = np.ctypeslib.as_array(ptr, shape=(height, width, 3)).copy()

#                 elif pixel_type == PixelType_Gvsp_RGB8_Packed:
#                     raw_img = np.ctypeslib.as_array(ptr, shape=(height, width, 3))
#                     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_RGB2BGR)

#                 elif pixel_type == PixelType_Gvsp_Mono8:
#                     raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
#                     bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_GRAY2BGR)

#                 else:
#                     cam.MV_CC_FreeImageBuffer(stOutFrame)
#                     continue

#                 cam.MV_CC_FreeImageBuffer(stOutFrame)

#                 # Giữ frame mới nhất trong queue
#                 if frame_queue.full():
#                     try:
#                         frame_queue.get_nowait()
#                     except Exception:
#                         pass
                
#                 # Đẩy tuple (tên_camera, ảnh) vào queue
#                 frame_queue.put((cam_name, bgr_img))
#                 print(f"[{cam_name}] Đã chụp và đẩy ảnh vào queue ({width}x{height})")
    
#     finally:
#         cam.MV_CC_StopGrabbing()
#         cam.MV_CC_CloseDevice()
#         cam.MV_CC_DestroyHandle()
#         print(f"[{cam_name}] Đã đóng kết nối an toàn.")




import os
import sys
import time
import queue
import threading  # 👉 Đã bổ sung import threading
from ctypes import *
import numpy as np
import cv2

# Nạp thư mục DLL của MVS
mvs_dll_dir = r"C:\Program Files (x86)\MVS\Development\Samples\Python\MvImport"
if not os.path.exists(mvs_dll_dir):
    mvs_dll_dir = r"C:\Program Files (x86)\Common Files\MVS\Runtime\Win64_x64"

if hasattr(os, 'add_dll_directory') and os.path.exists(mvs_dll_dir):
    os.add_dll_directory(mvs_dll_dir)
os.environ['PATH'] = mvs_dll_dir + ';' + os.environ.get('PATH', '')

from MvImport.MvCameraControl_class import *


def trigger_ng_pulse(cam, duration=1.0):
    """Bật chân Line0 trong duration giây rồi tự động tắt (chạy ngầm)."""
    def _pulse():
        try:
            cam.MV_CC_SetEnumValueByString("UserOutputSelector", "UserOutput0")
            cam.MV_CC_SetBoolValue("UserOutputValue", True)
            print("🚨 [GPIO Cam 20MP] Kích ON chân Line0 (NG Output)")
            time.sleep(duration)
            cam.MV_CC_SetBoolValue("UserOutputValue", False)
            print("⚪ [GPIO Cam 20MP] Đã ngắt chân Line0 (OFF)")
        except Exception as e:
            print(f"❌ [GPIO Error] Lỗi kích chân Line0: {e}")

    threading.Thread(target=_pulse, daemon=True).start()


# 👉 Bổ sung tham số cmd_queue=None vào danh sách đối số
def grabber_process(cam_name: str, target_serial: str, frame_queue, stop_event, config: dict = None, cmd_queue=None):        
    cam = MvCamera()
    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayerType = MV_GIGE_DEVICE

    ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
    if ret != 0 or deviceList.nDeviceNum == 0:
        print(f"[{cam_name}] Không tìm thấy bất kỳ camera nào trên mạng!")
        return

    selected_device = None
    for i in range(deviceList.nDeviceNum):
        dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
        if dev_info.nTLayerType == MV_GIGE_DEVICE:
            gige_info = dev_info.SpecialInfo.stGigEInfo
            sn = "".join([chr(c) for c in gige_info.chSerialNumber if c != 0]).strip()
            if sn == target_serial:
                selected_device = dev_info
                break

    if selected_device is None:
        print(f"[{cam_name}] Không tìm thấy camera có Serial Number: {target_serial}")
        return

    ret = cam.MV_CC_CreateHandle(selected_device)
    if ret != 0:
        print(f"[{cam_name}] Lỗi tạo handle: {ret}")
        return

    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print(f"[{cam_name}] Lỗi mở thiết bị: {ret}")
        cam.MV_CC_DestroyHandle()
        return

    # 1. Cấu hình ROI
    if "width" in config and "height" in config:
        cam.MV_CC_SetIntValue("OffsetX", 0)
        cam.MV_CC_SetIntValue("OffsetY", 0)
        cam.MV_CC_SetIntValue("Width", int(config["width"]))
        cam.MV_CC_SetIntValue("Height", int(config["height"]))
        if "offset_x" in config:
            cam.MV_CC_SetIntValue("OffsetX", int(config["offset_x"]))
        if "offset_y" in config:
            cam.MV_CC_SetIntValue("OffsetY", int(config["offset_y"]))
        
    # 2. Cấu hình Exposure Time
    if "exposure" in config:
        cam.MV_CC_SetEnumValue("ExposureAuto", 0)
        cam.MV_CC_SetFloatValue("ExposureTime", float(config["exposure"]))
    
    # 3. Cấu hình Hardware Trigger & Chống rung phím
    trigger_source = config.get("trigger_source", 0)
    cam.MV_CC_SetEnumValue("TriggerMode", 1)                 # 1: Bật Trigger Mode
    cam.MV_CC_SetEnumValue("TriggerSource", trigger_source)  # 0: Line 0, 1: Line 1, 2: Line 2
    cam.MV_CC_SetEnumValue("TriggerActivation", 0)           # 0: Rising Edge
    cam.MV_CC_SetIntValue("LineDebouncerTime", 20000)        # Lọc chống dội 20ms

    # 4. Cấu hình chân Line0 làm Output nếu là Cam 20MP
    if "20MP" in cam_name or "Line0" in config.get('name', ''):
        try:
            cam.MV_CC_SetEnumValueByString("LineSelector", "Line0")
            cam.MV_CC_SetEnumValueByString("LineSource", "UserOutput0")
            cam.MV_CC_SetEnumValueByString("UserOutputSelector", "UserOutput0")
            cam.MV_CC_SetBoolValue("UserOutputValue", False)  # Mặc định tắt
            print(f"[{cam_name}] Đã cấu hình chân Line0 làm UserOutput0 thành công.")
        except Exception as e:
            print(f"[{cam_name}] Cảnh báo cấu hình Line0: {e}")

    # Tối ưu gói mạng
    nPacketSize = cam.MV_CC_GetOptimalPacketSize()
    if nPacketSize > 0:
        cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
    cam.MV_CC_SetIntValue("GevSCPD", 0)

    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print(f"[{cam_name}] Lỗi bắt đầu grab: {ret}")
        cam.MV_CC_CloseDevice()
        cam.MV_CC_DestroyHandle()
        return

    print(f"[{cam_name}] Sẵn sàng (SN: {target_serial}). Đang chờ xung Line {trigger_source}...")

    stOutFrame = MV_FRAME_OUT()
    memset(byref(stOutFrame), 0, sizeof(stOutFrame))

    try:
        while not stop_event.is_set():
            # 👉 1. Kiểm tra lệnh kích chân Line0 từ sequence_engine gửi sang
            if cmd_queue is not None:
                try:
                    cmd = cmd_queue.get_nowait()
                    if cmd == "PULSE_NG":
                        trigger_ng_pulse(cam, duration=1.0)
                except queue.Empty:
                    pass

            # 👉 2. Lấy frame từ buffer (timeout 50ms để liên tục quay lại kiểm tra cmd_queue)
            ret = cam.MV_CC_GetImageBuffer(stOutFrame, 50)
            if ret == 0:
                width = stOutFrame.stFrameInfo.nWidth
                height = stOutFrame.stFrameInfo.nHeight
                pixel_type = stOutFrame.stFrameInfo.enPixelType

                ptr = cast(stOutFrame.pBufAddr, POINTER(c_ubyte))

                if pixel_type == PixelType_Gvsp_BayerRG8:
                    raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
                    bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_BayerRG2BGR)

                elif pixel_type == PixelType_Gvsp_BayerGR8:
                    raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
                    bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_BayerGR2BGR)

                elif pixel_type == PixelType_Gvsp_BGR8_Packed:
                    bgr_img = np.ctypeslib.as_array(ptr, shape=(height, width, 3)).copy()

                elif pixel_type == PixelType_Gvsp_RGB8_Packed:
                    raw_img = np.ctypeslib.as_array(ptr, shape=(height, width, 3))
                    bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_RGB2BGR)

                elif pixel_type == PixelType_Gvsp_Mono8:
                    raw_img = np.ctypeslib.as_array(ptr, shape=(height, width))
                    bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_GRAY2BGR)

                else:
                    cam.MV_CC_FreeImageBuffer(stOutFrame)
                    continue

                cam.MV_CC_FreeImageBuffer(stOutFrame)

                # Giữ frame mới nhất trong queue
                if frame_queue.full():
                    try:
                        frame_queue.get_nowait()
                    except Exception:
                        pass
                
                frame_queue.put((cam_name, bgr_img))
                print(f"[{cam_name}] Đã chụp và đẩy ảnh vào queue ({width}x{height})")
    
    finally:
        cam.MV_CC_StopGrabbing()
        cam.MV_CC_CloseDevice()
        cam.MV_CC_DestroyHandle()
        print(f"[{cam_name}] Đã đóng kết nối an toàn.")