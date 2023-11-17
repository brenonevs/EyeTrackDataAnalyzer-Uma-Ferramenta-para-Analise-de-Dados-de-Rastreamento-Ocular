import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
import matplotlib.colors as mcolors

def analisar_e_plotar(caminho_arquivo):
    data = pd.read_csv(caminho_arquivo, header=None, delim_whitespace=True, names=["x", "y"])

    x = data.y.values 
    y = data.x.values 

    density = gaussian_kde([x,y])
    d = density([x,y])

    plt.figure(figsize=(12, 8))
    ax = sns.kdeplot(x=x, y=y, cmap='Reds', fill=True) 
    plt.gca().invert_yaxis()

    x_min = x.min() - 20
    x_max = x.max() + 20
    y_min = y.min() - 20
    y_max = y.max() + 20

    if x_min < 0:
        x_min = 0
    
    if y_min < 0:
        y_min = 0

    plt.xlim(x_min, x_max)
    plt.ylim(y_max, y_min)  

    plt.title('Mapa de Calor das Coordenadas de Olhar')
    plt.xlabel('Coordenada X (Colunas)')
    plt.ylabel('Coordenada Y (Linhas)')

    return plt

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

def criar_colorbar_gradiente(duracao_maxima, duracao_minima):
    fig, ax = plt.subplots(figsize=(1, 3)) 
    
    cores = mcolors.LinearSegmentedColormap.from_list('gradiente', [(1, 1, 1), (1, 0, 0)], N=256)
    
    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=cores), cax=ax, orientation='vertical',
                        ticks=[0, 1]) 
    
    cbar.ax.set_yticklabels([f'{duracao_minima} ms', f'{duracao_maxima} ms'])
    cbar.set_label('Duração')
    
    plt.subplots_adjust(left=0.452, bottom=0.11, right=0.583, top=0.88, wspace=0.2, hspace=0.2)

def selecionar_arquivo():

    caminho_arquivo = "output_filtered_coordinates_coordenadas.txt"

    if caminho_arquivo: 
        plot_heatmap = analisar_e_plotar(caminho_arquivo)
        nome_arquivo = 'output_filtered_coordinates.txt'
        duracao_maxima, duracao_minima = calcular_duracao_max_min(nome_arquivo)
        if duracao_maxima is not None and duracao_minima is not None:
            criar_colorbar_gradiente(duracao_maxima, duracao_minima)
            plt.show() 
        else:
            print("Nenhuma duração encontrada no arquivo.")

selecionar_arquivo()
