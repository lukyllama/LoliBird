# This code is for testing purposes only

import random
import httpx
import os
import time
import requests

def generate_warp_keys():
    try:
        # Fetch base keys from the provided URL
        base_keys_response = requests.get('https://gitlab.com/Misaka-blog/warp-script/-/raw/main/files/24pbgen/base_keys')
        if base_keys_response.status_code != 200:
            print("Failed to fetch base keys.")
            return

        # Extract base keys from the response
        base_keys = base_keys_response.content.decode('UTF8').split(',')

        # Number of keys to generate
        num_keys = int(input("Enter how many WARP+ Keys you need:\n> "))
        generated_keys = []

        for _ in range(num_keys):
            try:
                # Request registration to Cloudflare
                registration_response = requests.post("https://api.cloudflareclient.com/v0a2223/reg", headers={
                    "CF-Client-Version": "a-6.11-2223",
                    "Host": "api.cloudflareclient.com",
                    "Connection": "Keep-Alive",
                    "Accept-Encoding": "gzip",
                    "User-Agent": "okhttp/3.12.1",
                })

                if registration_response.status_code != 200:
                    print("Failed to register.")
                    return

                registration_data = registration_response.json()
                id = registration_data["id"]
                token = registration_data["token"]

                # Fetch a random key from the base keys
                key = random.choice(base_keys)

                # Associate the key with the registered account
                update_license_response = requests.put(f"https://api.cloudflareclient.com/v0a2223/reg/{id}/account", headers={
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {token}",
                }, json={"license": key})

                if update_license_response.status_code != 200:
                    print("Failed to update license.")
                    return

                # Fetch account details
                account_response = requests.get(f"https://api.cloudflareclient.com/v0a2223/reg/{id}/account", headers={
                    "Authorization": f"Bearer {token}"
                })

                if account_response.status_code != 200:
                    print("Failed to fetch account details.")
                    return

                account_data = account_response.json()
                referral_count = account_data["referral_count"]
                license = account_data["license"]

                generated_keys.append({"license": license, "referral_count": referral_count})

                print(f"License Key: {license}\nData Count: {referral_count} GB(s)")

                # Cleanup: delete the registered account
                requests.delete(f"https://api.cloudflareclient.com/v0a2223/reg/{id}", headers={
                    "Authorization": f"Bearer {token}"
                })

            except Exception as e:
                print(f"Error occurred: {e}")
                time.sleep(15)

            if (_ + 1) % 2 == 0:  # Pause after every 2 iterations
                time.sleep(60)

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Below is a list of generated keys, copy, paste and enjoy")
        print("For more content have a look at Xiao Misaka’s broken website")
        for key_data in generated_keys:
            print(f"License Key: {key_data['license']}\nData Count: {key_data['referral_count']} GB(s)")

        input('\n(Enter) to exit.\n')

    except Exception as e:
        print(f"Error occurred: {e}")

# Call the function to generate keys
generate_warp_keys()
