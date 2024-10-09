import urllib.parse
import json
import requests

# Function to load the authorization tokens from query.txt
def load_authorizations():
    with open('query.txt', 'r') as file:
        lines = file.readlines()
        authorizations = []
        for line in lines:
            line = line.strip()
            if line.startswith("user=") or line.startswith("query="):
                authorizations.append(line)  # Collect all authorization values
        return authorizations

# Function to extract user information from the authorization string
def extract_user_info(auth_data):
    user_info_str = auth_data.split("user=")[1].split("&")[0]
    user_info_decoded = urllib.parse.unquote(user_info_str)  # Decode URL-encoded string
    user_info = json.loads(user_info_decoded)  # Convert JSON-like string to dictionary
    return user_info

# Function to get headers with the current authorization token
def get_headers(authorization_token):
    return {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "authorization": f"tma {authorization_token}",  # Insert the full token here
        "origin": "https://staggering.tonkombat.com",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\", \"Microsoft Edge WebView2\";v=\"129\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "Referer": "https://staggering.tonkombat.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

# Function to upgrade pocket-size or mining-tok
def upgrade(upgrade_type, authorization_token):
    headers = get_headers(authorization_token)
    url = "https://liyue.tonkombat.com/api/v1/upgrades"
    payload = {"type": upgrade_type}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print(f"{upgrade_type.capitalize()} successfully upgraded.")
        print("Join Grup https://t.me/dasarpemulung")
        return response.json()  # Just in case a response is returned, even though it's typically empty
    else:
        print(f"Error upgrading {upgrade_type}: {response.status_code}")
        return None

# Function to claim daily
def claim_daily(authorization_token):
    headers = get_headers(authorization_token)
    url = "https://liyue.tonkombat.com/api/v1/daily"
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        print("Join Grup https://t.me/dasarpemulung")
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def claim_point(authorization_token):
    headers = get_headers(authorization_token)
    url = "https://liyue.tonkombat.com/api/v1/users/claim"
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        print("Join Grup https://t.me/dasarpemulung")
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None


# Function to get the task information
def get_task(authorization_token):
    headers = get_headers(authorization_token)
    url = "https://liyue.tonkombat.com/api/v1/tasks/progresses"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Join Grup https://t.me/dasarpemulung")
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Function to clear a task
def clear_task(task_id, authorization_token):
    headers = get_headers(authorization_token)
    url = f"https://liyue.tonkombat.com/api/v1/tasks/{task_id}"
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

# Ask for user preferences
def ask_user_preference():
    print("Join Grup https://t.me/dasarpemulung")
    auto_upgrade = input("Enable auto upgrade? (y/n): ").strip().lower()
    auto_claim_task = input("Enable auto claim task? (y/n): ").strip().lower()
    enable_daily_claim = input("Enable daily claim? (y/n): ").strip().lower()
    enable_claim_point = input("Enable Claim Battle Point ? (y/n): ").strip().lower()
    return auto_upgrade == 'y', auto_claim_task == 'y', enable_daily_claim == 'y', enable_claim_point == 'y'

# Main process for each user
def process_user(auth_data, auto_upgrade, auto_claim_task, enable_daily_claim,enable_claim_point):
    user_info = extract_user_info(auth_data)
    username = user_info.get('username')
    first_name = user_info.get('first_name', 'Unknown')

    print(f"Processing account: {username} ({first_name})")

    # Perform upgrades if enabled
    if auto_upgrade:
        upgrade("pocket-size", auth_data)
        upgrade("mining-tok", auth_data)

    # Perform daily claim if enabled
    if enable_daily_claim:
        daily = claim_daily(auth_data)
        if daily:
            print(f"Daily claim successful for {username}")
            print("Join Grup https://t.me/dasarpemulung")
        else:
            print(f"Failed daily claim for {username}")

    # Perform task claiming if enabled
    if auto_claim_task:
        task_data = get_task(auth_data)
        if task_data:
            print(f"Tasks retrieved for {username}.")
            for task in task_data['data']:
                task_id = task['id']
                task_name = task['name']
                task_type = task['type']
                task_reward = task['reward_amount']

                print(f"Processing task: {task_name} (ID: {task_id}, Type: {task_type}, Reward: {task_reward})")
                clear_result = clear_task(task_id, auth_data)
                if clear_result:
                    print(f"Task {task_name} cleared for {username}.")
                    print("Join Grup https://t.me/dasarpemulung")
                else:
                    print(f"Failed to clear task {task_name} for {username}.")
        else:
            print(f"Failed to retrieve tasks for {username}.")

def main():
    # Ask for user preferences
    auto_upgrade, auto_claim_task, enable_daily_claim,enable_claim_point = ask_user_preference()

    # Load all authorizations from query.txt
    authorizations = load_authorizations()

    # Process each authorization one by one
    for auth_data in authorizations:
        process_user(auth_data, auto_upgrade, auto_claim_task, enable_daily_claim,enable_claim_point)

# Run the main function
if __name__ == "__main__":
    main()
