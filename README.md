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
- **Environment-Driven:** Built to support secure .env configurations to keep your API keys safe from reverse engineering.
- **Lightweight:** Minimal dependencies (`requests` and `ecdsa` only).

## 📦 Installation

You can install the Signet SDK directly from the source repository:

```bash
git clone https://github.com/trezanix/signet-python-sdk.git
cd signet-python-sdk
pip install .
```

`Note: For the implementation examples below, you will also need the python-dotenv package to securely load your credentials.`

```bash
pip install python-dotenv
```

## 🚀 Quick Start

Implementing Signet into your application requires setting up your secure environment, followed by two phases: Online Activation (done once) and Offline Verification (done on every app startup).

1. Secure Configuration (`.env`)

Never hardcode your API keys in your Python script. Create a .env file in the root directory of your application and add your Signet Console credentials:

```python
SIGNET_API_URL="https://api.yourdomain.com"
SIGNET_API_KEY="sgnt_live_xxxxxxxxxxxxxxxxxxxxxxxx"
SIGNET_PRODUCT_SLUG="your-product-slug"
SIGNET_PUBLIC_KEY="-----BEGIN PUBLIC KEY-----\nYOUR_PUBLIC_KEY_DATA_HERE\n-----END PUBLIC KEY-----"
```

`(Tip: Replace the newlines in your Public Key with \n to keep it on a single line).`

2. Initialize the SDK

Load the environment variables and initialize the Signet Client in your main application file.

```python
import os
from dotenv import load_dotenv
from signet import SignetClient

# Load secure configuration
load_dotenv()

API_URL = os.getenv("SIGNET_API_URL")
API_KEY = os.getenv("SIGNET_API_KEY")
PRODUCT_SLUG = os.getenv("SIGNET_PRODUCT_SLUG")
PUBLIC_KEY_PEM = os.getenv("SIGNET_PUBLIC_KEY", "").replace("\\n", "\n")

# Initialize the Signet Client
client = SignetClient(
    api_url=API_URL,
    api_key=API_KEY,
    public_key_pem=PUBLIC_KEY_PEM
)
```

3. Phase 1: Online Activation (First-time setup)

Run this when the user enters their serial key for the first time. It requires internet access.

```python
# The user's serial key (usually prompted via input() or GUI)
serial_key = "XXXX-XXXX-XXXX-XXXX-XXXX"

# Activate and bind to this hardware.
# This will automatically create a local 'license.cert' file.
result = client.activate_license(
    license_key=serial_key,
    product_slug=PRODUCT_SLUG,
    save_path="license.cert"
)

if result["success"]:
    print("✅ License activated successfully!")
else:
    print(f"❌ Activation failed: {result['message']}")
```

4. Phase 2: Offline Verification (Zero-Trust Guard)

Run this check every time your application starts. It is 100% offline and mathematically verifies the ECDSA signature against the local hardware ID.

```python
import sys

# Verify the local certificate
is_valid = client.verify_local_license(cert_path="license.cert")

if is_valid:
    print("✅ License is valid and bound to this machine. Booting app...")
    # Start your main application logic here!
else:
    print("❌ Invalid, expired, or tampered license! Hardware mismatch detected.")
    sys.exit(1) # Force close the application
```

(For a complete, interactive production-ready script, check out `examples/production_example.py` in the repository).

## 🏗️ Architecture: How it Works

1. Hardware ID Generation: The SDK extracts the machine's hardware identifiers, hashes it with SHA-256, and sends it to the Signet API.
2. HSM Signing: The Signet server registers the device and passes the payload to a custom Trezanix Micro HSM. The HSM signs the payload using a heavily guarded Private Key (ECDSA secp256r1).
3. Local Validation: The signature and payload are sent back and saved locally (license.cert). Future validations are done completely offline by checking the signature against the embedded Public Key and comparing the current hardware ID.

## 📄 License

This SDK is open-sourced software licensed under the **[MIT License](https://opensource.org/licenses/MIT)**.
