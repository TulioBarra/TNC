import requests
from datetime import datetime, timedelta
from grafoDeputado import grafoDeputado
import unicodedata
import csv as csv
import pandas as pd

# Mudar os caminhos conforme necessário
arq_grafo = r"C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-grafo.csv"
arq_votacoes = r"C:\\Users\\tulio\\Documents\\AEDSIII\\NetworkLib\\votacaoVotos-deputados.csv"





def processar_votos(votos, g, lista_votos, id, p):
  
    qtd_votos = len(votos)
    if qtd_votos == 0:
        return None
    for deputado in range(qtd_votos):
        if votos[deputado][7] in p:
            deputado_nome = votos[deputado][6]+","+votos[deputado][7]
            if id == votos[deputado][0]:
                g.add_deputado(deputado_nome)
                tipo_voto = votos[deputado][3]
                if tipo_voto == "Sim" and id == votos[deputado][0]:
                    g.add_grafo(lista_votos[0], deputado_nome)
                elif tipo_voto == "Não" and id == votos[deputado][0]:
                    g.add_grafo(lista_votos[1], deputado_nome)
                elif tipo_voto == "Obstrução" and id == votos[deputado][0]:
                    g.add_grafo(lista_votos[2], deputado_nome)
       

def salvar_dados(g, arq_grafo, arq_votacoes):
    g.salvar_grafo(arq_grafo)
    g.salvar_votacoes(arq_votacoes)
    print("DADOS SALVOS")   

def remover_caracter(texto):
     return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def substituir_caracter(texto, sub):
    for caracter, substituto in sub.items():
        texto = texto.replace(caracter, substituto)
    return texto
        

def normalizar():
    vd_23 = pd.read_csv('NetworkLib\\deputados.csv', encoding='ISO-8859-1')
    re_23 = pd.read_csv('NetworkLib\\normalizado.csv', encoding='ISO-8859-1')
        
    vg_23 = pd.read_csv('NetworkLib\\grafos.csv', encoding='ISO-8859-1')
    qtd_p = len(vg_23)
    qtd_c = len(vd_23)
    for i in range(qtd_c):
        for j in range(qtd_p):
            if(vg_23['Candidato1'][j]==vd_23['Candidato'][i]):
                re_23.loc[j, 'Votos'] = (vg_23 ['Votos'][j]/vd_23['Votos'][i])
                print(i, j)
    re_23.to_csv('NetworkLib\\normalizado.csv', index=False)
    

def inversao_peso():
    re_23 = pd.read_csv('NetworkLib\\normalizado.csv', encoding='ISO-8859-1')
    mm_23 = pd.read_csv('NetworkLib\\invertido.csv', encoding='ISO-8859-1')
        
    qtd_p = len(re_23)
    x=1
    for x in range(qtd_p):
        mm_23.loc[x, 'Candidato1'] = re_23['Candidato1'][x]
        mm_23.loc[x, 'Candidato2'] = re_23['Candidato2'][x]
            
        mm_23.loc[x, 'Votos'] = (1 - re_23['Votos'][x])
        print(x)
    mm_23.to_csv('NetworkLib\\invertido.csv', index=False)

def treshold(tre):
    
    with open('NetworkLib\\treshold.csv', mode='r', newline='', encoding='ISO-8859-1') as file_csv:
        leitor_csv = csv.reader(file_csv)
        cabecalho = next(leitor_csv)
    with open('NetworkLib\\treshold.csv', mode='w', newline='', encoding='utf-8') as file_csv:
        escritor_csv = csv.writer(file_csv)
        escritor_csv.writerow(cabecalho)
    
    fm_23 = pd.read_csv('NetworkLib\\treshold.csv', encoding='ISO-8859-1')
    re_23 = pd.read_csv('NetworkLib\\normalizado.csv', encoding='ISO-8859-1')
        
    qtd_p = len(re_23)
    x=1
    for x in range(qtd_p):
        if(re_23['Votos'][x] > tre):
            fm_23.loc[x, 'Candidato1'] = re_23['Candidato1'][x]
            fm_23.loc[x, 'Partido1'] = re_23['Partido1'][x]
            fm_23.loc[x, 'Candidato2'] = re_23['Candidato2'][x]
            fm_23.loc[x, 'Partido2'] = re_23['Partido2'][x]
            fm_23.loc[x, 'Votos'] = re_23['Votos'][x]
            print(x)
    fm_23.to_csv('NetworkLib\\treshold.csv', index=False)          


