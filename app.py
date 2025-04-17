from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/login')
def login():
    return render_template('pages/login.html')

@app.route('/canchas')
def canchas():
    return render_template('pages/canchas.html')

@app.route('/cancha')
def cancha():
    return render_template('pages/cancha.html')

@app.route('/carrito')
def carrito():
    return render_template('pages/carrito.html')

@app.route('/panel')
def panel():
    return render_template('pages/panel.html')

@app.route('/maestra_interna')
def maestra_interna():
    return render_template('base_interna.html')





if __name__ == '__main__':
    app.run(debug=True)
