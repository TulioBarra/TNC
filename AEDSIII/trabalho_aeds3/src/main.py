import json
import numpy as np
from grafos import Grafos
from json_manager import JsonManager
import requests
import matplotlib.pyplot as plt

# read
# readlines -> cada linha do texto se torna um item em uma lista
# write -> escrever
#ARQUIVO DE VOTAÇÕES: ./votacoesVotos-2023.json

link = "https://dadosabertos.camara.leg.br/swagger/api.html#api"


arquivojs = requests.get(link+'/votacoes/1/votos')
print(arquivojs)



def operacoes(file): 
       
    votos = []
    tamanho= 1000
    
    with open(file, encoding="utf-8") as data:
        dados = json.load(data)
        
    #Escreve no arquivo json
    with open("./deputados.json", "w", encoding="utf-8") as file:
        file.write(("""\n{\n"dados": ["""))
        with open("./votos_em_comum.json", "w", encoding="utf-8") as file_2:
            file_2.write(("""\n{\n"dados": ["""))
            j=0
            
            for i in range(0, tamanho):
                idVotacao = dados["dados"][i]["idVotacao"]
                voto = dados["dados"][i]["voto"]
                deputado_id = dados["dados"][i]["deputado_"]["id"]
                deputado_nome = dados["dados"][i]["deputado_"]["nome"]
                
                if voto == "Não":
                    voto = "Nao"

                votos_js={}
                
                conta_votos=0
                for j in range(0, tamanho):
                    if dados["dados"][j]["voto"] == 'Sim' and dados["dados"][j]["deputado_"]["nome"] == dados["dados"][i]["deputado_"]["nome"]:
                        conta_votos+=1
                
                if dados["dados"][i]["voto"] == 'Sim' and not(deputado_nome in votos):
                    votos.append(deputado_nome)
                    votos_js = {
                        "nome": deputado_nome,
                        "quantidade_votos_positivos": conta_votos
                        }
                                
                #Estrutura do json    
                dicionario = {
                    "idVotacao": idVotacao,
                    "voto": voto,
                    "deputado_id": deputado_id,
                    "deputado_nome": deputado_nome,
                }

                objeto_json = json.dumps(dicionario, indent=2)
                file.write(objeto_json+',')
                
                if(votos_js != {}):
                    objeto_json_2 = json.dumps(votos_js, indent=2)
                    file_2.write(objeto_json_2+',')
                
                
                votos_js["nome"] = ""
                votos_js["quantidade_votos_positivos"] = 0

            file_2.write("\n]\n}")
        file.write("\n]\n}")


    with open('./qtd_votos.json', encoding="utf-8") as quantidade:
        qtd = json.load(quantidade)
        
    with open("qtd_votos.txt", "w", encoding="utf-8") as arquivo:
        for i in range(0, len(qtd["dados"])):
            arquivo.write("Deputado: "+ qtd["dados"][i]["nome"] + '\n')
            arquivo.write("Quantidade de aprovações: "+ str(qtd["dados"][i]["quantidade_votos_positivos"]) + '\n\n')
                
    

    votos=[]
    with open("./votos_em_comum.json", "w", encoding="utf-8") as file:
        with open("./votos_em_comum.txt", "w", encoding="utf-8") as arquivo:
            
        
            file.write(("""\n{\n"dados": ["""))
            a=0
            for i in range(0, tamanho):
                    idVotacao = dados["dados"][i]["idVotacao"]
                    voto = dados["dados"][i]["voto"]
                    deputado_id = dados["dados"][i]["deputado_"]["id"]
                    deputado_nome = dados["dados"][i]["deputado_"]["nome"]
                    
                    if voto == "Não":
                        voto = "Nao"

                    votos_em_comum = {
                            "deputado_1": "",
                            "deputado_2": "",
                            "quantidade_votos_em_comum": 0,
                            "porcentagem_de_votos_em_comum": 0,
                            }
                    conta_votos_em_comum=0
                    conta_votos=0
                    
                    for j in range(0, tamanho):
                        
                        if (dados["dados"][i]["voto"] == 'Sim' and
                            dados["dados"][i]["deputado_"]["nome"] != dados["dados"][j]["deputado_"]["nome"] and
                            dados["dados"][j]["voto"] == 'Sim' and
                            dados["dados"][i]["idVotacao"] == dados["dados"][j]["idVotacao"]):
                            
                            votos_em_comum["deputado_1"] = dados["dados"][j]["deputado_"]["nome"]
                            votos_em_comum["deputado_2"] = dados["dados"][i]["deputado_"]["nome"] 
                            
                            votos_em_comum["quantidade_votos_em_comum"] += 1
                            
                            
                            
                            
                            arquivo.write("Deputado 1 : "+ dados["dados"][j]["deputado_"]["nome"] + '\n')
                            arquivo.write("Deputado 2 : "+ dados["dados"][i]["deputado_"]["nome"]  + '\n')
                            arquivo.write("Quantidade de votos em comum: "+ str(votos_em_comum["quantidade_votos_em_comum"]) + '\n\n')
                            
                            
                            
                    if(votos_em_comum["quantidade_votos_em_comum"]):
                       
                     
                        with open('qtd_votos.json', encoding="utf-8") as data:
                            quantidade_votos = json.load(data)
                            
                            votos_em_comum["porcentagem_de_votos_em_comum"] = (quantidade_votos["dados"][a]["quantidade_votos_positivos"]/votos_em_comum["quantidade_votos_em_comum"])
                        
                    a = a+1
                    objeto_json = json.dumps(votos_em_comum, indent=2) 
                    file.write(objeto_json)
                    file.write(',')
                    
        file.write("\n]\n}")
        
        
 


      
                
file = input("Informe o arquivo de votações:")
operacoes(file)

print("O grafo foi escrito nos arquivos:\n - qtd_votos.json \n - votos_em_comum.json \n - qtd_votos.txt \n - votos_em_comum.txt")