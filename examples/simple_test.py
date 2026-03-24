from signet import SignetClient

# ---------------------------------------------------------
# SIGNET CONFIGURATION (Replace with data from your Dashboard)
# ---------------------------------------------------------
# 1. Enter API URL
API_URL = "https://signet.example.com"  # Replace with your actual API URL

# 2. Enter the API Key generated in the 'api_keys' table
API_KEY = "sgnt_api_xxx_replace_with_your_key" 

# 3. ENTER PUBLIC KEY (ECDSA Public Key from Dashboard)
# Ensure the format retains the PEM Header & Footer
PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEYourPublicKeyDataHere...
(Replace this line with the actual Public Key from the Signet Dashboard)
-----END PUBLIC KEY-----"""

def run_test():
    # Initialize the SDK
    client = SignetClient(
        api_url=API_URL,
        api_key=API_KEY,
        public_key_pem=PUBLIC_KEY_PEM
    )

    print("--- PHASE 1: ONLINE ACTIVATION ---")
    serial_user = input("Enter License Serial Key: ") # Replace with your actual license key
    
    # Attempting activation (Hitting API)
    # This will automatically create a 'license.cert' file if successful
    result = client.activate_license(serial_user, save_path="license.cert")
    
    if result["success"]:
        print(f"✅ {result['message']}")
        
        print("\n--- PHASE 2: OFFLINE VERIFICATION (ZERO-TRUST) ---")
        # Attempting local verification without internet access
        is_valid = client.verify_local_license(cert_path="license.cert")
        
        if is_valid:
            print("✅ Verification Successful! Application allowed to run.")
        else:
            print("❌ Verification Failed! Hardware mismatch or invalid signature.")
            
    else:
        print(f"❌ {result['message']}")

if __name__ == "__main__":
    run_test()