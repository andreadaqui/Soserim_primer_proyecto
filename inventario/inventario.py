import json
import csv
import os

# Ruta donde se guardarán los archivos
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

TXT_FILE = os.path.join(DATA_DIR, "datos.txt")
JSON_FILE = os.path.join(DATA_DIR, "datos.json")
CSV_FILE = os.path.join(DATA_DIR, "datos.csv")


# =============================
# GUARDAR EN TXT
# =============================
def guardar_txt(producto):

    with open(TXT_FILE, "a", encoding="utf-8") as f:
        linea = f"{producto.get_id()},{producto.get_nombre()},{producto.get_cantidad()},{producto.get_precio()}\n"
        f.write(linea)


# =============================
# LEER TXT
# =============================
def leer_txt():

    datos = []

    if not os.path.exists(TXT_FILE):
        return datos

    with open(TXT_FILE, "r", encoding="utf-8") as f:
        for linea in f:
            datos.append(linea.strip())

    return datos


# =============================
# GUARDAR JSON
# =============================
def guardar_json(producto):

    datos = []

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            try:
                datos = json.load(f)
            except:
                datos = []

    datos.append({
        "id": producto.get_id(),
        "nombre": producto.get_nombre(),
        "cantidad": producto.get_cantidad(),
        "precio": producto.get_precio()
    })

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4)


# =============================
# LEER JSON
# =============================
def leer_json():

    if not os.path.exists(JSON_FILE):
        return []

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# =============================
# GUARDAR CSV
# =============================
def guardar_csv(producto):

    archivo_existe = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not archivo_existe:
            writer.writerow(["id", "nombre", "cantidad", "precio"])

        writer.writerow([
            producto.get_id(),
            producto.get_nombre(),
            producto.get_cantidad(),
            producto.get_precio()
        ])


# =============================
# LEER CSV
# =============================
def leer_csv():

    datos = []

    if not os.path.exists(CSV_FILE):
        return datos

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for fila in reader:
            datos.append(fila)

    return datos