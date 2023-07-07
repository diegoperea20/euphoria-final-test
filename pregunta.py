import json

class Producto:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio

    def to_dict_producto(self):
        return {
            'nombre': self.nombre,
            'precio': self.precio
        }

    @classmethod
    def from_dict_producto(cls, dict_obj):
        return cls(dict_obj['nombre'], dict_obj['precio'])


class CarritoCompras:
    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def eliminar_producto(self, producto):
        for p in self.productos:
            if p.nombre == producto.nombre and p.precio == producto.precio:
                self.productos.remove(p)
                return

    def to_dict(self):
        return {
            'productos': [producto.to_dict_producto() for producto in self.productos]
        }

    @classmethod
    def from_dict(cls, dict_obj):
        carrito = cls()
        for producto_dict in dict_obj['productos']:
            producto = Producto.from_dict_producto(producto_dict)
            carrito.agregar_producto(producto)
        return carrito


# Ejemplo de uso del carrito de compras



# Crear carrito de compras
carrito = CarritoCompras()
print(f'Camiseta : 20.0\nPantalon : 40.0\nZapatos : 50.0')
while True:
    
    producto = input('Ingrese el nombre del producto (o "salir" para terminar): ')

    if producto == "salir":
        break

    # Verificar si el producto existe y agregarlo al carrito
    if producto == "Camiseta":
        producto_seleccionado = Producto('Camiseta', 20.0)
        carrito.agregar_producto(producto_seleccionado)
        print("Producto agregado al carrito.")
    elif producto == "Pantalon":
        producto_seleccionado = Producto('Pantalon', 40.0)
        carrito.agregar_producto(producto_seleccionado)
        print("Producto agregado al carrito.")
    elif producto == "Zapatos":
        producto_seleccionado = Producto('Zapatos', 50.0)
        carrito.agregar_producto(producto_seleccionado)
        print("Producto agregado al carrito.")
    else:
        print("Producto no válido. Intente nuevamente.")
        continue

    # Mostrar productos en el carrito
    print("Productos en el carrito:")
    for producto in carrito.productos:
        print(producto.nombre, producto.precio)

    # Eliminar un producto del carrito
    decision_eliminar = input("Desea eliminar un producto del carrito? (si/no): ")
    if decision_eliminar == "si":
        producto_eliminar = input("Ingrese el nombre del producto a eliminar: ")
        precio_eliminar = float(input("Ingrese el precio del producto a eliminar: "))

        producto_a_eliminar = Producto(producto_eliminar, precio_eliminar)
        carrito.eliminar_producto(producto_a_eliminar)

    # Mostrar productos restantes en el carrito
    print("Productos en el carrito ")
    for producto in carrito.productos:
        print(producto.nombre, producto.precio)
