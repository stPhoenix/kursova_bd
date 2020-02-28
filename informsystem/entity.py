import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import sqlite3

bp = Blueprint('entity', __name__, url_prefix='/entity')
list_query = 'SELECT E.F_Entity_ID,\
                     E.F_Entity_Price,\
                     E.F_Entity_Quantity,\
                     E.F_Entity_Height,\
                     E.F_Entity_Width,\
                     E.F_Entity_Length,\
                     E.F_Entity_Color,\
                     T.F_Type_Name,\
                     Mk.F_Maker_Name,\
                     Mt.F_Material_Name\
              FROM F_Entity E, F_Type T, F_Maker Mk, F_Material Mt\
              WHERE E.F_Type_ID = T.F_Type_ID\
              AND   E.F_Maker_ID = Mk.F_Maker_ID\
              AND   E.F_Material_ID = Mt.F_Material_ID'
detail_query = 'SELECT * FROM F_Entity E, F_Maker Mk, F_Type T, F_Material Mt WHERE E.F_Entity_ID=? \
                AND Mk.F_Maker_ID=E.F_Maker_ID \
                AND T.F_Type_ID=E.F_Type_ID \
                AND Mt.F_Material_ID=E.F_Material_ID'

@bp.route('/list', methods=('GET', 'POST'))
def entity_list():
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    all_query = list_query
    sort_query = {
        'id_asc': ' ORDER BY E.F_Entity_ID ASC',
        'id_desc': ' ORDER BY E.F_Entity_ID DESC',
        'price_asc': ' ORDER BY E.F_Entity_Price ASC',
        'price_desc': ' ORDER BY E.F_Entity_Price DESC',
    }
    args = []
    try:
        if request.args.get('sort'):
               all_query += sort_query[request.args.get('sort')]
        if request.method == 'POST':
            for key, value in request.form.items(True):
                all_query += ' AND ?=? '
                args.append('E.'+key)
                args.append(value)  
        data = {}
        data['f_type'] = query_db('SELECT * FROM F_Type')
        data['f_maker'] = query_db('SELECT * FROM F_Maker')
        data['f_material'] = query_db('SELECT * FROM F_Material')
        data['list'] = query_db(all_query, tuple(args))
        result['data'] = data
        
        
    except sqlite3.Error as e:
        result['error'] = True
        result['message'] = e.args[0]


    return render_template('entity/list.html', c_module='entity', result=result)

@bp.route('/add', methods=('GET', 'POST'))
def entity_add():
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    try:
        data = {}
        data['f_type'] = query_db('SELECT * FROM F_Type')
        data['f_maker'] = query_db('SELECT * FROM F_Maker')
        data['f_material'] = query_db('SELECT * FROM F_Material')
        result['data'] = data
    except sqlite3.Error as e:
        result['error'] = True
        result['message'] = e.args[0]
    
    if request.method == 'POST':
        try:
            query_db('INSERT INTO F_Entity (F_Entity_Price,\
                                            F_Entity_Quantity,\
                                            F_Entity_Height,\
                                            F_Entity_Width,\
                                            F_Entity_Length,\
                                            F_Entity_Color,\
                                            F_Type_ID,\
                                            F_Maker_ID,\
                                            F_Material_ID) VALUES (?,?,?,?,?,?,?,?,?)', (request.form['price'],
                                                                                request.form['quantity'],
                                                                                request.form['height'],
                                                                                request.form['width'],
                                                                                request.form['length'],
                                                                                request.form['color'],
                                                                                request.form['f_type_id'],
                                                                                request.form['f_maker_id'],
                                                                                request.form['f_material_id']))
            result['success'] = True
            result['message'] = 'Success'

        except sqlite3.Error as e:
            result['error'] = True
            result['message'] = e.args[0]
    return render_template('entity/add.html', c_module='entity', result=result)

@bp.route('/delete/<id>', methods=('GET',))
def entity_delete(id):
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    try:
        query_db('DELETE FROM F_Entity WHERE F_Entity_ID=?', (id,))
        result['data'] = query_db(list_query)
        result['success'] = True
        result['message'] = 'Deleted'
    except sqlite3.Error as e:
        result['error'] = True
        result['message'] = e.args[0]
    return render_template('entity/list.html', c_module='entity', result=result)

@bp.route('/detail/<id>', methods=('GET', 'POST'))
def entity_detail(id):
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    try:
        data = {}
        data['item'] = query_db(detail_query,(id,), True)
        data['f_type'] = query_db('SELECT * FROM F_Type')
        data['f_maker'] = query_db('SELECT * FROM F_Maker')
        data['f_material'] = query_db('SELECT * FROM F_Material')
        result['data'] = data
        if request.method == 'POST':
            query_db('UPDATE F_Entity SET   F_Entity_Price=?,\
                                            F_Entity_Quantity=?,\
                                            F_Entity_Height=?,\
                                            F_Entity_Width=?,\
                                            F_Entity_Length=?,\
                                            F_Entity_Color=?,\
                                            F_Type_ID=?,\
                                            F_Maker_ID=?,\
                                            F_Material_ID=?\
                                       WHERE F_Entity_ID=?', (request.form['price'],
                                                              request.form['quantity'],
                                                              request.form['height'],
                                                              request.form['width'],
                                                              request.form['length'],                                                                       request.form['color'],
                                                              request.form['f_type_id'],
                                                              request.form['f_maker_id'],
                                                              request.form['f_material_id'],
                                                              id))
            result['success'] = True
            result['message'] = 'Updated'
    except sqlite3.Error as e:
        result['error'] = True
        result['message'] = e.args[0]

    return render_template('entity/detail.html', c_module='entity', result=result)