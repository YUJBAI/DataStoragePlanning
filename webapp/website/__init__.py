from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from datetime import date, timedelta, datetime

import numpy as np
import pandas as pd



db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    basedir = path.abspath(path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(basedir, 'database.db')
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    app.jinja_env.globals.update(calculate_accmult = calculate_accmult)
    app.jinja_env.globals.update(calculate_cost = calculate_cost)

    from .models import User, History

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def isFloat(num):
    """
    A function to check whether a string is a float or not.

    PARAMETERS
    ----------
        num : Str
            String of input.
    RETURNS
    -------
        Bool
            if string is a number, return True else False.

    Creator : Gilbert Putra, harlimgilbert@gmail.com
    """
    try:
        float(num)
        return True
    except ValueError:
        return False

def calculate_accmult(storage_type, years = 10):
    """
    A function to calculate accumulation multiplier based on storage type.

    PARAMETERS
    ----------
        storage_type : Str
            There are only two types; Bought and Rental.
        
        years : int
            Number of years expected to accumulate over. Default is 10.
    
    RETURNS
    -------
        int
            if storage type is bought return years else accumulate the years.
    
    Creator : Gilbert Putra, harlimgilbert@gmail.com
    """
    if storage_type == "Bought":
        return years
    elif storage_type == "Rental":
        return sum(np.arange(0, years+1))

def calculate_cost(datagenerated, storage_price, storage_type, months):
    """
    A function to calculate the storage cost.

    PARAMETERS
    ----------
        datagenerated : Float
            The amount of data generated per day.
        
        storage_price : Float
            The price of storage in GB/Month AUD.

        storage_type : Str
            The type of the storage. Rental or Bought.
        
        months : int
            The number of months expected to accumulate.

    RETURNS
    -------
        float
            The total cost of the storage after accumulation respective to each type.

    Creator : Gilbert Putra, harlimgilbert@gmail.com
    """
    return datagenerated * 365 * storage_price * 12 * calculate_accmult(storage_type, years = months)

def add_storage(data, start_date, data_generated_per_year):
    """
    A function to add storage generation per year from the usual data growth.

    PARAMETERS
    ----------
        data : List 
            List of List of data generation before additional storage starting 
            from today.

        start_date : Str
            Starting date of the additional storage. Format: "%d/%m/%Y".

        data_generated_per_year : Float
            The amount of data generated per year.

    RETURNS
    -------
        List
            List of List of data generation after additional storage.

    Creator : Gilbert Putra, harlimgilbert@gmail.com
    """
    start_date = datetime.strptime(start_date, "%d/%m/%Y").date()
    tmp_list = []
    i = 0
 
    for x in range(len(data) - 1):
        curr = data[x]
        after = data[x+1]
        
        curr_date = start_date + timedelta(days=365*i)
        
        tmp_list.append([curr[0], curr[1], 400, "o"])
        if curr[0] < curr_date and after[0] > curr_date:
            tmp_list.append([curr_date, "", data_generated_per_year, "a"])
            i += 1
            
    tmp_list.append([data[-1][0], data[-1][1], 400, "o"])   
    #if data[-1][0] < start_date + timedelta(days=365*i):
    #    tmp_list.append([start_date + timedelta(days=365*i), "", data_generated_per_year, "a"])

    tmp_df = pd.DataFrame(tmp_list, columns = ['date', '1', '2', '3']).sort_values(by = "date").values.tolist()
  
    return tmp_df

def data_correction(data):
    """
    A function to correct the data formatting.
    
    PARAMETERS
    ----------
        data : List
            List of List of data generation after additional storage.
    
    RETURNS
    -------
        tmp : List
            List of List of corrected data.

    Creator : Gilbert Putra, harlimgilbert@gmail.com
    """    
    for i in range(1, len(data)):
        prev_row = data[i - 1]
        curr_row = data[i]
        
        if prev_row[1] != '' and curr_row[1] != prev_row[1] + curr_row[2]:
            curr_row[1] = prev_row[1] + curr_row[2]
    
    tmp = [[data[0][0], data[0][1]]]
    for i in range(1, len(data)):
        prev_row = data[i - 1]
        curr_row = data[i]
        
        if curr_row[3] == 'a':
            tmp.append([curr_row[0], prev_row[1]])
            tmp.append([curr_row[0], curr_row[1]])
        elif curr_row[3] == 'o':
            tmp.append([curr_row[0], curr_row[1]])
        
    return tmp

def generate_graph_data(start_date, data_generated_per_year, year = 5, initial_data_size = 600, gradient = 400):
    """
    A function to pipeline additional storage from user input, creating before and after data.

    PARAMETERS
    ----------
        start_date : Str
            Starting date of the additional storage. Format: "%d/%m/%Y".

        data_generated_per_year : Float
            The amount of data generated per year.
        
        year : int
            The amount year to visualise. Default is 5.

        initial_data_size : Float
            The initial amount of allocated disk storage. Default is 600.
        
        gradient : Float
            The expected growth of initial data size. Default is 400.

    RETURNS
    -------
        data : List
            List of dictionary of data generation before additional storage starting 
            from today.

        after_data : List 
            List of dictionary of data generation after additional storage starting 
            from today.

    Creator : Gilbert Putra, harlimgilbert@gmail.com
    """
    data = [[(date.today() + timedelta(days=365 * i)), initial_data_size + gradient*i] for i in range(year + 1)]
    #data = [[(date.today() + timedelta(days=365 * i)), initial_data_size*i] for i in range(year + 1)]

    after_data = add_storage(data, start_date, data_generated_per_year)
    after_data = data_correction(after_data)
    
    for row in data:
        row[0] = row[0].strftime("%Y-%m-%d")
    for row in after_data:
        row[0] = row[0].strftime("%Y-%m-%d")
    
    data = [{'x': row[0], 'y': row[1]} for row in data]
    after_data = [{'x': row[0], 'y': row[1]} for row in after_data]
    
    return data, after_data

def check_date(date_string, format = "%d/%m/%Y"):
    """
    A function to check date format and if date given happens after today.

    PARAMETERS
    ----------
        date_string : Str
            String of date.
        
        format : Str
            String Format. Default is "%d/%m/%Y".

    RETURNS
    -------
        Bool
            Return True if date_string satisfies the format and happens
            after today. Else return False.

    Creator : Gilbert Putra, harlimgilbert@gmail.com
    """
    try:
        now = datetime.strptime(date_string, format).date()
        if date.today() < now:
            return True
        else:
            return False
    except ValueError:
        #raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        return False
