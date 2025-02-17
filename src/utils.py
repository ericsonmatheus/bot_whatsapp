import tkinter as tk
from pathlib import Path
from tkinter import messagebox, simpledialog

PROJECT_ROOT = Path(__file__).resolve().parent.parent


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

    file_path = f"{PROJECT_ROOT}/src/message.txt"

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    default_message = content

    def on_confirm():
        nonlocal message_to_send
        message_to_send = text_widget.get("1.0", "end-1c")
        window.destroy()

    def on_cancel():
        nonlocal message_to_send
        message_to_send = None
        window.destroy()

    window = tk.Tk()
    window.title("Editar Mensagem")
    window.geometry("860x800")

    text_widget = tk.Text(window, wrap="word", font=("Arial", 12))
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)
    text_widget.insert("1.0", default_message)

    button_frame = tk.Frame(window)
    button_frame.pack(fill="x", pady=5)

    confirm_button = tk.Button(button_frame, text="Confirmar", command=on_confirm)
    confirm_button.pack(side="left", padx=10)

    cancel_button = tk.Button(button_frame, text="Cancelar", command=on_cancel)
    cancel_button.pack(side="right", padx=10)

    message_to_send = None

    window.mainloop()

    if message_to_send is None:
        print("Operação cancelada pelo usuário.")
        exit()

    return message_to_send


# def show_errors(error):
#     window = tk.Tk()
#     window.withdraw()
#     messagebox.showinfo(
#         "Erro durante a execução!",
#         "Envie o print/foto do erro para o suporte em seguida pode prosseguir: \n\n" + "Motivo do erro: " + error,
#     )
#     window.destroy()


def save_message_sent(message):
    file_path = f"{PROJECT_ROOT}/src/message.txt"

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(message)
