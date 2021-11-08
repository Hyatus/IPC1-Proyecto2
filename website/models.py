from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(100))
     gender = db.Column(db.VARCHAR())
     username = db.Column(db.String(100), unique=True)
     email = db.Column(db.String(100), unique=True)
     password = db.Column(db.String(100))
     #Acá hacemos la relación de los Post con los usuarios
     #Se hace referencia a todos los post que el usuario tiene, backref nos devuelve el usuario y hace referencia automáticamente a la clase usuario y nos permite hacer la adición directa de la publicación a éste, passive_delete hace referencia al CASCADE al momento de eliminar a un usuario se borran también las publicaciones 
     post = db.relationship('Post', backref='user', passive_deletes=True )


class Post(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      tipo = db.Column(db.Text, nullable=False) 
      url = db.Column(db.Text, nullable=False) 
      category = db.Column(db.Text, nullable=False) 
      fecha_creacion = db.Column(db.DateTime(timezone=True), default=func.now())
      #Le pasamos el id del usuario para saber quién hizo la publicación
      #Se utiliza como una llave alterna que liga el id de esta base de datos con la de los usuarios
      #CASCADE quiere decir que cuando se elimine el usuario eliminará también todas las publicaciones que este usuario ha hecho
      #nullable no puede ser nulo el valor para poder ser ingresado en la tabla
      author = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)

