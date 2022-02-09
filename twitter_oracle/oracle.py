import opencontracts
from bs4 import BeautifulSoup
import email, re, time
import quopri

with opencontracts.enclave_backend() as enclave:

  enclave.print("Twitter Oracle started running in the Enclave! Log into Twitter to prove your handle.")

  instructions = f"""
  1) Login
  2) Click on '(...) More' -> 'Settings' -> 'Your Acount'
  3) Enter your password and hit 'Submit'
  """
  
  def extract_handle(mhtml):
    mht_string = quopri.decodestring(mhtml.replace("=\n", "")).decode('latin-1')
    mhtml = email.message_from_string(mht_string)
    url, target = mhtml['Snapshot-Content-Location'], "https://twitter.com/settings/your_twitter_data/account"
    assert url == target, f"You hit 'Submit' on {url}, but should do so on 'target'"
    html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
    text = list(BeautifulSoup(html.get_payload(decode=False)).strings)
    info = text.index('Account information')
    assert text[info + 1] == "Username"
    return text[info + 2][1:]
  
  handle = enclave.interactive_session(url='https://twitter.com/home', 
                                       parser=extract_handle,
                                       instructions=instructions)
  
  address = enclave.user_input(f"Verified that {enclave.user()} belongs to @{handle}!")
  enclave.submit(handle, enclave.user(), types=("string", "address"), function_name="claim")
