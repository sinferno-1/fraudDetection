import webbrowser
import time

def open_link_in_tab(url, num_times=100, delay_seconds=1):
    for _ in range(num_times):
        webbrowser.open_new_tab(url)
        time.sleep(delay_seconds)

if __name__ == "__main__":
    # Replace 'your_url_here' with the actual URL you want to open
    url = 'https://d220-2a09-bac5-3e64-18c8-00-278-cc.ngrok-free.app/'

    # Set the number of times to open the link and the delay between each open
    num_times = 10
    delay_seconds = 1

    # Call the open_link_in_tab function with the specified URL, number of times, and delay
    open_link_in_tab(url, num_times, delay_seconds)
