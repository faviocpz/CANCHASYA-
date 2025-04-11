from flask import Flask, render_template
from conexion import obtener_conexion

conn = obtener_conexion()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run()



