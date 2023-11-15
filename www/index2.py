from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, jsonify #, safe_join, abort, 
#from flask_login import LoginManager, login_user, logout_user, login_required
from datetime import datetime
#from flask_uploads import UploadSet, configure_uploads, IMAGES
import os
import csv
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import sqlite3
import logging
import inspect
from flask_sqlalchemy import SQLAlchemy


# #Models:
# from models.ModelUser import ModelUser

# #Entities:
# from models.entities.Users import User


__author__ = "ThierryM23"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.secret_key = 'B!1w8NAt1T^%kvhUI*S^'
# The absolute path of the directory containing images for users to download
app.config["CLIENT_IMAGES"] = APP_ROOT + "/static/images/gallery"
# The absolute path of the directory containing CSV files for users to download
app.config["CLIENT_CSV"] = APP_ROOT + "/static/csv"
# The absolute path of the directory containing PDF files for users to download
app.config["CLIENT_PDF"] = APP_ROOT + "/static/pdf"
# the absolute path para las fotos de los platos
app.config['UPLOAD_FOLDER'] = APP_ROOT + "/static/images/photos"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# login_manager_app = LoginManager(app)

# @login_manager_app.user_loader 
# def load_user(id):
#     return db_sql("SELECT id, name, email, is_admin FROM product WHERE id=(?)", (id))

CONNECTED = False
USERNAME = 'Guest'
listuser = ['thierry', 'NONO']

# Configurar el nivel de registro y el archivo de registro
log_level = logging.INFO  # Puedes ajustar el nivel según tus necesidades
log_file = 'app.log'  # Nombre del archivo de registro

# Crear un manejador de registro para escribir en el archivo
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(log_level)

# Crear un formato para el registro
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(log_format)

# Agregar el manejador de registro a la aplicación Flask
app.logger.addHandler(file_handler)
app.logger.setLevel(log_level)

# Configura el conjunto de archivos para imágenes
#photos = UploadSet("photos", IMAGES)
#app.config["UPLOADED_PHOTOS_DEST"] = "/static/images/photos/"  # Directorio donde se almacenarán las imágenes
#configure_uploads(app, photos)
"""
#BASE DE DATOS con Flask Alchemy
db = SQLAlchemy(app)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite: ///www/webdata.db' # ruta absoluta
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


#Models:
from models.ModelUser import ModelUser

#Entities:
from models.entities.Users import User
"""

#DBASE DE DATOS conneccion() con Sqlite3

DB_NAME = "webdata.db"

def get_database_connection():
    con = sqlite3.connect(DB_NAME)
    return con


def db_sql(sql:str, todo: bool):
    con = get_database_connection()
    cursor = con.cursor()
    cursor.execute(sql)
    if todo:
        results = cursor.fetchall()
    else:
        results = cursor.fetchone()    
    app.logger.info('con a bd ' + str(results[0]) + ' - ' + str(results[1]))
    con.commit()
    con.close()
    return results

def insertar_product(contenido):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO product (contenido) VALUES (?)', (contenido,))
    conn.commit()
    conn.close()

def listar_product():
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product')
    registros = cursor.fetchall()
    conn.close()
    return registros

def allowed_file_images(filename):
    # Define una función para verificar la extensión del archivo si es necesario
    ALLOWED_EXTENSIONS_IMAGES = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGES

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



#ROUTES las paginas Web


@app.route('/')
def home():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    return render_template("home.html", titulo="Bienvenue")

@app.route('/location')
def locate():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    return render_template("location.html", titulo="Bienvenue")

@app.route('/carta')
def carta():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    registros = listar_product()
     
    return render_template("carta.html", titulo="Bienvenue", results=registros)

@app.route('/newplat', methods=['POST'])
def newplat():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    data = request.form.to_dict()
    app.logger.info(data )
    
    sql = "INSERT INTO product ( idcat, categorie, titre, description, prix, image) VALUES (" + str(data['idcat']) + ", '" +  data['categorie'] + "', '" + data['titre'] + "', '" + data['descripcion'] + "', " + str(data['prix']) + ", 'fondo.png')"
    app.logger.info(sql )
    conn = get_database_connection()
    cursor = conn.cursor()        
    result = cursor.execute(sql) 
    conn.commit()
    app.logger.info(result )
    conn.close()
    #flash('Nouveau plat ajoutée', 'alert-succes')
    return redirect(url_for('carta'))

