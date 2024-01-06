import requests
import json

# Substitua 'SUA_CHAVE_API' pela sua chave API real
API_KEY = 'AIzaSyDRl5XjlSdr-dSWUFGYNtchnZ1EmI4NyLY'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

def fazer_solicitacao():
    # instrucao_fixa = "Voce é um Developer de python e deve sempre fazer todas as melhorias possíveis e retornar o codigo COMPLETO com as implementacoes. Desta vez quero que voce implemente um sistema de entendimento contextual da conversa atual que estou tendo."
    instrucao_fixa = "voce e um especialista em python e vai implementar dentro deste sistema algo parecido com cache para voce entender o contexto de nossa conversa atual. De algum jeito de armazenar as informações de nossas interações da conversa atual, este codigo que envio nao teve sucesso. Me retorne o codigo completo com a implementacao."
    texto_para_enviar = """ 
import requests
import json
from collections import deque

API_KEY = 'AIzaSyDRl5XjlSdr-dSWUFGYNtchnZ1EmI4NyLY'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

# Criando uma lista duplamente encadeada (deque) para armazenar o histórico de mensagens
historico_conversa = deque(maxlen=10)

def fazer_solicitacao(texto, contexto=None):
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        'contents': [{
            'parts': [{
                'text': texto
            }]
        }]
    }

    if contexto:
        data['context'] = contexto

    params = {
        'key': API_KEY
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, params=params)

        if response.status_code == 200:
            resposta_json = response.json()

            if 'candidates' in resposta_json and resposta_json['candidates']:
                proximo_contexto = resposta_json.get('context', None)
                texto_gerado = resposta_json['candidates'][0]['content']['parts'][0]['text']
                historico_conversa.append((texto, resposta_json))
                return texto_gerado, proximo_contexto
            else:
                print('Resposta JSON inválida.')
                return None, None
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Erro na solicitação: {e}')
        return f'Erro na solicitação: {e}', None

if __name__ == '__main__':
    contexto_conversa = None

    while True:
        texto_para_enviar = input('Digite a mensagem para a API (ou digite "sair" para encerrar): ').strip()

        if texto_para_enviar.lower() == 'sair':
            break

        resposta, contexto_conversa = fazer_solicitacao(texto_para_enviar, contexto_conversa)

        if resposta:
            print(resposta)

    # Imprimindo o histórico das conversas
    print('\nHistórico de conversas:')
    for mensagem, resposta_json in historico_conversa:
        print(f'Você: {mensagem}\n')
        print(f'Modelo: {resposta_json["candidates"][0]["content"]["parts"][0]["text"]}\n')

    """

    headers = {
        'Content-Type': 'application/json',
    }

    # Construir dados para a API com instrução fixa e texto
    data = {
        'contents': [{
            'parts': [{
                'text': f'{instrucao_fixa}\n{texto_para_enviar}'
            }]
        }]
    }

    params = {
        'key': API_KEY
    }

    response = requests.post(API_URL, headers=headers, json=data, params=params)

    if response.status_code == 200:
        resposta_json = response.json()

        # Exibir apenas o texto gerado
        texto_gerado = resposta_json['candidates'][0]['content']['parts'][0]['text']
        return texto_gerado
    else:
        return f'Erro: Status Code: {response.status_code}, Mensagem: {response.text}'

if __name__ == '__main__':
    resposta = fazer_solicitacao()

    # Exibir apenas o texto gerado
    print(resposta)
