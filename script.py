import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, request
from markupsafe import escape

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]

"""
    A function to get the user's access and refresh tokens stored in the 'token.json' file.
	If the said credentials do not exist or not valid, the file is created automatically as the user logs in. The latter situation also assumes that the user has provided
	a 'secrets.json' file generated when they first created a client for this app.
"""
def getCreds():
	creds = None
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", SCOPES)	  	
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file("secrets.json", SCOPES)
			creds = flow.run_local_server()
		with open("token.json", "w") as token:
			token.write(creds.to_json())
	return creds

"""
    Using the credentials to connect, this function queries the drive storage to find files (of the .csv, .txt, .pdf or .png formats)
    whose text contains the target string.
    Files in drive are not explicitly characterized by their full path, so the latter is reconstructed by recursively querying the id and name of parent folders.
"""
def fetch(s, creds):
	try:
		query = f"(mimeType='text/csv' or mimeType='text/plain' or mimeType='application/pdf' or mimeType='image/png') and fullText contains '{s}'" #.csv, .txt, .pdf or .png		
		sf = build("drive", "v3", credentials=creds).files()
		items = sf.list(q=query, fields="files(id, name, parents)").execute().get("files", [])
		res = ''
		for item in items:
			path = ''
			x = item
			while ('parents' in x):
				x = sf.get(fileId=x['parents'][0], fields='id, name, parents').execute()
				path = f"{x['name']}/{path}"
			res += path+item['name']+"\n"
		return res
	
	except HttpError as error:
		print(f"An error occurred: {error}")
		return "Error!"

creds = getCreds()
app = Flask()

"""
    Function to generate the web page on the server that is then queried through the curl command mentioned in the assignment
"""
@app.route('/search')
def search():
    q = request.args.get('q', 'Flask')
    return f"{escape(fetch(q, creds))}"