@app.route('/carta_up/<string:id>', methods=['GET', 'POST'])
def carta_up(id):
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    app.logger.info(id)
    
    #if request.method == "POST":        
    data = request.form.to_dict()
    app.logger.info(data)
    app.logger.info("******** carta_up <string:id>  POST     *************")
    if data['accion']== 'upload':
        fichier = request.files['archivo']
        app.logger.info("******** carta_up <string:id>  POST  Accion = Upload   *************")
        app.logger.info(fichier.filename)
        if fichier.filename == '':
            return redirect(request.url)

        if fichier and allowed_file_images(fichier.filename):
            # Genera un nuevo nombre de archivo para evitar conflictos
            fichier.save(os.path.join(app.config['UPLOAD_FOLDER'], fichier.filename))
            sql = "UPDATE product SET image = '" + fichier.filename + "' WHERE product.id=" + id   
            app.logger.info(fichier.filename) 
            app.logger.info(sql) 
            conn = get_database_connection()
            cursor = conn.cursor()        
            cursor.execute(sql) 
            conn.commit()
            conn.close()
            app.logger.info("actulizado el campo de image en la base por el product " + id) 
        
    elif data['accion']=='save':
        app.logger.info("******** carta_up <string:id>  POST  Accion = save   *************")
        app.logger.info("******** carta_up <string:id>  POST  Accion = save   *************")
        nombre_image = "NULL"
        if "'archivo'" not in request.files:
            if "'nombre_archivo'" in request.files:
                nombre_image = data['nombre_archivo']
        else:
            if data['archivo'] != "":
                nombre_image = data['archivo']
            else:
                nombre_image = data['nombre_archivo']
        
        sql = "UPDATE product SET idcat = " + str(data['idcat']) + ", categorie = '" +  data['categorie'] + "', titre = '" + data['titre'] + "', description = '" + data['descripcion'] + "', prix = " + str(data['prix']) + ", image = '" + nombre_image + "' WHERE product.id=" + id
        app.logger.info(sql)
        app.logger.info("******** carta_up  POST   save  *************")
        conn = get_database_connection()
        cursor = conn.cursor()        
        cursor.execute(sql) 
        conn.commit()
        conn.close()
        app.logger.info("******** carta_up <string:id>  POST  Accion = save  FIN *************")
        return redirect(request.url)
        
    elif data['accion']=='Delete':
        app.logger.info("******** carta_up <string:id>  POST  Accion = Delete   *************")       
        sql = "DELETE FROM product WHERE product.id = " + id       
        app.logger.info(sql)
        
        conn = get_database_connection()
        cursor = conn.cursor()        
        cursor.execute(sql) 
        conn.commit()
        conn.close()
        app.logger.info(" se borro el registro numero " + id)
        app.logger.info("******** carta_up <string:id>  POST  Accion = delete  fin  *************")
        return redirect(url_for('carta'))  
    else:
        return redirect(request.url)
 
    return redirect(url_for('carta'))
    
              
@app.route('/carta_del/<string:id>', methods=['GET', 'POST'])
def carta_del(id):
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    app.logger.info(id)
    if request.method == "GET":
        sql = "DELETE FROM product WHERE product.id = " + id
        app.logger.info("******   GET carta delete *******")
        app.logger.info(sql)
        app.logger.info("******   GET DELETE  *******")
        conn = get_database_connection()
        cursor = conn.cursor()        
        cursor.execute(sql) 
        conn.commit()
        conn.close()
        return redirect(url_for('carta'))  
    else:
        app.logger.info("******  POST carta delete   ******")
        data = request.form.to_dict()
        app.logger.info(data)
        app.logger.info("******** POST carta delete   ******")
    return redirect(url_for('carta'))
        
@app.route('/subir_foto/<string:id>', methods=['POST'])
def subir_foto(id):
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    app.logger.info(" subir_ foto con id=")
    app.logger.info(id)
    if 'archivo' not in request.files:
        return redirect(request.url)

    archivo = request.files['archivo']

    if archivo.filename == '':
        return redirect(request.url)

    if archivo and allowed_file(archivo.filename):
        # Genera un nuevo nombre de archivo para evitar conflictos
        nuevo_nombre = 'nuevo_nombre' + os.path.splitext(archivo.filename)[1]
        archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], nuevo_nombre))
        return 'Archivo subido exitosamente como {}'.format(nuevo_nombre)

@app.route('/about')
def about():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    titulo: str = "About Page"
    return render_template('about.html', titulo="Le mot du chef", bg_image="modif-2.jpeg")


