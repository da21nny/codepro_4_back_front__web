# importamos flask para crear nuestra aplicacion
from flask import Flask
# importamos el objeto db definido en models.py
from models import db

# instanciando - creamos la aplicacion Flask
app = Flask(__name__)

# vamos a indicar a Flask donde esta la base de datos y que tipo de base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///alumnos_registrados.db'

# conectamos la base de datos con nuestra aplicacion Flask
db.init_app(app)

with app.app_context():
    db.create_all()