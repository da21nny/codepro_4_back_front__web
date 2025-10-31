# importamos la extension que permite usar SQLAlchemy con Flask
from flask_sqlalchemy import SQLAlchemy

# instanciamos sqlalchemy - esto no va a servir para conectar la base de datos a flask
db = SQLAlchemy()

# definir una clase (que va a representar nuestra tabla) llamada alumno
class Alumnos(db.Model):
    # atributo de clase
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    cedula = db.Column(db.Integer, nullable=False)
    
    calificaciones = db.relationship('Calificaciones', back_populates='alumno')
    
    def __init__(self, nombre, apellido, cedula):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        

class Calificaciones(db.Model):
    __tablename__ = 'calificaciones'  

    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String(80), nullable=False) 
    calificacion = db.Column(db.Integer, nullable=False)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'))

    alumno = db.relationship('Alumnos', back_populates='calificaciones')

    def __init__(self, name, calificacion, alumno_id):

        self.name = name
        self.calificacion = calificacion
        self.alumno_id = alumno_id

