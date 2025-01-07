import requests
from datetime import datetime
import re

def get_quote():
    response = requests.get("https://api.quotable.io/random?maxLength=100")
    if response.status_code == 200:
        print("Successfully fetched quote.")  # Debug print
        return response.json()['content']
    print("Failed to fetch quote.")  # Debug print
    return "Failed to fetch quote"

def update_readme():
    try:
        with open('README.md', 'r') as file:
            content = file.read()
        print("Successfully read README.md.")  # Debug print
    except Exception as e:
        print(f"Error reading README.md: {e}")  # Debug print
        return

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"Current date: {current_date}")  # Debug print
    quote = get_quote()

    # Use regex to replace only the date and quote
    content = re.sub(r'Last updated: .*', f'Last updated: {current_date}', content)
    content = re.sub(r'> .*', f'> {quote}', content)

    try:
        with open('README.md', 'w') as file:
            file.write(content)
        print("README.md successfully updated.")  # Debug print
    except Exception as e:
        print(f"Error writing to README.md: {e}")  # Debug print

if __name__ == "__main__":
    update_readme()
