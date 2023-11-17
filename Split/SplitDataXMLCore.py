from xml.etree import ElementTree as ET
import re
import os

# Função para ler o arquivo de resumo e extrair alvos de olhar e intervalos de IDs de eventos
def read_summary_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return re.findall(r'gaze_target: (.+?)\nfirst_event_id: (\d+)\nlast_event_id: (\d+)', content)

# Função para extrair respostas relevantes para um determinado intervalo de ID de evento
def extract_responses(root, first_event_id, last_event_id):
    responses = []
    for response in root.iter('response'):
        event_id = int(response.get('event_id'))
        if first_event_id <= event_id <= last_event_id:
            responses.append(response)
    return responses

# Função para criar e salvar novos arquivos XML
def create_xml_files(gaze_targets, root, output_directory):
    for gaze_target, first_id, last_id in gaze_targets:
        responses = extract_responses(root, int(first_id), int(last_id))
        gaze_tree = ET.Element('gazes')
        gaze_tree.extend(responses)
        file_name = f"{gaze_target}_core.xml"
        file_path = os.path.join(output_directory, file_name)
        tree = ET.ElementTree(gaze_tree)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

# Caminho para o arquivo XML e arquivo de resumo
xml_file_path = 'itrace_core-1699381311260.xml'  # O arquivo deve estar no mesmo diretório do script
summary_file_path = 'summary.txt'  # O arquivo deve estar no mesmo diretório do script

# Lendo o arquivo XML
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Lendo o arquivo de resumo e obtendo os alvos de olhar e os intervalos de IDs de eventos
gaze_targets = read_summary_file(summary_file_path)

# Diretório atual para salvar os novos arquivos XML
output_directory = os.getcwd()

# Criando novos arquivos XML para cada alvo de olhar
create_xml_files(gaze_targets, root, output_directory)