from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    servicios = [
        {"codigo": "S01", "nombre": "Mantenimiento"},
        {"codigo": "S02", "nombre": "Instalación"}
    ]
    return render_template("index.html", servicios=servicios)

if __name__ == "__main__":
    app.run()
