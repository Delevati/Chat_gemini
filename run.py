import requests
import re
import google.generativeai as genai
import dotenv
import os

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

safety_settings = [

]

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def apply_color_to_text(text):
    colored_text = re.sub(r'\*\*(.*?)\*\*|\d+\.\s', lambda match: f'{TerminalColors.YELLOW}{match.group(0)}{TerminalColors.RESET}', text)
    return colored_text

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
            return apply_color_to_text(texto_gerado), proximo_contexto

        print(f'{TerminalColors.RED}Resposta JSON inválida.{TerminalColors.RESET}')
        return None, None

    except requests.exceptions.RequestException as e:
        erro_msg = f'Erro na solicitação: {e}'
        print(f'{TerminalColors.RED}{erro_msg}{TerminalColors.RESET}')
        return erro_msg, None

def main():
    while True:
        request = input(f'{TerminalColors.BOLD}Fala guri:{TerminalColors.RESET}\n')
        if request.lower() == 'sair':
            break

        resposta, _ = solicity(request)

        if resposta:
            print(f'\n{TerminalColors.GREEN}*** RESPOSTA:{TerminalColors.RESET}\n')
            print(resposta)
            print(''.join([TerminalColors.UNDERLINE + TerminalColors.BLUE + '_' + TerminalColors.RESET for _ in range(50)]))

if __name__ == '__main__':
    main()
