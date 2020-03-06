import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import sqlite3

list_query = 'SELECT * FROM F_Maker '
detail_query = 'SELECT * FROM F_Maker WHERE F_Maker_ID=?'


from .base_views import ListView, DeleteView, DetailUpdateView, AddView


class F_MakerList(ListView):
    template_name = 'f_maker/list.html'
    list_query=list_query
    c_module = 'f_maker'
    sort_query = {
        'default': ' ORDER BY F_Maker_ID ASC LIMIT 10 ', 
        'id_asc': ' ORDER BY F_Maker_ID ASC LIMIT 10 ',
        'id_desc': ' ORDER BY F_Maker_ID DESC LIMIT 10 ',
        'name_asc': ' ORDER BY F_Maker_Name ASC LIMIT 10 ',
        'name_desc': ' ORDER BY F_Maker_Name DESC LIMIT 10 ',
    }
    page_next_query= {
        'default': ' WHERE AND F_Maker_ID > %s ',
        'id_asc': ' WHERE AND F_Maker_ID > %s ',
        'id_desc': ' WHERE AND F_Maker_ID < %s ',
        'price_asc': ' WHERE AND F_Maker_ID > %s ',
        'price_desc': ' WHERE AND F_Maker_ID < %s ',
    }
    page_prev_query={
        'id_asc': ' WHERE AND F_Maker_ID < %s ',
        'id_desc': ' WHERE AND F_Maker_ID > %s ',
        'price_asc': ' WHERE AND F_Maker_ID < %s ',
        'price_desc': ' WHERE AND F_Maker_ID > %s ',
    }
    id_field='f_maker_id'
    filter_field='f_maker_filter'
    sort_field='f_maker_sort'
        

    def get_query_objects(self):
        return ()


class F_MakerDelete(DeleteView):
    template_name = 'f_maker/list.html'
    c_module = 'f_maker'
    delete_query = 'DELETE FROM F_Maker WHERE F_Maker_ID=?'



class F_MakerDetailUpdate(DetailUpdateView):
    template_name='f_maker/detail.html'
    c_module='f_maker'
    detail_query=detail_query
    update_query='UPDATE F_Maker SET   F_Maker_Name=?\
                                WHERE  F_Maker_ID=?'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_maker_name',)
        return fn


class F_MakerAdd(AddView):
    template_name='f_maker/add.html'
    c_module='f_maker'
    detail_query=detail_query
    insert_query='INSERT INTO F_Maker (F_Maker_Name) VALUES (?)'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_maker_name',)
        return fn