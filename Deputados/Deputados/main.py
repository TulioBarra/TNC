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
    ano = int(input("Digite o ano a se considerar (2022 ou 2023):"))
    treshold = float(input("Informe o mínimo de peso:"))
#Normalizacao 2022---------------------------------------------------------------------------------------------------------------------------------
    if(ano==2022):
        vd_22 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-deputados.csv', encoding='ISO-8859-1')
        re_22 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2022.csv', encoding='ISO-8859-1')
        
        vg_22 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2022-grafo.csv', encoding='ISO-8859-1')
        qtd_p = len(vg_22)
        qtd_c = len(vd_22)
        for i in range(qtd_c):
            for j in range(qtd_p):
                if(vg_22['Candidato1'][j]==vd_22['Candidato'][i]):
                    re_22.loc[j, 'Votos'] = (vg_22 ['Votos'][j]/vd_22['Votos'][i])
                    print(i, j)
        re_22.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2022.csv', index=False) 
#------------------------------------------------------------------------------------------------------------------------------------------------
#Inversao de peso 2022-------------------------------------------------------------------------------------------------------------------------------------
        re_2022 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2022.csv', encoding='ISO-8859-1')
        mm_22 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\minimizado-2022.csv', encoding='ISO-8859-1')
        
        qtd_p = len(re_22)
        x=1
        for x in range(qtd_p):
            mm_22.loc[x, 'Candidato1'] = re_2022['Candidato1'][x]
            mm_22.loc[x, 'Candidato2'] = re_2022['Candidato2'][x]
            
            mm_22.loc[x, 'Votos'] = (1 - re_2022['Votos'][x])
            print(x)
        mm_22.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\minimizado-2022.csv', index=False)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#TRESHOLD Limite de peso minimo 2022--------------------------------------------------------------------------------------------------------------------
        
        fm_22 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\filtro_maiores-2022.csv', encoding='ISO-8859-1')
        re_22 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2022.csv', encoding='ISO-8859-1')
        
        qtd_p = len(re_22)
        x=1
        for x in range(qtd_p):
            if(re_22['Votos'][x] > treshold):
                fm_22.loc[x, 'Candidato1'] = re_22['Candidato1'][x]
                fm_22.loc[x, 'Candidato2'] = re_22['Candidato2'][x]
                fm_22.loc[x, 'Votos'] = re_22['Votos'][x]
                print(x)
        fm_22.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\filtro_maiores-2022.csv', index=False)
#------------------------------------------------------------------------------------------------------------------------------------------------
#Normalizacao 2023---------------------------------------------------------------------------------------------------------------------------------
    if(ano==2023):
        vd_23 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2023-deputados.csv', encoding='ISO-8859-1')
        re_23 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2023.csv', encoding='ISO-8859-1')
        
        vg_23 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-2023-grafo.csv', encoding='ISO-8859-1')
        qtd_p = len(vg_23)
        qtd_c = len(vd_23)
        for i in range(qtd_c):
            for j in range(qtd_p):
                if(vg_23['Candidato1'][j]==vd_23['Candidato'][i]):
                    re_23.loc[j, 'Votos'] = (vg_23 ['Votos'][j]/vd_23['Votos'][i])
                    print(i, j)
        re_23.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2023.csv', index=False) 
#------------------------------------------------------------------------------------------------------------------------------------------------
#Inversao de peso 2023-------------------------------------------------------------------------------------------------------------------------------------
        re_23 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2023.csv', encoding='ISO-8859-1')
        mm_23 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\minimizado-2023.csv', encoding='ISO-8859-1')
        
        qtd_p = len(re_23)
        x=1
        for x in range(qtd_p):
            mm_23.loc[x, 'Candidato1'] = re_23['Candidato1'][x]
            mm_23.loc[x, 'Candidato2'] = re_23['Candidato2'][x]
            
            mm_23.loc[x, 'Votos'] = (1 - re_23['Votos'][x])
            print(x)
        mm_23.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\minimizado-2023.csv', index=False)
#----------------------------------------------------------------------------------------------------------------------------------------------------------
#TRESHOLD Limite de peso minimo 2023--------------------------------------------------------------------------------------------------------------------
        
        fm_23 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\filtro_maiores-2023.csv', encoding='ISO-8859-1')
        re_23 = pd.read_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\results-2023.csv', encoding='ISO-8859-1')
        
        qtd_p = len(re_23)
        x=1
        for x in range(qtd_p):
            if(re_23['Votos'][x] > treshold):
                fm_23.loc[x, 'Candidato1'] = re_23['Candidato1'][x]
                fm_23.loc[x, 'Candidato2'] = re_23['Candidato2'][x]
                fm_23.loc[x, 'Votos'] = re_23['Votos'][x]
                print(x)
        fm_23.to_csv('C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\filtro_maiores-2023.csv', index=False)
#--------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
