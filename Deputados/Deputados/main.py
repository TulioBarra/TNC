import requests
from datetime import datetime, timedelta
from grafoDeputado import grafoDeputado
import csv as csv
import pandas as pd

# Mudar os caminhos conforme necessário
arq_grafo_2022 = r"C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-grafo.csv"
arq_votacoes_2022 = r"C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-deputados.csv"
arq_grafo_2023 = r"C:\Users\tulio\Documents\AEDSIII\NetworkLib\votacaoVotos-2023-grafo.txt"
arq_votacoes_2023 = r"C:\Users\tulio\Documents\AEDSIII\NetworkLib\votacaoVotos-2023-deputados.txt"

def fazer_requisicao(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Falha na requisição. Código de status:', response.status_code)
        return None

def buscar_votos(session, id):
    url = f"https://dadosabertos.camara.leg.br/api/v2/votacoes/{id}/votos"
    response = session.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Falha na requisição da votação. Código de status:', response.status_code)
        return None

def processar_votos(votos, g, lista_votos):
    qtd_votos = len(votos["dados"])
    if qtd_votos == 0:
        return None
    for deputado in range(qtd_votos):
        deputado_nome = votos["dados"][deputado]["deputado_"]["nome"]
        g.add_deputado(deputado_nome)
        tipo_voto = votos["dados"][deputado]["tipoVoto"]
        if tipo_voto == "Sim":
            g.add_grafo(lista_votos[0], deputado_nome)
        elif tipo_voto == "Não":
            g.add_grafo(lista_votos[1], deputado_nome)
        elif tipo_voto == "Obstrução":
            g.add_grafo(lista_votos[2], deputado_nome)

def salvar_dados(g, arq_grafo, arq_votacoes):
    g.salvar_grafo(arq_grafo)
    g.salvar_votacoes(arq_votacoes)
    print("DADOS SALVOS")             

def main():
    df = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-deputados.csv')
    
    
    cv = df
    print(cv)
    
    df = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-grafo.csv')
    if(df['Candidato1']):
        print(df)
        
        
    
if __name__ == "__main__":
    main()
