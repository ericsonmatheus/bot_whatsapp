import webbrowser
from datetime import datetime
from pathlib import Path
from time import sleep
from urllib.parse import quote

import openpyxl
import pandas as pd
import pyautogui
from pyautogui import ImageNotFoundException

from utils import get_message_to_send, get_quantity_to_send, save_message_sent, show_errors

PROJECT_ROOT = Path(__file__).resolve().parent.parent

quantity_to_send = get_quantity_to_send()

message_to_send = get_message_to_send()

# Open the browser and access WhatsApp Web until it loads for the first time
webbrowser.open("https://web.whatsapp.com/")
sleep(30)

# Read the spreadsheet and store information about name and phone number
customers = pd.read_excel(f"{PROJECT_ROOT}/Clientes_Whatsapp/clientes.xlsx")
workbook = openpyxl.load_workbook(f"{PROJECT_ROOT}/Clientes_Whatsapp/clientes.xlsx")
customers_page = workbook["Sheet1"]


current_date = datetime.today()
current_date = current_date.strftime("%d_%m_%Y")
try:
    sent_customers = pd.read_excel(
        f"{PROJECT_ROOT}/Clientes_Whatsapp/Mensagens_Enviadas/clientes_enviados_{current_date}.xlsx"
    )
except FileNotFoundError:
    sent_customers = pd.DataFrame(columns=customers.columns)

for i, row in enumerate(customers_page.iter_rows(min_row=2), start=0):
    if i >= quantity_to_send:
        break

    phone = row[0].value
    phone_number = str(f"55{phone}")

    try:
        link_mensagem_whatsapp = (
            f"https://web.whatsapp.com/send?phone={phone}&text={quote(message_to_send)}"
        )
        webbrowser.open(link_mensagem_whatsapp)
        sleep(50)
        seta = pyautogui.locateCenterOnScreen(f"{PROJECT_ROOT}/src/images/seta.png")
        sleep(5)
        pyautogui.click(seta[0], seta[1])
        sleep(5)
        pyautogui.hotkey("ctrl", "w")
        sleep(2)
        row = customers.iloc[[0]]
        sent_customers = pd.concat([sent_customers, row], ignore_index=True)
        customers = customers.drop(i)

        sent_customers.to_excel(
            f"{PROJECT_ROOT}/Clientes_Whatsapp/Mensagens_Enviadas/clientes_enviados_{current_date}.xlsx",
            index=False,
        )
        customers.to_excel(f"{PROJECT_ROOT}/Clientes_Whatsapp/clientes.xlsx", index=False)
    except ImageNotFoundException:
        show_errors("O Navegador estava inacessível quanto tentamos enviar uma mensagem.")
    except Exception as e:
        show_errors(e.__doc__[:100] + "...")

pyautogui.hotkey("alt", "f4")
save_message_sent(message_to_send)
