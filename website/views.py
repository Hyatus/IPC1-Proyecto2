# Contiene todo lo relacionado con el blog como el home page, etc...
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
#Importamos la clase Post
from .models import Post, User
from . import db

# Importamos las librerías que nos serviran para mostrar las páginas que solamente aparecen si hay una sesión iniciada


views = Blueprint("views",__name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)

@views.route("/new-post", methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == "POST":

       tipo = request.form.get('tipo')
       url = request.form.get('url')
       category = request.form.get('category')
       post = Post(tipo=tipo,url=url,category=category,author=current_user.id)
       #Añadimos el nuevo post relacionado con el user id a la tabla
       db.session.add(post)
       db.session.commit()
       flash('Publicación agregada con éxito!', category='success')
       return redirect(url_for('views.home'))

    return render_template('newpost.html', user=current_user)




