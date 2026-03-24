# Signet Python SDK 🛡️

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-teal.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Official Python SDK for **Signet** — The free, bulletproof, and hardware-backed software licensing platform engineered by **[Trezanix](https://trezanix.com)**.

Signet Python SDK allows developers to easily integrate military-grade license validation, Node-Locked hardware binding, and offline ECDSA cryptographic verification into their Python applications with just a few lines of code.

---

## ✨ Key Features

- **Node-Locked Binding (Anti-Piracy):** Automatically binds licenses to the end-user's physical hardware footprint (MAC Address & OS). If the software is copied to another machine, it locks down instantly.
- **Zero-Trust Offline Verification:** Uses locally cached ECDSA (secp256r1) signatures to verify licenses mathematically. Your app can validate licenses 100% offline without hitting our servers.
- **Privacy First:** Hardware IDs are uniquely hashed locally using SHA-256 before being sent to the server.
- **Lightweight:** Minimal dependencies (`requests` and `ecdsa` only).

## 📦 Installation

You can install the Signet SDK directly from source:

```bash
git clone [https://github.com/trezanix/signet-python-sdk.git](https://github.com/trezanix/signet-python-sdk.git)
cd signet-python-sdk
pip install .
```

## 🚀 Quick Start
Implementing Signet into your application requires only two phases: Online Activation (done once) and Offline Verification (done on every app startup).

1. Initialize the Client

You will need your API Key and the Public Key provided in your Signet Console.
```python
from signet import SignetClient

# 1. Initialize the Signet Client
client = SignetClient(
    api_url="[https://signet-console.com](https:signet-console.com)",
    api_key="sgnt_api_xxxxxxxxxxxxxxxxxxxx",
    public_key_pem="""-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEYourPublicKeyDataHere...
-----END PUBLIC KEY-----"""
)
```
2. Phase 1: Online Activation

Run this when the user enters their serial key for the first time. It requires internet access.

```python
# The user's serial key
serial_key = "XXXX-XXXX-XXXX-XXXX-XXXX"

# Activate and bind to this hardware.
# This will automatically create a local 'license.cert' file.
result = client.activate_license(serial_key, save_path="license.cert")

if result["success"]:
    print("✅ License activated successfully!")
else:
    print(f"❌ Activation failed: {result['message']}")
```

3. Phase 2: Offline Verification (Zero-Trust)

Run this check every time your application starts. It is 100% offline and mathematically verifies the ECDSA signature against the local hardware ID.

```python
# Verify the local certificate
is_valid = client.verify_local_license(cert_path="license.cert")

if is_valid:
    print("✅ License is valid and bound to this machine. Booting app...")
    # Start your main application logic here
else:
    print("❌ Invalid, expired, or tampered license! Hardware mismatch detected. Exiting.")
    exit(1)
```

## 🏗️ Architecture: How it Works
1. Hardware ID Generation: The SDK extracts the machine's MAC Address and OS, hashes it with SHA-256, and sends it to the Signet API.
2. HSM Signing: The Signet server registers the device and passes the payload to a custom Trezanix Micro HSM. The HSM signs the payload using a heavily guarded Private Key (ECDSA secp256r1).
3. Local Validation: The signature and payload are sent back and saved locally (license.cert). Future validations are done completely offline by checking the signature against the embedded Public Key and comparing the current hardware ID.

## 📄 License
This SDK is open-sourced software licensed under the **[MIT License](https://opensource.org/licenses/MIT)**.