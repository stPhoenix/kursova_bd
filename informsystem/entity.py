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
              AND   E.F_Material_ID = Mt.F_Material_ID '
detail_query = 'SELECT * FROM F_Entity E, F_Maker Mk, F_Type T, F_Material Mt WHERE E.F_Entity_ID=? \
                AND Mk.F_Maker_ID=E.F_Maker_ID \
                AND T.F_Type_ID=E.F_Type_ID \
                AND Mt.F_Material_ID=E.F_Material_ID'


from .base_views import ListView, DeleteView, DetailUpdateView, AddView


class EntityList(ListView):
    template_name = 'entity/list.html'
    list_query=list_query
    c_module = 'entity'
    sort_query = {
        'default': ' ORDER BY E.F_Entity_ID ASC LIMIT 10 ', 
        'id_asc': ' ORDER BY E.F_Entity_ID ASC LIMIT 10 ',
        'id_desc': ' ORDER BY E.F_Entity_ID DESC LIMIT 10 ',
        'price_asc': ' ORDER BY E.F_Entity_Price ASC LIMIT 10 ',
        'price_desc': ' ORDER BY E.F_Entity_Price DESC LIMIT 10 ',
    }
    page_next_query= {
        'default': ' WHERE e.f_entity_id > %s ',
        'id_asc': ' WHERE e.f_entity_id > %s ',
        'id_desc': ' WHERE e.f_entity_id < %s ',
        'price_asc': ' WHERE e.f_entity_id > %s ',
        'price_desc': ' WHERE e.f_entity_id < %s ',
    }
    page_prev_query={
        'id_asc': ' WHERE e.f_entity_id < %s ',
        'id_desc': ' WHERE e.f_entity_id > %s ',
        'price_asc': ' WHERE e.f_entity_id < %s ',
        'price_desc': ' WHERE e.f_entity_id > %s ',
    }
    id_field='e.f_entity_id'
    filter_field='entity_filter'
    sort_field='entity_sort'
        

    def get_query_objects(self):
        qo = (('f_type','SELECT * FROM F_Type'),
              ('f_maker','SELECT * FROM F_Maker'),
              ('f_material','SELECT * FROM F_Material'))
        return qo


class EntityDelete(DeleteView):
    template_name = 'entity/list.html'
    c_module = 'entity'
    delete_query = 'DELETE FROM F_Entity WHERE F_Entity_ID=?'



class EntityDetailUpdate(DetailUpdateView):
    template_name='entity/detail.html'
    c_module='entity'
    detail_query=detail_query
    update_query='UPDATE F_Entity SET   F_Entity_Price=?,\
                                        F_Entity_Quantity=?,\
                                        F_Entity_Height=?,\
                                        F_Entity_Width=?,\
                                        F_Entity_Length=?,\
                                        F_Entity_Color=?,\
                                        F_Type_ID=?,\
                                        F_Maker_ID=?,\
                                        F_Material_ID=?\
                                  WHERE F_Entity_ID=?'
    
    def get_query_objects(self):
        qo = (('f_type','SELECT * FROM F_Type'),
              ('f_maker','SELECT * FROM F_Maker'),
              ('f_material','SELECT * FROM F_Material'))
        return qo

    def get_form_names(self):
        fn =   ('price',
                'quantity',
                'height',
                'width',
                'length',
                'color',
                'f_type_id',
                'f_maker_id',
                'f_material_id')
        return fn


class EntityAdd(AddView):
    template_name='entity/add.html'
    c_module='entity'
    detail_query=detail_query
    insert_query='INSERT INTO F_Entity (F_Entity_Price,\
                                        F_Entity_Quantity,\
                                        F_Entity_Height,\
                                        F_Entity_Width,\
                                        F_Entity_Length,\
                                        F_Entity_Color,\
                                        F_Type_ID,\
                                        F_Maker_ID,\
                                        F_Material_ID) VALUES (?,?,?,?,?,?,?,?,?)'
    
    def get_query_objects(self):
        qo = (('f_type','SELECT * FROM F_Type'),
              ('f_maker','SELECT * FROM F_Maker'),
              ('f_material','SELECT * FROM F_Material'))
        return qo

    def get_form_names(self):
        fn =   ('price',
                'quantity',
                'height',
                'width',
                'length',
                'color',
                'f_type_id',
                'f_maker_id',
                'f_material_id')
        return fn

#@bp.route('/add', methods=('GET', 'POST'))
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
        except sqlite3.Warning as e:
            result['error'] = True
            result['message'] = e.args[0]

    return render_template('entity/add.html', c_module='entity', result=result)

#@bp.route('/delete/<id>', methods=('GET',))
def entity_delete(id):
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    try:
        query_db('DELETE FROM F_Entity WHERE F_Entity_ID=?', (id,))
        return redirect(url_for('entity_list'))
        
    except sqlite3.Error as e:
        result['error'] = True
        result['message'] = e.args[0]
    return render_template('entity/list.html', c_module='entity', result=result)

#@bp.route('/detail/<id>', methods=('GET', 'POST'))
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