from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Bienvenido a Sosermin – Servicios Mineros Cuenca del Río Mira."

@app.route("/item/<codigo>")
def item(codigo):
    return f"Item con código {codigo} registrado correctamente en Sosermin."

if __name__ == "__main__":
    app.run(debug=True)
