import time
from pyModbusTCP.client import ModbusClient

class PLCModbusClient:
    def __init__(self, ip="192.168.1.50", port=502):
        self.ip = ip
        self.port = port
        self.client = ModbusClient(self.ip, port=self.port)
        self.is_connected = False
        # self.connect()

    def connect(self):
        try:
            self.is_connected = self.client.connect()
            if self.is_connected:
                print(f"[Modbus] Kết nối thành công PLC tại {self.ip}:{self.port}")
            else:
                print(f"[Modbus] Không thể kết nối PLC tại {self.ip}:{self.port}")
        except Exception as e:
            print(f"[Modbus Error] Lỗi kết nối: {e}")
            self.is_connected = False

    def send_inspection_result(self, result_code: int, reg_addr: int = 0, coil_done_addr: int = 0):
        """
        result_code: 1=OK, 2=NG, 3=TIMEOUT_NG
        """
        if not self.is_connected:
            print(f"[Modbus SIM] Kết quả phán định: {result_code}")
            return False

        try:
            # 1. Ghi mã kết quả vào Holding Register
            self.client.write_register(address=reg_addr, value=result_code)
            
            # 2. Bắn xung Strobe (Coil) báo cho PLC biết dữ liệu đã sẵn sàng
            self.client.write_coil(address=coil_done_addr, value=True)
            time.sleep(0.05)
            self.client.write_coil(address=coil_done_addr, value=False)
            return True
        except Exception as e:
            print(f"[Modbus Error] Lỗi ghi dữ liệu: {e}")
            self.is_connected = False
            return False

    def close(self):
        if self.is_connected:
            self.client.close()
            self.is_connected = False