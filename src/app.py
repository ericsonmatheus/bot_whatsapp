import openpyxl
import os
import pandas as pd
import pyautogui
import pywhatkit as kit
import pytz
import webbrowser

from datetime import datetime, timedelta
from time import sleep

from utils import get_quantity_to_send, get_message_to_send

quantity_to_send = get_quantity_to_send()

message_to_send = get_message_to_send()

# Open the browser and access WhatsApp Web until it loads for the first time
webbrowser.open('https://web.whatsapp.com/')
sleep(10)

# Read the spreadsheet and store information about name and phone number
customers = pd.read_excel("./Clientes_Whatsapp/clientes.xlsx")
workbook = openpyxl.load_workbook("./Clientes_Whatsapp/clientes.xlsx")
customers_page = workbook['Sheet1']


current_date = datetime.today()
current_date = current_date.strftime("%d_%m_%Y")
try:
    sent_customers = pd.read_excel(f"./Clientes_Whatsapp/Mensagens_Enviadas/clientes_enviados_{current_date}.xlsx")
except FileNotFoundError:
    sent_customers = pd.DataFrame(columns=customers.columns)

for i, row in enumerate(customers_page.iter_rows(min_row=2), start=0):
    if i >= quantity_to_send:
        break

    phone = row[0].value
    phone_number = str(f"+55{phone}")
    message = message_to_send
    # Criar links personalizados do whatsapp e enviar mensagens para cada cliente
    # com base nos dados da planilha
    try:
        timezone = pytz.timezone("America/Sao_Paulo")
        now = datetime.now(timezone)
        send_time = now + timedelta(minutes=1)
        hour, minute = send_time.hour, send_time.minute
        wait_time = 10

        kit.sendwhatmsg(phone_number, message, hour, minute, wait_time)
        sleep(2)
        pyautogui.hotkey('ctrl','w')
        sleep(2)
        row = customers.iloc[[i]]
        sent_customers = pd.concat([sent_customers, row], ignore_index=True)
        customers = customers.drop(i)
    except Exception as e:
        print(e)
        print(f'Não foi possível enviar mensagem para o número {phone} - index: {i}')
        with open('erros.csv','a',newline='',encoding='utf-8') as file:
            file.write(f'{phone}{os.linesep}')

sent_customers.to_excel(f"./Clientes_Whatsapp/Mensagens_Enviadas/clientes_enviados_{current_date}.xlsx", index=False)
customers.to_excel("./Clientes_Whatsapp/clientes.xlsx", index=False)