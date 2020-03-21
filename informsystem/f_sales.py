import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import sqlite3

list_query = 'SELECT * FROM F_Sales '
detail_query = 'SELECT * FROM F_Sales WHERE F_Sales_ID=?'


from .base_views import ListView, DeleteView, DetailUpdateView, AddView


class F_SalesList(ListView):
    template_name = 'f_sales/list.html'
    list_query=list_query
    c_module = 'f_sales'
    sort_query = {
        'default': ' ORDER BY F_Sales_ID ASC LIMIT 10 ', 
        'id_asc': ' ORDER BY F_Sales_ID ASC LIMIT 10 ',
        'id_desc': ' ORDER BY F_Sales_ID DESC LIMIT 10 ',
        'date_asc': ' ORDER BY F_Entity_Date ASC LIMIT 10 ',
        'date_desc': ' ORDER BY F_Entity_Date DESC LIMIT 10 ',
    }
    page_next_query= {
        'default': ' WHERE AND F_Sales_ID > %s ',
        'id_asc': ' WHERE AND F_Sales_ID > %s ',
        'id_desc': ' WHERE AND F_Sales_ID < %s ',
        'date_asc': ' WHERE AND F_Sales_ID > %s ',
        'date_desc': ' WHERE AND F_Sales_ID < %s ',
    }
    page_prev_query={
        'id_asc': ' WHERE AND F_Sales_ID < %s ',
        'id_desc': ' WHERE AND F_Sales_ID > %s ',
        'date_asc': ' WHERE AND F_Sales_ID < %s ',
        'date_desc': ' WHERE AND F_Sales_ID > %s ',
    }
    id_field='f_sales_id'
    filter_field='f_sales_filter'
    sort_field='f_sales_sort'
        

    def get_query_objects(self):
        return ()


class F_SalesDelete(DeleteView):
    template_name = 'f_sales/list.html'
    c_module = 'f_sales'
    delete_query = 'DELETE FROM F_Sales WHERE F_Sales_ID=?'
    redirect_url='f_sales_list'



class F_SalesDetailUpdate(DetailUpdateView):
    template_name='f_sales/detail.html'
    c_module='f_sales'
    detail_query=detail_query
    update_query='UPDATE F_Sales SET F_Sales_Quantity=?, \
                                     F_Entity_ID=?, \
                                     F_Entity_Date=? \
                               WHERE F_Sales_ID=?'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_sales_quantity',
                'f_entity_id',
                'f_entity_date',
                )
        return fn


class F_SalesAdd(AddView):
    template_name='f_sales/add.html'
    c_module='f_sales'
    detail_query=detail_query
    insert_query='INSERT INTO F_Sales (F_Sales_Quantity, F_Entity_ID, F_Entity_Date) VALUES (?,?,?)'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_sales_quantity',
                'f_entity_id',
                'f_entity_date')
        return fn
    

    def dispatch_request(self):
        if request.method == 'POST':
            try:
                fid = request.form['f_entity_id']
                quantity = int(query_db('SELECT f_entity_quantity FROM F_Entity WHERE F_Entity_ID=?',(fid,),True)[0])
                new_quantity = quantity - int(request.form['f_sales_quantity'])
                if  new_quantity < 0:
                    self.result['error'] = True
                    self.result['message'] = 'Придбаних одиниць більше ніж в наявності!'
                    return render_template(self.template_name, c_module=self.c_module, result=self.result)
                else:
                    query_db('UPDATE F_Entity SET F_Entity_Quantity=? WHERE F_Entity_ID=?', (new_quantity, fid))
                    return super().dispatch_request()

            except sqlite3.Error as e:
                self.result['error'] = True
                self.result['message'] = e.args[0]
                return render_template(self.template_name, c_module=self.c_module, result=self.result)
        else:
            return super().dispatch_request()
