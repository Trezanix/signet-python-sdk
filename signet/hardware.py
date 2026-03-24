import uuid
import hashlib
import platform

def get_machine_id() -> str:

    try:
        mac_num = uuid.getnode()
        mac_str = ':'.join(('%012X' % mac_num)[i:i+2] for i in range(0, 12, 2))
        os_info = platform.system()
        raw_id = f"{mac_str}-{os_info}".encode('utf-8')
        hardware_id = hashlib.sha256(raw_id).hexdigest()

        return hardware_id
    except Exception as e:
        return "UNKNOWN-HARDWARE-ID"

if __name__ == "__main__":
    print(f"This Device's Machine ID: {get_machine_id()}")