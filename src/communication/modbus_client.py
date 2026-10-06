import time
import threading
from pyModbusTCP.client import ModbusClient


class PLCModbusClient:
    def __init__(self, ip="192.168.1.100", port=502):
        self.ip = ip
        self.port = port
        self.client = ModbusClient(host=self.ip, port=self.port, auto_open=True, auto_close=False, timeout=1.0)
        self.lock = threading.Lock()  # Khóa bảo vệ socket khi đọc/ghi đồng thời
        self.connect()

    def connect(self):
        try:
            if not self.client.is_open:
                if self.client.open():
                    print(f"[Modbus] Kết nối thành công PLC tại {self.ip}:{self.port}")
                else:
                    print(f"[Modbus] Không thể kết nối PLC tại {self.ip}:{self.port}")
        except Exception as e:
            print(f"[Modbus Error] Lỗi kết nối: {e}")

    def send_inspection_result(self, result_code: int, reg_addr: int = 138, reset_delay: float = 0.2):
        """
        1. Ghi mã kết quả (1: OK, 2: NG) vào thanh ghi (mặc định D138).
        2. Tự động reset giá trị thanh ghi về 0 sau reset_delay (0.2s) ở luồng ngầm.
        """
        def _send_and_reset():
            with self.lock:
                if not self.client.is_open:
                    self.connect()

                try:
                    # 1. Ghi kết quả kiểm tra (1 hoặc 2)
                    success = self.client.write_single_register(reg_addr, result_code)
                    if success:
                        print(f"📡 [Modbus] Gửi thành công D{reg_addr} = {result_code}")
                    else:
                        print(f"❌ [Modbus] Ghi thất bại vào D{reg_addr} (Value: {result_code})")
                        return

                    # 2. Đợi 0.2 giây
                    time.sleep(reset_delay)

                    # 3. Đưa thanh ghi về 0
                    reset_ok = self.client.write_single_register(reg_addr, 0)
                    if reset_ok:
                        print(f"⚪ [Modbus] Đã reset D{reg_addr} = 0")
                    else:
                        print(f"❌ [Modbus] Lỗi reset D{reg_addr} về 0")

                except Exception as e:
                    print(f"❌ [Modbus Error] Lỗi truyền thông: {e}")

        # Khởi chạy ngầm để không chặn luồng FSM của sequence_engine
        threading.Thread(target=_send_and_reset, daemon=True).start()

    def close(self):
        with self.lock:
            if self.client.is_open:
                self.client.close()
                print("[Modbus] Đã đóng kết nối PLC.")