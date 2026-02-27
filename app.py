import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DB_NAME = "inventario.db"

# ===============================
# CLASE PRODUCTO (POO)
# ===============================
class Producto:
    def __init__(self, id, nombre, cantidad, precio):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    # Getters
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Setters
    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio


# ===============================
# CLASE INVENTARIO (Diccionario)
# ===============================
class Inventario:
    def __init__(self):
        self.productos = {}

    def cargar_desde_db(self):
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()
        conexion.close()

        for fila in filas:
            producto = Producto(fila[0], fila[1], fila[2], fila[3])
            self.productos[fila[0]] = producto

    def mostrar_todos(self):
        return self.productos.values()

    def buscar_por_nombre(self, nombre):
        if not nombre:
            return self.productos.values()

        return [p for p in self.productos.values()
                if nombre.lower() in p.get_nombre().lower()]

    def actualizar_producto(self, id, cantidad=None, precio=None):
        if id in self.productos:
            if cantidad is not None:
                self.productos[id].set_cantidad(cantidad)
            if precio is not None:
                self.productos[id].set_precio(precio)


# ===============================
# CREAR BASE DE DATOS
# ===============================
def crear_bd():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        cantidad INTEGER,
        precio REAL
    )
    """)

    conexion.commit()
    conexion.close()


# ===============================
# RUTAS
# ===============================

@app.route("/")
def menu():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/productos")
def productos():
    inventario = Inventario()
    inventario.cargar_desde_db()
    lista = inventario.mostrar_todos()
    return render_template("productos.html", productos=lista)


@app.route("/agregar", methods=["POST"])
def agregar():
    id = request.form["id"]
    nombre = request.form["nombre"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos VALUES (?, ?, ?, ?)",
                   (id, nombre, cantidad, precio))
    conexion.commit()
    conexion.close()

    return redirect(url_for("productos"))


@app.route("/eliminar/<int:id>")
def eliminar(id):
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

    return redirect(url_for("productos"))


@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE productos
        SET cantidad = ?, precio = ?
        WHERE id = ?
    """, (cantidad, precio, id))
    conexion.commit()
    conexion.close()

    return redirect(url_for("productos"))


@app.route("/buscar")
def buscar():
    nombre = request.args.get("nombre")

    inventario = Inventario()
    inventario.cargar_desde_db()
    resultados = inventario.buscar_por_nombre(nombre)

    return render_template("productos.html", productos=resultados)


# ===============================
# EJECUCIÓN
# ===============================
if __name__ == "__main__":
    crear_bd()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)  