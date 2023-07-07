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

