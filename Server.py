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
        

class Countries(db.Model):
    __tableName__ = 'COUNTRIES'
    id = db.Column('COUNTRY_ID', db.String(2), primary_key=True)
    country_name = db.Column('COUNTRY_NAME', db.String(40))
    region_id = db.Column('REGION_ID', db.Integer)
    
    def __init__(self, id, country_name, region_id):
        self.id = id
        self.country_name = country_name
        self.region_id = region_id
    
    
class Departments(db.Model):
    __tableName__ = 'DEPARTMENTS'
    id = db.Column('DEPARTMENT_ID', db.Integer, primary_key=True)
    department_name = db.Column('DEPARTMENT_NAME', db.String(30))
    manager_id = db.Column('MANAGER_ID', db.Integer)
    location_id = db.Column('LOCATION_ID', db.Integer)
    
    def __init__(self, id, department_name, manager_id, location_id):
        self.id = id
        self.department_name = department_name
        self.manager_id = manager_id
        self.location_id = location_id
    
        
class Employees(db.Model):
    __tableName__ = 'EMPLOYEES'
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

class JobHistory(db.Model):
    __tableName__ = 'JOB_HISTORY'
    id = db.Column('EMPLOYEE_ID', db.Integer, primary_key=True)
    start_date = db.Column('START_DATE', db.DATE, primary_key=True)
    end_date = db.Column('END_DATE', db.Date)
    job_id = db.Column('JOB_ID', db.String(10))
    department_id = db.Column('DEPARTMENT_ID', db.Integer)
    
    def __init__(self, id, start_date, end_date, job_id, department_id):
        self.id = id
        self.start_date = start_date
        self.job_id = job_id
        self.department_id = department_id
    

class Jobs(db.Model):
    __tableName__ = 'JOBS'
    id = db.Column('JOB_ID', db.String(10), primary_key=True)
    job_title = db.Column('JOB_TITLE', db.String(35))
    min_salary = db.Column('MIN_SALARY', db.Float)
    max_salary = db.Column('MAX_SALARY', db.Float)
    
    def __init__(self, id, job_title, min_salary, max_salary):
        self.id = id
        self.job_title = job_title
        self.min_salary = min_salary
        self.max_salary = max_salary
        
class Locations(db.Model):
    __tableName__ = 'LOCATIONS'
    id = db.Column('LOCATION_ID',db.Integer,primary_key=True)
    street_address = db.Column('STREET_ADDRESS', db.String(12))
    postal_code = db.Column('POSTAL_CODE', db.String(35))
    city = db.Column('CITY', db.String(30))
    state_provice = db.Column('STATE_PROVINCE', db.String(25))
    country_id = db.Column('COUNTRY_ID', db.String(2))
    
    def __init__(self, id, street_address, postal_code, city, state_provice, country_id):
        self.id = id
        self.street_address = street_address
        self.postal_code = postal_code
        self.city = city
        self.state_provice = state_provice
        self.country_id = country_id
    

class Regions(db.Model):
    __tableName__ = 'REGIONS'
    id = db.Column('REGION_ID', db.Integer, primary_key=True)
    region_name = db.Column('REGION_NAME',db.String(25))
    
    def __init__(self, id, region_name):
        self.id = id
        self.region_name = region_name
        
        
@app.route('/countries', methods=['GET'])
def function_countries():
    return json.dumps(db.session.query(Countries).all(), cls=AlchemyEncoder)
    

@app.route('/departments', methods=['GET'])
def function_departments():
    return json.dumps(db.session.query(Departments).all(), cls=AlchemyEncoder)
    
    
@app.route('/employees', methods=['GET'])
def function_employees():
    return json.dumps(db.session.query(Employees).all(), cls=AlchemyEncoder)


@app.route('/jobs/history', methods=['GET'])
def function_job_history():
    return json.dumps(db.session.query(JobHistory).all(), cls=AlchemyEncoder)
    
    
@app.route('/jobs', methods=['GET'])
def function_jobs():
    return json.dumps(db.session.query(Jobs).all(), cls=AlchemyEncoder)


@app.route('/locations', methods=['GET'])
def function_locations():
    return json.dumps(db.session.query(Locations).all(), cls=AlchemyEncoder)
    

@app.route('/regions', methods=['GET'])
def function_regions():
    return json.dumps(db.session.query(Regions).all(), cls=AlchemyEncoder)
    
    
if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True, host='0.0.0.0')