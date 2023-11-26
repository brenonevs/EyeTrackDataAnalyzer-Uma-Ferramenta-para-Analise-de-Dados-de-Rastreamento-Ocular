import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
import matplotlib.colors as mcolors
import tkinter as tk
from tkinter import filedialog
import matplotlib.image as mpimg 

def iniciar_tkinter():
    root = tk.Tk()
    root.withdraw()
    return root

def encontrar_trechos_codigo(root):
    caminho_arquivo = filedialog.askopenfilename(title='Selecione um arquivo Java', parent=root, filetypes=[("Java files", "*.java")])
    if not caminho_arquivo:
        return [], []

    inicio_snippet = "///* CODE SNIPPET STARTS HERE *///"
    fim_snippet = "///* CODE SNIPPET ENDS HERE *///"
    linhas_inicio = []
    linhas_fim = []

    with open(caminho_arquivo, 'r') as arquivo:
        for numero_linha, linha in enumerate(arquivo, 1):
            if inicio_snippet in linha:
                linhas_inicio.append(numero_linha)
            elif fim_snippet in linha:
                linhas_fim.append(numero_linha)

    return linhas_inicio, linhas_fim

def coluna_mais_longa(linha_minima, linha_maxima, root): 
    arquivo_java = filedialog.askopenfilename(parent=root, title='Selecione um arquivo Java', filetypes=[('Arquivos Java', '*.java')])
    if arquivo_java:
        try:
            with open(arquivo_java, 'r') as file:
                codigo_java = file.read()

            linhas = codigo_java.split('\n')
            linhas_intervalo = linhas[linha_minima - 1:linha_maxima]
            max_comprimento = max(len(linha) for linha in linhas_intervalo)

            return max_comprimento

        except Exception as e:
            print(f"Ocorreu um erro ao processar o arquivo: {e}")
            return None
    else:
        print("Nenhum arquivo foi selecionado.")
        return None

def analisar_e_plotar(caminho_arquivo, caminho_imagem, nome_arquivo_duracao, root):
    data = pd.read_csv(caminho_arquivo, header=None, delim_whitespace=True, names=["x", "y"])
    x = data.y.values 
    y = data.x.values 

    density = gaussian_kde([x, y])

    img = mpimg.imread(caminho_imagem)
    plt.figure(figsize=(12, 8))

    y_min = encontrar_trechos_codigo(root)[0][0]
    y_max = encontrar_trechos_codigo(root)[1][0]
    x_min = 0
    x_max = coluna_mais_longa(y_min, y_max, root)

    plt.imshow(img, aspect='auto', extent=[x_min, x_max, y_max, y_min])
    sns.kdeplot(x=x, y=y, cmap='Reds', fill=True, alpha=0.55)

    plt.xlim(x_min, x_max)
    plt.ylim(y_max, y_min)

    plt.title('Mapa de Calor das Coordenadas de Olhar')
    plt.xlabel('Coordenada X (Colunas)')
    plt.ylabel('Coordenada Y (Linhas)')

    duracao_maxima, duracao_minima = calcular_duracao_max_min(nome_arquivo_duracao)

    if duracao_maxima is not None and duracao_minima is not None:
        cores = mcolors.LinearSegmentedColormap.from_list('gradiente', [(1, 1, 1), (1, 0, 0)], N=256)
        cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=cores), orientation='vertical', ticks=[0, 1])
        cbar.ax.set_yticklabels([f'{duracao_minima} ms', f'{duracao_maxima} ms'])

    plt.show()

def calcular_duracao_max_min(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    duracoes = []
    for linha in linhas:
        if linha.startswith("Duracao:"):
            duracao = int(linha.split(":")[1].strip().split()[0])
            duracoes.append(duracao)

    if duracoes:
        duracao_maxima = max(duracoes)
        duracao_minima = min(duracoes)
        return duracao_maxima, duracao_minima
    else:
        return None, None

def selecionar_arquivo(root):
    caminho_arquivo = "output_filtered_coordinates_coordenadas.txt"
    caminho_imagem = filedialog.askopenfilename(parent=root, title="Selecione a Imagem de Fundo", filetypes=[("Image files", "*.jpg;*.png")])
    nome_arquivo_duracao = 'output_filtered_coordinates.txt'

    if caminho_arquivo: 
        analisar_e_plotar(caminho_arquivo, caminho_imagem, nome_arquivo_duracao, root)

root = iniciar_tkinter()
selecionar_arquivo(root)
