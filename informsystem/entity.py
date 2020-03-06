import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import sqlite3

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
        'default': ' AND e.f_entity_id > %s ',
        'id_asc': ' AND e.f_entity_id > %s ',
        'id_desc': ' AND e.f_entity_id < %s ',
        'price_asc': ' AND e.f_entity_id > %s ',
        'price_desc': ' AND e.f_entity_id < %s ',
    }
    page_prev_query={
        'id_asc': ' AND e.f_entity_id < %s ',
        'id_desc': ' AND e.f_entity_id > %s ',
        'price_asc': ' AND e.f_entity_id < %s ',
        'price_desc': ' AND e.f_entity_id > %s ',
    }
    id_field='f_entity_id'
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