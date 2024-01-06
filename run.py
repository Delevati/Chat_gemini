import requests

API_KEY = 'AIzaSyDRl5XjlSdr-dSWUFGYNtchnZ1EmI4NyLY'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

def solicity(texto, contexto=None):
    headers = {'Content-Type': 'application/json'}
    data = {'contents': [{'parts': [{'text': texto}]}]}

    if contexto:
        data['context'] = contexto

    params = {'key': API_KEY}

    try:
        response = requests.post(API_URL, headers=headers, json=data, params=params)
        response.raise_for_status()

        resposta_json = response.json()
        candidatos = resposta_json.get('candidates', [])

        if candidatos:
            proximo_contexto = resposta_json.get('context')
            texto_gerado = candidatos[0]['content']['parts'][0]['text']
            return texto_gerado, proximo_contexto
        else:
            print('Resposta JSON inválida.')
            return None, None

    except requests.exceptions.RequestException as e:
        print(f'Erro na solicitação: {e}')
        return f'Erro na solicitação: {e}', None

def main():
    while True:
        request = input('Fala guri: ').strip()

        if request.lower() == 'sair':
            break

        resposta, _ = solicity(request)

        if resposta:
            print('\n *** RESPOSTA:', resposta)
            print(''.join(['_' for _ in range(50)]))

if __name__ == '__main__':
    main()
