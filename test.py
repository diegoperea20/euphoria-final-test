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

# Crear productos
producto1 = Producto('Camiseta', 20.0)
producto2 = Producto('Pantalon', 40.0)

# Crear carrito de compras
carrito = CarritoCompras()

# Agregar productos al carrito
carrito.agregar_producto(producto1)
carrito.agregar_producto(producto2)


# Serializar carrito a JSON
carrito_json = json.dumps(carrito.to_dict())
print(carrito_json)

# Deserializar JSON a carrito
carrito_dict = json.loads(carrito_json)
carrito_deserializado = CarritoCompras.from_dict(carrito_dict)

# Eliminar un producto del carrito
carrito_deserializado.eliminar_producto(producto1)

# Mostrar productos restantes en el carrito
for producto in carrito_deserializado.productos:
    print(producto.nombre, producto.precio)
