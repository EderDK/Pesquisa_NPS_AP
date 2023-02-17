import streamlit as st
from PIL import Image
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path
import emoji


def SheetsNPS(user_id, rating, option):
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
            body={"values": [[user_id, rating, option]]}
        ).execute()
        # print(row)

    except HttpError as err:
        print('A')
        

st.title('Pesquisa de Satisfação')

# Adiciona campo de entrada para CPF, RG ou CNPJ
user_id = st.text_input('Seu CPF, RG ou CNPJ')

# Carregando as imagens
imagem_feliz = Image.open("zzfeliz.png")
imagem_triste = Image.open("zztriste.png")

# Definindo as opções
opcoes = ["Feliz", "Triste"]

# Inicializando a opção selecionada na sessão
if "opcao_selecionada" not in st.session_state:
    st.session_state.opcao_selecionada = None

# Criando o botão com a imagem para a opção "Feliz"
with st.container():
    botao_feliz = st.image(imagem_feliz, width=100, output_format='PNG')
    if botao_feliz.button("", key="Feliz"):
        st.session_state.opcao_selecionada = "Feliz"

# Criando o botão com a imagem para a opção "Triste"
with st.container():
    botao_triste = st.image(imagem_triste, width=100, output_format='PNG')
    if botao_triste.button("", key="Triste"):
        st.session_state.opcao_selecionada = "Triste"

# Exibindo a opção selecionada
option = st.session_state.opcao_selecionada

submit_button = st.button('Enviar respostas')

# Obtém as respostas da pesquisa do usuário
rating = st.slider('De 0 a 10, qual é o seu nível de satisfação?', 0, 10)

if submit_button:
    if not user_id:
        st.warning('Por favor, informe seu CPF, RG ou CNPJ.')
    elif not option:
        st.warning('Por favor, selecione como você se sente.')
    else:
        SheetsNPS(user_id, rating, option)
        st.success('As suas respostas foram enviadas com sucesso!')
    