import os
import sys

# Đường dẫn mặc định tới thư mục chứa MvCameraControl.dll (Windows 64-bit)
mvs_dll_dir = r"C:\Program Files (x86)\MVS\Development\Samples\Python\MvImport"
if not os.path.exists(mvs_dll_dir):
    # Thư mục Runtime chính thức của MVS
    mvs_dll_dir = r"C:\Program Files (x86)\Common Files\MVS\Runtime\Win64_x64"

# Nạp thư mục DLL vào môi trường Python (bắt buộc cho Python 3.8+)
if hasattr(os, 'add_dll_directory') and os.path.exists(mvs_dll_dir):
    os.add_dll_directory(mvs_dll_dir)
os.environ['PATH'] = mvs_dll_dir + ';' + os.environ.get('PATH', '')

# Import các module từ thư mục MvImport của Hikrobot
from MvImport.MvCameraControl_class import *
import time
import numpy as np
import cv2
from ctypes import *


def grabber_process(dev_index: int, frame_queue, stop_event, config: dict = None):
    if config is None:
        config = {"exposure": 20000}
        
    cam = MvCamera()
    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayerType = MV_GIGE_DEVICE

    ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
    if ret != 0 or deviceList.nDeviceNum <= dev_index:
        print(f"[Cam{dev_index}] Khong tim thay camera tai index {dev_index}")
        return
    
    stDeviceInfo = cast(deviceList.pDeviceInfo[dev_index], POINTER(MV_CC_DEVICE_INFO)).contents
    ret = cam.MV_CC_CreateHandle(stDeviceInfo)
    if ret != 0:
        print(f"[Cam{dev_index}] Khong the khoi tao camera: {ret}")
        return
    
    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print(f"[Cam{dev_index}] Khong the mo camera: {ret}")
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
        
    # 2. Cấu hình Exposure Time (Dùng SetFloatValue và SetEnumValue)
    if "exposure" in config:
        cam.MV_CC_SetEnumValue("ExposureAuto", 0)
        cam.MV_CC_SetFloatValue("ExposureTime", float(config["exposure"]))
    
    # 3. Cấu hình Hardware Trigger & Lọc chống dội nút
    cam.MV_CC_SetEnumValue("TriggerMode", 1)
    cam.MV_CC_SetEnumValue("TriggerSource", 0)
    cam.MV_CC_SetEnumValue("TriggerActivation", 0)
    cam.MV_CC_SetIntValue("LineDebouncerTime", 20000)  # Lọc chống dội 20ms
    
    nPacketSize = cam.MV_CC_GetOptimalPacketSize()
    if nPacketSize > 0:
        cam.MV_CC_SetIntValue("GevSCPSPacketSize", nPacketSize)
    cam.MV_CC_SetIntValue("GevSCPD", 0)

    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print(f"[Cam{dev_index}] Khong the bat dau chup: {ret}")
        cam.MV_CC_CloseDevice()
        cam.MV_CC_DestroyHandle()
        return

    print(f"[Cam {dev_index}] Khoi dong thanh cong. Dang cho xung kich Line 0...")

    stOutFrame = MV_FRAME_OUT()
    memset(byref(stOutFrame), 0, sizeof(stOutFrame))

    try:
        while not stop_event.is_set():
            ret = cam.MV_CC_GetImageBuffer(stOutFrame, 100)
            if ret == 0:
                width = stOutFrame.stFrameInfo.nWidth
                height = stOutFrame.stFrameInfo.nHeight
                frame_len = stOutFrame.stFrameInfo.nFrameLen

                pData = (c_ubyte * frame_len)()
                cdll.msvcrt.memcpy(byref(pData), stOutFrame.pBufAddr, frame_len)
                raw_data = np.frombuffer(pData, dtype=np.uint8)

                raw_img = raw_data.reshape((height, width))
                bgr_img = cv2.cvtColor(raw_img, cv2.COLOR_BayerRG2BGR)

                cam.MV_CC_FreeImageBuffer(stOutFrame)

                # 👉 KIỂM TRA ĐẦY QUEUE TRƯỚC RỒI MỚI PUT DUY NHẤT 1 LẦN
                if frame_queue.full():
                    try:
                        frame_queue.get_nowait()
                    except:
                        pass
                
                frame_queue.put((dev_index, bgr_img))
                print(f"[Cam {dev_index}] Đã đẩy duy nhất 1 frame vào queue.")
    
    finally:
        cam.MV_CC_StopGrabbing()
        cam.MV_CC_CloseDevice()
        cam.MV_CC_DestroyHandle()
        print(f"[Cam{dev_index}] Da dong camera an toan.")



    
        
    
    

    