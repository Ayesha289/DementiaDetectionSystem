from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user, logout_user
from flask_cors import CORS, cross_origin
from .models import MedHistory, User
from . import db
import pickle
import numpy as np

views =  Blueprint('views', __name__)
CORS(views, resources={r"/*": {"origins": "*"}})
model = pickle.load( open('web/model.pkl','rb'))

@views.route('/')
@cross_origin()
def home():
    try:
        return render_template('home.html', user=current_user)
    except Exception as e:
        return render_template('error.html')

@views.route('/connect')
@cross_origin()
def login():
    try:
        return render_template('login.html')
    except Exception as e:
        return render_template('error.html')

@views.route('/result')
@cross_origin()
@login_required
def result():
    try: 
        return render_template('result.html')
    except Exception as e:
        return render_template('error.html')

@views.route('/history')
@cross_origin()
@login_required
def history():
    try: 
        return render_template('history.html')
    except Exception as e:
        return render_template('error.html')

@views.route('/error')
@cross_origin()
def error():
    return render_template('error.html', user=current_user)

@views.route('/form', methods=['GET', 'POST'])
@cross_origin(allow_headers=['Content-Type'])
@login_required
def form():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            visit = request.form.get('visit')
            mrDelay = request.form.get('mrDelay')
            gender = request.form.get('gender')
            if gender == 'm' or gender == 'M':
                gender = 0
            elif gender == 'f' or gender == 'F':
                gender = 1
            age = request.form.get('age')
            edu = request.form.get('edu')
            ses = request.form.get('ses')
            ses = float(ses)
            mmse = request.form.get('mmse')
            mmse = float(mmse)
            cdr = request.form.get('cdr')
            cdr = float(cdr)
            etiv = request.form.get('etiv')
            nwbv = request.form.get('nwbv')
            nwbv = float(nwbv)
            asf = request.form.get('asf')
            asf = float(asf)

            features = np.array([[visit, mrDelay, gender, age, edu, ses, mmse, cdr, etiv, nwbv, asf]])
            predict = model.predict(features)
            if predict == 0:
                result = 'Dementia Detected'
            elif predict == 1:
                result = 'Possibility of Dementia'
            else:
                result = 'No dementia detected'

            new_record = MedHistory(name = name, visit = visit, mr_delay = mrDelay, gender = gender, age = age, edu = edu, ses = ses, mmse = mmse, cdr = cdr, etiv = etiv, nwbv = nwbv, asf = asf, result = result, user_id=current_user.id)
            db.session.add(new_record)
            db.session.commit()
            return render_template('result.html', predict=predict)
        except Exception as e:
            return render_template('error.html')
    else:
        return render_template('form.html')
    
@views.route('/getData', methods=['GET'])
@cross_origin()
@login_required
def getData():
    if request.method == 'GET':
        try:
            admin = 0
            login_id = current_user.id
            if (current_user.first_name == 'admin'):
                admin = 1
            data = MedHistory.query.filter_by(user_id=login_id).all()
            info = [{'id': med.id, 'name': med.name, 'result': med.result} for med in data]
            if admin:
                info = [{'id': med.id, 'name': med.name, 'visit': med.visit, 'mrDelay':  med.mr_delay, 'gender': med.gender, 'age': med.age, 'edu':med.edu, 'ses': med.ses, 'mmse': med.mmse, 'cdr': med.cdr, 'etiv': med.etiv, 'nwbv': med.nwbv, 'asf': med.asf, 'result': med.result } for med in data]
            if data:
                data_exists = 1
                return render_template('history.html', history=info, data_exists=data_exists,  admin=admin)
            else:
                data_exists = 0
                return render_template('history.html', data_exists=data_exists)
        except Exception as e:
            return render_template('error.html')