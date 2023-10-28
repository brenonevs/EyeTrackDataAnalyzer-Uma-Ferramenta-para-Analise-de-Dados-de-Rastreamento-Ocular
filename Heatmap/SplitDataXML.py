import xml.etree.ElementTree as ET
import os

def create_xml_file(responses, gaze_target_value, session_id, environment):
    
    filename = ''.join(e for e in gaze_target_value if e.isalnum() or e in ["-", "_"])
    
    root = ET.Element('itrace_plugin', session_id=session_id)
    root.append(environment)

    gazes = ET.SubElement(root, 'gazes')
    for response in responses:
        gazes.append(response)

    tree = ET.ElementTree(root)
    tree.write(f'{filename}.xml', encoding='utf-8', xml_declaration=True)

tree = ET.parse('experimento.xml')
root = tree.getroot()


environment = root.find('environment')
session_id = root.get('session_id')


last_gaze_target = None
responses = []

for response in root.iter('response'):
    gaze_target = response.get('gaze_target')

    if last_gaze_target is None:
        last_gaze_target = gaze_target

    if gaze_target != last_gaze_target:

        create_xml_file(responses, last_gaze_target, session_id, environment)
        responses = []
        last_gaze_target = gaze_target

    responses.append(response)

if responses:
    create_xml_file(responses, last_gaze_target, session_id, environment)
