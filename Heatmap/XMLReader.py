import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import os

def LeituraXML(arquivo):
    tree = ET.parse(arquivo)
    root = tree.getroot()
    lista = []

    for elem in root.iter():
        if elem.tag == 'response':
            lista.append(elem.attrib)

    return lista

def ArmazenaLinhaColuna(arquivo):
    leitura_arquivo_xml = LeituraXML(arquivo)

    nome_base = os.path.basename(arquivo)
    nome_sem_extensao = os.path.splitext(nome_base)[0]
    novo_nome_arquivo = f"{nome_sem_extensao}.txt"

    with open(novo_nome_arquivo, 'w') as novo_arquivo:
        print(f"Armazenando dados em {novo_nome_arquivo}...")

        for dados in leitura_arquivo_xml:
            linha = dados.get('source_file_line', 'N/A')  
            coluna = dados.get('source_file_col', 'N/A') 
            plugin_time = dados.get('plugin_time', 'N/A')  

            novo_arquivo.write(f'{linha} {coluna}\n')

    print(f"Dados armazenados em {novo_nome_arquivo}")

def selecionar_arquivo():
    root = tk.Tk()  
    root.withdraw()  

    caminho_arquivo = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])

    if caminho_arquivo:  
        ArmazenaLinhaColuna(caminho_arquivo)

selecionar_arquivo()
