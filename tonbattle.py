import time
import requests
import urllib.parse
import json
import brotli

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
        "accept-encoding": "gzip, deflate, br",  # Added br for Brotli support
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

# Function to decompress Brotli response if needed, with fallback handling
def decompress_brotli_response(response):
    # Check if the response uses Brotli encoding
    if 'br' in response.headers.get('Content-Encoding', ''):
        try:
            print("Decompressing Brotli response...")
            return brotli.decompress(response.content)
        except brotli.error as e:
            print(f"Brotli decompression failed: {e}")
            print("Returning raw response content.")
            return response.content
    return response.content  # Return raw content if not Brotli

# Function to find an enemy
def find_enemy(authorization_token):
    headers = get_headers(authorization_token)
    url = "https://liyue.tonkombat.com/api/v1/combats/find"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = decompress_brotli_response(response)
        try:
            enemy_data = json.loads(content).get('data')
            if enemy_data:
                print(f"Enemy found: {enemy_data['username']} (User ID: {enemy_data['user_id']})")
                return enemy_data
            else:
                print("No enemy found.")
                return None
        except json.JSONDecodeError:
            print("Error decoding the response as JSON.")
            print("Response content:", content)
            return None
    else:
        print(f"Error finding enemy: {response.status_code}")
        return None

# Function to fight an enemy
def fight_enemy(enemy_id, authorization_token):
    headers = get_headers(authorization_token)
    url = "https://liyue.tonkombat.com/api/v1/combats/fight"
    data = {"opponent_id": enemy_id}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        content = decompress_brotli_response(response)
        try:
            fight_data = json.loads(content).get('data')
            if fight_data:
                print(f"Fight result against {fight_data['enemy']['username']}: Winner - {fight_data['winner']}")
                return fight_data
            else:
                print("No fight data returned.")
                return None
        except json.JSONDecodeError:
            print("Error decoding the response as JSON.")
            print("Response content:", content)
            return None
    else:
        print(f"Error during fight. Status code: {response.status_code}")
        print("Response content:", response.text)
        return None

# Cooldown for 1 hour (3600 seconds)
def cooldown():
    print("Cooling down for 1 hour due to a failed battle attempt...")
    time.sleep(3600)  # Sleep for 1 hour (3600 seconds)

# Main process for each user
def process_user(auth_data):
    user_info = extract_user_info(auth_data)
    username = user_info.get('username')
    first_name = user_info.get('first_name', 'Unknown')

    print(f"Processing account: {username} ({first_name})")

    # Find an enemy
    enemy_data = find_enemy(auth_data)
    if enemy_data:
        enemy_id = enemy_data['user_id']
        
        # Fight the enemy
        fight_result = fight_enemy(enemy_id, auth_data)
        if fight_result:
            print(f"Battle completed for {username}")
        else:
            cooldown()  # If battle failed, start cooldown
    else:
        cooldown()  # If no enemy found, start cooldown

def main():
    # Load all authorizations from query.txt
    authorizations = load_authorizations()

    # Process each authorization one by one
    for auth_data in authorizations:
        process_user(auth_data)

# Run the main function
if __name__ == "__main__":
    main()
