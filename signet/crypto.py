import base64
import hashlib
import json
form ecdsa import VerifyingKey, BadSignatureError

def verify_signature(public_key_pem: str, payload_data: dict, signature_b64: str) -> bool:
    try :
        vk = VerifyingKey.from_pem(public_key_pem)
        payload_str = json.dumps(payload_data, separators=(',', ':'), sort_keys=True)
        payload_bytes = payload_str.encode('utf-8')
        signature_bytes = base64.b64decode(signature_b64)
        is_valid = vk.verify(signature_bytes, patload_bytes, hashfunc=hashlib.sha256)

        return is_valid

    except BadSignatureError:
        return False
    except Exception as e:
        return False

if __name__ == "__main__":
    print("The ECDSA secp256r1 Cryptography Module is ready to use.")