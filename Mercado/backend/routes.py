from flask import jsonify, request
from app import app, db
from models import *


#Para autentificar
from flask_bcrypt import check_password_hash, generate_password_hash
import jwt
import datetime
#------------------------------




# Define la función para crear el esquema dinámicamente
def create_table_schema(id):
    class TableSchema(ma.Schema):
        class Meta:
            fields = ('id', 'title', 'price','amount')

    table_schema = TableSchema()
    tables_schema = TableSchema(many=True)

    globals()[f'table_{id}_schema'] = table_schema
    globals()[f'tables_{id}_schema'] = tables_schema


#----------------------------



@app.route('/loginup', methods=['POST'])
def create_user():
    email=request.json['email']
    user=request.json['user']
    password = generate_password_hash(request.json['password'])
    existing_user = User.query.filter_by(user=user).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409
    new_user = User(email, user, password)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user)

@app.route('/loginup', methods=['GET'])
def get_users():
    all_users=User.query.all()
    result=users_schema.dump(all_users)
    return jsonify(result)                    

@app.route('/loginup/<id>', methods=['GET'])
def get_user(id):
    user=User.query.get(id)
    return user_schema.jsonify(user) 

@app.route('/loginup/<id>', methods=['PUT'])
def update_user(id):
    user_to_update = User.query.get(id)  # Renombrar la variable aquí
    
    email = request.json['email']
    new_user = request.json['user']
    password = generate_password_hash(request.json['password'])

    user_to_update.email = email
    user_to_update.user = new_user  # Renombrar la variable aquí
    user_to_update.password = password
    
    db.session.commit()
    return user_schema.jsonify(user_to_update)



@app.route('/loginup/<id>', methods=['DELETE'])
def delete_user(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)


#Login IN (Iniciar sesion)
@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    username = data['user']
    password = data['password']

    user = User.query.filter_by(user=username).first()
    if user and check_password_hash(user.password, password):
        # Las credenciales son válidas, puedes generar un token de autenticación aquí
        token = generate_token(user)  # Ejemplo: función para generar el token

        return jsonify({'token': token ,"user_id": user.id}), 200

    # Las credenciales son incorrectas
    return jsonify({'error': 'Credenciales inválidas'}), 401


def generate_token(user):
    # Definir las opciones y configuraciones del token
    token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira en 1 hora
    }
    secret_key = 'tuclavesecretadeltoken'  # Cambia esto a tu clave secreta real

    # Generar el token JWT utilizando PyJWT
    token = jwt.encode(token_payload, secret_key, algorithm='HS256')
    return token


#------------------------------
#Product
@app.route('/products', methods=['POST'])
def create_product():
    code=request.json['code']
    title=request.json['title']
    price=request.json['price']

    new_product=Product(code, title, price)
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)

@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/products/<id>', methods=['GET'])
def get_product_id(id):
    product=Product.query.get(id)
    return product_schema.jsonify(product) 

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    product_to_update = Product.query.get(id)  # Renombrar la variable aquí
    
    code = request.json['code']
    title = request.json['title']
    price = request.json['price']
  

    product_to_update.code = code
    product_to_update.title = title  # Renombrar la variable aquí
    product_to_update.price = price
    
    db.session.commit()
    return product_schema.jsonify(product_to_update)

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product=Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

#----------------------------
#carrito_user
@app.route('/tableuser', methods=['POST'])
def create_tableuser():
    try:
        id = request.json.get('id')
        if not id:
            return 'User not provided', 400

        table_name = f'table_{id}'
        user_table = type(table_name, (db.Model,), {
            'id': db.Column(db.Integer, primary_key=True),
            'title': db.Column(db.String(200)),
            'price': db.Column(db.String(100)),
            'amount': db.Column(db.Integer)
        })

        create_table_schema(id)  # Llama a la función para crear el esquema dinámicamente

        db.create_all()
        return 'User table created successfully', 201

    except Exception as e:
        return str(e), 500


from sqlalchemy import inspect

@app.route('/tableuser/<id>', methods=['POST'])
def post_tableuser(id):
    try:
        # Obtener los datos de temperatura y humedad de la solicitud JSON
        title = request.json.get('title')
        price = request.json.get('price')
        amount = request.json.get('amount')

        # Verificar si la tabla existe en la base de datos
        table_name = f'table_{id}'
        inspector = inspect(db.engine)
        if table_name not in inspector.get_table_names():
            return 'Table not found', 404

        # Crear una instancia de la clase de la tabla dinámica
        TableClass = type(table_name, (db.Model,), {})
        table_entry = TableClass(title=title, price=price, amount=amount)

        # Agregar la nueva entrada a la base de datos
        db.session.add(table_entry)
        db.session.commit()

        return jsonify({'message': 'Data added successfully'}), 200

    except Exception as e:
        return str(e), 500  # Devuelve el mensaje de error en caso de que ocurra una excepción


from sqlalchemy import inspect
from sqlalchemy import Table

@app.route('/tableuser/<id>', methods=['GET'])
def get_tableuser(id):
    try:
        table_name = f'table_{id}'  # Genera el nombre de la tabla a buscar
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):  # Verifica si la tabla existe en la base de datos
            return 'Table not found', 404

        # Reflect the tables from the database
        db.reflect()

        # Obtén la tabla dinámica a partir del nombre
        table = db.Model.metadata.tables[table_name]

        # Realiza la consulta a la tabla
        table_data = db.session.query(table).all()

        # Procesa los datos obtenidos y devuélvelos como respuesta
        data = []
        for row in table_data:
            data.append({
                'id': row.id,
                'title': row.title,
                'price': row.price,
                'amount': row.amount
            })

        return jsonify(data), 200

    except Exception as e:
        return str(e), 500  # Devuelve el mensaje de error en caso de que ocurra una excepción

#delete row of table_id carrito
@app.route('/tableuser/<id>/<id_row>', methods=['DELETE'])
def delete_row_table_id(id, id_row):
    try:
        table_name = f'table_{id}'  # Genera el nombre de la tabla a buscar
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):  # Verifica si la tabla existe en la base de datos
            return 'Table not found', 404

        # Reflect the tables from the database
        db.reflect()

        # Obtén la tabla dinámica a partir del nombre
        table = db.Model.metadata.tables[table_name]

        # Realiza la consulta para eliminar el id_row seleccionado
        delete_query = table.delete().where(table.c.id == id_row)
        db.session.execute(delete_query)
        db.session.commit()

        return 'Product deleted', 200

    except Exception as e:
        return str(e), 500  # Devuelve el mensaje de error en caso de que ocurra una excepción





from sqlalchemy import text
# delete table_user

@app.route('/tableuser/account/<id>', methods=['DELETE'])
def delete_table_id_account(id):
    try:
        table_name = f'table_{id}'  # Genera el nombre de la tabla a buscar
        inspector = inspect(db.engine)
        if not inspector.has_table(table_name):  # Verifica si la tabla existe en la base de datos
            return 'Table not found', 404

        # Ejecuta la sentencia SQL para eliminar la tabla
        delete_query = text(f"DROP TABLE {table_name}")
        with db.engine.connect() as connection:
            connection.execute(delete_query)

        return 'Table_id deleted', 200

    except Exception as e:
        return str(e), 500  # Devuelve el mensaje de error en caso de que ocurra una excepción
