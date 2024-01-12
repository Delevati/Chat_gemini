import requests
import json
import dotenv
import os

dotenv.load_dotenv()

def solicity():
    instrucao_fixa = "Suas_instrucoes_aqui"
    texto_para_enviar = "Texto_de_input",

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'contents': [{
            'parts': [{
                'text': f'{instrucao_fixa}\n{texto_para_enviar}'
            }]
        }]
    }

    params = {
        'key': os.getenv("API_KEY")
    }

    response = requests.post(os.getenv("API_URL"), headers=headers, json=data, params=params)

    if response.status_code == 200:
        resposta_json = response.json()

        texto_gerado = resposta_json['candidates'][0]['content']['parts'][0]['text']
        return texto_gerado
    else:
        return f'Erro: Status Code: {response.status_code}, Mensagem: {response.text}'

if __name__ == '__main__':
    resposta = solicity()

    print(resposta)
