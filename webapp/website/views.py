from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import History, Storage
from . import *

import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        instrument = request.form.get("instrument")
        dataGenerated = request.form.get('dataGenerated')
        price = request.form.get('price')
        lifetime = request.form.get('lifetime')
        startDate = request.form.get('startDate')
        initialSize = request.form.get('initialSize')
        new_history = History(name=instrument,
                              data_generated=float(dataGenerated),
                              price=float(price),
                              lifetime=float(lifetime),
                              start_date=startDate,
                              initial_size=float(initialSize),
                              user_id=current_user.id)
        db.session.add(new_history)
        db.session.commit()
    return jsonify('success')

@views.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'POST':
        name = request.form.get("name")
        price = request.form.get('price')
        type = request.form.get('storageType')
        
        if name == "":
            flash("Please fill storage name!", category='error')
        elif price == "" or not isFloat(price):
            flash("Please fill in the Storage Price!", category= "error")
        elif type == "":
            flash("Please fill in the Accumulation Multiplier!", category= "error")
        else:
            new_storage = Storage(name = name, 
                            price = float(price),
                            type = type,
                            user_id=current_user.id)
            db.session.add(new_storage)
            db.session.commit()
            flash('Storage Added!', category='success')

    return render_template("setting.html", user=current_user)

@views.route('/view-history/<history_id>', methods=['POST','GET'])
def view_history(history_id):
    input_user = History.query.filter_by(id=history_id).first()
    if input_user:
        data_using_linear_model_without_instrument, data_using_linear_model_with_instrument = generate_graph_data(start_date = input_user.start_date,
                                    data_generated_per_year = input_user.data_generated * 365,
                                    year = 5,
                                    initial_data_size = input_user.initial_size,
                                    gradient = input_user.initial_size * 1 / 3)
    else:
        history_id=0
        data_using_linear_model_without_instrument = data_using_linear_model_with_instrument = None
    return render_template("view_history.html", user=current_user, before = data_using_linear_model_without_instrument,
                           after = data_using_linear_model_with_instrument, history_id=input_user.id)



@views.route('/delete-history', methods=['POST'])
def delete_history():
    history = json.loads(request.data)
    historyId = history['historyId']
    history = History.query.get(historyId)
    if history:
        if history.user_id == current_user.id:
            db.session.delete(history)
            db.session.commit()

    return jsonify({})

@views.route('/delete-storage', methods=['POST'])
def delete_storage():
    storage = json.loads(request.data)
    storageId = storage['storageId']
    storage = Storage.query.get(storageId)
    if storage:
        if storage.user_id == current_user.id:
            db.session.delete(storage)
            db.session.commit()

    return jsonify({})

@views.route('/update', methods=['POST','GET'])
def update():
        history_id = request.form['id']
        name = request.form['name']
        data_generated = request.form['data_generated']
        price = request.form['price']
        lifetime = request.form['lifetime']
        start_date = request.form['start_date']
        initial_size = request.form['initial_size']
        history_id = int(history_id)
        History.query.filter_by(id=history_id).update({'name': name, 'data_generated': data_generated, 'price': price,
                                                       'lifetime': lifetime, 'start_date': start_date, 'initial_size': initial_size})
        db.session.commit()
        succuss = 1
        return jsonify(succuss)


@views.route('/modal/<history_id>', methods=['POST','GET'])
def modal(history_id):
    print(history_id)
    input_user = History.query.filter_by(id=history_id).first()
    print(History)
    if input_user:
        bef_data, aft_data = generate_graph_data(start_date=input_user.start_date,
                                                 data_generated_per_year=input_user.data_generated * 365,
                                                 year=5,
                                                 initial_data_size=input_user.initial_size,
                                                 gradient=input_user.initial_size * 1 / 3)
    else:
        history_id = 0
        bef_data = aft_data = None
    return render_template("modal.html", user=current_user, before = bef_data, after = aft_data, history_id=input_user.id)

# @views.route('/delete', methods=['POST'])
# def delete(database, id):
#     storage = json.loads(request.data)
#     storageId = storage['Id']
#     storage = database.query.get(storageId)
#     if storage:
#         if storage.user_id == current_user.id:
#             db.session.delete(storage)
#             db.session.commit()

#     return jsonify({})

