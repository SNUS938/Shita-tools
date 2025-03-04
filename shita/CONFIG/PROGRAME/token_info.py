import requests

# Ask for the token
token = input("\n🔑 Enter your Discord token: ")

# API Headers
headers = {
    "Authorization": token,
    "Content-Type": "application/json"
}

# Fetch account details
response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

if response.status_code == 200:
    user_data = response.json()
    print("\n👤 Account Information:")
    print(f"📛 Username: {user_data['username']}#{user_data['discriminator']}")
    print(f"🆔 ID: {user_data['id']}")
    print(f"📧 Email: {user_data.get('email', 'Not linked')}")
    print(f"📞 Phone: {user_data.get('phone', 'Not linked')}")
    print(f"🎁 Nitro: {'✅ Yes' if user_data.get('premium_type', 0) in [1, 2] else '❌ No'}")
    
    # Fetch billing info
    billing_response = requests.get("https://discord.com/api/v9/users/@me/billing/payment-sources", headers=headers)
    if billing_response.status_code == 200 and len(billing_response.json()) > 0:
        print(f"💳 Billing Method: ✅ Yes")
    else:
        print(f"💳 Billing Method: ❌ No")

else:
    print("\n🚫 Invalid token! Please check and try again.")

