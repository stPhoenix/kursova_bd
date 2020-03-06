import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import sqlite3

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def main():
    result = {'error': False, 'message': None, 'data': None}
    try:
        data = {}
        data['f_entity'] = query_db('SELECT count(*) FROM F_Entity', one=True)
        data['f_type'] = query_db('SELECT count(*) FROM F_Type', one=True)
        data['f_maker'] = query_db('SELECT count(*) FROM F_Maker', one=True)
        data['f_material'] = query_db('SELECT count(*) FROM F_Material', one=True)
        data['f_set'] = query_db('SELECT count(*) FROM F_Set', one=True)
        data['f_sales'] = query_db('SELECT count(*) FROM F_Sales', one=True)
        result['data'] = data
    except sqlite3.Error as e:
        result['error'] = True
        result['message'] = e.args[0]
    return render_template('main.html', result=result, c_module='main')

@bp.route('/query', methods=('GET', 'POST'))
def query():
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    if request.method == 'POST':
        try:
            result['data'] = query_db(request.form['query'])
            result['success'] = True
            result['message'] = 'Success'
        
        except sqlite3.Error as e:
            result['error'] = True
            result['message'] = e.args[0]


    return render_template('query.html', result=result, c_module='query')