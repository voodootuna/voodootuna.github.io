# -*- coding: utf-8 -*-
import json
import requests as req
from bs4 import BeautifulSoup
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time

sample_form_data = {
	'electionForm':'electionForm',
	'electionForm:eleNid':'',
	'javax.faces.ViewState':'H4sIAAAAAAAAANVWXWhcRRSebLq1aWNYE9MfbGxIo6YQ73bVtqlpsbHZmNXNWrK6mETQyd7p3UnvvXM7M7t7tz+hFVRQxEItIm1R0AcfUl98V6QPQtGgQRCUgoogPpSKKD74oDNz9979yW6TgApedodh7zlnvvOd75zZhRsg7DAK7piDBajlOTa1cchyE9AJ3/bNJ1c3P/9lKwiNgY0mgfoYzHJCE6CN5yhiOWLqrvPIISCf9uIGsUbEN8xBeO45rMfyFHTNJFVYE9qG9uTsHMry4XOLz7wdYbvMEACuI+xD+eNgHrRKT0e43DnTwGfrx3+mfzz27TXfpyXwCRUo6Jf2rnYUZhHTUAHZXDtC0SSydUQzGBXj8qffB051j3925SsZgoJ7l7scJpZDbLFLlxhHlnL6yBj6LbOY6fCcepY7Vdnec+zNq/j6tkXPtrtCp3rrJZJ8rS211Tr9vspDkN5VsRqhFJaSmHH37FLPW5/Cy62gJQHWMXwCeTQV18mV1WHP+qi1NIccjYuaIJqGBUSnrn148PylzydCIJQEbVkTMpaCFuKgU/EblfxG05xi2xhOgo1M+OgqBgebPQtMomlEMTTxCThromHXcQqS9w4m1wgH8cZInk4EXPY3YlVmiWxER3TocERF0beUa46JVnPiB1+0LaS/vpFYrpWQh0GS+Kg4WWN5u4xDribiTOPQ0ObYUQGMIm0UCQYo5LiAGiA51X8G3byQPKC4ut0mI9TwX3Fwl8LmRpEZnUA8R/S46wj5M0xsQVyHyK7KXKLarmp7fxNYyNSegkZ9JOA9Le1KPds8YoVpvd3x5JZN069//4unsq7ArmLx7ouvpH+dXjrga2yHj6NBtITlmNcn54fap87flCdL9DuKNpjeefIwsTliHNqcJQVpQR01bGOeIha2BZnEHkUcYhPpA03tDZPMQlO8ZsJt12kQqe/u+jlR1uSVpcxPP/ecfMyvPXAct3gZXIw60EAsagcQqrajsOQD0twct8zeQw/tH4zt3t9rlutzsO/fS63PVaK8W619/zmN8tR+qSG+2vH2P2BUjPfeZlNGzvZJQjioPGJEiU8wJVrnRR+u5N5/hBJHNHrpCVRifqBO1V8dFZLjdt6qfulwsF7MVJ7Qg8tT2SVEZgainT+8894fZ18eCskpHi5AM49EvKqipfLWLKIvLVzo2fTGd6/6Il/viLjdYlBkJV9jhFoPy7uUx2JDlWsy2LXUjUNfefeBnbeoSdZEkA4ICYFqyTS43EYUiEApM2CqrBSKDFl8Gpc4CfWFEXtg3+DePb1QuSVXIw8fSrlz+op7Voe8qi4ZgvUgD6DK35TDfWvgMAUevwUSJoBkc+X8m8tZgEhhvZZquRmWfL4AzqzE54ODe2Nr4XONsALan/1Hk125OpGa6ugcVorQYBeWTjU9vZtQQ3MotlB9W0MHi9YehRw2bWsZSONgAyXFhPiL6HEQ+0s8Ctv22nt7tGRDC2e9XmDKtkNGUn/HgOv+Deb+Y9dACwAA',
	'electionForm:j_idt39': 'electionForm:j_idt39',

}

url = 'https://oec.govmu.org/pages/nomination/nominationDayDetailed.xhtml'

prefix="electionForm:j_idt"
circ_map = {
	1:15,
	2:18,
	3:21,
	4:24,
	5:27,
	6:30,
	7:33,
	8:36,
	9:39,
	10:42,
	11:45,
	12:48,
	13:51,
	14:54,
	15:57,
	16:60,
	17:63,
	18:66,
	19:69,
	20:72,
	21:75
}

headers = {
	'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:19.0) Gecko/20100101 Firefox/19.0'
}

SAMPLE_SPREADSHEET_ID = '1eOqvk6dd373ibmJ0YO_arNjTUrVJHTtE4glBYdCKKls'
SAMPLE_RANGE_NAME = '1!A2:H'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def update_data(sheet_id, sheet_range, values):


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

    body = {
			'values' : values,
			#'majorDimension' : 'COLUMNS',
			}

    result = service.spreadsheets().values().update(
    spreadsheetId=sheet_id, range=sheet_range,
    valueInputOption='RAW', body=body).execute()



