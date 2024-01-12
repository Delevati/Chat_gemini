import requests
import re
import google.generativeai as genai
import dotenv
import os
import tkinter as tk
from tkinter import Label, Entry, Button, Scrollbar, Text, END, messagebox

dotenv.load_dotenv()

class TerminalColors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'


generation_config = {
    "temperature": 8.0,
    "top_p": 5,
    "top_k": 5,
    "max_output_tokens": 2048,
}

safety_settings = []

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

class TextExchangeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Troca de Texto")
        
        self.create_widgets()

    def create_widgets(self):
        self.text_output = Text(self.root, wrap=tk.WORD, height=15, width=50, state=tk.DISABLED)
        self.text_output.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        scrollbar = Scrollbar(self.root, command=self.text_output.yview)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.text_output['yscrollcommand'] = scrollbar.set

        Label(self.root, text="Digite a mensagem:").grid(row=1, column=0, columnspan=2, pady=5)

        self.text_input = Entry(self.root, width=40)
        self.text_input.grid(row=2, column=0, columnspan=2, pady=5)

        Button(self.root, text="Enviar", command=self.send_message).grid(row=3, column=0, columnspan=2, pady=10)

    def send_message(self):
        user_input = self.text_input.get()
        if user_input.lower() == 'sair':
            self.root.destroy()
        else:
            response, _ = solicity(user_input)

            if response:
                self.display_response(response)

            self.text_input.delete(0, END)  # Limpar a caixa de entrada

    def display_response(self, response):
        self.text_output.config(state=tk.NORMAL)
        self.text_output.insert(END, f'{response}\n\n')
        self.text_output.config(state=tk.DISABLED)
        self.text_output.yview(tk.END)  # Rolagem automática para a última mensagem visível

def apply_color_to_text(text):
    colored_text = re.sub(r'\*\*(.*?)\*\*|\d+\.\s', lambda match: f'{TerminalColors.YELLOW}{match.group(0)}{TerminalColors.RESET}', text)
    return colored_text

def solicity(texto, contexto=None):
    headers = {'Content-Type': 'application/json'}
    
    # Modificando aqui para agrupar todas as linhas em uma única string
    texto = texto.replace('\n', ' ')
    
    data = {'contents': [{'parts': [{'text': texto}]}]}

    if contexto:
        data['context'] = contexto

    params = {'key': os.getenv("API_KEY")}

    try:
        with requests.post(os.getenv("API_URL"), headers=headers, json=data, params=params) as response:
            response.raise_for_status()
            resposta_json = response.json()

        candidatos = resposta_json.get('candidates', [])

        if candidatos:
            proximo_contexto = resposta_json.get('context')
            texto_gerado = candidatos[0]['content']['parts'][0]['text']
            return apply_color_to_text(texto_gerado), proximo_contexto

        print(f'{TerminalColors.RED}Resposta JSON inválida.{TerminalColors.RESET}')
        return None, None

    except requests.exceptions.RequestException as e:
        erro_msg = f'Erro na solicitação: {e}'
        print(f'{TerminalColors.RED}{erro_msg}{TerminalColors.RESET}')
        return erro_msg, None

if __name__ == "__main__":
    root = tk.Tk()
    app = TextExchangeUI(root)
    root.mainloop()