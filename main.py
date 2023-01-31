import requests, time, secrets, json


# Loads all json values (make sure to set them or the code wont work!)
with open("config.json", "r") as file:
    config = json.load(file)

# Sets the variables

token = config['Authorization']
xSuperProperties = config['X-Super-Properties']
currentPassword = config['currentPassword']
twoFAStatus = config['2FA']
if config['2FA'] == True:
    twoFACode = config['2FA-Backup-Code']

# Whitelist locations (where you usually log in from)
whitelist = []

# The request URL
url = "https://discord.com/api/v9/auth/sessions"

# Sets the headers 
headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Authorization": token,
        "Priority": "u=3, i",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "en-US",
        "X-Super-Properties": xSuperProperties
}

# Change Password Function
def change_password(password) -> bool:
    global token
    url = "https://discord.com/api/v9/users/@me"
    if twoFAStatus == True:
        data = {'code': twoFACode, 'password': currentPassword, 'new_password': password}
    else:
        data = {'password': currentPassword, 'new_password': password}
    r = requests.patch(url=url, data=data, headers=headers)
    if r.status_code == 200:
        token = r.json()['token']
        headers['Authorization'] = token
        return True
    else:
        print(f"Request returned status code {r.status_code} with: {r.text}")
        return False


# Generate Password Function

def generate_password(length):
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = "".join(secrets.choice(alphabet) for i in range(length))
    return password

while True:
    r = requests.get(url=url, headers=headers)
    if r.status_code != 200:
        print(f"Request returned status code {r.status_code} with: {r.text}")
        exit(1)
    
    try: 
        data = r.json()
    except:
        print("Failed to grab json")
        exit(0)
    
    current_locations = []
    for session in data['user_sessions']:
        print(session['client_info']['location'])
        current_locations.append(session['client_info']['location'])
    for location in current_locations:
        if location not in whitelist:
            print(f"[!] Non Whitelisted Location Found! [{location}]\n[!] Changing password now..")
            password = generate_password(secrets.randbelow(11) + 10)
            print(f"[!] Created password: {password}")
            passChange = change_password(password)
            if passChange == True:
                print(f"[!] Updated password and devalidated token!\n[?] New Token: {token}")
                break
            else:
                print("[!] Failed to log out attacker (password change failed)")
                break

    time.sleep(10) # Check every 10 seconds
