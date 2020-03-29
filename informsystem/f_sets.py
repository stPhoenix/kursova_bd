import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import psycopg2

list_query = 'SELECT * FROM F_Sets '
detail_query = 'SELECT * FROM F_Sets WHERE F_Set_ID=%s AND F_Entity_ID=%s'


from .base_views import ListView, DeleteView, DetailUpdateView, AddView


class F_SetsList(ListView):
    template_name = 'f_sets/list.html'
    list_query=list_query
    c_module = 'f_sets'
    sort_query = {
        'default': ' ORDER BY F_Set_ID ASC LIMIT 10 ', 
        'set_id_asc': ' ORDER BY F_Set_ID ASC LIMIT 10 ',
        'set_id_desc': ' ORDER BY F_Set_ID DESC LIMIT 10 ',
        'entity_id_asc': ' ORDER BY F_Entity_ID ASC LIMIT 10 ',
        'entity_id_desc': ' ORDER BY F_Entity_ID DESC LIMIT 10 ',
    }
    page_next_query= {
        'default': ' WHERE AND F_Sets_ID > %s ',
        'id_asc': ' WHERE AND F_Sets_ID > %s ',
        'id_desc': ' WHERE AND F_Sets_ID < %s ',
        'price_asc': ' WHERE AND F_Sets_ID > %s ',
        'price_desc': ' WHERE AND F_Sets_ID < %s ',
    }
    page_prev_query={
        'id_asc': ' WHERE AND F_Sets_ID < %s ',
        'id_desc': ' WHERE AND F_Sets_ID > %s ',
        'price_asc': ' WHERE AND F_Sets_ID < %s ',
        'price_desc': ' WHERE AND F_Sets_ID > %s ',
    }
    id_field='f_set_id'
    filter_field='f_sets_filter'
    sort_field='f_sets_sort'
        

    def get_query_objects(self):
        return ()


class F_SetsDelete(DeleteView):
    template_name = 'f_sets/list.html'
    c_module = 'f_sets'
    delete_query = 'DELETE FROM F_Sets WHERE F_Set_ID=%s AND F_Entity_ID=%s'
    redirect_url='f_sets_list'

    def dispatch_request(self, s_id, e_id):
        self.reset_result()
        try:
            query_db(self.delete_query, (s_id, e_id))
            return redirect(url_for(self.redirect_url))
        
        except (Exception, psycopg2.Error) as e:
            self.result['error'] = True
            self.result['message'] = e
            return render_template(self.template_name, c_module=self.c_module, result=self.result)


class F_SetsDetailUpdate(DetailUpdateView):
    template_name='f_sets/detail.html'
    c_module='f_sets'
    detail_query=detail_query
    update_query='UPDATE F_Sets SET   F_Set_ID=%s, F_Entity_ID=%s\
                                WHERE  F_Set_ID=%s AND F_Entity_ID=%s'
    
    def dispatch_request(self, s_id, e_id):
        self.reset_result()
        try:
            data = {}
            data['item'] = query_db(self.detail_query,(s_id, e_id), True)
            for item in self.get_query_objects():
                data[item[0]] = query_db(item[1])
            self.result['data'] = data
            if request.method == 'POST':
                form_args = []
                for key in self.get_form_names():
                    form_args.append(request.form[key])
                form_args.append(s_id)
                form_args.append(e_id)
                query_db(self.update_query, tuple(form_args))
                self.result['success'] = True
                self.result['message'] = 'Updated'
        except (Exception, psycopg2.Error) as e:
            self.result['error'] = True
            self.result['message'] = e

        return render_template(self.template_name, c_module=self.c_module, result=self.result)

    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_set_id',
                'f_entity_id')
        return fn


class F_SetsAdd(AddView):
    template_name='f_sets/add.html'
    c_module='f_sets'
    insert_query='INSERT INTO F_Sets (F_Set_ID, F_Entity_ID) VALUES (%s, %s)'
    
    def get_query_objects(self):
        qo = ()
        return qo

    def get_form_names(self):
        fn =   ('f_set_id',
                'f_entity_id')
        return fn