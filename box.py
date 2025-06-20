import customtkinter as ctk
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import messagebox, filedialog


# Настройки интерфейса
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")


def select_xml_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(filetypes=[("XML files", "*.xml"), ("All files", "*.*")])


# Загрузка XML и извлечение всех кодов из <Акциз>
def load_excise_codes(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    namespace = {'V8Exch': 'http://www.1c.ru/V8/1CV8DtUD/'}
    excise_codes = set()

    for row in root.findall(".//V8Exch:Data//Row", namespace):
        akziz = row.findtext("ШтрихкодКоробки")
        if akziz:
            excise_codes.add(akziz.strip())
    return excise_codes

# Проверка кода и отображение результата
def check_code():
    code = entry.get().strip()
    if not code:
        return
    if code in excise_codes:
        indicator.configure(fg_color="green")
    else:
        indicator.configure(fg_color="red")
    entry.delete(0, ctk.END)  # Очистка ввода

# Загрузка XML-файла
xml_file = select_xml_file() # Укажи путь к XML-файлу
excise_codes = load_excise_codes(xml_file)

# Интерфейс
app = ctk.CTk()
app.title("Проверка акцизных кодов")
app.geometry("400x200")

label = ctk.CTkLabel(app, text="Отсканируйте код:")
label.pack(pady=10)

entry = ctk.CTkEntry(app, width=300)
entry.pack(pady=5)
entry.focus()

entry.bind("<Return>", lambda event: check_code())

indicator = ctk.CTkLabel(app, text=" ", width=30, height=30, corner_radius=15, fg_color="gray")
indicator.pack(pady=20)

app.mainloop()
