from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import check_password_hash, generate_password_hash
#from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
import os
import logging 
import inspect

app = Flask(__name__)
 
SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^'
PWD = os.path.abspath(os.curdir)	
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/db.db'.format(PWD)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///db.db'.format(PWD)
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy(app)

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

# Flask Login 
# login_manager = LoginManager()
# login_manager.init_app(app)

# Definición de la tabla User
class Product(db.Model):   #"id","idcat","titre","description","prix","image","categorie"
    __tablename__ = 'product'
    id          = db.Column(db.Integer, primary_key=True)
    idcat       = db.Column(db.Integer)
    titre       = db.Column(db.String(124), nullable=False)
    descripcion = db.Column(db.String(256),  )
    prix        = db.Column(db.Numeric, nullable=False)
    image       = db.Column(db.String(128))
    categorie   = db.Column(db.String(128), nullable=False)
        
    def __init__(self,  titre,  prix, categorie):
        self.titre = titre
        self.prix = prix
        self.categorie = categorie
        
    
    # def __repr__(self):
    #     return f'<Plat {self.titre}>'
    
    # def save(self):
    #     if not self.id:
    #         db.session.add(self)
    #     db.session.commit()
        
    # @staticmethod
    # def get_by_id(id):
    #     return Product.query.get(id)
    # @staticmethod
    # def get_by_categorie(categorie):
    #     return Product.query.filter_by(categorie=categorie).all()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __init__(self, name, email, password):
        self.email = email
        self.password = generate_password_hash(password)
    
    # def __repr__(self):
    #     return f'<User {self.email}>'
    
    # @staticmethod
    # def set_password(self, password):
    #     self.password = generate_password_hash(password)
    
    # @staticmethod
    # def check_password(self, password):
    #     return check_password_hash(self.password, password,)
    
    # def save(self):
    #     if not self.id:
    #         db.session.add(self)
    #     db.session.commit()
    
    # @staticmethod
    # def get_by_id(id):
    #     return User.query.get(id)
    
    # @staticmethod
    # def get_by_email(email):
    #     return User.query.filter_by(email=email).first()
    
    # @staticmethod
    # def get_by_name(name):
    #     return User.query.filter_by(name=name).first()

#@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    
    if request.method == 'POST':
        name = request.form['username']
        app.logger.info(name)
        password = request.form['password']
        app.logger.info(password)
        user = User.query.filter_by(name=name).first()
        #user = User.get_by_id(2)
        app.logger.info(user)
        if user and user.password == password:
            app.logger.info("entre en el doble if de name y passw")
            app.logger.info(user.password)
            #login_user(user)
            return render_template('signup.html', display="formulario recibido", data=name,ok='True')
        else:
            return render_template('signup.html', display="formulario recibido", data=name,ok='False')
    return render_template('home.html')


@app.route('/logout')
#login_required
def logout():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    #logout_user()
    return 'You have been logged out.'

@app.route('/products')
#@login_required
def products():
    user_id = current_user.id
    user_products = Product.query.filter_by(user_id=user_id).all()
    return render_template('products.html', products=user_products)


@app.route('/')
def home():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    #return "Bienvenue"
    return render_template("home.html", titulo="Bienvenue")

@app.route('/about')
def about():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    titulo: str = "About Page"
    return render_template('about.html', titulo="Le mot du chef", bg_image="modif-2.jpeg")


@app.route('/location')
def locate():
    nombre_funcion = inspect.currentframe().f_code.co_name
    app.logger.info(nombre_funcion)
    return render_template("location.html", titulo="Bienvenue")


# db.create_all()
# user1 = User(1, "Auberge", "aubergerefleurie@thierry.work", "NoNo", -1)
# db.session.add(user1) # Agregar objeto a la solicitud
# db.session.commit()
# app.logger.info(user1)
# user2 = User(1, "thierry", "thierrye@thierry.work", "1234", -1)
# db.session.add(user2) # Agregar objeto a la solicitud
# db.session.commit()
# app.logger.info(user2)



if __name__ == '__main__':
    db.create_all()
    user1 = User(1, "Auberge", "aubergerefleurie@thierry.work", "NoNo", -1)
    db.session.add(user1) # Agregar objeto a la solicitud
    db.session.commit()
    app.logger.info(user1)
    user2 = User(1, "thierry", "thierrye@thierry.work", "1234", -1)
    db.session.add(user2) # Agregar objeto a la solicitud
    db.session.commit()
    app.logger.info(user2)
    app.run(debug=True)