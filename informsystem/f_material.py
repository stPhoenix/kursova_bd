import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db


list_query = 'SELECT * FROM F_Material '
detail_query = 'SELECT * FROM F_Material WHERE F_Material_ID=%s'


from .base_views import ListView, DeleteView, DetailUpdateView, AddView


class F_MaterialList(ListView):
    template_name = 'f_material/list.html'
    list_query=list_query
    c_module = 'f_material'
    sort_query = {
        'default': ' ORDER BY F_Material_ID ASC LIMIT 10 ', 
        'id_asc': ' ORDER BY F_Material_ID ASC LIMIT 10 ',
        'id_desc': ' ORDER BY F_Material_ID DESC LIMIT 10 ',
        'name_asc': ' ORDER BY F_Material_Name ASC LIMIT 10 ',
        'name_desc': ' ORDER BY F_Material_Name DESC LIMIT 10 ',
    }
    page_next_query= {
        'default': ' WHERE AND F_Material_ID > %s ',
        'id_asc': ' WHERE AND F_Material_ID > %s ',
        'id_desc': ' WHERE AND F_Material_ID < %s ',
        'price_asc': ' WHERE AND F_Material_ID > %s ',
        'price_desc': ' WHERE AND F_Material_ID < %s ',
    }
    page_prev_query={
        'id_asc': ' WHERE AND F_Material_ID < %s ',
        'id_desc': ' WHERE AND F_Material_ID > %s ',
        'price_asc': ' WHERE AND F_Material_ID < %s ',
        'price_desc': ' WHERE AND F_Material_ID > %s ',
    }
    id_field='f_material_id'
    filter_field='f_material_filter'
    sort_field='f_material_sort'
        

    def get_query_objects(self):
        return ()


class F_MaterialDelete(DeleteView):
    template_name = 'f_material/list.html'
    c_module = 'f_material'
    delete_query = 'DELETE FROM F_Material WHERE F_Material_ID=%s'
    redirect_url='f_material_list'



class F_MaterialDetailUpdate(DetailUpdateView):
    template_name='f_material/detail.html'
    c_module='f_material'
    detail_query=detail_query
    update_query='UPDATE F_Material SET   F_Material_Name=%s\
                                WHERE F_Material_ID=%s'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_material_name',)
        return fn


class F_MaterialAdd(AddView):
    template_name='f_material/add.html'
    c_module='f_material'
    detail_query=detail_query
    insert_query='INSERT INTO F_Material (F_Material_Name) VALUES (%s)'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_material_name',)
        return fn