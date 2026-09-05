from src.pipeline.sequence_engine import inspection_manager_process
import sys
import multiprocessing as mp
from PySide6.QtWidgets import QApplication, QMainWindow

from src.drivers.hik_camera import grabber_process
# from src.pipeline.sequece_engine import inspection_manager_process
from src.ui.ui_main import UiMainWindow


def main():
    mp.freeze_support()
    
    stop_event = mp.Event()
    q_cam1 = mp.Queue(maxsize=1)
    q_cam2 = mp.Queue(maxsize=1)
    res_queue = mp.Queue(maxsize=10)

    cfg_cam1 = {
        "width": 2592,
        "height": 1944,
        "exposure": 20000,
        "offset_x": 0,
        "offset_y": 0,
    }

    cfg_cam2 = {
        "width": 2592,
        "height": 1944,
        "exposure": 20000,
        "offset_x": 0,
        "offset_y": 0,
    }
    
    p_cam1 = mp.Process(target=grabber_process, args=(0, q_cam1, stop_event, cfg_cam1))
    p_cam2 = mp.Process(target=grabber_process, args=(1, q_cam2, stop_event, cfg_cam2))

    p_seq = mp.Process(target=inspection_manager_process, args=(q_cam1, q_cam2, res_queue, stop_event))
    
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