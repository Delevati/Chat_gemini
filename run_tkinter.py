import tkinter as tk
from tkinter import scrolledtext, ttk
import requests
import regex
import dotenv
import os

dotenv.load_dotenv()

generation_config = {
    "temperature": None,
    "top_p": None,
    "top_k": None,
    "max_output_tokens": None,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def apply_color_to_text(text_widget, text, tag):
    color_map = {
        r'\*\*(.*?)\*\*': 'yellow',
    }

    for pattern, color in color_map.items():
        matches = regex.finditer(pattern, text)
        for match in matches:
            start, end = match.span()
            text_widget.tag_add(tag, f"1.{start}", f"1.{end}")

    return text

def solicity(texto, contexto=None):
    headers = {'Content-Type': 'application/json'}

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
            return texto_gerado, proximo_contexto

        print('\033[91mResposta JSON inválida.\033[0m')
        return None, None

    except requests.exceptions.RequestException as e:
        erro_msg = f'Erro na solicitação: {e}'
        print(f'\033[91m{erro_msg}\033[0m')
        return erro_msg, None

class TerminalApp:
    def __init__(self, root):
        self.root = root
        root.title("LLM Terminal")
        root.geometry("800x600")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#2E2E2E")
        style.configure("TButton", background="#444", foreground="white")
        style.configure("TLabel", background="#2E2E2E", foreground="white")
        style.configure("TText", background="#333", foreground="white", font=("Helvetica Neue", 15))
        style.map("TButton", background=[("active", "#555")])

        # Configuração de pesos para dividir a área de conversação e os botões
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=8)
        root.rowconfigure(1, weight=2)

        # Criar um Frame para conter os controles deslizantes
        sliders_frame = ttk.Frame(root, style="TFrame")
        sliders_frame.grid(row=0, column=1, sticky=tk.NSEW)

        # Configurar pesos para dividir a largura entre a área de conversação e os controles deslizantes
        sliders_frame.columnconfigure(0, weight=1)

        # Adicionar a área de conversação
        self.text_entry = scrolledtext.ScrolledText(root, wrap=tk.NONE, bg="#333", fg="white", insertbackground="white")
        self.text_entry.grid(row=0, column=0, sticky=tk.NSEW)

        # Adicionar os controles deslizantes no Frame
        self.create_slider(sliders_frame, "Temperatura", "temperature", row=0, column=0)
        self.create_slider(sliders_frame, "Top P", "top_p", row=1, column=0)
        self.create_slider(sliders_frame, "Top K", "top_k", row=2, column=0)
        self.create_slider(sliders_frame, "Max Tokens", "max_output_tokens", multiple=512, max_value=10000, row=3, column=0)

        # Configurar barra de rolagem horizontal para a área de conversação
        horizontal_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=self.text_entry.xview)
        horizontal_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        self.text_entry.configure(xscrollcommand=horizontal_scrollbar.set)


    def create_slider(self, root, label_text, config_key, multiple=1, max_value=None, row=0, column=0):
        label = ttk.Label(root, text=label_text)
        label.grid(row=row, column=column, sticky=tk.E, padx=5, pady=5)

        variable = tk.DoubleVar() if "temperature" in config_key else tk.IntVar()
        variable.set(generation_config[config_key] if generation_config[config_key] is not None else 10)

        def update_label(value, key=config_key):
            variable = generation_config[key]
            variable.set(value)
            label = next((w for w in self.root.winfo_children() if w.winfo_name() == key + "_label"), None)
            if label:
                label.config(text=f"{key.replace('_', ' ').title()}: {variable.get()}")

        scale = tk.Scale(
            root, from_=1, to=max_value, orient=tk.HORIZONTAL, label=label_text,
            variable=variable, command=lambda x, key=config_key: update_label(x, key),
            resolution=multiple
        )
        scale.set(variable.get())
        scale.grid(row=row+1, column=column, sticky=tk.E, padx=5, pady=5)

        label = ttk.Label(root, text=f"{label_text}: {variable.get()}", name=f"{config_key}_label")
        label.grid(row=row+2, column=column, sticky=tk.E, padx=5, pady=5)

        generation_config[config_key] = variable

    def process_input(self, event):
        input_text = self.text_entry.get("1.0", tk.END)
        input_text = input_text.strip()

        # Adiciona a mensagem do usuário à saída da conversação com espaçamento
        self.text_entry.config(state=tk.NORMAL)
        self.text_entry.insert(tk.END, f"\nVocê: {input_text}\n")

        # Envia a mensagem para a LLM
        response, _ = solicity(input_text)

        # Adiciona a resposta da LLM à saída da conversação com espaçamento
        if response:
            apply_color_to_text(self.text_entry, response, 'yellow')
            self.text_entry.insert(tk.END, f"LLM: {response}\n")

        self.text_entry.see(tk.END)  # Rolagem automática para a última linha
        self.text_entry.config(state=tk.DISABLED)

# Chamando a função para criar a interface gráfica
root = tk.Tk()
app = TerminalApp(root)
root.mainloop()
