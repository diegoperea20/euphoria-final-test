from app import db, ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    user= db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, email, user, password):
        self.email = email
        self.user = user
        self.password = password
        
#Product
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code= db.Column(db.String(200))
    title= db.Column(db.String(200))
    price = db.Column(db.String(200))

    def __init__(self, code, title, price):
        self.code = code
        self.title = title
        self.price = price


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'user', 'password')


user_schema = UserSchema()
users_schema = UserSchema(many=True)

#Product
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'code', 'title', 'price')


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)