@app.route('/search', methods=['GET', 'POST'])
def search():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    if request.method == "GET":
        return render_template('search.html')
    elif request.method == "POST":
        data = request.form.to_dict()
        print(data)
        return "formulario recibido"
    else:
        return "metodo no aceptable"
 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    if request.method == "POST":
        data = request.form.to_dict()
        app.logger.info(data)
        if data['username'] == "Auberge":
            if  data['password'] == "NoNo":
                #login_user(Logged_user)
                logged_user=True
                app.logger.info('usuario logueado')
                flash("User logeado",'alert-success')
                return render_template('signup.html', display="formulario recibido", data=data,ok='True')
            else:   
                logged_user=False
                flash("invalid Password",'alert-warning')
                return render_template('signup.html', display="formulario recibido", data=data,ok='False')        
             
        else:
            flash("User not found",'alert-warning')
        return render_template('signup.html', display="formulario recibido", data=data,ok='False')
    else: 
        app.logger.info('signup GET')
        flash("no se por donde pasate",'alert-danger')
        return render_template('signup.html', display="formulario recibido", data=data,ok='False')
        


@app.route('/upload', methods=['POST'])
def upload():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    app.logger.info("funccion upload")
    target = app.config["CLIENT_IMAGES"]
    app.logger.info(target)
    # if not os.path.isdir(target):
    #         os.mkdir(target)
    # else:
    #     print("Couldn't create upload directory: {}".format(target))
    if not os.path.isdir(target):
        os.mkdir(target)
    app.logger.info(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png") or (ext == ".jpeg"):
            app.logger.info("File supported moving on...")
            #filename = filename.replace(" ","_")
            #filename = filename.replace("'","_")
            destination = "/".join([target, filename])            
            app.logger.info("Accept incoming file:", filename)
            app.logger.info("Save it to:", destination)
            upload.save(destination)
        else:
            app.logger.info("Files uploaded are not supported...")
        #destination = "/".join([target, filename])
        #app.logger.info("Accept incoming file:", filename)
        #app.logger.info("Save it to:", destination)
        #upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("gallery.html", func='upload', image_name=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    app.logger.info("funccion send_image")
    app.logger.info(filename)
    #filename = filename.replace(" ","_")
    #filename = filename.replace("'","_")
    #app.logger.info(filename)
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename)
    except FileNotFoundError:
        abort(404)


@app.route('/gallery')
def get_gallery():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    app.logger.info("funccion get_gallery")
    print(APP_ROOT)
    print(os.path)
    print(os.listdir(APP_ROOT + '/static/images/gallery'))

    image_names = os.listdir(APP_ROOT + '/static/images/gallery')
    return render_template('gallery.html', titulo="Gallery Page", func='gallery', image_names=image_names)


@app.route('/add_gallery', methods=['POST'])
def add_gallery():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    app.logger.info("funccion add_gallery")
    if request.method == 'POST':
        action = request.form['btn']
        print(action)
        data = request.form.to_dict()
        print(data)
    if action == 'cancel':
        # destination = 'static/images/gallery' + filename
        # print(destination)
        # os.remove(destination)
        print('borrar el archivo')
    else:
        app.logger.info("funccion add_gallery boton ok")
        app.logger.info("Guardar el archivo")
        image_names = os.listdir(APP_ROOT + '/static/images/gallery')
    return render_template('gallery.html', titulo="Gallery Page", func='gallery', image_names=image_names)


@app.route('/form2', methods=['GET', 'POST'])
def form2():
    return render_template('form2.html')


@app.route('/form1', methods=['GET', 'POST'])
def form1():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    if request.method == "GET":
        return render_template('form1.html')
    elif request.method == "POST":
        data = request.form.to_dict()
        print(data)
        return render_template('signup.html', display="formulario recibido", data=data)
    else:
        return render_template('form1.html')


