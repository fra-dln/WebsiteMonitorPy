# Importing libraries
import time
import hashlib
import smtplib
from urllib.request import urlopen, Request
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS='test.allert@outlook.com'
MY_PASSWORD='Password4321'
TO_='kecco9939@gmail.com'
URL='http://www.sbai.uniroma1.it/~daniela.sforza/'
MESSAGE="Hey the websites you are monitoring has changed!"


# setting the URL you want to monitor
url = Request(URL, 
              headers={'User-Agent': 'Mozilla/5.0'})

# setup the smtp 
s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
s.starttls()
s.login(MY_ADDRESS, MY_PASSWORD)
  
# to perform a GET request and load the 
# content of the website and store it in a var
response = urlopen(url).read()
  
# to create the initial hash
currentHash = hashlib.sha224(response).hexdigest()
print("running")
time.sleep(10)
while True:
    try:
        # perform the get request and store it in a var
        response = urlopen(url).read()
          
        # create a hash
        currentHash = hashlib.sha224(response).hexdigest()
          
        # wait for 3600 seconds
        time.sleep(3600)
          
        # perform the get request
        response = urlopen(url).read()
          
        # create a new hash
        newHash = hashlib.sha224(response).hexdigest()
  
        # check if new hash is same as the previous hash
        if newHash == currentHash:
            continue
  
        # if something changed in the hashes
        else:
            # notify
            print("something changed")

            #create a message
            msg = MIMEMultipart()
            msg['From']=MY_ADDRESS
            msg['To']=TO_
            msg['Subject']="NOTIFY"

            #put text in message
            msg.attach(MIMEText(MESSAGE, 'plain'))

            #send and delete message
            s.send_message(msg)
            del msg

            # again read the website
            response = urlopen(url).read()
  
            # create a hash
            currentHash = hashlib.sha224(response).hexdigest()
  
            # wait for 3600 seconds
            time.sleep(3600)
            continue
              
    # To handle exceptions
    except Exception as e:
        print("error")