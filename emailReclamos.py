import poplib, email, os, sys, platform, getpass
from email import parser
import re

SERVER_NAME = "pop.gmail.com"
PORT = 995
USERNAME = "senseitarg@gmail.com"
PASSWORD = "iotplatform"

def check_mail_connection(username, password, server_name, port):
	try:
		client = poplib.POP3_SSL(SERVER_NAME, PORT)
		client.user(USERNAME)
		client.pass_(PASSWORD)
	except Exception as error:
		print ("ERROR: mail connection", str(error))
	return client

def fetch_all_mails():
    print("Info:Procedure:fetch_mail")
    pop_conn = check_mail_connection(USERNAME, PASSWORD, SERVER_NAME, PORT)
    numMessages = len(pop_conn.list()[1])
    print("Info:Total number of messages:", +numMessages)
    for i in range(numMessages):
        print ("Info:Mail number:", i)
        raw_email = b"\n".join(pop_conn.retr(i + 1)[1])
        print(raw_email)
        parsed_email = parser.Parser().parsestr(raw_email)
        Body = []
        sUB = parsed_email['Subject']
        print ("Info:Subject:", sUB)
        print ("Info:To:" + parsed_email['To'])
        f = re.findall(r'[\w\.-]+@[\w\.-]+', (parsed_email['From']))
        #You can print other parameters as weel. Such as attachement, if yes, then you can download the attachment. 
        print ("Mail From:", f[0])
        print ("Thread-Index", parsed_email['Thread-Index'])
        print ("In-Reply-To", parsed_email['In-Reply-To'])
        print ("Message-ID", parsed_email['Message-ID'])
        print ("References", parsed_email['References'])
        if parsed_email.is_multipart() == False:
            print("Info: This mail is not multilple lines.")
            Final_body = parsed_email.get_payload()
        else:
            print("Info: Multiline in body")
            
            for payload in parsed_email.get_payload():
                print(payload.get_payload)
                Body.append(payload.get_payload())
            Final_body='\n'.join(Body)
            #Final_body = '\n'.join(str(v) for v in Body)
            #Body = parsed_email.get_payload()
        print("Info: Here is the Body contents : ",Final_body)
        pop_conn.quit()

fetch_all_mails()
#newClient = check_mail_connection(USERNAME, PASSWORD, SERVER_NAME, PORT)
#print(newClient)
#welcomeMsg = POP3.getwelcome()
#print(welcomeMsg)