import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
from matplotlib.colors import Normalize
from matplotlib.ticker import PercentFormatter
import tkinter as tk
from tkinter import filedialog

def analisar_e_plotar(caminho_arquivo):
    
    with open('Main.java', 'r') as file:
        content = file.readlines()

    num_lines = len(content)
    num_columns = max(len(line) for line in content)

    print(num_columns, num_lines)

    data = pd.read_csv(caminho_arquivo, header=None, delim_whitespace=True, names=["x", "y"])

    x = data.y.values 
    y = data.x.values 

    density = gaussian_kde([x,y])
    d = density([x,y])

    plt.figure(figsize=(12, 8))
    ax = sns.kdeplot(x=x, y=y, cmap='Reds', fill=True, cbar=True, cbar_kws={'label': 'Porcentagem Relativa (%)'}) 
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

    plt.show()

def selecionar_arquivo():
    root = tk.Tk()  
    root.withdraw()  

    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])

    if caminho_arquivo: 
        analisar_e_plotar(caminho_arquivo)

selecionar_arquivo()
