import requests
from datetime import datetime
import re

def get_quote():
    response = requests.get("https://api.quotable.io/random?maxLength=100")
    if response.status_code == 200:
        return response.json()['content']
    return "Failed to fetch quote"

def update_readme():
    with open('README.md', 'r') as file:
        content = file.read()

    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    quote = get_quote()

    # Use regex to replace only the date and quote
    content = re.sub(r'Last updated: .*', f'Last updated: {current_date}', content)
    content = re.sub(r'> .*', f'> {quote}', content)

    with open('README.md', 'w') as file:
        file.write(content)

if __name__ == "__main__":
    update_readme()
