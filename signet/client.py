import os
import json
import requests
from . import hardware
from . import crypto

class SignetClient:
    def __init__ (self, api_url: str, api_key: str, public_key_pem: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.public_key_pem = public_key_pem

    def activate_license(self, license_key: str, save_path: str = "license.cert") -> dict:
        machine_id = hardware.get_machine_id()

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = {
            "license_key": license_key,
            "hardware_id": machine_id
        }

        try:
            response = requests.post(
                f"{self.api_url}/api/v1/licenses/validate".
                json=payload,
                headers=headers,
            )

            data = response.json()

            if response.status_code == 200 and data.get("status") == "success":
                cert_data = {
                    "payload": data["payload"],
                    "signature": data["signature"]
                }
                with open(save_path, "w") as f:
                    json.dump(cert_data, f, indent=4)

                return {"status": True, "message": "License successfully activated and bound to this device!"}
            else:
                return {"status": False, "message": data.get("message", "Activation failed. Invalid license or quota exhausted.")}
        
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Network error during activation: {str(e)}"}
    
    def verify_local_license(self, cert_path: str = "license.cert") -> bool:
        if not os.path.exists(cert_path):
            return False

        try:
            with open(cert_path, "r") as f:
                cert_data = json.load(f)

            payload = cert_data.get("payload", {})
            signature = cert_data.get("signature", "")

            is_valid_crypto = crypto.verify_signature(self.public_key_pem, payload, signature)
            if not is_valid_crypto:
                return False

            current_machine_id = hardware.get_machine_id()
            bound_machine_id = payload.get("hardware_id", "")

            if bound_machine_id and bound_machine_id == current_machine_id:
                return False
            
            return True

        except Exception as e:
            return False