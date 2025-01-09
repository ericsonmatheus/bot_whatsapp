import tkinter as tk
from tkinter import simpledialog, messagebox

def get_quantity_to_send():
    while True:
        window = tk.Tk()
        window.withdraw()

        user_input = simpledialog.askstring(
            "Quantidades", "Quantos clientes devem receber mensagem?"
        )
        window.destroy()

        if user_input is None:
            return None

        try:
            quantidade = int(user_input)

            print(f"Quantidade informada: {quantidade}")
            return quantidade
        except (ValueError, TypeError):
            window = tk.Tk()
            window.withdraw()
            messagebox.showinfo("AVISO!", "Você digitou um número inválido! Tente novamente.")
            window.destroy()

def get_message_to_send():
    message_to_send = """
        Olá *Prezado militar*, tudo bem?

        📍Espero que esteja bem. Sou Valquíria Faria Representante do banco SABEMI, especialista em Empréstimo consignado.

        📍Estamos oferecendo condições especiais em empréstimos consignados para militares  do Exército e Pensionistas,estamos com taxas de juros reduzidas para refin e compra de dívida de todos os bancos.

        📍Estou à disposição para realizar uma simulação personalizada e sem compromisso. Aguardo seu retorno para discutirmos como podemos beneficiar suas condições financeiras, caso queira agendar um horário posso passar maiores informações, trabalhamos com vários bancos!

        Atenciosamente *Valquiria Faria*
    """
    return message_to_send