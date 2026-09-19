# #main.py

# from src.pipeline.sequence_engine import inspection_manager_process
# import sys
# import multiprocessing as mp
# from PySide6.QtWidgets import QApplication, QMainWindow

# from src.drivers.hik_camera import grabber_process
# # from src.pipeline.sequece_engine import inspection_manager_process
# from src.ui.ui_main import UiMainWindow


# def main():
#     mp.freeze_support()
    
#     stop_event = mp.Event()
#     q_cam1 = mp.Queue(maxsize=1)
#     q_cam2 = mp.Queue(maxsize=1)
#     res_queue = mp.Queue(maxsize=10)

#     # Tạo Queue nhận lệnh điều khiển chân Output cho Cam 1
#     cmd_cam1 = mp.Queue(maxsize=10)

#     # Điền đúng Serial Number đọc được từ phần mềm MVS/IRAYPLE
#     SN_CAM_5MP = "K06635181"   # Thay bằng Serial Number thật
#     SN_CAM_20MP = "CC10853BAK00009"  # Thay bằng Serial Number thật

#     cfg_cam1 = {
#         "width": 4000,
#         "height": 1848,
#         "exposure": 5000,
#         "offset_x": 498,
#         "offset_y": 762,
#         "trigger_source": 2,  # 1: Line 1 cho IRAYPLE
#     }

#     cfg_cam2 = {
#         "width": 2000,
#         "height": 700,
#         "exposure": 1700,
#         "offset_x": 400,
#         "offset_y": 600,
#         "trigger_source": 0,  # 0: Line 0 cho Hikvision
#     }
    
#     p_cam1 = mp.Process(target=grabber_process, args=("Cam1_20MP", SN_CAM_20MP, q_cam1, stop_event, cfg_cam1, cmd_cam1))
#     p_cam2 = mp.Process(target=grabber_process, args=("Cam2_5MP", SN_CAM_5MP,  q_cam2, stop_event, cfg_cam2))

#     p_seq = mp.Process(target=inspection_manager_process, args=(q_cam1, q_cam2, res_queue, stop_event, cmd_cam1))
    
#     p_seq.start()
#     p_cam1.start()
#     p_cam2.start()

#     app = QApplication(sys.argv)
#     main_window = UiMainWindow(stop_event, res_queue)
#     main_window.showMaximized()
#     exit_code = app.exec()

#     stop_event.set()
#     p_seq.join()
#     p_cam1.join()
#     p_cam2.join()

#     sys.exit(exit_code)

# if __name__ == "__main__":
#     main()






import sys
import multiprocessing as mp
from PySide6.QtWidgets import QApplication

from src.drivers.hik_camera import grabber_process
from src.pipeline.sequence_engine import inspection_manager_process
from src.ui.ui_main import UiMainWindow


def main():
    mp.freeze_support()
    
    stop_event = mp.Event()
    q_cam1 = mp.Queue(maxsize=1)
    q_cam2 = mp.Queue(maxsize=1)
    res_queue = mp.Queue(maxsize=10)

    # Queue nhận lệnh điều khiển chân Output cho Cam 1
    cmd_cam1 = mp.Queue(maxsize=10)

    SN_CAM_5MP = "K06635181"
    SN_CAM_20MP = "CC10853BAK00009"

    cfg_cam1 = {
        "width": 4000,
        "height": 1848,
        "exposure": 5000,
        "offset_x": 498,
        "offset_y": 762,
        "trigger_source": 2,  # Line 2 cho IRAYPLE
    }

    cfg_cam2 = {
        "width": 2000,
        "height": 700,
        "exposure": 1700,
        "offset_x": 400,
        "offset_y": 600,
        "trigger_source": 0,  # Line 0 cho Hikvision
    }
    
    # Cam 1: Nhận thêm cmd_cam1
    p_cam1 = mp.Process(
        target=grabber_process, 
        args=("Cam1_20MP", SN_CAM_20MP, q_cam1, stop_event, cfg_cam1, cmd_cam1)
    )
    
    # Cam 2: Để cmd_queue là None
    p_cam2 = mp.Process(
        target=grabber_process, 
        args=("Cam2_5MP", SN_CAM_5MP, q_cam2, stop_event, cfg_cam2, None)
    )

    # Sequence Engine: Truyền đúng thứ tự tham số (q_cam1, q_cam2, res_queue, cmd_cam1, stop_event)
    p_seq = mp.Process(
        target=inspection_manager_process, 
        args=(q_cam1, q_cam2, res_queue, stop_event, cmd_cam1)
    )
    
    p_seq.start()
    p_cam1.start()
    p_cam2.start()

    app = QApplication(sys.argv)
    main_window = UiMainWindow(stop_event, res_queue)
    main_window.showMaximized()
    exit_code = app.exec()

    stop_event.set()
    p_seq.join()
    p_cam1.join()
    p_cam2.join()

    sys.exit(exit_code)

if __name__ == "__main__":
    main()