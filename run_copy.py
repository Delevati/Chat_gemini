import requests
import json
from kfp import dsl
from kfp.components import create_component_from_func

API_KEY = 'AIzaSyDRl5XjlSdr-dSWUFGYNtchnZ1EmI4NyLY'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

# Criar um componente a partir da função gerar_resposta
gerar_resposta_op = create_component_from_func(
    func=create_component_from_func,
    output_component_file='gerar_resposta_component.yaml',
)

def gerar_resposta(texto: str, contexto: str = None) -> str:
    import requests

    headers = {'Content-Type': 'application/json'}
    data = {'contents': [{'parts': [{'text': texto}]}]}

    if contexto:
        data['context'] = contexto

    params = {'key': API_KEY}

    try:
        response = requests.post(API_URL, headers=headers, json=data, params=params)

        if response.status_code == 200:
            resposta_json = response.json()

            if 'candidates' in resposta_json and resposta_json['candidates']:
                proximo_contexto = resposta_json.get('context', None)
                texto_gerado = resposta_json['candidates'][0]['content']['parts'][0]['text']
                return texto_gerado, proximo_contexto
            else:
                print('Resposta JSON inválida.')
                return None, None
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f'Erro na solicitação: {e}')
        return f'Erro na solicitação: {e}', None

@dsl.pipeline(
    name='Gerar Resposta com Cache',
    description='Pipeline para gerar resposta com cache'
)
def gerar_resposta_pipeline(texto: str, contexto: str = None):
    gerar_resposta_op(texto, contexto)

if __name__ == '__main__':
    from kfp.compiler import Compiler
    from kfp import client as kfp_client

    # Compile the pipeline
    Compiler().compile(gerar_resposta_pipeline, 'gerar_resposta_pipeline.yaml')

    # Define the Kubeflow Pipelines metadata
    client = kfp_client.Client()
    exp = client.create_experiment(name='gerar_resposta_experiment')

    # Submit the pipeline run
    run = client.run_pipeline(
        experiment_id=exp.id,
        job_name='gerar-resposta-job',
        pipeline_package_path='gerar_resposta_pipeline.yaml',
        params={'texto': 'Digite a mensagem para a API', 'contexto': 'Seu contexto aqui'}
    )

    print(f'Pipeline run submitted: {run}')
