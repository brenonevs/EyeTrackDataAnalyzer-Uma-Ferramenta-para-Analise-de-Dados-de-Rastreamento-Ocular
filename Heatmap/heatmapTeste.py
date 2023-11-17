import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
import tkinter as tk
from tkinter import filedialog
import matplotlib.image as mpimg  # Importar a biblioteca para carregar a imagem

def encontrar_trechos_codigo():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter

    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Java files", "*.java")])
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

def coluna_mais_longa(linha_minima, linha_maxima): 
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    arquivo_java = filedialog.askopenfilename(
        title='Selecione um arquivo Java',
        filetypes=[('Arquivos Java', '*.java')]
    )

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



def analisar_e_plotar(caminho_arquivo, caminho_imagem):

    data = pd.read_csv(caminho_arquivo, header=None, delim_whitespace=True, names=["x", "y"])
    x = data.y.values 
    y = data.x.values 

    density = gaussian_kde([x, y])
    d = density([x, y])

    # Carregar a imagem de fundo
    img = mpimg.imread(caminho_imagem)

    plt.figure(figsize=(12, 8))

    y_min = encontrar_trechos_codigo()[0][0]
    y_max = encontrar_trechos_codigo()[1][0]
    
    x_min = 0
    x_max = coluna_mais_longa(y_min, y_max)

    print(f"xmin: {x_min}")
    print(f"xmax: {x_max}")
    print(f"ymin: {y_min}")
    print(f"ymax: {y_max}")

    # Exibir a imagem de fundo dentro dos mesmos limites do heatmap
    plt.imshow(img, aspect='auto', extent=[x_min, x_max, y_max, y_min])

    # Criar o heatmap sobre a imagem de fundo
    ax = sns.kdeplot(x=x, y=y, cmap='Reds', fill=True, alpha=0.55, cbar=True, cbar_kws={'label': 'Porcentagem Relativa (%)'})

    plt.xlim(x_min, x_max)
    plt.ylim(y_max, y_min)

    plt.title('Mapa de Calor das Coordenadas de Olhar')
    plt.xlabel('Coordenada X (Colunas)')
    plt.ylabel('Coordenada Y (Linhas)')

    plt.show()

def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()

    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    caminho_imagem = filedialog.askopenfilename(title="Selecione a Imagem de Fundo", filetypes=[("Image files", "*.jpg;*.png")])

    if caminho_arquivo and caminho_imagem: 
        analisar_e_plotar(caminho_arquivo, caminho_imagem)

selecionar_arquivo()