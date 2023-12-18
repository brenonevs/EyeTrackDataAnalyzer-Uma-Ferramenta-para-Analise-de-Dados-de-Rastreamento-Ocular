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

def extract_additional_tags(root):
    additional_tags = []
    for child in root:
        if child.tag != 'response':
            additional_tags.append(child)
    return additional_tags

def create_xml_files(gaze_targets, root, output_directory, additional_tags):
    for gaze_target, first_id, last_id in gaze_targets:
        responses = extract_responses(root, int(first_id), int(last_id))
        gaze_tree = ET.Element(root.tag, root.attrib)  # Use the root tag and attributes of the original XML
        gaze_tree.extend(additional_tags)  # Add the additional tags
        gaze_tree.extend(responses)  # Add the responses
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

additional_tags = extract_additional_tags(root)

gaze_targets = read_summary_file(summary_file_path)

output_directory = os.getcwd()

create_xml_files(gaze_targets, root, output_directory, additional_tags)
