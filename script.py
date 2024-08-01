import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

print('---- starting script ----')

url = "https://ruangmei.com/news/shorts/en/"

# Initialize counters and locks
request_count = 0
loop_count = 0
count_lock = Lock()
loop_lock = Lock()

def fetch_url(url):
    global request_count
    try:
        response = requests.get(url)
        with count_lock:
            request_count += 1
            print(f'----- Request count: {request_count}')
        # print(f' URL -> {url}')
        if response.status_code != 200:
            print(f'----- Response code: {response.status_code}')
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
    
    

def main(num_requests=1):
    global loop_count
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        while True:
            with loop_lock:
                loop_count += 1
                print(f'------------------------------')
                print(f'----- Loop count: {loop_count} ({num_requests})')
                print(f'------------------------------')
                
            futures = [executor.submit(fetch_url, url) for _ in range(num_requests)]
            for future in as_completed(futures):
                future.result()
            
            # You can adjust the sleep time based on how often you want to make requests
            time.sleep(1)  # Wait for 1 second before making the next batch of requests

if __name__ == "__main__":
    # Set the number of concurrent requests you want to make
    num_requests = 5  # Change this number as needed
    main(num_requests)
