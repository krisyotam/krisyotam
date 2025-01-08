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
        # Format quote into two lines
        return f'> "{quote}"\n> — {author}'
    return "Failed to fetch quote"

def update_readme():
    with open('README.md', 'r') as file:
        content = file.read()

    # Set up CST timezone using pytz
    cst = pytz.timezone('US/Central')
    current_date = datetime.now(cst).strftime("%B %d, %Y, %I:%M %p CST")  # Convert to CST and format

    quote = get_quote()

    # Use regex to replace the current date
    content = re.sub(r'_Current Date:_ .*', f'_Current Date:_ {current_date}', content, 1)

    # Use regex to replace the entire quote block (multi-line quote and author)
    content = re.sub(r'> ".*?"\n> — .*', quote, content, flags=re.DOTALL)

    # Find the quote section and everything below it
    quote_and_below = re.search(r'(?<=_Current Date:_ .*?\n)(.*)', content, flags=re.DOTALL).group(1)

    # Define the markdown sections to reinsert
    markdown_sections = """
<details>
  <summary><strong>My Philosophy</strong></summary>

  "Everything should be as simple as it can be, but not simpler." This mantra drives my work. I believe in simplicity, clarity, and frugality in design. My goal is to create software that prioritizes usability and performance, designed for experienced users who value simplicity and efficiency.

  I view complexity as the enemy of good software. By stripping away unnecessary features and focusing on the core purpose, I aim to craft software that is not only easy to maintain but also fast, secure, and sustainable. True progress is achieved through intentional subtraction, where each decision is made with purpose, and every line of code has meaning.

  My work is rooted in the belief that simplicity is the key to ingenuity. Software should empower users, respect their privacy, and prioritize functionality over form.

</details>

---

<details>
  <summary>💵 <strong>Support Me</strong></summary>

  <br />

  | **Currency**          | **Wallet Address**                                                                                              |
  |-----------------------|------------------------------------------------------------------------------------------------------------------|
  | **Bitcoin (BTC)**     | `bc1qqzsrdz8qa3xe2rp7aajrm88fqge9xxs3v8xu4h`                                                                   |
  | **Ethereum (ETH)**    | `0x43edF701622F4F1174F322dC8D2f5AbdA642275a`                                                                   |
  | **XRP Ledger (XRP)**  | `rNKP3PXSstJnhUgUskNKaXWhd7ueiss6Mn`                                                                           |
  | **BNB**               | `bnb1t49kkmutyvnsc8xv7r5mu9tfu2u66qhcmqaurw`                                                                   |
  | **Monero (XMR)**      | `4717EuNPoTrTQsiLdGSDAMAJQcze6mVuE8KmBhL9RFT43Xe2FsxWSQtc5trrfdYPS5aUjB8gJApwURcRmMFdccBCJPfeD8M`              |
  | **Solana (SOL)**      | `FcrRBcvWsqdVZpS9ZZ6Dt476QA1L95cdh7GqgUGX5RpH`                                                                 |

</details>
"""

    # Replace everything after the quote with the markdown sections
    new_content = re.sub(quote_and_below, markdown_sections.strip(), content, flags=re.DOTALL)

    with open('README.md', 'w') as file:
        file.write(new_content)

if __name__ == "__main__":
    update_readme()
