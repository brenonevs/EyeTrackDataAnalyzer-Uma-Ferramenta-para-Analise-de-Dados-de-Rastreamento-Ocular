from xml.etree import ElementTree as ET
import re
import os
import tkinter as tk
from tkinter import filedialog

def select_file():
    root = tk.Tk()
    root.withdraw() 
    file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    return file_path

def read_summary_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return re.findall(r'gaze_target: (.+?)\nfirst_event_id: (\d+)\nlast_event_id: (\d+)', content)

def extract_responses(root, first_event_id, last_event_id):
    responses = []
    for response in root.iter('response'):
        event_id = int(response.get('event_id'))
        if first_event_id <= event_id <= last_event_id:
            responses.append(response)
    return responses

def create_xml_files(gaze_targets, root, output_directory):
    for gaze_target, first_id, last_id in gaze_targets:
        responses = extract_responses(root, int(first_id), int(last_id))
        gaze_tree = ET.Element('gazes')
        gaze_tree.extend(responses)
        file_name = f"{gaze_target}_core.xml"
        file_path = os.path.join(output_directory, file_name)
        tree = ET.ElementTree(gaze_tree)
        tree.write(file_path, encoding='utf-8', xml_declaration=True)

xml_file_path = select_file()
if not xml_file_path:
    raise Exception("No XML file selected")

summary_file_path = 'summary.txt'  

tree = ET.parse(xml_file_path)
root = tree.getroot()

gaze_targets = read_summary_file(summary_file_path)

output_directory = os.getcwd()

create_xml_files(gaze_targets, root, output_directory)
