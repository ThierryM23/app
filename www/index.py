from flask import Flask, render_template, request, send_from_directory, redirect, url_for, safe_join, abort
from datetime import datetime
import os
import csv
from werkzeug.utils import secure_filename

# import psycopg2


__author__ = "ThierryM23"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite: ///src/webdata.db' # ruta absoluta
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# The absolute path of the directory containing images for users to download
app.config["CLIENT_IMAGES"] = APP_ROOT + "/static/images/gallery"
# The absolute path of the directory containing CSV files for users to download
app.config["CLIENT_CSV"] = APP_ROOT + "/static/csv"
# The absolute path of the directory containing PDF files for users to download
app.config["CLIENT_PDF"] = APP_ROOT + "/static/pdf"

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

CONNECTED = False
USERNAME = 'Guest'
listuser = ['thierry', 'NONO']


#
# # global constant DB
# PSQL_HOST = 'localhost'
# PSQL_PORT = '5432'
# PSQL_USER = 'postgres'
# PSQL_PASS = 'root'
# PSQL_DB = 'pruebas'
#
# # connection
# conn_string = "host="+ PSQL_HOST +" port="+ PSQL_PORT +" dbname="+ PSQL_DB +" user=" + PSQL_USER \
# +" password="+ PSQL_PASS
# conn = psycopg2.connect(conn_string)
# cursor = conn.cursor()
#
# # Query
# SQL = "SELECT id, usuario, pass, email, fecha FROM usuarios;"
# cursor.execute(SQL)
# # get values
# all_values = cursor.fetchall()
# cursor.close()
# conn.close()
# print('get values: ', all_values)
#


# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)
#
#     def __init__(self, name, email):
#         self.name = name
#         self.email = email
#
#     def __repr__(self):
#         return '<User %r>' % self.name
#
#
# # Crear tabla, insertar datos
# @app.before_first_request
# def create_db():
#     # Recreate database each time for demo
#     # db.drop_all()
#     db.create_all()
#     admin = User('admin', 'admin@example.com')
#     db.session.add(admin)
#     guestes = [User('guest1', 'guest1@example.com'),
#                User('guest2', 'guest2@example.com'),
#                User('guest3', 'guest3@example.com'),
#                User('guest4', 'guest4@example.com')]
#     db.session.add_all(guestes)
#     db.session.commit()
#
#
# # Consultar
# @app.route('/user')
# def users():
#     users = User.query.all()
#     return "<br>".join(["{0}: {1}".format(user.name, user.email) for user in users])
# # Consultar
# @app.route('/user/<int:id>')
# def user(id):
#     user = User.query.filter_by(id=id).one()
#     return "{0}: {1}".format(user.name, user.email)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def home():
    return render_template("home.html", titulo="Home Page", name="Thierry")


@app.route('/about')
def about():
    titulo: str = "About Page"
    return render_template('about.html', titulo="About Page")


@app.route('/search', methods=['GET', 'POST'])
def search():
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
    if request.method == "GET":
        # Obtenemos la información del parametro "nombreUser"
        # Esto lo hacemos con "request.args.get"
        # nombreUser = request.args.get('nombreUser')
        return render_template('signup.html')
    elif request.method == "POST":
        # Obtenemos la información del parametro "nombreUser"
        # Esto lo hacemos con el diccionario "form"
        # nombreUser = request.form['nombreUser'] o crear un dict con form.to_dict
        data = request.form.to_dict()
        print(data)
        print(data['username'])
        print(data['password'])
        return render_template('signup.html', display="formulario recibido", data=data)
    else:
        return "metodo no aceptable"


@app.route('/upload', methods=['POST'])
def upload():
    target = app.config["CLIENT_IMAGES"]
    print(target)
    # if not os.path.isdir(target):
    #         os.mkdir(target)
    # else:
    #     print("Couldn't create upload directory: {}".format(target))
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png"):
            print("File supported moving on...")
        else:
            print("Files uploaded are not supported...")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("gallery.html", func='upload', image_name=filename)


@app.route('/upload/<filename>')
def send_image(filename):
    print(filename)
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename)
    except FileNotFoundError:
        abort(404)


@app.route('/gallery')
def get_gallery():
    print(APP_ROOT)
    print(os.path)
    print(os.listdir(APP_ROOT + '/static/images/gallery'))

    image_names = os.listdir(APP_ROOT + '/static/images/gallery')
    return render_template('gallery.html', titulo="Gallery Page", func='gallery', image_names=image_names)


@app.route('/add_gallery', methods=['POST'])
def add_gallery():
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
        print('Guardar el archivo')
    image_names = os.listdir('src/static/images/gallery')
    return render_template('gallery.html', titulo="Gallery Page", func='gallery', image_names=image_names)


@app.route('/form1', methods=['GET', 'POST'])
def form1():
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
    results = []

    with open(APP_ROOT + '/static/csv/carteSaison.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            results.append(dict(row))

    # Carte; Ordre; Categories;titre; description;prix

    return render_template('menuqr.html', resultados=results)


@app.route('/menuboissons', methods=['GET', 'POST'])
def menuboissons():
    results = []

    with open(APP_ROOT + '/static/csv/carteboissons.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            results.append(dict(row))

    # Carte; Ordre; Categories;titre; description;prix

    return render_template('menuboissons.html', resultados=results)


@app.route('/carte')
def carte():
    return render_template("carte.html", titulo="carte Page", name="Thierry")


@app.route('/auberge')
def auberge():
    return render_template("voy.html")


@app.route('/csvimport', methods=['GET', 'POST'])
def csvimport():
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
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
