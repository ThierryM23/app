"""from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from run import db


class User(db.Model, UserMixin):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<User {self.email}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
"""
from index2 import db

class Product(db.Model):   #"id","idcat","titre","description","prix","image","categorie"
    __tablename__ = 'product'
    id          = db.Column(db.Integer, primary_key=True)
    idcat       = db.Column(db.Integer)
    titre       = db.Column(db.String(124), nullable=False)
    descripcion = db.Column(db.String(256),  )
    prix        = db.Column(db.Numeric, nullable=False)
    image       = db.Column(db.String(128))
    categorie   = db.Column(db.String(128), nullable=False)
        
    def __init__(self, idcat, titre, descripcion, prix, image, categorie):
        self.idcat = idcat
        self.titre = titre
        self.descripcion = descripcion
        self.prix = prix
        self.image = image
        self.categorie = categorie
        
    
    def __repr__(self):
        return f'<Plat {self.titre}>'
    
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_by_id(id):
        return Product.query.get(id)
    @staticmethod
    def get_by_categorie(categorie):
        return Product.query.filter_by(categorie=categorie).all()

class User(db.Model, UserMixin):
    __tablename__ = 'blog_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return f'<User {self.email}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_by_id(id):
        return User.query.get(id)
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()