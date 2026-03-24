import json
import base64
import hashlib
from ecdsa import VerifyingKey, BadSignatureError
from ecdsa.util import sigdecode_der

def verify_signature(public_key_pem, payload, signature_b64):
    """
    Verify the ECDSA signature against the given payload and public key.
    """
    try:
        vk = VerifyingKey.from_pem(public_key_pem)
        
        message = json.dumps(payload, separators=(',', ':')).encode('utf-8')
        
        signature = base64.b64decode(signature_b64)
        
        try:
            return vk.verify(signature, message, hashfunc=hashlib.sha256)
        except BadSignatureError:
            try:
                return vk.verify(signature, message, hashfunc=hashlib.sha256, sigdecode=sigdecode_der)
            except BadSignatureError:
                return False
                
    except Exception as e:
        print(f"DEBUG Crypto Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("The ECDSA secp256r1 Cryptography Module is ready to use.")