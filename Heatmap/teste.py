import xml.etree.ElementTree as ET
import time
from datetime import datetime


def ctime_to_datetime (raw_start_time):
    translator = {
        "Jan":'1',
        "Feb":'2',
        "Mar":'3',
        "Apr":'4',
        "May":'5',
        "Jun":'6',
        "Jul":'7',
        "Aug":'8',
        "Sep":'9',
        "Oct":'10',
        "Nov":'11',
        "Dec":'12'
    }

    raw_start_time = time.ctime(raw_start_time /1000)

    raw_start_time = raw_start_time.split() #transformo em lista 
    raw_start_time[1] = str(translator[raw_start_time[1]]) #troco o nome dos meses por valores
    raw_start_time.remove(raw_start_time[0]) #removo o dia da semana
    raw_start_time[3] = raw_start_time[3][2:] #cortando informação do ano desnecessária
    raw_start_time = ' '.join(raw_start_time) #reuno novamente em uma string
    
    ret_value = datetime.strptime(raw_start_time,"%m %d %H:%M:%S %y")

    return ret_value

def LeituraXML(arquivo):

    nome_arquivo_xml = arquivo
    tree = ET.parse(nome_arquivo_xml)
    root = tree.getroot()
    lista = []
    lista_tempos = []

    for elem in root.iter():
        if elem.tag == 'response':
            lista.append(elem.attrib)
        elif elem.tag == 'plugin_time':
            lista_tempos.append(ctime_to_datetime(elem))

    return lista, lista_tempos

print(LeituraXML("13_Code_Snippetjava.xml"))