def scraphtml(circ_no):
	form_data = {
		'electionForm':'electionForm',
		'electionForm:eleNid':'',
		'javax.faces.ViewState':'H4sIAAAAAAAAANVWXWhcRRSebLq1aWNYE9MfbGxIo6YQ73bVtqlpsbHZmNXNWrK6mETQyd7p3UnvvXM7M7t7tz+hFVRQxEItIm1R0AcfUl98V6QPQtGgQRCUgoogPpSKKD74oDNz9979yW6TgApedodh7zlnvvOd75zZhRsg7DAK7piDBajlOTa1cchyE9AJ3/bNJ1c3P/9lKwiNgY0mgfoYzHJCE6CN5yhiOWLqrvPIISCf9uIGsUbEN8xBeO45rMfyFHTNJFVYE9qG9uTsHMry4XOLz7wdYbvMEACuI+xD+eNgHrRKT0e43DnTwGfrx3+mfzz27TXfpyXwCRUo6Jf2rnYUZhHTUAHZXDtC0SSydUQzGBXj8qffB051j3925SsZgoJ7l7scJpZDbLFLlxhHlnL6yBj6LbOY6fCcepY7Vdnec+zNq/j6tkXPtrtCp3rrJZJ8rS211Tr9vspDkN5VsRqhFJaSmHH37FLPW5/Cy62gJQHWMXwCeTQV18mV1WHP+qi1NIccjYuaIJqGBUSnrn148PylzydCIJQEbVkTMpaCFuKgU/EblfxG05xi2xhOgo1M+OgqBgebPQtMomlEMTTxCThromHXcQqS9w4m1wgH8cZInk4EXPY3YlVmiWxER3TocERF0beUa46JVnPiB1+0LaS/vpFYrpWQh0GS+Kg4WWN5u4xDribiTOPQ0ObYUQGMIm0UCQYo5LiAGiA51X8G3byQPKC4ut0mI9TwX3Fwl8LmRpEZnUA8R/S46wj5M0xsQVyHyK7KXKLarmp7fxNYyNSegkZ9JOA9Le1KPds8YoVpvd3x5JZN069//4unsq7ArmLx7ouvpH+dXjrga2yHj6NBtITlmNcn54fap87flCdL9DuKNpjeefIwsTliHNqcJQVpQR01bGOeIha2BZnEHkUcYhPpA03tDZPMQlO8ZsJt12kQqe/u+jlR1uSVpcxPP/ecfMyvPXAct3gZXIw60EAsagcQqrajsOQD0twct8zeQw/tH4zt3t9rlutzsO/fS63PVaK8W619/zmN8tR+qSG+2vH2P2BUjPfeZlNGzvZJQjioPGJEiU8wJVrnRR+u5N5/hBJHNHrpCVRifqBO1V8dFZLjdt6qfulwsF7MVJ7Qg8tT2SVEZgainT+8894fZ18eCskpHi5AM49EvKqipfLWLKIvLVzo2fTGd6/6Il/viLjdYlBkJV9jhFoPy7uUx2JDlWsy2LXUjUNfefeBnbeoSdZEkA4ICYFqyTS43EYUiEApM2CqrBSKDFl8Gpc4CfWFEXtg3+DePb1QuSVXIw8fSrlz+op7Voe8qi4ZgvUgD6DK35TDfWvgMAUevwUSJoBkc+X8m8tZgEhhvZZquRmWfL4AzqzE54ODe2Nr4XONsALan/1Hk125OpGa6ugcVorQYBeWTjU9vZtQQ3MotlB9W0MHi9YehRw2bWsZSONgAyXFhPiL6HEQ+0s8Ctv22nt7tGRDC2e9XmDKtkNGUn/HgOv+Deb+Y9dACwAA',
		'electionForm:j_idt{0}'.format(circ_map[circ_no]):'electionForm:j_idt{0}'.format(circ_map[circ_no]),

	}

	resp = req.post(url, headers=headers, data=form_data)
	soup = BeautifulSoup(resp.content, features="html.parser")

	table = soup.find('table', attrs={'class':['table,','table-bordered']})
	table_body = table.find('tbody')
	rows = table_body.find_all('tr')
	data = []
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    data.append([ele for ele in cols if ele]) # Get rid of empty values

	return data


def scrapallcirc():
	historical_data = {}
	for i in range(1,22):
		print("scrapping circ", i)
		data = scraphtml(i)
		time.sleep(5)
		historical_data[i]=data
	with open('./nomination_live.json','w') as f:
		json.dump(historical_data, f)


def main():
	scrapallcirc()
	with open('./nomination_live.json', 'r') as f:
		data = f.read()
		data = json.loads(data)
		for i in range(1, 22):
			print("updating sheet ", i)
			sheet_id = SAMPLE_SPREADSHEET_ID
			sheet_range = '{}!A2:Z'.format(i)
			values = data["{}".format(i)]
			update_data(sheet_id, sheet_range, values)


if __name__ == "__main__":
	print("--------------STARTING SCRIPT---------------")
	start = time.time()
	PERIOD_OF_TIME = 3600 # 60 min
	while True :
		print("**NEW SCRAP @", time.time())
		main()
		print("**TAKING A NAP FOR 10 secs")
		time.sleep(10)
		if time.time() > start + PERIOD_OF_TIME :
			print("--------------TERMINATING SCRIPT---------------")
			break

	
