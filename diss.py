import os
import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET
from xml.dom import minidom

def select_txt_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

def get_output_xml_path(input_path):
    folder = os.path.dirname(input_path)
    base = os.path.splitext(os.path.basename(input_path))[0]
    return os.path.join(folder, base + ".xml")

def main():
    input_file = select_txt_file()
    if not input_file:
        print("Файл не выбран.")
        return

    output_file = get_output_xml_path(input_file)

    # Чтение строк из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Формируем XML-структуру
    disaggregation = ET.Element('disaggregation', attrib={'action_id': '31', 'version': '2'})
    inn = ET.SubElement(disaggregation, 'trade_participant_inn')
    inn.text = '2315989590'
    packings_list = ET.SubElement(disaggregation, 'packings_list')

    for code in lines:
        packing = ET.SubElement(packings_list, 'packing')
        kitu = ET.SubElement(packing, 'kitu')
        kitu.text = f"<![CDATA[{code}]]>"  # временно, заменим ниже вручную

    # Преобразование через minidom и замена текста на CDATA
    rough_string = ET.tostring(disaggregation, 'utf-8')
    reparsed = minidom.parseString(rough_string)

    for node, code in zip(reparsed.getElementsByTagName("kitu"), lines):
        if node.firstChild:
            node.removeChild(node.firstChild)
        node.appendChild(reparsed.createCDATASection(code))

    # Сохраняем в файл
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reparsed.toprettyxml(indent="    ", encoding="UTF-8").decode('utf-8'))

    print(f"XML сохранён как: {output_file}")

if __name__ == "__main__":
    main()
