import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import sqlite3
import flask_excel as excel


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


@bp.route('/download/f_entity', methods=('GET',))
def download():
    data = {}
    data['items'] = query_db('SELECT count(*) FROM F_Entity',one=True)
    data['quantity'] = query_db('SELECT SUM(f_entity_quantity) FROM F_Entity', one=True)
    data['types'] = query_db('SELECT * FROM F_Type')
    data['t_quantity'] = query_db('SELECT f_type_id, count(*) FROM F_Entity GROUP BY f_type_id')

    f_types = {}
    for fid, name in data['types']:
        f_types[fid] = name

    d = [
        ["Рядків одиниць мебелі", data['items'][0]],
        [" "],
        ["Загальна кількість мебелі", data['quantity'][0]],
        [" "],
        ["Назва виду", "Кількість"]
    ]

    for fid, quantity in data['t_quantity']:
        d.append([f_types[fid], quantity])

    return excel.make_response_from_array(d, "xls")


@bp.route('/download/f_sales', methods=('GET',))
def download_sales():
    data = {}
    data['items'] = query_db('SELECT count(*) FROM F_Sales',one=True)
    data['quantity'] = query_db('SELECT SUM(f_sales_quantity) FROM F_Sales', one=True)
    data['best_sales'] = query_db('SELECT f_entity_date, f_sales_quantity FROM F_Sales ORDER BY f_sales_quantity DESC LIMIT 10')

    d = [
        ["Рядків продажів", data['items'][0]],
        [" "],
        ["Загальна кількість проданих о мебелі", data['quantity'][0]],
        [" "],
        ["ТОП 10 продажів"],
        ["Дата", "Кількість"]
    ]

    for date, quantity in data['best_sales']:
        d.append([date, quantity])

    return excel.make_response_from_array(d, "xls")