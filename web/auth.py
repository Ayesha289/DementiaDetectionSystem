from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS, cross_origin

from . import db, mail
from .models import User
from .email import forget_pass_email

auth = Blueprint('auth', __name__)
CORS(auth, resources={r"/*": {"origins": "*"}})

@auth.route('/login', methods=['GET', 'POST'])
@cross_origin(allow_headers=['Content-Type'])
def login():
    if request.method == 'POST':
        try:
            if request.args.get("f") == "f2":
                email = request.form.get('email')
                password = request.form.get('password')

                user = User.query.filter_by(email=email).first()
                if user:
                    if check_password_hash(user.password, password):
                        login_user(user, remember=True)
                        return redirect(url_for('views.home'))
                        # return jsonify("Successfully Logged In")
                    else:
                        flash('Invalid credentials!', 'warning')
                elif not user:
                    flash('Invalid credentials!', 'warning')
            
            elif request.args.get("f") == "f1":
                email = request.form.get('email')
                firstName = request.form.get('fname')
                pass1 = request.form.get('password1')
                pass2 = request.form.get('password2')

                user = User.query.filter_by(email=email).first()
                if user:
                    flash('Email Already Exists!', 'warning')
                elif len(email) < 4:
                    flash('Email is invalid!', 'warning')
                elif len(firstName) < 2:
                    flash('First Name must be greater than 1 character!', 'warning')
                elif pass1 != pass2:
                    flash('Passwords not matching!')
                elif len(pass1) < 7:
                    flash('Password must be atleast 6 characters long!', 'warning')
                else:
                    #add user to database
                    new_user = User(email=email, first_name=firstName, password=generate_password_hash(pass1, method='pbkdf2:sha256', salt_length=16))
                    db.session.add(new_user)
                    db.session.commit()
                    login_user(new_user, remember=True)
                    return redirect(url_for('views.home'))
                
            elif request.args.get("f") == "f3":
                email = request.form.get('email')
                user = User.query.filter_by(email=email).first()
                if user:
                    flash('Check your email for password reset instructions!', 'success')
                    forget_pass_email(user)

                else:
                    flash('Enter a valid email!', 'warning')
        except Exception as e:
            return render_template('error.html')

    return render_template("login.html", user=current_user)

@auth.route('/logout', methods=['GET'])
@cross_origin()
@login_required
def logout():
    if request.method == 'GET':
        try:
            logout_user()
            return redirect(url_for('auth.login'))
        except Exception as e:
            return render_template('error.html')
    
@auth.route('/password_reset_verified/<token>', methods=['GET', 'POST'])
@cross_origin()
def reset_verified(token):
    try:
        user = User.verify_reset_token(token)
        if not user:
            print('no user found')
            return redirect(url_for('auth.login'))
        password = request.form.get('password')
        if password:
            user.set_password(password, commit=True)
            return redirect(url_for('auth.login'))
        return render_template('passwordReset.html')
    except Exception as e:
        return render_template('error.html')
