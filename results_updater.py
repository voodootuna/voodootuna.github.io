from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.


historical_data = {	
}


def get_value(row, index):
	val = ''
	try:
		val = row[index]
	except IndexError:
		pass

	return val


def main():
	SAMPLE_SPREADSHEET_ID = '1NmFe-ladkuaq33_TrKRF3Vvv5GP7IFzr4C-pgn7vhtY'
	SAMPLE_RANGE_NAME = '1!A2:H'

	for i in range(1,22):
		print("CIRCONSCRIPTION NO:", i)
		values = get_data(SAMPLE_SPREADSHEET_ID, '{0}!A2:H'.format(i))
		for row in values:
			# Print columns A and E, which correspond to indices 0 and 4.

			name = get_value(row, 0)
			party = get_value(row, 2)
			icon = get_value(row, 6)
			votes = get_value(row, 7)

			historical_data[str(i)] = {'name':name,'party':party,'icon_name':icon, 'votes':votes}

	with open("./results_live.json", "w") as f:
	#print(save_data)
		json.dump(historical_data, f)
	print('===============================')





def get_data(sheet_id, sheet_range):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=sheet_range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
  
    return values





if __name__ == '__main__':
    main()