import requests
import time

def fetch_data(url, num_requests=10, delay_seconds=1):
    for _ in range(num_requests):
        try:
            response = requests.get(url)

            if response.status_code == 200: #in case status is success
                print("Data fetched successfully:")
                print(response.text)
            else:
                print(f"Failed to fetch data. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Add a delay between requests
        time.sleep(delay_seconds)

if __name__ == "__main__":
    url = 'https://671a-2a09-bac1-3680-8798-00-23-3c0.ngrok-free.app/'
    
    num_requests = 100
    delay_seconds = 1
    
    fetch_data(url, num_requests, delay_seconds)
