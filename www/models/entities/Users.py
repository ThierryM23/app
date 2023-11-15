from werkzeug.security import check_password_hash, generate_password_hash
#from flask_login import UserMixin


class User():
    
    def __init__(self, id, name, email, password, is_admin) -> None:
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.is_admin = is_admin
    
    def __repr__(self):
        return f'<User {self.name}>'
    @classmethod
    def set_password(self, password):
        self.password = generate_password_hash(password)
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    
    
    #print(generate_password_hash("NoNo"))
    """
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