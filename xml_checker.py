from tkinter import *
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import customtkinter as ctk

def select_bottles():
    def submit(value):
        nonlocal bottles
        bottles = value
        root.destroy()  # Закрываем окно после выбора

    ctk.set_appearance_mode("dark")  # Темный режим
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Выбор количества")
    root.geometry("300x200")

    ctk.CTkLabel(root, text="Сколько бутылок в коробке?", font=("Arial", 16, "bold")).pack(pady=15)

    ctk.CTkButton(root, text="12", command=lambda: submit(12), width=200).pack(pady=8)
    ctk.CTkButton(root, text="6", command=lambda: submit(6), width=200).pack(pady=8)

    bottles = 12
    root.mainloop()

    return bottles


def select_xml_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("XML files", "*.xml"), ("All files", "*.*")])


def select_log_file(xml_filename):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Выберите папку для сохранения лог-файла")
    if folder_path:
        log_filename = os.path.splitext(os.path.basename(xml_filename))[0] + "_errors.txt"
        return os.path.join(folder_path, log_filename)
    return None

def validate_xml(file_path, log_file):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        messagebox.showerror("Ошибка", f"Ошибка парсинга XML: {e}")
        return

    errors = []
    namespace = {'ns': 'http://masterutm.center-inform.ru/packing'}
    all_codes = {}

    for pallet in root.findall('ns:Pallet', namespace):
        pallet_barcode = pallet.find('ns:Barcode', namespace)
        pallet_barcode = pallet_barcode.text if pallet_barcode is not None else "Нет штрихкода паллеты"

        for box in pallet.findall('ns:Boxes/ns:Box', namespace):
            box_barcode = box.find('ns:Barcode', namespace)
            box_barcode = box_barcode.text if box_barcode is not None else "Нет штрихкода короба"
            mark_codes = box.find('ns:MarkCodes', namespace)

            if mark_codes is None:
                errors.append(f"Ошибка: В коробке {box_barcode} отсутствует MarkCodes.")
                continue

            codes = [code.text for code in mark_codes.findall('ns:Code', namespace) if code.text]

            if len(codes) != bottles:
                errors.append(f"{pallet_barcode}    {box_barcode}    Количество бутылок {len(codes)}")

            for code in codes:
                if len(code) != 150:
                    errors.append(f"{pallet_barcode}    {box_barcode}    ФСМ имеет неверную длину, вместо 150 символов - {len(code)}")
                if any(c.islower() or '\u0400' <= c <= '\u04FF' for c in code or code[0:21].isalnum()):
                    errors.append(f"{pallet_barcode}    {box_barcode}    ФСМ содержит некорректные символы.")

                # Проверяем наличие кода в словаре all_codes
                if code in all_codes:
                    errors.append(f"{pallet_barcode}    {box_barcode}    Дубликат ФСМ {code[3:14]}")
                    errors.append(f"{all_codes[code][0]}    {all_codes[code][1]}    Дубликат ФСМ {code[3:14]}")
                all_codes[code] = (pallet_barcode, box_barcode)

    if errors:
        with open(log_file, "w", encoding="utf-8") as log:
            log.write("\n".join(errors))
        messagebox.showinfo("Результат", "Ошибки сохранены.")
    else:
        messagebox.showinfo("Результат", "Ошибок нет.")


bottles = select_bottles()

xml_file = select_xml_file()


if xml_file:
    log_file = select_log_file(xml_file)
    if log_file:
        validate_xml(xml_file, log_file)
    else:
        messagebox.showinfo("Результат", "Сохранение log-файла отменено.")
else:
    messagebox.showinfo("Результат", "Выбор XML-файла отменен.")
