from flask import Flask, jsonify, request, render_template, redirect, url_for
from modelo import Producto, CarritoCompras

app = Flask(__name__)

carrito = CarritoCompras()

productos_bb = []
producto1 = Producto('Camiseta', 20.0)
producto2 = Producto('Pantalon', 40.0)

productos_bb.append(producto1)
productos_bb.append(producto2)

@app.route('/', methods=['GET'])
def mostrar_carrito():
    productos = carrito.productos
    return render_template('carrito.html', productos=productos,productos_bb=productos_bb)

@app.route('/carrito/agregar', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    producto = Producto(nombre, precio)
    carrito.agregar_producto(producto)
    return redirect(url_for('mostrar_carrito'))

@app.route('/carrito/eliminar', methods=['POST'])
def eliminar_producto():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    producto = Producto(nombre, precio)
    carrito.eliminar_producto(producto)
    return redirect(url_for('mostrar_carrito'))
