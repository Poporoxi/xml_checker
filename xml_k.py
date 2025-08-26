import os
from collections import defaultdict
from tkinter import filedialog, messagebox
import xml.etree.ElementTree as ET

REFERENCE = {
    "04630027300508": "04630027301727",
    "04630027300782": "04630027301550",
    "04630027300799": "04630027301543",
    "04630027300812": "04630027301413",
    "04630027300829": "04630027301406",
    "04630027300836": "04630027301536",
    "04630027300843": "04630027301529",
    "04630027300911": "04630027301512",
    "04630027300980": "04630027301505",
    "04630027301000": "04630027301499",
    "04630027301017": "04630027301482",
    "04630027301079": "04630027301475",
    "04630027301093": "04630027301451",
    "04630027301109": "04630027301444",
    "04630027301130": "04630027301468",
    "04630027301253": "04630027301604",
    "04630027301260": "04630027301598",
    "04630027301277": "04630027301659",
    "04630027301284": "04630027301734",
    "04630027301291": "04630027301642",
    "04630027301307": "04630027301666",
    "04630027301314": "04630027301628",
    "04630027301321": "04630027301581",
    "04630027301376": "04630027301567",
    "04630027301390": "04630027301574",
    "04630027301697": "04630027301765",
    "04630027301710": "04630027301758",
    "04630027301703": "04630027301741",
    "04630027301772": "04630027301789",
    "04630027301802": "04630027301819",
}

def select_file():
    file_path = filedialog.askopenfilename(
        title="Выберите XML файл",
        filetypes=[("XML files", "*.xml")]
    )
    if file_path:
        process_file(file_path)

def process_file(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        rows = root.findall('.//Row')

        aktsiz_map = defaultdict(list)
        barcode_map = defaultdict(list)

        errors = []

        # Собираем данные
        for i, row in enumerate(rows, start=1):
            aktsiz_el = row.find('Акциз')
            barcode_el = row.find('ШтрихкодКоробки')

            aktsiz_val = (aktsiz_el.text[2:16] if aktsiz_el is not None and aktsiz_el.text else '').strip()
            barcode_val = (barcode_el.text[2:16] if barcode_el is not None and barcode_el.text else '').strip()

            # 1. Проверка на пустые значения
            if not aktsiz_val or not barcode_val:
                errors.append(f"Есть пустой Акциз или Штрихкод!")
                continue

            aktsiz_map[aktsiz_val].append(i)
            barcode_map[barcode_val].append(i)

            # 3. Проверка на соответствие по справочнику
            if aktsiz_val in REFERENCE:
                expected_barcode = REFERENCE[aktsiz_val]
                if barcode_val != expected_barcode:
                    errors.append(
                        f"GTIN {aktsiz_val} должен быть с КИГУ {expected_barcode}, "
                        f"а найден {barcode_val}"
                    )
            else:
                errors.append(f"GTIN {aktsiz_val} отсутствует в справочнике!")

        # 2. Проверка уникальных значений (они считаются ошибкой)
        for val, indices in aktsiz_map.items():
            if len(indices) == 1:
                errors.append(f"Ошибка: GTIN {val}")

        for val, indices in barcode_map.items():
            if len(indices) == 1:
                errors.append(f"Ошибка: КИГУ {val}")

        # Итог
        if errors:
            base_name = os.path.splitext(os.path.basename(file_path))[0]  # имя исходного файла без .xml
            save_name = f"{base_name}_errors.txt"
            save_path = os.path.join(os.getcwd(), save_name)  # сохранить в папку запуска

            with open(save_path, "w", encoding="utf-8") as f:
                f.write("\n".join(errors))
            messagebox.showinfo("Результат", "Найдены ошибки!")
        else:
            messagebox.showinfo("Результат", "Ошибок не найдено")

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))





if __name__ == '__main__':
    select_file()