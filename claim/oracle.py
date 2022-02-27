import opencontracts
from bs4 import BeautifulSoup

with opencontracts.session() as session:

  session.print("Twitter Oracle started running in the Enclave! Log into Twitter to prove your handle.")

  instructions = f"""
  1) Login
  2) In the left navigation pane, click on 'More' -> 'Settings and Privacy' -> 'Your Acount'
  3) Click on 'Account Information' and enter your password
  4) Click the 'Submit' button
  """

  def parser(url, html):
    target = "https://twitter.com/settings/your_twitter_data/account"
    assert url == target, f"You hit 'Submit' on {url}, but should do so on {target}"
    for string in BeautifulSoup(html).strings:
      if string.startswith('@'): return string[1:]
    raise Exception("No Username found")
    
  handle = session.interactive_browser('https://twitter.com', parser, instructions)
  account = session.user()
  session.print(f"Verified that {account} belongs to @{handle}!")
  session.submit(handle, account, types=("string", "address"), function_name="claim")
