import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

list_query = 'SELECT * FROM F_Type '
detail_query = 'SELECT * FROM F_Type WHERE F_Type_ID=%s'


from .base_views import ListView, DeleteView, DetailUpdateView, AddView


class F_TypeList(ListView):
    template_name = 'f_type/list.html'
    list_query=list_query
    c_module = 'f_type'
    sort_query = {
        'default': ' ORDER BY F_Type_ID ASC LIMIT 10 ', 
        'id_asc': ' ORDER BY F_Type_ID ASC LIMIT 10 ',
        'id_desc': ' ORDER BY F_Type_ID DESC LIMIT 10 ',
        'name_asc': ' ORDER BY F_Type_Name ASC LIMIT 10 ',
        'name_desc': ' ORDER BY F_Type_Name DESC LIMIT 10 ',
    }
    page_next_query= {
        'default': ' WHERE AND F_Type_ID > %s ',
        'id_asc': ' WHERE AND F_Type_ID > %s ',
        'id_desc': ' WHERE AND F_Type_ID < %s ',
        'price_asc': ' WHERE AND F_Type_ID > %s ',
        'price_desc': ' WHERE AND F_Type_ID < %s ',
    }
    page_prev_query={
        'id_asc': ' WHERE AND F_Type_ID < %s ',
        'id_desc': ' WHERE AND F_Type_ID > %s ',
        'price_asc': ' WHERE AND F_Type_ID < %s ',
        'price_desc': ' WHERE AND F_Type_ID > %s ',
    }
    id_field='f_type_id'
    filter_field='f_type_filter'
    sort_field='f_type_sort'
        

    def get_query_objects(self):
        return ()


class F_TypeDelete(DeleteView):
    template_name = 'f_type/list.html'
    c_module = 'f_type'
    delete_query = 'DELETE FROM F_Type WHERE F_Type_ID=%s'
    redirect_url = 'f_type_list'



class F_TypeDetailUpdate(DetailUpdateView):
    template_name='f_type/detail.html'
    c_module='f_type'
    detail_query=detail_query
    update_query='UPDATE F_Type SET   F_Type_Name=%s\
                                WHERE F_Type_ID=%s'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_type_name',)
        return fn


class F_TypeAdd(AddView):
    template_name='f_type/add.html'
    c_module='f_type'
    detail_query=detail_query
    insert_query='INSERT INTO F_Type (F_Type_Name) VALUES (%s)'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_type_name',)
        return fn