def main():
    
    
   
    
    g = grafoDeputado()
    
    partido = input("Digite os partidos: ")
    p = partido.split()
    
    ano = input("Digite o ano: ")
    peso_min = float(input("Digite o peso minimo: "))
    
    vd = pd.read_csv('votacoesVotos-'+ano+'.csv', encoding='utf-8')
    i=0
    j=0
    qtd_pautas = len(vd)
    pautas = []
    pautas.append(vd['idVotacao'][i]) 
    for i in range(qtd_pautas):
        
        if pautas[j] != vd['idVotacao'][i]:
            j=j+1
            
            pautas.append(vd['idVotacao'][i])
    print(pautas)
        

    qtd_pautas = len(pautas)

    votos = []
    
    for x in range(qtd_pautas):
        lista_votos = [[],[],[]]
        id = pautas[x]
        print(x)
        with open('votacoesVotos-'+ano+'.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            s=0
            for row in reader:
                
                if row[0] == id:
                    
                    votos.append(row)
                    
                    s += 1
            
            if votos:
                processar_votos(votos, g, lista_votos, id, p)

        
    
            
    salvar_dados(g, arq_grafo, arq_votacoes)
            
    g = grafoDeputado()
    
    cabecalho_destino = None
    substituicao1 = {' ':','}
    substituicao2 = {'"':' '}
   #GRAFO------------------------------------------------------------------------------------------------------------------- 
    with open('NetworkLib\\votacaoVotos-gr.csv', mode='r', newline='', encoding='ISO-8859-1') as file_destino:
        reader_destino = csv.reader(file_destino)
        cabecalho_destino = next(reader_destino)
        
    novo_conteudo = []
    with open('NetworkLib\\votacaoVotos-grafo.csv', mode='r', newline='', encoding='ISO-8859-1') as file_origem:
        reader_origem = csv.reader(file_origem)
        next(reader_origem)
        
        for row in reader_origem:
            row = [substituir_caracter(campo, substituicao1) for campo in row]
           
            row = [remover_caracter(campo) for campo in row]
            novo_conteudo.append(row)
    with open('NetworkLib\\votacaoVotos-gr.csv', mode='w', newline='', encoding='ISO-8859-1') as file_destino:
        writer_destino = csv.writer(file_destino)
        writer_destino.writerow(cabecalho_destino)
        writer_destino.writerows(novo_conteudo)
        
    #GRAFO-------------------------------------------------------------------------------------------------------------------     
        
    
    
    with open('NetworkLib\\votacaoVotos-dep.csv', mode='r', newline='', encoding='ISO-8859-1') as file_destino:
        reader_destino = csv.reader(file_destino)
        cabecalho_destino = next(reader_destino)
        
    novo_conteudo = []
    
    
    with open('NetworkLib\\votacaoVotos-deputados.csv', mode='r', newline='', encoding='ISO-8859-1') as file_origem:
        reader_origem = csv.reader(file_origem)
        
        
        for row in reader_origem:
            row = [substituir_caracter(campo, substituicao1) for campo in row]
            
            row = [remover_caracter(campo) for campo in row]
            novo_conteudo.append(row)
    
    
    with open('NetworkLib\\votacaoVotos-dep.csv', mode='w', newline='', encoding='ISO-8859-1') as file_destino:
        writer_destino = csv.writer(file_destino)
        writer_destino.writerow(cabecalho_destino)
        writer_destino.writerows(novo_conteudo)
    
    
    with open('NetworkLib\\votacaoVotos-dep.csv', 'r', newline='', encoding='ISO-8859-1') as arquivo_entrada, \
     open('NetworkLib\\deputados.csv', 'w', newline='', encoding='ISO-8859-1') as arquivo_saida:
         reader = csv.reader(arquivo_entrada, quoting=csv.QUOTE_NONE)
         writer = csv.writer(arquivo_saida)
         
         for row in reader:
             row = [campo.strip('"') for campo in row]
             writer.writerow(row)
    
    with open('NetworkLib\\votacaoVotos-gr.csv', 'r', newline='', encoding='ISO-8859-1') as arquivo_entrada, \
     open('NetworkLib\\grafos.csv', 'w', newline='', encoding='ISO-8859-1') as arquivo_saida:
         reader = csv.reader(arquivo_entrada, quoting=csv.QUOTE_NONE)
         writer = csv.writer(arquivo_saida)
         
         for row in reader:
             row = [campo.strip('"') for campo in row]
             writer.writerow(row)
#GRAFO------------------------------------------------------------------------------------------------------------------- 
    
    with open('NetworkLib\\grafos.csv', mode='r', newline='', encoding='ISO-8859-1') as file_origem:
        leitor_csv = csv.reader(file_origem)
        dados_origem = list(leitor_csv)
    
    with open('NetworkLib\\normalizado.csv', mode='w', newline='', encoding='utf-8') as file_destino:
        escritor_csv = csv.writer(file_destino)
        escritor_csv.writerows(dados_origem)
    
    
    with open('NetworkLib\\grafos.csv', mode='r', newline='', encoding='ISO-8859-1') as file_origem:
        leitor_csv = csv.reader(file_origem)
        dados_origem = list(leitor_csv)
    
    with open('NetworkLib\\invertido.csv', mode='w', newline='', encoding='utf-8') as file_destino:
        escritor_csv = csv.writer(file_destino)
        escritor_csv.writerows(dados_origem)
        
    
    
    
    
    
    normalizar()
    inversao_peso()
    treshold(peso_min)
    
            
    
    
    

   
            
if __name__ == "__main__":
    main()
