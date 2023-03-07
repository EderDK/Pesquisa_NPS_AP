import streamlit as st
from PIL import Image
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
from time import sleep
import emoji
from datetime import datetime


def SheetsNPS(user_id, rating, option, data, hora):
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1-HjOi7-0y-O3h2xVI8Ul2SnwOR8qIdxZbmmTgWMx4cQ'
    SAMPLE_RANGE_NAME = 'Pesquisa_Respostas!A2:C'
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
        DISCOVERY_SERVICE_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
        service = build('sheets', 'v4', credentials=creds,
                        discoveryServiceUrl=DISCOVERY_SERVICE_URL)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])
        if not values:
            print('No data found.')

        # Iterate over the rows
        result = service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED",
            body={"values": [[user_id, rating, option, data, hora]]}
        ).execute()
        # print(row)
    except HttpError as err:
        print('A')

st.markdown('<center><h1 style="font-size: 24pt; margin-bottom: 30px;">Pesquisa de Satisfação</h1></center>', unsafe_allow_html=True)

data = datetime.today()
data = data.strftime("%d/%m/%Y")

hora = datetime.now().strftime("%H:%M")
# Adiciona campo de entrada para CPF, RG ou CNPJ
user_id = st.text_input('Seu CPF/CNPJ')

st.write('')

# Obtém as respostas da pesquisa do usuário
rating = st.slider('De 0 a 10, qual é o seu nível de satisfação?', 0, 10)

st.markdown('<center><h1 style="font-size: 18pt; ">Como foi sua experiência?</h1></center>', unsafe_allow_html=True)

# Divide a tela em duas colunas para colocar os botões lado a lado
_, _ , col1, col2, col3, _ , _ = st.columns([1.6, 1, 1.3, 1.5, 2, 1, 1])

# Adiciona botões de "feliz" e "triste" em col1
with col1:
    option_feliz = st.button(emoji.emojize(':smiling_face_with_smiling_eyes: Feliz'), key='Feliz')

# Adiciona um espaço em branco entre os botões
st.write("")

with col2:
    option_neutro = st.button(emoji.emojize(':neutral_face: Neutro'), key='Neutra')

with col3:
    option_triste = st.button(emoji.emojize(':disappointed_face: Triste'), key='Triste')

# Verifica qual botão foi clicado e atribui a opção correspondente
if option_feliz:
    option = 'Feliz'
elif option_neutro:
    option = 'Neutro'
elif option_triste:
    option = 'Triste'
else:
    option = None

if option != None:
    if not user_id:
        st.warning('Por favor, informe seu CPF, RG ou CNPJ.')
    elif not option_feliz and not option_triste and not option_neutro:
        st.warning('Por favor, selecione como você se sente.')
    else:
        SheetsNPS(user_id, rating, option, data, hora)
        user_id = ""
        st.success('As suas respostas foram enviadas com sucesso!')
        sleep(2)
        st.experimental_rerun()
        
        # Conecta ao sheets e manda as respostas na planilha.
    