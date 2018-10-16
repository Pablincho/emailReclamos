import poplib, email, os, sys, platform, getpass
from email import parser
import re
import logging
import time

logging.basicConfig(filename='emailReclamos.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

USERNAME = "senseitarg@gmail.com"
PASSWORD = "iotplatform"
SERVER_NAME = "pop.gmail.com"
PORT = 995

class ReadMail(object):
	def __init__(self, user, passw, server, port):
		self.username = user
		self.password = passw
		self.server_name = server
		self.port = port 
		self.check_mail_connection(self.username, self.password, self.server_name, self.port) 

	def check_mail_connection(self, username, password, server_name, port):
		try:
			client = poplib.POP3_SSL(server_name, port)
			client.user(username)
			client.pass_(password)
		except Exception as error:
			print ("ERROR: mail connection", str(error))
		return client

	def fetch_all_mails(self):
		raw_email = []
		print("Info:Procedure:fetch_mail")
		pop_conn = self.check_mail_connection(self.username, self.password, self.server_name, self.port)
		numMessages = len(pop_conn.list()[1])
		print("Info:Total number of messages:", +numMessages)
		for i in range(numMessages):
			print ("Info:Mail number:", i)
			#print(pop_conn.retr(i + 1)[1])
			#raw_email = "\n".join(pop_conn.retr(i + 1)[1])
			raw_email.append(b"\n".join(pop_conn.retr(i + 1)[1]))
			#print(raw_email)
		#print(raw_email)
		return raw_email

class ParseEmail(object):

	def parseEmail(self, raw_email):
		for pos, value in enumerate(raw_email):
			#print(value)
			#formatedValue = b"\n".join(str(raw_email))
			#print (formatedValue)
			parsed_email = parser.Parser().parsestr(str(value))
			#print(parsed_email)
			Body = []
			sUB = parsed_email['Subject']
			print ("Info:Subject:", sUB)
			print ("Info:To:" + str(parsed_email['To']))
			f = re.findall(r'[\w\.-]+@[\w\.-]+', (str(parsed_email['From'])))
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
			print("Here is the Body contents : ",Final_body)
        	#pop_conn.quit()

if __name__ == '__main__':
	mail = ReadMail(USERNAME, PASSWORD, SERVER_NAME, PORT)
	emailParser = ParseEmail() 

	while True:
		newMails = mail.fetch_all_mails()
		#print newMails
		emailParser.parseEmail(newMails)
		time.sleep(2)
