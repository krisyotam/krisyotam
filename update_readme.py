import requests
from datetime import datetime
import re

def get_quote():
    # Disable SSL verification (use this with caution)
    response = requests.get("https://api.quotable.io/random", verify=False)
    if response.status_code == 200:
        quote_data = response.json()
        quote = quote_data["content"]
        author = quote_data["author"]
        # Format quote into two lines
        return f'> "{quote}"\n> — {author}'
    return "Failed to fetch quote"

def update_readme():
    with open('README.md', 'r') as file:
        content = file.read()

    # Format the date into a more readable format
    current_date = datetime.now().strftime("%B %d, %Y, %I:%M %p UTC")

    quote = get_quote()

    # Use regex to replace only the date and quote
    content = re.sub(r'_Current Date:_ .*', f'_Current Date:_ {current_date}', content)
    content = re.sub(r'> .*', quote, content)

    with open('README.md', 'w') as file:
        file.write(content)

if __name__ == "__main__":
    update_readme()
