# Contiene todo lo relacionado con autenticación y login
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user


auth = Blueprint("auth",__name__)


@auth.route("/login", methods=['GET','POST'])
def login():
     if request.method == 'POST':
         username = request.form.get("username")
         password = request.form.get("password")
           
        # Buscamos al usuario si este existe y que nos devuelva el objeto
         user = User.query.filter_by(username=username).first()
         #Comparamos la contraseña para ver si es correcta
         if user: 
           if user.password == password:
             flash("Sesión iniciada", category="success")
             #Verificamos si la sesión está iniciada
             login_user(user,remember=True)
             return redirect(url_for('views.home'))
           else:
             flash("contraseña incorrecta! ", category="error")  
         else:
             flash("Usuario no existe!", category="error")

     return render_template("login.html", user=current_user)


@auth.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST': 
       name = request.form.get("name")
       gender = request.form.get("gender")
       username = request.form.get("username")
       email = request.form.get("email")
       password = request.form.get("password")

       #Buscamos que el username no exista 
       #Si hay algún resultado no se puede agregar el usuario
       username_exists = User.query.filter_by(username=username).first()
       #Buscamos que el correo tampoco exista
       email_exists = User.query.filter_by(email=email).first()
       # Buscamos números en la cadena 
       contiene_numero = any(chr.isdigit() for chr in password)

       if username_exists:
           #Si el usuario existe enviamos un mensaje de alerta
           flash('Este nombre de usuario ya existe!', category='error')
       elif email_exists:
           #Si el email ya existe enviamos un mensaje de alerta
            flash('Este correo ya está registrado!', category='error')
       elif not (contiene_numero):
           #Verificamos que el password contenga números
            flash('La contraseña debe contener un número! ', category='error')
       elif not(caracterEspecial(password)):
           #Verificamos que el password contenga un caracter especial
            flash('La contraseña debe contener un caracter especial!', category='error')
       else:
           new_user = User(name=name,gender=gender,username=username,email=email,password=password)
           #Se prepara, un paso previo a agregar
           db.session.add(new_user)
           # Se agrega a la base de datos
           db.session.commit()
           login_user(new_user,remember=True)
           flash('Usuario se ha creado con éxito! ')
           return redirect(url_for('views.home'))

    return render_template("register.html", user=current_user)

@auth.route("/logout")
#Este decorador nos permite que unicamente si hay una sesión iniciada podemos tener acceso
@login_required
def logout():
    logout_user()
    # Hacemos referencia a una función dentro de view, que redirige a la url que está en la función
    return redirect(url_for("views.home"))

@auth.route("/update-profile", methods=['GET','POST'])
@login_required
def update_profile():
    user = User.query.filter_by(id=current_user.id).first()
    
    nombreCompleto = user.name
    username = user.username

    if request.method == 'POST': 
       name = request.form.get("name")
       username = request.form.get("username")
       password = request.form.get("password")
       #Buscamos que el username no exista 
       #Si hay algún resultado no se puede agregar el usuario
       username_exists = User.query.filter_by(username=username).first()
       # Buscamos números en la cadena 
       contiene_numero = any(chr.isdigit() for chr in password)

       if username_exists:
           #Si el usuario existe enviamos un mensaje de alerta
           flash('Este nombre de usuario ya existe!', category='error')
       elif not (contiene_numero):
           #Verificamos que el password contenga números
            flash('La contraseña debe contener un número! ', category='error')
       elif not(caracterEspecial(password)):
           #Verificamos que el password contenga un caracter especial
            flash('La contraseña debe contener un caracter especial!', category='error')
       else:
           user.name = name
           user.username = username
           user.password = password
           # Se agrega a la base de datos
           db.session.commit()
           flash('Usuario se ha modificado con éxito!')
           return redirect(url_for('views.home'))    
        
    return render_template("update.html", user=current_user, nombreCompleto=nombreCompleto,username=username)


@auth.route("/about")
def about():
    return render_template("about.html", user=current_user)


@auth.route("/admin/load", methods=['GET','POST'])
@login_required
def load():
    if request.method == "POST":

        if request.files["publicaciones"]:
            publicaciones = request.files["publicaciones"]
            print(publicaciones)
            return redirect(request.url)

        elif request.files["usuarios"]:
            usuarios = request.files["usuarios"] 
            print(usuarios)   
            return redirect(request.url)


    return render_template("load.html", user=current_user)



def caracterEspecial(test_str):
    import re
    #busca en la cadena si hay valores a-z o 0-9
    pattern = r'[^\.a-z0-9A-Z]'
    if re.search(pattern, test_str):
      return True
    else:
       return False

