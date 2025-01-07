import requests
from datetime import datetime
import re

def get_quote():
    response = requests.get("https://quotes.rest/qod?language=en")
    if response.status_code == 200:
        quote_data = response.json()['contents']['quotes'][0]
        return f'"{quote_data["quote"]}" — {quote_data["author"]}'
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
