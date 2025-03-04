from selenium import webdriver
import time
import sys

# Emojis 🎭
BROWSER_EMOJIS = {"1": "🌐 Chrome", "2": "🎮 Edge", "3": "🛠 Firefox"}

# Ask for the token
token = input("\n🔑 Enter your Discord token: ")

script = """
function login(token) {
    setInterval(() => {
        document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
    }, 50);
    setTimeout(() => {
        location.reload();
    }, 2500);
}
"""

# Ask the user to choose a browser
print("\n💻 Choose your browser:")
print(f"[1] {BROWSER_EMOJIS['1']}")
print(f"[2] {BROWSER_EMOJIS['2']}")
print(f"[3] {BROWSER_EMOJIS['3']}")

browser_choice = input("\n🔍 Your choice: ")

# Initialize the appropriate browser based on the user's choice
if browser_choice in ['1', '01']:
    try:
        navigator = "Chrome"
        print(f"\n{navigator} starting... 🌐")
        driver = webdriver.Chrome()  # Ensure the correct driver is installed for Chrome
        print(f"{navigator} ready! ✅")
    except Exception as e:
        print(f"❌ Error: {navigator} not installed or driver not up to date. {str(e)}")
        sys.exit()

elif browser_choice in ['2', '02']:
    if sys.platform.startswith("linux"):
        print("❌ Edge is not supported on Linux.")
        sys.exit()
    else:
        try:
            navigator = "Edge"
            print(f"\n{navigator} starting... 🎮")
            driver = webdriver.Edge()  # Ensure the correct driver is installed for Edge
            print(f"{navigator} ready! ✅")
        except Exception as e:
            print(f"❌ Error: {navigator} not installed or driver not up to date. {str(e)}")
            sys.exit()

elif browser_choice in ['3', '03']:
    if sys.platform.startswith("linux"):
        print("❌ Firefox is not supported on Linux.")
        sys.exit()
    else:
        try:
            navigator = "Firefox"
            print(f"\n{navigator} starting... 🛠")
            driver = webdriver.Firefox()  # Ensure the correct driver is installed for Firefox
            print(f"{navigator} ready! ✅")
        except Exception as e:
            print(f"❌ Error: {navigator} not installed or driver not up to date. {str(e)}")
            sys.exit()
else:
    print("❌ Invalid choice! Exiting...")
    sys.exit()

# Open Discord login page
driver.get("https://discord.com/login")
time.sleep(2)

# Animation while logging in with token
print("\n🔄 Logging in with the provided token... Please wait.")
for i in range(5):  # 5 seconds of animation, adjust as needed
    print(f"🔄 Logging in {'.' * (i % 3 + 1)}", end='\r')
    time.sleep(1)

# Execute the token injection script
driver.execute_script(script + f'\nlogin("{token}")')

# Keep the page open
input("\nPress Enter to exit and close the browser...")

# Close the browser when done
driver.quit()
