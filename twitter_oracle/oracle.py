import opencontracts
from bs4 import BeautifulSoup
import email, re, time
import quopri

with opencontracts.enclave_backend() as enclave:

  enclave.print("Twitter Oracle started running in the Enclave!")
   
  instructions = f"""
  1) Login and click on a tweet.
  2) Click the 'Submit' button on the right.
  """
  
  def extract_from_tweet(mhtml):
    mht_string = quopri.decodestring(mhtml.replace("=\n", "")).decode('latin-1')
    mhtml = email.message_from_string(mht_string)
    url = mhtml['Snapshot-Content-Location']
    match = re.match('^https://twitter.com/.*/status/.*', url)
    assert match is not None, 'Need to click on a specific tweet before hitting submit.'
    handle, _, status_id = url.replace('https://twitter.com/', '').split("/")
    status_id = int(status_id)
    html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
    parsed = BeautifulSoup(html.get_payload(decode=False))
    title = parsed.find(attrs={'http-equiv': 'origin-trial'}).findNextSibling()
    tweet = title.text.split(': "', 1)[1].strip('" / Twitter')
    unix_time = ((status_id>>22) + 1288834974657)
    return handle, unix_time, tweet
  
  handle, unix_time, tweet = enclave.interactive_session(url='https://twitter.com/home',
                                                       parser=extract_from_tweet,
                                                       instructions=instructions)
  
  enclave.print(f"Verified that '{handle}' tweeted '{tweet}' at unix time {unix_time}")
  time.sleep(4)
  enclave.submit(handle, tweet,
                 types=("string", "uint256", "address"),
                 function_name="submitTweet")
