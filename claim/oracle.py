import opencontracts
from bs4 import BeautifulSoup
import email, re, time

with opencontracts.enclave_backend() as enclave:

  enclave.print("Twitter Oracle started running in the Enclave! Log into Twitter to prove your handle.")

  instructions = f"""
  1) Login
  2) Click on '(...) More' -> 'Settings and Privacy' -> 'Your Acount'
  3) Click on 'Account Information' -> enter your password -> hit 'Submit'
  """
  
  def extract_handle(url, html):
    target = "https://twitter.com/settings/your_twitter_data/account"
    assert url == target, f"You hit 'Submit' on {url}, but should do so on {target}"
    text = list(BeautifulSoup(html).strings)
    info = text.index('Account information')
    assert text[info + 1] == "Username"
    return text[info + 2][1:]
  
  handle = enclave.interactive_session(url='https://twitter.com/home',
                                       parser=extract_handle,
                                       instructions=instructions)
  account = enclave.user()
  enclave.print(f"Verified that {account} belongs to @{handle}!")
  enclave.submit(handle, account, types=("string", "address"), function_name="claim")
