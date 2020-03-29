import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

list_query = 'SELECT * FROM F_Set '
detail_query = 'SELECT * FROM F_Set WHERE F_Set_ID=%s'


from .base_views import ListView, DeleteView, DetailUpdateView, AddView


class F_SetList(ListView):
    template_name = 'f_set/list.html'
    list_query=list_query
    c_module = 'f_set'
    sort_query = {
        'default': ' ORDER BY F_Set_ID ASC LIMIT 10 ', 
        'id_asc': ' ORDER BY F_Set_ID ASC LIMIT 10 ',
        'id_desc': ' ORDER BY F_Set_ID DESC LIMIT 10 ',
        'name_asc': ' ORDER BY F_Set_Name ASC LIMIT 10 ',
        'name_desc': ' ORDER BY F_Set_Name DESC LIMIT 10 ',
    }
    page_next_query= {
        'default': ' WHERE AND F_Set_ID > %s ',
        'id_asc': ' WHERE AND F_Set_ID > %s ',
        'id_desc': ' WHERE AND F_Set_ID < %s ',
        'price_asc': ' WHERE AND F_Set_ID > %s ',
        'price_desc': ' WHERE AND F_Set_ID < %s ',
    }
    page_prev_query={
        'id_asc': ' WHERE AND F_Set_ID < %s ',
        'id_desc': ' WHERE AND F_Set_ID > %s ',
        'price_asc': ' WHERE AND F_Set_ID < %s ',
        'price_desc': ' WHERE AND F_Set_ID > %s ',
    }
    id_field='f_set_id'
    filter_field='f_set_filter'
    sort_field='f_set_sort'
        

    def get_query_objects(self):
        return ()


class F_SetDelete(DeleteView):
    template_name = 'f_set/list.html'
    c_module = 'f_set'
    delete_query = 'DELETE FROM F_Set WHERE F_Set_ID=%s'
    redirect_url='f_set_list'


class F_SetDetailUpdate(DetailUpdateView):
    template_name='f_set/detail.html'
    c_module='f_set'
    detail_query=detail_query
    update_query='UPDATE F_Set SET   F_Set_Name=%s\
                                WHERE  F_Set_ID=%s'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_set_name',)
        return fn


class F_SetAdd(AddView):
    template_name='f_set/add.html'
    c_module='f_set'
    detail_query=detail_query
    insert_query='INSERT INTO F_Set (F_Set_Name) VALUES (%s)'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_set_name',)
        return fn