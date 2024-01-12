import requests
import re
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
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'

def apply_color_to_text(text):
    # Se encontrar '**', aplica a cor aos caracteres entre '**'
    if '**' in text:
        colored_text = re.sub(r'\*\*(.*?)\*\*', f'{TerminalColors.YELLOW}\\1{TerminalColors.RESET}', text)
    else:
        colored_text = text

    # Se encontrar índices numéricos seguidos por ponto, aplica a cor
    colored_text = re.sub(r'(\d+\.\s)', f'{TerminalColors.YELLOW}\\1{TerminalColors.RESET}', colored_text)
    
    return colored_text

def solicity(texto, contexto=None):
    headers = {'Content-Type': 'application/json'}
    data = {'contents': [{'parts': [{'text': texto}]}]}

    if contexto:
        data['context'] = contexto

    params = {'key': os.getenv("API_KEY")}

    try:
        response = requests.post(os.getenv("API_URL"), headers=headers, json=data, params=params)
        response.raise_for_status()

        resposta_json = response.json()
        candidatos = resposta_json.get('candidates', [])

        if candidatos:
            proximo_contexto = resposta_json.get('context')
            texto_gerado = candidatos[0]['content']['parts'][0]['text']
            return apply_color_to_text(texto_gerado), proximo_contexto
        else:
            print(f'{TerminalColors.RED}Resposta JSON inválida.{TerminalColors.RESET}')
            return None, None

    except requests.exceptions.RequestException as e:
        erro_msg = f'Erro na solicitação: {e}'
        print(f'{TerminalColors.RED}{erro_msg}{TerminalColors.RESET}')
        return erro_msg, None

def main():
    while True:
        request = input(f'{TerminalColors.BOLD}Fala guri:{TerminalColors.RESET} ').strip()

        if request.lower() == 'sair':
            break

        resposta, _ = solicity(request)

        if resposta:
            print(f'\n{TerminalColors.GREEN}*** RESPOSTA:{TerminalColors.RESET}\n')
            print(resposta)
            print(''.join([TerminalColors.UNDERLINE + TerminalColors.BLUE + '_' + TerminalColors.RESET for _ in range(50)]))

if __name__ == '__main__':
    main()
