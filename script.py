import requests
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

print('---- starting script ----')

url = "https://ruangmei.com/"
# url = "https://liamtra.com/"
# url = "https://live-liamtra-media.s3.ap-south-1.amazonaws.com/serviceListings/multipleImageTes0.1692866412.jpg"
# url = "https://ruangmei.com/news/shorts/en/"


# Initialize counters and locks
request_count = 0
loop_count = 0
count_lock = Lock()
loop_lock = Lock()

def fetch_url(url):
    global request_count
    start_time = time.time()
    try:
        response = requests.get(url)
        elapsed_time = time.time() - start_time
        with count_lock:
            request_count += 1
            print(f'-- Request count: {request_count} - {elapsed_time:.3f} seconds')
        if response.status_code != 200:
            print(f'-- Response code: {response.status_code}')
    except requests.RequestException as e:
        elapsed_time = time.time() - start_time
        print(f"An error occurred: {e}")
        print(f'-- Response time: {elapsed_time:.3f} seconds')

def main(num_requests=1, num_loops=None):
    global loop_count
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        while True:
            with loop_lock:
                loop_count += 1
                print('--------------------------------------')
                print(f'-- Loop count: {loop_count} ({num_requests})')
                print(f'-- Target: {url} ')
                print('--------------------------------------')
                
                
            futures = [executor.submit(fetch_url, url) for _ in range(num_requests)]
            for future in as_completed(futures):
                future.result()
            
            # Break the loop if the number of loops is defined and reached
            if num_loops is not None and loop_count >= num_loops:
                break
            
            # You can adjust the sleep time based on how often you want to make requests
            time.sleep(random.randint(1, 5))  # Wait for 1 second before making the next batch of requests

if __name__ == "__main__":
    # Set the number of concurrent requests you want to make
    num_requests = 1  # Change this number as needed
    # Set the number of loops (None for infinite loop)
    num_loops = None  # Change this number as needed or set to None for infinite loop
    main(num_requests, num_loops)
