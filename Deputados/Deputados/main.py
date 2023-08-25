import requests
from datetime import datetime, timedelta
from grafoDeputado import grafoDeputado
import csv as csv
import pandas as pd

# Mudar os caminhos conforme necessário
arq_grafo_2022 = r"C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-grafo.csv"
arq_votacoes_2022 = r"C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-deputados.csv"
arq_grafo_2023 = r"C:\Users\tulio\Documents\AEDSIII\NetworkLib\votacaoVotos-2023-grafo.csv"
arq_votacoes_2023 = r"C:\Users\tulio\Documents\AEDSIII\NetworkLib\votacaoVotos-2023-deputados.csv"

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
    
#Normalizacao [0,1]_2022-----------------------------------------------------------------------------------------------------
    cv = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-deputados.csv', encoding='ISO-8859-1')
    
    
    df = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2022.csv', encoding='ISO-8859-1')
    
    
    dp = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-grafo.csv', encoding='ISO-8859-1')
    qtd_p = len(dp)
    qtd_c = len(cv)
    for i in range(qtd_c):
        for j in range(qtd_p):
            if(dp['Candidato1'][j]==cv['Candidato'][i]):
                df.loc[j, 'Votos'] = (dp ['Votos'][j]/cv['Votos'][i])
                print(i, j)
    df.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2022.csv', index=False)
    
#----------------------------------------------------------------------------------------------------------------------

#Normalizacao [0,1]_2023-----------------------------------------------------------------------------------------------------
    cv = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2023-deputados.csv', encoding='ISO-8859-1')
    
    
    df = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2023.csv', encoding='ISO-8859-1')
    
    
    dp = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2023-grafo.csv', encoding='ISO-8859-1')
    qtd_p = len(dp)
    qtd_c = len(cv)
    for i in range(qtd_c):
        for j in range(qtd_p):
            if(dp['Candidato1'][j]==cv['Candidato'][i]):
                df.loc[j, 'Votos'] = (dp ['Votos'][j]/cv['Votos'][i])
                print(i, j)
    df.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2023.csv', index=False)
    
#----------------------------------------------------------------------------------------------------------------------


#Inversao de peso_2022-----------------------------------------------------------------------------------------------

    dr = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2022.csv', encoding='ISO-8859-1')
    
    dm = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\minimizado-2022.csv', encoding='ISO-8859-1')
    
    qtd_p = len(dr)
    
    for x in range(qtd_p):
        dm.loc[x, 'Votos'] = (1 - dr['Votos'][x])
    
    dm.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\minimizado-2022.csv', index=False)
#--------------------------------------------------------------------------------------------------------------  

#Inversao de peso_2023-----------------------------------------------------------------------------------------------

    dr = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2023.csv', encoding='ISO-8859-1')
    
    dm = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\minimizado-2023.csv', encoding='ISO-8859-1')
    
    qtd_p = len(dr)
    
    for x in range(qtd_p):
        dm.loc[x, 'Votos'] = (1 - dr['Votos'][x])
    
    dm.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\minimizado-2023.csv', index=False)
#--------------------------------------------------------------------------------------------------------------  



    
#TRESHOLD COLOCAR LIMITE MINIMO DE PESO_2023---------------------------------------------------------------------------
    treshold = float(input("Informe o mínimo de peso:"))
    
    fm = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\filtro_maiores-2023.csv', encoding='ISO-8859-1')
    dr = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2023.csv', encoding='ISO-8859-1')
    
    qtd_p = len(dr)
    x=1
    for x in range(qtd_p):
        if(dr['Votos'][x] > treshold):
            fm.loc[x, 'Candidato1'] = dr['Candidato1'][x]
            fm.loc[x, 'Candidato2'] = dr['Candidato2'][x]
            fm.loc[x, 'Votos'] = dr['Votos'][x]
            print(x)
        
    
    fm.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\filtro_maiores-2023.csv', index=False)
#-------------------------------------------------------------------------------------------------------------------------------

#TRESHOLD COLOCAR LIMITE MINIMO DE PESO_2022---------------------------------------------------------------------------
    treshold = float(input("Informe o mínimo de peso:"))
    
    fm = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\filtro_maiores-2022.csv', encoding='ISO-8859-1')
    dr = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2022.csv', encoding='ISO-8859-1')
    
    qtd_p = len(dr)
    x=1
    for x in range(qtd_p):
        if(dr['Votos'][x] > treshold):
            fm.loc[x, 'Candidato1'] = dr['Candidato1'][x]
            fm.loc[x, 'Candidato2'] = dr['Candidato2'][x]
            fm.loc[x, 'Votos'] = dr['Votos'][x]
            print(x)
        
    
    fm.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\filtro_maiores-2022.csv', index=False)
#-------------------------------------------------------------------------------------------------------------------------------
    
    

if __name__ == "__main__":
    main()
