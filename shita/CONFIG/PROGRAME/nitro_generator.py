import random
import string
import threading
import requests
import time
import sys

# Fonction pour générer un code Nitro
def generate_nitro():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Fonction pour vérifier un code Nitro
def check_nitro(webhook_url):
    while True:
        nitro_code = generate_nitro()
        nitro_url = f"https://discord.gift/{nitro_code}"

        response = requests.get(f"https://discord.com/api/v9/entitlements/gift-codes/{nitro_code}?with_application=false&country_code=US")

        if response.status_code == 200:
            print(f"[✓] VALID Nitro: {nitro_url}")
            data = {
                "username": "SHITA NITRO",
                "content": f"Valid Nitro found! 🎉 {nitro_url}"
            }
            requests.post(webhook_url, json=data)
        else:
            print(f"[x] INVALID Nitro: {nitro_url}")

        time.sleep(1)  # Petite pause pour éviter le spam extrême

# Démarrer plusieurs threads
def start_threads(webhook_url, num_threads):
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=check_nitro, args=(webhook_url,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

# Vérification des arguments
if len(sys.argv) < 3:
    print("Usage: python nitro_generator.py <webhook_url> <number_of_threads>")
    sys.exit(1)

webhook_url = sys.argv[1]
num_threads = int(sys.argv[2])

start_threads(webhook_url, num_threads)
