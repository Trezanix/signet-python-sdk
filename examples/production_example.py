import os
import sys
import json
import time
from dotenv import load_dotenv
from signet import SignetClient

# Load secret configuration from .env file
load_dotenv()

# =====================================================================
# 🛡️ SYSTEM CONFIGURATION
# =====================================================================
API_URL = os.getenv("SIGNET_API_URL")
API_KEY = os.getenv("SIGNET_API_KEY")
PRODUCT_SLUG = os.getenv("SIGNET_PRODUCT_SLUG")
LICENSE_FILE = "license.cert"

# Fetch the public key and restore the actual newline characters
PUBLIC_KEY_PEM = os.getenv("SIGNET_PUBLIC_KEY", "").replace("\\n", "\n")

if not API_KEY or not PUBLIC_KEY_PEM or not API_URL or not PRODUCT_SLUG:
    print("\n[FATAL] Missing environment configuration.")
    print("        Please ensure SIGNET_API_URL, SIGNET_API_KEY, SIGNET_PRODUCT_SLUG,")
    print("        and SIGNET_PUBLIC_KEY are properly set in your .env file.\n")
    sys.exit(1)

# =====================================================================
# 🖥️ TERMINAL UI HELPERS
# =====================================================================
def print_header(title):
    print("\n" + "=" * 60)
    print(f"{title.center(60)}")
    print("=" * 60)

def print_log(level, message):
    levels = {
        "INFO": "ℹ️  [INFO] ",
        "SUCCESS": "✅ [OK]   ",
        "WARN": "⚠️  [WARN] ",
        "ERROR": "❌ [ERROR]"
    }
    prefix = levels.get(level, "[LOG]")
    print(f"{prefix} {message}")

# =====================================================================
# 🚀 CORE APPLICATION BOOT
# =====================================================================
def get_app_name():
    """Extracts application name dynamically or falls back to default."""
    try:
        with open(LICENSE_FILE, "r") as f:
            cert_data = json.load(f)
        raw_slug = cert_data.get("payload", {}).get("product", PRODUCT_SLUG)
        return raw_slug.replace("-", " ").title()
    except Exception:
        return PRODUCT_SLUG.replace("-", " ").title() if PRODUCT_SLUG else "Premium Application"

def boot_application():
    """Simulates the main enterprise application logic."""
    app_name = get_app_name()
    
    print_header(f"WELCOME TO {app_name.upper()}")
    print_log("SUCCESS", "License verified mathematically (Zero-Trust).")
    print_log("SUCCESS", "Node-locked hardware signature matched.")
    print_log("INFO", "Initializing core modules...\n")
    
# =====================================================================
# 🔐 AUTHENTICATION & SECURITY GUARD
# =====================================================================
def verify_or_activate(client: SignetClient) -> bool:
    print_header("SECURITY MODULE BOOT SEQUENCE")
    print_log("INFO", "Verifying local hardware constraints...")
    
    # 1. Zero-Trust Offline Verification
    if os.path.exists(LICENSE_FILE):
        if client.verify_local_license(cert_path=LICENSE_FILE):
            return True
        else:
            print_log("WARN", "Integrity check failed. Hardware mismatch or invalid signature.")
    else:
        print_log("INFO", "No local certificate found. First-time setup required.")

    # 2. Online Activation Fallback (Clean & Professional UX)
    print_header("ORGANIZATION LICENSE ACTIVATION")
    print("This software requires a valid serial key assigned to your")
    print("device. Please contact your administrator if you do not")
    print("have your organization's serial key.\n")
    
    try:
        serial_user = input("▶ Enter Serial Key : ").strip()
    except KeyboardInterrupt:
        print("\n")
        return False

    if not serial_user:
        print_log("ERROR", "Serial key cannot be empty.")
        return False

    print_log("INFO", "Establishing secure connection to licensing server...")
    time.sleep(0.5) # Slight delay for UX realism
    
    result = client.activate_license(
        license_key=serial_user, 
        product_slug=PRODUCT_SLUG, 
        save_path=LICENSE_FILE
    )
    
    if result["success"]:
        print_log("SUCCESS", result['message'])
        time.sleep(1)
        return True
    else:
        print_log("ERROR", result['message'])
        print("\n💡 Troubleshooting:")
        print("   - Ensure you typed the key exactly as provided.")
        print("   - Check if this key is already bound to another machine.")
        print("   - Verify your internet connection.\n")
        return False

# =====================================================================
# ⚙️ MAIN ENTRY POINT
# =====================================================================
def main():
    client = SignetClient(
        api_url=API_URL,
        api_key=API_KEY,
        public_key_pem=PUBLIC_KEY_PEM
    )

    if verify_or_activate(client):
        boot_application()
    else:
        print_header("SYSTEM HALTED")
        print_log("ERROR", "Access Denied. Application will now exit.\n")
        sys.exit(1)

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    main()