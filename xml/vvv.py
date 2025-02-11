import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import os


# Функция для выбора XML файла
def select_xml_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("XML files", "*.xml"), ("All files", "*.*")]
    )
    return file_path


# Функция для выбора папки сохранения лог-файла
def select_log_file(xml_filename):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Выберите папку для сохранения лог-файла")

    if folder_path:
        log_filename = os.path.splitext(os.path.basename(xml_filename))[0] + "_errors.txt"
        return os.path.join(folder_path, log_filename)
    return None


# Функция проверки данных в XML
def validate_xml(file_path, log_file):
    tree = ET.parse(file_path)
    root = tree.getroot()

    errors = []

    namespace = {'ns': 'http://masterutm.center-inform.ru/packing'}

    for pallet in root.findall('ns:Pallet', namespace):
        pallet_barcode = pallet.find('ns:Barcode', namespace).text if pallet.find('ns:Barcode',
                                                                                  namespace) is not None else "Нет штрихкода паллеты"

        for box in pallet.findall('ns:Boxes/ns:Box', namespace):
            box_barcode = box.find('ns:Barcode', namespace).text if box.find('ns:Barcode',
                                                                             namespace) is not None else "Нет штрихкода короба"
            mark_codes = box.find('ns:MarkCodes', namespace)

            if mark_codes is None:
                errors.append(f"Ошибка: В коробке {box_barcode} отсутствует MarkCodes.")
                continue

            codes = [code.text for code in mark_codes.findall('ns:Code', namespace) if code.text]

            # Проверка количества Code в MarkCodes
            if len(codes) != 12:
                errors.append(
                    f"{pallet_barcode}    {box_barcode}    количество бутылок {len(codes)}")

            for i, code in enumerate(codes):
                # Проверка длины Code
                if len(code) != 150:
                    errors.append(
                        f"{pallet_barcode}    {box_barcode}    ФСМ имеет длину {len(code)}")

                # Проверка наличия маленьких латинских букв
                if any(c.islower() for c in code):
                    errors.append(
                        f"{pallet_barcode}    {box_barcode}    ФСМ содержит маленькие латинские буквы.")

                # Проверка наличия кириллических символов
                if any('\u0400' <= c <= '\u04FF' for c in code):
                    errors.append(
                        f"{pallet_barcode}    {box_barcode}    ФСМ содержит кириллические символы.")

    if len(errors) == 0:
        messagebox.showinfo("Результат", "Ошибок нет")




    # Запись ошибок в лог-файл
    with open(log_file, "w", encoding="utf-8") as log:
        if errors:
            log.write("\n".join(errors))
            messagebox.showinfo("Результат", "Ошибки сохранены.")


# Основной процесс
xml_file = select_xml_file()
if xml_file:
    log_file = select_log_file(xml_file)
    if log_file:
        validate_xml(xml_file, log_file)
    else:
        messagebox.showinfo("Результат", "Сохраниние log файла отменено.")
else:
    messagebox.showinfo("Результат", "Выбор XML-файла отменен.")

