import requests
from datetime import datetime
import pytz
import re

def get_quote():
    # Disable SSL verification (use this with caution)
    response = requests.get("https://api.quotable.io/random", verify=False)
    if response.status_code == 200:
        quote_data = response.json()
        quote = quote_data["content"]
        author = quote_data["author"]
        # Format quote into two lines with an en dash
        return f'> "{quote}"\n> – {author}'
    return "Failed to fetch quote"

def update_readme():
    with open('README.md', 'r') as file:
        content = file.read()

    # Set up CST timezone using pytz
    cst = pytz.timezone('US/Central')
    current_date = datetime.now(cst).strftime("%B %d, %Y, %I:%M %p CST")  # Convert to CST and format

    quote = get_quote()

    # Update the current date
    content = re.sub(r'_Current Date:_ .*', f'_Current Date:_ {current_date}', content, 1)

    # Update the quote block (use a robust pattern for multiline quotes)
    quote_pattern = r'> ".*?(?:\n.*?)*"\n> – .*'
    content = re.sub(quote_pattern, quote, content, flags=re.DOTALL)

    with open('README.md', 'w') as file:
        file.write(content)

    print("README.md updated successfully.")

if __name__ == "__main__":
    update_readme()

