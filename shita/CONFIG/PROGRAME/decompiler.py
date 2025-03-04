import sys
import os
import re
import pefile

# Liste des malwares connus
STEALER_SIGNATURES = {
    "Blank Grabber": ["webhook", "grabber", "blank"],
    "Luna Grabber": ["luna", "webhook", "passwords"],
    "RedLine Stealer": ["redline", "cookies", "discord"]
}

def extract_webhooks(file_path):
    try:
        with open(file_path, "rb") as f:
            content = f.read().decode(errors="ignore")
        
        webhooks = re.findall(r"https://discord(?:app)?\.com/api/webhooks/\d+/\S+", content)
        if webhooks:
            print("\n🚨 Webhooks found in the file:")
            for webhook in webhooks:
                print(f" - {webhook}")
        else:
            print("\n✅ No Webhooks found.")

    except Exception as e:
        print(f"Error extracting webhooks: {e}")

def detect_malware(file_path):
    try:
        with open(file_path, "rb") as f:
            content = f.read().decode(errors="ignore")
        
        found_stealers = []
        for malware, signatures in STEALER_SIGNATURES.items():
            if any(sig in content for sig in signatures):
                found_stealers.append(malware)

        if found_stealers:
            print("\n🚨 Potential Malware Detected:")
            for stealer in found_stealers:
                print(f" - {stealer}")
        else:
            print("\n✅ No known malware detected.")

    except Exception as e:
        print(f"Error analyzing malware: {e}")

def analyze_pe(file_path):
    try:
        pe = pefile.PE(file_path)
        print("\n📌 PE File Information:")
        print(f" - Machine: {hex(pe.FILE_HEADER.Machine)}")
        print(f" - Number of Sections: {pe.FILE_HEADER.NumberOfSections}")
        print(f" - Entry Point: {hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint)}")
    except Exception as e:
        print(f"Error reading PE file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python malware_scanner.py <file.exe>")
        sys.exit(1)

    exe_path = sys.argv[1]

    if not os.path.exists(exe_path):
        print("[ERROR] File not found!")
        sys.exit(1)

    print("\n🔍 Starting Malware Analysis...\n")
    extract_webhooks(exe_path)
    detect_malware(exe_path)
    analyze_pe(exe_path)
