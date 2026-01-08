import requests
import re

url = "http://127.0.0.1:5000/accounts/login/"
try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        inputs = re.findall(r'<input[^>]*>', response.text)
        print("Inputs found:")
        for i in inputs:
            print(i)
        
        # Also print raw text around "password" to see what's before it
        print("\nContext around password:")
        start = response.text.find('type="password"')
        print(response.text[max(0, start-500):start+200])
    else:
        print("Failed to fetch page")
except Exception as e:
    print(f"Error: {e}")
