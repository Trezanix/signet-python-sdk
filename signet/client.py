import os
import json
import requests
from . import hardware
from . import crypto

class SignetClient:
    def __init__(self, api_url: str, api_key: str, public_key_pem: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.public_key_pem = public_key_pem

    def activate_license(self, license_key: str, product_slug: str, save_path: str = "license.cert") -> dict:
        machine_id = hardware.get_machine_id()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "license_key": license_key,
            "product_slug": product_slug,
            "hardware_id": machine_id,
            "device_name": "Python Client Device"
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/api/v1/licenses/validate", 
                json=payload, 
                headers=headers,
                timeout=10
            )

            try:
                data = response.json()
            except ValueError:
                return {
                    "success": False, 
                    "message": f"Server returned non-JSON response (Status: {response.status_code})"
                }
            
            is_success = data.get("status") == "success"
            
            if response.status_code == 200 and is_success:
                cert_data = {
                    "payload": data.get("data", {}).get("signed_payload"),
                    "signature": data.get("signature")
                }
                
                with open(save_path, "w") as f:
                    json.dump(cert_data, f, indent=4)
                    
                return {"success": True, "message": "License successfully activated and bound to this device!"}
            else:
                return {
                    "success": False, 
                    "message": data.get("message", "Activation failed or server error.")
                }
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Network error: {str(e)}"}
        except Exception as e:
            return {"success": False, "message": f"Unexpected error: {str(e)}"}

    def verify_local_license(self, cert_path: str = "license.cert") -> bool:
        if not os.path.exists(cert_path):
            return False
            
        try:
            with open(cert_path, "r") as f:
                cert_data = json.load(f)
                
            payload = cert_data.get("payload")
            signature = cert_data.get("signature")
            
            if not payload or not signature:
                return False
            
            is_valid_crypto = crypto.verify_signature(self.public_key_pem, payload, signature)
            if not is_valid_crypto:
                return False
                
            current_machine_id = hardware.get_machine_id()
            bound_machine_id = payload.get("hardware_id")
            
            if bound_machine_id != current_machine_id:
                return False
                
            return True
                
        except Exception:
            return False