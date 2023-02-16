import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path


# Define o título e as opções do botão de envio da pesquisa
st.title('Pesquisa de Satisfação')
submit_button = st.button('Enviar respostas')

# Obtém as respostas da pesquisa do usuário
rating = st.slider('De 0 a 10, qual é o seu nível de satisfação?', 0, 10)
option = st.selectbox('Como você se sente?', ('Feliz', 'Triste'))


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Pwo_2Ljq-CB1fmtofYBCDrG3hZI8zIcQCBe6cJEJqBI'
SAMPLE_RANGE_NAME = 'acompanhamento!A1:K'
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save the refreshed credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the new credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
try:
    if submit_button:
    st.success('As suas respostas foram enviadas com sucesso!')
    DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = build('sheets', 'v4', credentials=creds, discoveryServiceUrl=DISCOVERY_SERVICE_URL)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')

        # Iterate over the rows  
        result=service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED",
            body={"values": [[rating, option]]}
        ).execute()
        #print(row)

except HttpError as err:


# Escreve as respostas da pesquisa na planilha se o botão de envio for clicado

