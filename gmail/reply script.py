import datetime
from email.mime.text import MIMEText
import os.path
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from email.message import EmailMessage
import requests


DELAY = 600

creds = None
# The file token.json stores the user's access and refresh tokens,and is
# created automatically when the authorization flow completes for the first
# time.
scopes = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify']
if os.path.exists('token.json'):
	creds = Credentials.from_authorized_user_file('token.json',scopes)
# If there are no (valid) credentials available,let the user log in.
if not creds or not creds.valid:
	if creds and creds.expired and creds.refresh_token:
		creds.refresh(Request())
	else:
		flow = InstalledAppFlow.from_client_secrets_file(
			'credentials.json',scopes)
		creds = flow.run_local_server(port=0)
	# Save the credentials for the next run
	with open('token.json','w') as token:
		token.write(creds.to_json())

def reply_message(sender,subject,text,message_id):
	try:
		service = build("gmail","v1",credentials=creds)
		message = EmailMessage()
		message.set_payload(text)
		message.add_header('Content-Type','text/html')

		message["To"] = sender
		message["From"] = "roger.wang@biologybowl.org"
		message["Subject"] = subject
		message["In-Reply-To"] = message_id
		message["References"] = message_id

		encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

		create_message = {"raw": encoded_message}

		send_message = (
			service.users()
			.messages()
			.send(userId="me",body = create_message)
			.execute()
		)
		print(f'Message Id: {send_message["id"]}\n')

	except HttpError as error:
		print(f"An error occurred: {error}")
		send_message = None

def get_auto_answer(input):
	question = input
	with open('context.txt') as f:
		context = '\n'.join(f.readlines())

	inference_request = {
		"inputs": [
			{
				"name": "question",
				"shape": [],
				"datatype": "BYTES",
				"data": [question],
				"parameters": {
					"content_type": "str"
				}
			},
			{
				"name": "context",
				"shape": [],
				"datatype": "BYTES",
				"data": [context],
				"parameters": {
					"content_type": "str"
				}
			}
		]
	}
	
	response = requests.post('http://0.0.0.0:8080/v2/models/faq/infer',json=inference_request).json()
	return response['outputs'][0]['data']

print('Server started.\n')
while True:
	service = build('gmail','v1',credentials=creds)

	results = service.users().labels().list(userId='me').execute()
	labels = results.get('labels',[])
	for label in labels:
		if label['name'] == 'Non-FAQ':
			non_faq_label_id = label['id']
		elif label['name'] == 'Auto-Answered':
			auto_answered_label_id = label['id']

	results = service.users().messages().list(userId='me',labelIds=['INBOX'],q="is:unread !label:non-faq").execute()
	messages = results.get('messages',[])
	print(datetime.datetime.now())

	if not messages:
		print("No messages\n")
		time.sleep(60)
		continue

	else:
		print("Messages found")

	for message in messages:

		msg = service.users().messages().get(userId='me',id = message['id']).execute()

		threads = service.users().threads().get(userId = 'me',id = message['threadId']).execute()
		if len(threads['messages']) > 1:
			service.users().messages().modify(userId='me',id = message['id'],body={'addLabelIds': [non_faq_label_id]}).execute()
			print("Message is part of a thread\n")
			continue
			
		headers = msg['payload']['headers']

		for header in headers:
			match header['name']:
				case 'From':
					from_name= header['value']
					from_email = re.findall('<(.*)>',from_name)[0]

					data = msg['payload']['parts'][0]['body']['data']	
					byte_code = base64.urlsafe_b64decode(data)
					text = str(byte_code.decode("utf-8"))
				
				case 'Subject':
					subject = header['value']

				case 'Message-ID':
					message_id = header['value']
		
		auto_answer = get_auto_answer(text)
		print(auto_answer)
		if float(auto_answer[0]) > 5:
			reply_message(from_email,subject,auto_answer[1] + '<br /><br />This is an automated response. If this did not answer your question, reply again.',message_id)

			service.users().messages().modify(userId='me',id = message['id'],body={'removeLabelIds': ['UNREAD'],'addLabelIds': [auto_answered_label_id]}).execute()
		else:
			service.users().messages().modify(userId='me',id = message['id'],body={'addLabelIds': [non_faq_label_id]}).execute()
			
	
	time.sleep(DELAY)