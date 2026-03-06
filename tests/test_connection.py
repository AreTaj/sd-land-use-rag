import requests
import logging

logging.basicConfig(level=logging.INFO)

url = "https://docs.sandiego.gov/municode/MuniCodeChapter11/Ch11Art01Division01.pdf"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Testing HTTPS connection to: {url}")
try:
    response = requests.head(url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print("Connection Successful!")
except requests.exceptions.SSLError as e:
    print(f"SSL Error: {e}")
except Exception as e:
    print(f"Other Error: {e}")

print("\nTesting with verify=False (Not recommended for production)")
try:
    response = requests.head(url, headers=headers, timeout=10, verify=False)
    print(f"Status Code: {response.status_code}")
    print("Connection Successful (unverified)!")
except Exception as e:
    print(f"Error even with verify=False: {e}")