@app.route('/menuqr', methods=['GET', 'POST'])
def menuqr():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    results = []
    con = get_database_connection()
    cursor = con.cursor()
    cursor.execute('select * from product order by ordercat , idcat ')
    data = cursor.fetchall()
    #app.logger.info(data)
    registros = []
    columnas = [d[0] for d in cursor.description]
    # transformar los registros en un diccionario
    for fila in data:
        registro = dict(zip(columnas, fila))
        registros.append(registro)
    app.logger.info(' menuQR registros #################################')
    #app.logger.info(registros)
    #app.logger.info('registros #################################')
     # Nombre del archivo CSV de salida
    archivo_csv = 'tabla.csv'
    """
    # Crea el archivo CSV y escribe los datos 
    with open(APP_ROOT + '/static/csv/tabalproduct.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Escribe el encabezado
        csv_writer.writerow([i[0] for i in cursor.description])
        # Escribe los datos
        csv_writer.writerows(data)
    """
    con.close()
    
    #app.logger.info(diccionario_registros)
    
    #leer el archivo csv
    """with open(APP_ROOT + '/static/csv/tabalproduct.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        print(csv_reader)
        for row in csv_reader:
            results.append(dict(row))
    app.logger.info(results)
    """
    # Carte; Ordre; Categories; titre; description; prix
    # Carte; cat; Ordre; Categories; titre; description; prix
    
    return render_template('menuqr.html', resultados=registros)


@app.route('/menuboissons', methods=['GET', 'POST'])
def menuboissons():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    results = []

    with open(APP_ROOT + '/static/csv/carteboissons.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            results.append(dict(row))

    # Carte; Ordre; Categories;titre; description;prix
    # Carte;ordre;cat;subcat;description;prix

    return render_template('menuboissons.html', resultados=results)


@app.route('/auberge')
def auberge():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    return render_template("voy.html")


@app.route('/csvimport', methods=['GET', 'POST'])
def csvimport():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    cSv : bool = False
    if request.method == 'GET':
        return render_template('csvimport.html', cSv=False)
    elif request.method == 'POST':
        results = []
        choisi = 'nada'
        data = request.form.to_dict()
        print(data)
        delimiteur = request.form['delimiter']
        # namefile = request.form['file']
        if data['btn'] == 'guardar':
            a = data['user_csv']
            carte = data['select']
            archivo = open(APP_ROOT + '/static/csv/carte' + carte + '.csv', "w")

            archivo.write(str((a)))
            archivo.close()
            choisi = carte
            carte = 'carte' if carte == 'autre' else carte
            data['btn'] = carte

        if data['btn'] == 'upload':
            print(data)
            print(request.files.getlist("file"))
            msg=""
            for upload in request.files.getlist("file"):
                print(upload)
                print("{} is the file name".format(upload.filename))
                filename = upload.filename
                # This is to verify files are supported
                ext = os.path.splitext(filename)[1]
                if (ext == ".jpg") or (ext == ".png") or (ext == ".jpeg"):
                    target = app.config["CLIENT_IMAGES"]
                    msg += "Fichier sauver dans Gallery: " + filename + '\r\n'
                    print("File image supported ")
                elif (ext == ".txt") or (ext == ".csv"):
                    target = app.config["CLIENT_CSV"]
                    msg += "Fichier sauver dans CSV : " + filename + '\r\n'
                    print("File CSV supported ")

                else:
                    print("Files uploaded are not supported...")
                    msg += "Fichier non supporter : " + filename + '\r\n'
                    return render_template('csvimport.html', cSv=False, msg=msg, )

                destination = "/".join([target, filename])
                filename.strip()
                print("Accept incoming file:", filename)
                print("Save it to:", destination)
                try:
                    upload.save(destination)
                except IOError:
                    msg += "Image could not be uploaded \r\n"
            return render_template('csvimport.html', cSv=False, msg=msg,)

        if data['btn'] == 'carte':
            with open(APP_ROOT + '/static/csv/cartecarte.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=';')
                line_count = 0
                for row in csv_reader:
                    results.append(dict(row))

                fieldnames = [key for key in results[0].keys()]
            choisi = 'carte'

        if data['btn'] == 'boissons':
            with open(APP_ROOT + '/static/csv/carteboissons.csv') as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=';')
                line_count = 0
                for row in csv_reader:
                    results.append(dict(row))

                fieldnames = [key for key in results[0].keys()]
            choisi = 'boissons'

        if data['btn'] == 'render':
            user_csv = request.form.get('user_csv').split('\n')
            reader = csv.DictReader(user_csv, delimiter=delimiteur)

            for row in reader:
                results.append(dict(row))

            fieldnames = [key for key in results[0].keys()]

        return render_template('csvimport.html', cSv=True, results=results, fieldnames=fieldnames, len=len, choisi=choisi)


@app.errorhandler(404)
def page_not_found(error):
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    return render_template('page_not_found.html'), 404


#if __name__ == '__main__':
#    app.run(debug=True)
