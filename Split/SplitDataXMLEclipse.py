import pandas as pd
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
from xml.dom import minidom

def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_xml_file(df_group, gaze_target_value, session_id, environment_attrs):
    filename = ''.join(e for e in gaze_target_value if e.isalnum() or e in ["-", "_"])
    root = ET.Element('itrace_plugin', session_id=session_id)


    environment = ET.SubElement(root, 'environment', environment_attrs)

    # Criando o elemento 'gazes'
    gazes = ET.SubElement(root, 'gazes')
    for _, row in df_group.iterrows():
        response = ET.SubElement(gazes, 'response', row.to_dict())

    # Formatando o XML
    formatted_xml = prettify(root)

    with open(f'{filename}.xml', 'w', encoding='utf-8') as file:
        file.write(formatted_xml)

def write_to_txt_file(df_group, gaze_target):
    with open('summary.txt', 'a') as file:
        file.write(f'gaze_target: {gaze_target}\n')
        file.write(f'first_event_id: {df_group.event_id.iloc[0]}\n')
        file.write(f'last_event_id: {df_group.event_id.iloc[-1]}\n\n')

def select_xml_file():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    return file_path

file_path = select_xml_file()

if file_path:
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Convertendo XML para DataFrame
    data = []
    for response in root.iter('response'):
        data.append(response.attrib)
    df = pd.DataFrame(data)

    # Obtendo informações do ambiente e sessão
    environment_attrs = root.find('environment').attrib
    session_id = root.get('session_id')

    # Processando cada grupo de 'gaze_target'
    for gaze_target, df_group in df.groupby('gaze_target'):
        create_xml_file(df_group, gaze_target, session_id, environment_attrs)
        write_to_txt_file(df_group, gaze_target)
