import requests
import json
import dotenv
import os

dotenv.load_dotenv()

def solicity():
    instrucao_fixa = "Voce eh um programa especializado em extrair alguns campos de uma string. Os campos a serem extraidos sao: [cnpj fornecedor][cnpj empresa][valorboleto][data competencia][numero do documento]"
    texto_para_enviar = "Boleto DDA Documento nao compensavel bradesco net empresa Dados do Banco Destinatario Banco Codigo 237 Nome Banco Bradesco SA Codigo de 23110106693516420 Identificacao DDA Dados do Beneficiario Beneficiario Nome FT VELLOITCORE PLATO 365 SOLUCOES EM TE CPFCNPJ 030962993000143 Endereco R EMILIO MALLET, 317 VILA GOMES CARDIM 03320000 SAO PAULO SP Agencia 02423 Conta 39952 3 Dados do Pagador Pagador Nome INSPER INSTITUTO DE ENSINO E PESQUISA CPFCNPJ 006070152000147 Endereco RUA QUATA 300 VILA OLIMPIA 04546042 SAO PAULO SP Dados do Boleto Data do Data do documento 01112023 processamento 01112023 Data e hora da impressao 01112023 145103 Data do vencimento 30112023 Data limite de pagamento 29012024 Nosso numero 09330500000026 Seu numero 000451 Especie do DM Carteira 9 documento CIP 000 Especie moeda R$ Quantidade Aceite N Valor do documento R$ 491188 Descontos R$ Abatimentos R$ Bonificacao R$ Juros R$ Multa R$ Valor a cobrar R$ Dados do beneficiario final Beneficiario final Nome Nao informado Endereco Nao informado Mensagemn de Instrucao VALORES EXPRESSOS EM REAIS 444 ^ JUROS POR DIA DE ATRASO 163 APOS 30112023 MULTA 98,23 Representacao Numerica Numero 2379242304 93305000007 02003995202 1 95500000491188 Sac Servi?o de 4l? Bradesco Deficiente Auditivo ou de Fala Cancelamentos, Reclam a??es Inform a??es Dem ais telefones Apoio a0 Cliente 0800 704 8383 0800 722 0099 Ptendim ento 24 horas, dias Por semana consulte 0 site Fale Conosco Ouvidoria 0800 727 9933 Ptendim ento de segunda 2 sextafeira das 8h ?s 18h, exceto feriados ",

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
        'key': os.getenv("API_KEY")
    }

    response = requests.post(os.getenv("API_URL"), headers=headers, json=data, params=params)

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
