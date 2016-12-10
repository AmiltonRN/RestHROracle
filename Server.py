#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 17:08:37 2016

@author: amilton
"""
import json
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy as SQL
from sqlalchemy.ext.declarative import DeclarativeMeta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'oracle://hr:hr@192.168.10.3:1521/XE'
db = SQL(app)

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != 'query' and x != 'query_class']:
                data = obj.__getattribute__(field)
                try:
                    if data != None:
                        if isinstance(data, datetime.datetime):
                            json.dumps(data.strftime('%Y-%m-%dT%H:%M:%SZ'))
                            fields[field] = data.strftime('%Y-%m-%dT%H:%M:%SZ')
                        elif isinstance(data, datetime.date):
                            json.dumps(data.strftime('%Y-%m-%d'))
                            fields[field] = data.strftime('%Y-%m-%d')
                        else:
                            json.dumps(data)
                            fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
    
        return json.JSONEncoder.default(self, obj)
        
        
class Employees (db.Model):
    id = db.Column('EMPLOYEE_ID', db.Integer, primary_key=True)
    first_name = db.Column('FIRST_NAME', db.String(20))
    last_name = db.Column('LAST_NAME', db.String(25))
    email = db.Column('EMAIL', db.String(25))
    phone_number = db.Column('PHONE_NUMBER', db.String(20))
    hire_date = db.Column('HIRE_DATE', db.Date)
    job_id = db.Column('JOB_ID', db.String(10))
    salary = db.Column('SALARY', db.Float)
    commission_pct = db.Column('COMMISSION_PCT', db.Float)
    manager_id = db.Column('MANAGER_ID', db.Integer)
    department_id = db.Column('DEPARTMENT_ID', db.Integer)
    

    def __init__(self, id, first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.hire_date = hire_date
        self.job_id = job_id
        self.salary = salary
        self.commission_pct = commission_pct
        self.manager_id = manager_id
        self.department_id = department_id

        
@app.route('/employees', methods=['GET'])
def function_employees():
    return json.dumps(db.session.query(Employees).all(), cls=AlchemyEncoder)
    
    
if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')