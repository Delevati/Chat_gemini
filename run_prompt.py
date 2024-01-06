import requests
import json

# Substitua 'SUA_CHAVE_API' pela sua chave API real
API_KEY = ''
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

def solicity():
    instrucao_fixa = "Você é um programa para extrair campos importantes de um texto, eu preciso que vc extraia os campos: Numero da nota, data e hora de emissao como um unico campo, o município onde o serviço foi prestado, o codigo do serviço, o valor total bruto da nota, o CPF ou CNPJ do prestador, CPF ou CNPJ do tomador e a Observacao/Descriminacao da nota. Me de a resposta com apenas os campos extraidos em um formato json e a chave dos valors deve os nomes das tags sendo essas exatas: numeroNFSe, dataEmissaoNFSe, municipioExecServico, codigoServico, valorServico, CPF_CNPJ_Prestador, CPF_CNPJ_Tomador e Observaca/Descriminação dos serviços."
    texto_para_enviar = "prefeitura municipal de fortaleza numero da fortaleza prefcitura secretaria municipal das financas nfse financas nota fiscal eletronica de servico nfse 41 data e hora da emissao 06022023 181818 competencia 022023 codigo de verificacao 842352057 numero do rps no nfse substituida local da prestacao fortaleza ce dados do prestador de servicos razao socialnome share consultoria em tecnologia da informacao ltda nome fantasia share tecnologia cpficnpj 35708358000158 insc municipal 5280737 municipio fortaleza ce endereco e cep r flor de lis,236 parangaba cep60740440 complemento telefone email fabiiolaellengmailcom dados do tomador de servicos razao socialnome gran tecnologia e educacao sia cpficnpj 18260822000177 inscricao municipal municipio brasilia df endereco e cep sbs quadra 2, sn 70070120 cep 70070120 complemento iala 201 sala 601 sala telefone 61999970117 email annarodriguesggeducacionalcombr discriminacao dos servicos alertas e notificacoes de termos nos diarios oficiais codigo de atividade cnae 103 631190099 tratamento de dados provedores de servicos de aplicacao e servicos de hospedagem na internet detalhamento especifico da construcao civil da obra codigo art tributos federais pis cofins irrs inssrs csllrs detalhamento de valores prestador dos servicos calculo do issqn devido no municipio valor dos servicos r$ 1990,00 natureza operacao valor dos servicos r$ 1990,00 desconto incondicionado 1tributacao no municipio deducoes permitidas em lei desconto condicionado regime especial tributacao desconto incondicionado retencoes federais 0,00 6microempresario e empresa de base de calculo 1990,00 outras retencoes opcao simples nacional aliquota % 5,00 iss retido 0,00 1 sim iss a reter sim x nao incentivador cultural valor liquido r$ 1990,00 valor do iss r$ 99,50 2 nao uma via desta nota fiscal sera enviada atraves do email fornecido pelo tomador dos servicos, no sitio httptliss fortalezacegovbr 2 a autenticidade desta nota fiscal podera ser validada no site httplliss fortalezace gov brl , com a utilizacao do codigo de verificacao 3 documento emitido por me ou epp optante pelo simples nacional nao gera direito a credito fiscal de iss e ipi avisos 4 servico sujeito ao anexo 3 5 servicos nao sujeitos ao fator r' e tributados pelo anexo iii, exceto para 0 exterior , sem retencao com iss devido ao proprio municipio codigo "

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
    resposta = solicity()

    # Exibir apenas o texto gerado
    print(resposta)
