from app import db


# Definir la clase "Product" que representa la tabla de productos
class Product(db.Model):
    __tablename__ = 'product'
    id          = db.Column(db.Integer, primary_key=True)
    idcat       = db.Column(db.Integer, nullable=False)
    titre       = db.Column(db.String(124), nullable=False)
    descripcion = db.Column(db.String(256)  )
    prix        = db.Column(db.Numeric, nullable=False)
    image       = db.Column(db.String(128))
    categorie   = db.Column(db.String(128))
    ordecat     = db.Column(db.Integer)
        
    def __init__(self, idcat, titre,  prix):
        self.idcat = idcat
        self.titre = titre
        self.prix = prix

    # Función para guardar un nuevo producto en la base de datos
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def read(cls, product_id):
        return cls.query.get(product_id)
    
    # Función para leer todos los productos de la base de datos
    @classmethod
    def read_all(cls):
        return cls.query.all()

    # Función para actualizar un producto en la base de datos
    def update(self):
        db.session.commit()

    # Función para borrar un producto de la base de datos
    def delete(self):
        db.session.delete(self)
        db.session.commit()





# # Crear un nuevo producto
# nuevo_producto = Product(name='Producto1', description='Descripción del producto 1')
# nuevo_producto.guardar()

# # Leer un producto por ID
# producto = Product.leer(1)  # Donde 1 es el ID del producto que deseas leer

# # Actualizar un producto
# producto.actualizar(name='Nuevo Nombre', description='Nueva descripción')

# # Borrar un producto
# producto.borrar()
