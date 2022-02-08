import opencontracts
from bs4 import BeautifulSoup
import email, re, time
import quopri

with opencontracts.enclave_backend() as enclave:

  enclave.print("Twitter Oracle started running in the Enclave! Log into Twitter to prove your handle.")

  instructions = f"""
  1) Login
  2) On the Twitter home page, click the 'Submit' button on the right.
  """
  
  def extract_handle(mhtml):
    mht_string = quopri.decodestring(mhtml.replace("=\n", "")).decode('latin-1')
    mhtml = email.message_from_string(mht_string)
    url = mhtml['Snapshot-Content-Location']
    assert url == "https://twitter.com/home", f"You clicked 'Submit' on '{url}', but should do so on 'https://twitter.com/home'!"
    html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
    parsed = BeautifulSoup(html.get_payload(decode=False))
    handle = parsed.find(attrs={'aria-label': 'Profile'})['href'].split('/')[-1]
    return handle
  
  handle = enclave.interactive_session(url='https://twitter.com/home', 
                                       parser=extract_handle,
                                       instructions=instructions)
  
  address = enclave.user_input(f"Verified that {enclave.user()} belongs to @{handle}!")
  enclave.submit(handle, enclave.user(), types=("string", "address"), function_name="submitTweet")
