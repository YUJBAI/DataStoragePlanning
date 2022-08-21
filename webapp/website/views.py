from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user

from .models import History, Storage
from . import *

import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    #bef_data = None
    #aft_data = None
    INPUTFORMAT = False
    if request.method == 'POST':
        instrument = request.form.get("instrument")
        dataGenerated = request.form.get('dataGenerated')
        price = request.form.get('price')
        lifetime = request.form.get('lifetime')
        startDate = request.form.get('startDate')
        initialSize = request.form.get('initialSize')

        if instrument == "":
            flash("Please fill in the Instrument's name!", category='error')
        elif dataGenerated == "":
            flash("Please fill in the Data Generated Per Year!", category= "error")
        elif not isFloat(dataGenerated):
            flash("Please make sure Data Generated Per Year is a number!", category= "error")
        elif price == "" or not isFloat(price):
            flash("Please fill in the Instrument's Price!", category= "error")
        elif not isFloat(price):
            flash("Please make sure Instrument's Price is a number!", category= "error")
        elif lifetime == "" or not isFloat(lifetime):
            flash("Please fill in the Expected Lifetime!", category= "error")
        elif not isFloat(lifetime):
            flash("Please make sure the Expected Lifetime is a number!", category= "error")
        elif startDate == "":
            flash("Please fill in the Start Date!", category= "error")
        elif not check_date(startDate):
            flash("Please make sure Start Date is in the correct format and is in the future!", category= "error")
        elif initialSize == "":
            flash("Please fill in the Initial Data Size!", category= "error")
        elif not isFloat(initialSize):
            flash("Please make sure Initial Data Size is a number!", category= "error")
        else:
            INPUTFORMAT = True
            new_history = History(name = instrument, 
                            data_generated = float(dataGenerated), 
                            price = float(price),
                            lifetime = float(lifetime),
                            start_date = startDate,
                            initial_size = float(initialSize),
                            user_id=current_user.id)
            db.session.add(new_history)
            db.session.commit()
            print(new_history)
            flash('Done Calculating!', category='success')

    if current_user.histories:
        input_user = current_user.histories[-1]
        bef_data, aft_data = generate_graph_data(start_date = input_user.start_date, 
                                    data_generated_per_year = input_user.data_generated * 365, 
                                    year = 5,
                                    initial_data_size = input_user.initial_size,
                                    gradient = input_user.initial_size * 1 / 3)
    else:
        bef_data = aft_data = None

    if INPUTFORMAT:
        return render_template("home.html", user=current_user, before = bef_data, after = aft_data)
    else:
        return render_template("home.html", user=current_user, before=bef_data, after=aft_data, form=request.form)

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
    print(history_id)
    input_user = History.query.filter_by(id=history_id).first()
    print(History)
    if input_user:
        #input_user = current_user.histories[-1]

        print(input_user)
        bef_data, aft_data = generate_graph_data(start_date = input_user.start_date,
                                    data_generated_per_year = input_user.data_generated * 365,
                                    year = 5,
                                    initial_data_size = input_user.initial_size,
                                    gradient = input_user.initial_size * 1 / 3)
    else:
        history_id=0
        bef_data = aft_data = None
    # print(type(history_id))
    # print(input_user.id)
    return render_template("view_history.html", user=current_user, before = bef_data, after = aft_data, history_id=input_user.id)



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
