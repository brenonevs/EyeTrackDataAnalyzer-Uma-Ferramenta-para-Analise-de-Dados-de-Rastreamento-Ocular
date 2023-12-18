import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import os
import regex as re

def LeituraXML(arquivo):
    tree = ET.parse(arquivo)
    root = tree.getroot()
    lista = []

    for elem in root.iter():
        if elem.tag == 'response' or elem.tag == 'plugin_time':
            lista.append(elem.attrib)

    return lista

def verifica_intersecao(principal, comparacao):
    x1_principal, x2_principal = principal[0]
    y1_principal, y2_principal = principal[1]

    x1_comparacao, x2_comparacao = comparacao[0]
    y1_comparacao, y2_comparacao = comparacao[1]

    intersecao_x = (x1_principal <= x2_comparacao) and (x1_comparacao <= x2_principal)
    intersecao_y = (y1_principal <= y2_comparacao) and (y1_comparacao <= y2_principal)

    return intersecao_x and intersecao_y

def processa_matrizes_e_escreve(arquivo, leitura_arquivo_xml, tamanho_matriz):
    diretorio_script = os.path.dirname(os.path.realpath(__file__))

    caminho_completo_arquivo = os.path.join(diretorio_script, arquivo)

    with open(caminho_completo_arquivo, 'w') as f_saida:
        matriz_principal = None
        tempo_inicial_regiao = None
        ultimo_tempo_regiao = None

        for dados in leitura_arquivo_xml:
            x_original = int(dados.get('source_file_line', 'N/A'))
            y_original = int(dados.get('source_file_col', 'N/A'))
            plugin_time_atual = int(dados.get('plugin_time', 'N/A'))

            matriz_atual = ((x_original - tamanho_matriz // 2, x_original + tamanho_matriz // 2),
                            (y_original - tamanho_matriz // 2, y_original + tamanho_matriz // 2))

            if matriz_principal is None:
                matriz_principal = matriz_atual
                tempo_inicial_regiao = plugin_time_atual
                ultimo_tempo_regiao = plugin_time_atual

                linha = f'{matriz_atual} {plugin_time_atual}\n'
                f_saida.write(linha)

            elif verifica_intersecao(matriz_principal, matriz_atual):
                ultimo_tempo_regiao = plugin_time_atual

                linha = f'{matriz_atual} {plugin_time_atual}\n'
                f_saida.write(linha)

            else:
                duracao = ultimo_tempo_regiao - tempo_inicial_regiao

                info_duracao = f'Duracao: {duracao} ms\n\n'
                f_saida.write(info_duracao)

                matriz_principal = matriz_atual
                tempo_inicial_regiao = plugin_time_atual
                ultimo_tempo_regiao = plugin_time_atual

                nova_linha = f'{matriz_atual} {plugin_time_atual}\n'
                f_saida.write(nova_linha)

        if matriz_principal is not None and ultimo_tempo_regiao is not None:
            duracao_final = ultimo_tempo_regiao - tempo_inicial_regiao
            info_duracao_final = f'Duracao: {duracao_final} ms\n'
            f_saida.write(info_duracao_final)

def escreve_pontos_e_duracao(arquivo, leitura_arquivo_xml, tamanho_matriz):
    diretorio_script = os.path.dirname(os.path.realpath(__file__))

    nome_arquivo_pontos = f"{os.path.splitext(arquivo)[0]}_pontos.txt"
    caminho_completo_arquivo_pontos = os.path.join(diretorio_script, nome_arquivo_pontos)

    with open(caminho_completo_arquivo_pontos, 'w') as f_saida_pontos:
        matriz_principal = None
        tempo_inicial_regiao = None
        ultimo_tempo_regiao = None
        pontos_regiao = []

        for dados in leitura_arquivo_xml:
            x_original = int(dados.get('source_file_line', 'N/A'))
            y_original = int(dados.get('source_file_col', 'N/A'))
            plugin_time_atual = int(dados.get('plugin_time', 'N/A'))

            matriz_atual = ((x_original - tamanho_matriz // 2, x_original + tamanho_matriz // 2),
                            (y_original - tamanho_matriz // 2, y_original + tamanho_matriz // 2))

            if matriz_principal is None:
                matriz_principal = matriz_atual
                tempo_inicial_regiao = plugin_time_atual
                ultimo_tempo_regiao = plugin_time_atual
                pontos_regiao.append((x_original, y_original))

            elif verifica_intersecao(matriz_principal, matriz_atual):
                ultimo_tempo_regiao = plugin_time_atual
                pontos_regiao.append((x_original, y_original))

            else:
                duracao = ultimo_tempo_regiao - tempo_inicial_regiao
                info_duracao = f'Duracao: {duracao} ms\n'
                f_saida_pontos.write(info_duracao)

                for ponto in pontos_regiao:
                    f_saida_pontos.write(f'{ponto}\n')
                f_saida_pontos.write('\n')  

                matriz_principal = matriz_atual
                tempo_inicial_regiao = plugin_time_atual
                ultimo_tempo_regiao = plugin_time_atual
                pontos_regiao = [(x_original, y_original)]

        if matriz_principal is not None and ultimo_tempo_regiao is not None and pontos_regiao:
            duracao_final = ultimo_tempo_regiao - tempo_inicial_regiao
            info_duracao_final = f'Duracao: {duracao_final} ms\n'
            f_saida_pontos.write(info_duracao_final)

            for ponto in pontos_regiao:
                f_saida_pontos.write(f'{ponto}\n')

    print(f"Dados de pontos armazenados em {caminho_completo_arquivo_pontos}")
    return caminho_completo_arquivo_pontos  


def filtra_duracoes_e_escreve(input_file_path, min_duration):

    output_file_name = 'output_filtered_coordinates.txt'
    
    with open(input_file_path, 'r') as file:
        content = file.read()

    blocks = re.split(r'Duracao: (\d+) ms', content)

    if not blocks[0].strip():
        blocks = blocks[1:]

    filtered_content = []


    for i in range(0, len(blocks), 2):  
        duration = int(blocks[i].strip()) 
        coordinates = blocks[i + 1].strip()  

        if duration >= min_duration:
            filtered_content.append(f'Duracao: {duration} ms\n{coordinates}')

    if filtered_content:
        with open(output_file_name, 'w') as output_file:
            output_file.write('\n\n'.join(filtered_content))
        print(f"Arquivo criado com sucesso: {output_file_name}")
    else:
        print("Nenhuma coordenada encontrada com a duração mínima especificada.")

def consolidar_coordenadas(arquivo_entrada):

    nome_base = os.path.basename(arquivo_entrada)
    nome_sem_extensao = os.path.splitext(nome_base)[0]
    arquivo_saida = f"{nome_sem_extensao}_coordenadas.txt"

    diretorio_script = os.path.dirname(os.path.realpath(__file__))
    caminho_completo_arquivo = os.path.join(diretorio_script, arquivo_saida)

    regex_coordenadas = re.compile(r'\((\d+),\s*(\d+)\)')

    try:
        with open(arquivo_entrada, 'r') as f_entrada, open(caminho_completo_arquivo, 'w') as f_saida:
            for linha in f_entrada:
                linha_limpa = linha.strip()
                if linha_limpa and not linha_limpa.startswith('Duracao:'):

                    match = regex_coordenadas.search(linha_limpa)
                    if match:
                        x, y = match.groups()  
                        f_saida.write(f"{x} {y}\n")  

    except FileNotFoundError:
        print(f"O arquivo {arquivo_entrada} não foi encontrado.")
    except Exception as e:
        print(f"Um erro ocorreu: {e}")

    print(f"Coordenadas consolidadas foram escritas em {caminho_completo_arquivo}")


def filtrar_coordenadas(root):
    caminho_arquivo_java = filedialog.askopenfilename(title='Selecione um arquivo Java', parent=root, filetypes=[("Java files", "*.java")])
    if not caminho_arquivo_java:
        return

    inicio_snippet = "///* CODE SNIPPET STARTS HERE *///"
    fim_snippet = "///* CODE SNIPPET ENDS HERE *///"
    
    linha_inicio = None
    linha_fim = None

    with open(caminho_arquivo_java, 'r') as arquivo:
        for numero_linha, linha in enumerate(arquivo, 1):
            if inicio_snippet in linha:
                linha_inicio = numero_linha
            elif fim_snippet in linha:
                linha_fim = numero_linha

    if linha_inicio is None or linha_fim is None:
        print("Não foram encontradas as linhas de início ou fim do snippet.")
        return
    
    print(linha_inicio, linha_fim)

    with open("output_filtered_coordinates_coordenadas.txt", 'r') as arquivo_coord:
        linhas_coord = arquivo_coord.readlines()

    linhas_filtradas = []
    for linha in linhas_coord:
        numero_linha = int(linha.split()[0])
        if linha_inicio <= numero_linha <= linha_fim:
            linhas_filtradas.append(linha)

    with open("output_filtered_coordinates_coordenadas.txt", 'w') as arquivo_coord:
        arquivo_coord.writelines(linhas_filtradas)

def selecionar_arquivo():
    root = tk.Tk()
    root.withdraw()

    caminho_arquivo = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])

    if caminho_arquivo:
        dados_xml = LeituraXML(caminho_arquivo)
        nome_base = os.path.basename(caminho_arquivo)
        nome_sem_extensao = os.path.splitext(nome_base)[0]
        novo_nome_arquivo = f"{nome_sem_extensao}_processed.txt"

        linha = int(input("Digite quantas linhas tem a matriz: "))
        coluna = int(input("Digita quantas colunas tem a matriz: "))

        processa_matrizes_e_escreve(novo_nome_arquivo, dados_xml, linha)
        
        arquivo_pontos_duracao = escreve_pontos_e_duracao(novo_nome_arquivo, dados_xml, coluna)

        duracao_minima_usuario = int(input("Digite o tempo mínimo de duração (em ms) que deseja analisar: "))

        filtra_duracoes_e_escreve(arquivo_pontos_duracao, duracao_minima_usuario) 

        consolidar_coordenadas("output_filtered_coordinates.txt")
        
        filtrar_coordenadas(root)


if __name__ == "__main__":
    selecionar_arquivo()