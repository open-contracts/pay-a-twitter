import opencontracts
from bs4 import BeautifulSoup
import email



def get_most_recent_tx(mhtml):
  mhtml = email.message_from_string(mhtml.replace("=\n", ""))
  url = mhtml['Snapshot-Content-Location']
  print(url,  url.startswith('https://account.venmo.com/u/'))
  assert url.startswith('https://account.venmo.com/u/')
  seller = url[28:]
  html = [_ for _ in mhtml.walk() if _.get_content_type() == "text/html"][0]
  parsed = BeautifulSoup(html.get_payload(decode=False))
  transactions = parsed.find_all(**{'data-testid' :'3D"betweenYou-feed-container"'})[0]
  messages = transactions.findAll('div', {'class': lambda c: c and c.startswith('3D"storyContent_')})
  message = messages[0].text.strip()
  amount = messages[0].findParent().findParent().findNextSibling().text.strip()
  assert amount.startswith("- $")
  amount = int(float(amount[3:])*100)
  return seller, amount, message



with opencontracts.enclave_backend() as enclave:

  enclave.print("Fiat Swap started running in the Enclave!")

  seller = enclave.user_input("Please enter the Venmo handle of the seller:")
  amount = int(enclave.user_input("Please enter the transaction price in cents (as integer):"))
  message = enclave.user_input("Please enter the message the seller wants you to use in the transaction:").strip()
  secret = enclave.user_input("Please enter the secret generated by the seller:")
  
  hash = enclave.keccak(seller, amount, message, secret, types=('string', 'uint256', 'string', 'string'))
  enclave.print(f"You are about to accept the offer with the offerHash {'0x' + hash.hex()}. Before proceeding:")
  enclave.print("- call the ethOffered() function to verify that you will receive enough ETH")
  enclave.print("- call the secondsLeft() function to verify that you have enough time to claim your payout")
  
  enclave.open_up_domain("venmo.com")
  mhtml = enclave.interactive_session(url='https://venmo.com', instructions=f"Login, then navigate to {seller}'s profile.\n Pay them ${float(amount)/100} and use the message '{message}'.\n Then navigate to the 'between you' page on {seller}'s profile and click the 'save and exit' button on the right.", tcp_port=14500)
  _seller, _amount, _message = get_most_recent_tx(mhtml)
  
  if (_seller == seller) and (_amount >= amount) and (_message == message):
    print(hash)
    enclave.submit(hash, types=("bytes32",), function_name="venmoPurchase")
  else:
    enclave.print(f"Unfortunately your transaction did not have the right parameters :( Seller: {_seller} | Amount: {_amount} | Message: {_message} ") 
