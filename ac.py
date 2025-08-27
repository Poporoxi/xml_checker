import os
import xml.etree.ElementTree as ET

import tkinter as tk
from tkinter import messagebox


# папки
INPUT_FOLDER = r"C:\АСИиУ\Розлив\Файлы АСИиУ"
OUTPUT_FOLDER = r"\\192.168.55.51\egais\Ежедневные отчеты производства"
LOG_FILE = r"\\192.168.55.51\egais\Ежедневные отчеты производства\log\log.txt"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# загрузим уже обработанные файлы
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        processed = set(f.read().splitlines())
else:
    processed = set()

# новые файлы
new_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".xml") and f not in processed]

# --- проверка на количество ---
if len(new_files) == 0:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка", "Новых файлов для обработки нет!")
    exit(1)
elif len(new_files) < 4:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка", f"Ожидалось 4 файла, найдено только {len(new_files)}!")
    exit(1)



# --- обработка ---
for filename in new_files:
    filepath = os.path.join(INPUT_FOLDER, filename)
    tree = ET.parse(filepath)
    root_elem = tree.getroot()

    # пространство имён
    ns = {
        "ns": "http://fsrar.ru/WEGAIS/WB_DOC_SINGLE_01",
        "as": "http://fsrar.ru/WEGAIS/Asiiu",
        "prod": "http://fsrar.ru/WEGAIS/ProductRef_v2"
    }

    for pos in root_elem.findall(".//as:Position", ns):
        start = int(pos.findtext("as:BottleCountStart", "0", ns))
        end = int(pos.findtext("as:BottleCountEnd", "0", ns))

        if start != end:
            start_date = pos.findtext("as:StartDate", "", ns).split("T")[0]  # YYYY-MM-DD
            product = pos.find("as:Product", ns)
            if product is not None:
                alc_code = product.findtext("prod:AlcCode", "", ns)
                full_name = product.findtext("prod:FullName", "", ns)
                capacity = product.findtext("prod:Capacity", "", ns)
                alc_volume = product.findtext("prod:AlcVolume", "", ns)
                qty = end - start

                # имя файла = start_date
                report_name = f"{start_date}.txt"
                report_path = os.path.join(OUTPUT_FOLDER, report_name)
                try:
                    with open(report_path, "a", encoding="utf-8") as rep:
                        rep.write(f"Дата: {start_date}\n")
                        rep.write(f"Код: {alc_code}\n")
                        rep.write(f"Название: {full_name}\n")
                        rep.write(f"Объем: {capacity}\n")
                        rep.write(f"Крепость: {alc_volume}\n")
                        rep.write(f"Количество: {qty}\n")
                        rep.write("-" * 30 + "\n")

                except Exception:
                    root = tk.Tk()
                    root.withdraw()
                    messagebox.showerror("Ошибка", f"Ошибка при записи файла: {Exception}")
                    exit(1)

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(filename + "\n")

    except Exception:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Ошибка", f"Ошибка при записи лога: {Exception}")
        exit(1)
