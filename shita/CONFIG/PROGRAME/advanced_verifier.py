import sys
import os
import re
import pefile
import json

# 🕵️‍♂️ Liste des signatures de stealers connus
STEALER_SIGNATURES = {
    "Blank Grabber": ["webhook", "grabber", "blank"],
    "Luna Grabber": ["luna", "webhook", "passwords"],
    "RedLine Stealer": ["redline", "cookies", "discord"],
    "Rhadamanthys": ["rhadamanthys", "wallets", "passwords"],
    "Vidar Stealer": ["vidar", "passwords", "telegram"]
}

# 🎯 Regex pour détecter les Webhooks Discord
WEBHOOK_REGEX = r"https://discord(?:app)?\.com/api/webhooks/\d+/\S+"

# 🛠 Regex pour extraire les tokens Discord
DISCORD_TOKEN_REGEX = r"[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9_-]{27}"

# 🔑 Regex pour trouver des mots de passe stockés
PASSWORD_REGEX = r"password\s*[:=]\s*['\"]?([a-zA-Z0-9@#$%^&*!?]+)['\"]?"

def extract_webhooks(content):
    """Détecte la présence de Webhooks Discord"""
    return bool(re.search(WEBHOOK_REGEX, content))

def extract_tokens(content):
    """Détecte la présence de Tokens Discord"""
    return bool(re.search(DISCORD_TOKEN_REGEX, content))

def extract_passwords(content):
    """Détecte la présence de mots de passe"""
    return bool(re.search(PASSWORD_REGEX, content))

def detect_malware(content):
    """Détecte si un malware connu est présent"""
    for malware, signatures in STEALER_SIGNATURES.items():
        if any(sig in content for sig in signatures):
            return True
    return False

def analyze_pe(file_path):
    """Analyse l’exécutable pour détecter une protection"""
    try:
        pe = pefile.PE(file_path)
        is_packed = False

        # Vérification de la présence de packers
        packers = ["UPX", "VMProtect", "Themida"]
        for section in pe.sections:
            for packer in packers:
                if packer.encode() in section.Name:
                    is_packed = True
                    break

        return {
            "Packed": is_packed
        }
    except Exception as e:
        return {"error": f"Error reading PE file: {e}"}

def analyze_malware(file_path):
    """Analyse complète du fichier"""
    try:
        with open(file_path, "rb") as f:
            content = f.read().decode(errors="ignore")

        results = {
            "file": file_path,
            "Malware Detected": detect_malware(content),
            "Steals Webhooks": extract_webhooks(content),
            "Steals Discord Tokens": extract_tokens(content),
            "Steals Passwords": extract_passwords(content),
            "Protected (UPX/VMProtect)": analyze_pe(file_path)["Packed"]
        }

        return results

    except Exception as e:
        return {"error": f"Error analyzing file: {e}"}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python malware_scanner.py <file.exe>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print("[ERROR] File not found!")
        sys.exit(1)

    print("\n🔍 Running Advanced Malware Analysis...\n")
    results = analyze_malware(file_path)

    # 📄 Affiche les résultats en JSON
    print(json.dumps(results, indent=4, ensure_ascii=False))
