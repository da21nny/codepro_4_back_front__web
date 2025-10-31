from flask import render_template, request, redirect, url_for
from conexion import app, db
from models import Alumnos, Calificaciones


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cargar_datos', methods=['GET', 'POST'])
def cargar_datos():
    # si el metodo es POST, significa que el usuario apreto enviar
    if request.method == 'POST':
        # tomamos los datos que se escribio en el formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedula']
        
        # creamos un nuevo alumno usando la clase del modelo de la base de datos - vamos a crear un objeto nuevo con esos datos
        datos_alumnos = Alumnos(nombre, apellido, cedula)
        
        # metemos dentro de esta caja al nuevo alumno para guardarlo
        db.session.add(datos_alumnos)
        # guardar los datos
        db.session.commit()
        
        # si el metodo es POST recibimos los datos y renderizamos la plantilla
        return render_template('cargar_datos.html')
    # si el metodo es GET, solo vamos a mostrar el formulario vacio
    return render_template('cargar_datos.html')


@app.route('/mostrar_datos', methods=['GET', 'POST'])
def mostrar_datos():
    lista_alumnos = Alumnos.query.all()
    
    return render_template('mostrar_datos.html', lista_alumnos=lista_alumnos)

@app.route('/cargar_calificaciones', methods=['GET', 'POST'])
def cargar_calificaciones():
    # si el usuarui envia el formulario (metodo post)
    if request.method == 'POST':
        materia = request.form['materia']
        calificacion = request.form['calificacion']
        cedula = request.form['cedula']
        
        alumno = Alumnos.query.filter_by(cedula=cedula).first()
        
        # si el alumno existe, vamos a guardar su califiacion
        if alumno != None:
            # creamos un nuevo registro de la calificacion
            calificacion = Calificaciones(materia, calificacion, alumno.id)
            
            # agregamos el registro a la sesion
            db.session.add(calificacion)
            # confirmamos y guardamos los datos
            db.session.commit()
        else:
            return 'el alumno no existe'
    
    # mostrar el forulario html para cargar califiaciones
    return render_template('cargar_calificaciones.html')


@app.route('/mostrar_calificaciones', methods=['GET', 'POST'])
def mostrar_calificaciones():
    # si el usuario envia el formulario con metodo post
    if request.method == 'POST':
        # vamos a tomar los datos (en este caso la cedula)
        alumno_ci = request.form['cedula']
        # buscamos en la base de datos el alumno con esa ceulda
        alumno = Alumnos.query.filter_by(cedula=alumno_ci).first()
        
        # si no se encuentran alumnos 
        if alumno is None:
            return 'el alumno no existe'
        
        # buscar las calificaciones que tengan el id del alumno
        calificaciones = Calificaciones.query.filter_by(alumno_id=alumno.id)
        
        # mostrar la pagina con los datos del alumnos y sus calificaciones
        return render_template('mostrar_calificaciones.html', alumno=alumno, calificaciones=calificaciones)
    
    # si el usuario entra a la pagina por primera vez (metodo get)
    # mostramos la pagina vacia sin datos
    return render_template('mostrar_calificaciones.html', alumno=None, calificaciones=None)


# Ruta para actualizar los datos de un alumno; el ID se pide desde un formulario
@app.route('/actualizar', methods=['GET', 'POST'])
def actualizar():
    # Si el usuario envía el formulario
    if request.method == 'POST':
        # Tomamos el ID escrito en el formulario
        alumno_id = request.form['id']
        # Buscamos el alumno por su ID
        alumno_actualizado = Alumnos.query.get(alumno_id)

        # Si el alumno existe
        if alumno_actualizado:
            # Tomamos el nuevo nombre
            nombre = request.form['nombre']
            # Tomamos el nuevo apellido
            apellido = request.form['apellido']
            # Tomamos la nueva cédula
            cedula = request.form['cedula']

            # Actualizamos los datos del alumno con los valores del formulario
            alumno_actualizado.nombre = nombre
            alumno_actualizado.apellido = apellido
            alumno_actualizado.cedula = cedula

            # en esta seccion no es necesario usar with porque flask ya manera el contexto
            db.session.commit()  # Guardamos los cambios en la base
            return redirect(url_for('mostrar_datos'))  # Redirigimos a la lista de alumnos
        else:
            return 'El alumno no existe'  # Si no se encontró el ID, mostramos un mensaje

    # Si es un GET, mostramos el formulario vacío
    return render_template('actualizar.html', alumno_actualizado=None)


#Creamos la ruta para eliminar... esta ruta no tiene una pagina HTML ya que desde mostrar_datos.html podemos acceder a esta ruta de acuerdo a la configuracion que realizamos en la misma"
@app.route('/eliminar', methods= ['GET', 'POST'])
def eliminar():

    if request.method == 'POST':
        #Guardamos en la variable id los datos obtenidos del formulario
        id = request.form['alumno_id']
        #Realizamos la consulta a nuestra base de datos para obtener los datos del alumno en referencia y creamos un nuevo objeto guardando en la variable 
        alumno_a_eliminar = Alumnos.query.filter_by(id=id).first()

        #Eliminamos los datos del alumno
        db.session.delete(alumno_a_eliminar)
        #Confirmamos la eliminacion
        db.session.commit() 

        return redirect(url_for('mostrar_datos'))#Redireccionamos a la pagina para mostrar los datos de la base de datos

# Renderizar las materias por alumnos 
# Una ruta que filtre en Alumnos por materias
# @app.route('/filtrar/<:id_materia>')