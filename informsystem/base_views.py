from flask.views import View

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

#import sqlite3
import psycopg2

from werkzeug.datastructures import MultiDict

class BaseView(View):
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    template_name=None
    c_module=None

    def reset_result(self):
        self.result = {'success': False, 'error': False, 'message': None, 'data': None}
    
    def get_query_objects(self):
        return NotImplementedError()

    def get_form_names(self):
        return NotImplementedError()

class ListView(BaseView):
    methods = ['GET', 'POST']
    list_query=None
    sort_query=None
    page_next_query=None
    page_prev_query=None
    id_field=None
    filter_field=None
    sort_field=None

    def filter_query(self, keys, form, query='', head=True, results=None):
        if keys == []:
            results.append(self.list_query+query)
            return
        key = keys.pop()
        qs = []
        for item in form.getlist(key):
            keys_copy = keys.copy()
            temp_query = ''
            if head:
                temp_query += query+' WHERE e.%s=%s '%(key, item) # TODO: fix table prefix name
                self.filter_query(keys_copy, form, temp_query, False, qs)
            else:
                temp_query+=query+' AND e.%s=%s '% (key, item) # TODO: fix table prefix name
                self.filter_query(keys_copy, form, temp_query, False, results)    
        if head:
            return ' UNION '.join(qs)


    def dispatch_request(self):
        self.reset_result()
        all_query = self.list_query
        next = 2
        prev = 1
        try:
            if request.method == 'POST':
                session[self.filter_field] = MultiDict(request.form)
            if request.args.get('reset_filter'):
                session.pop(self.filter_field, None)
            if self.filter_field in session:
                keys = list(session[self.filter_field].keys())
                all_query = self.filter_query(keys, MultiDict(session[self.filter_field]))
            if request.args.get('sort'):
                session[self.sort_field] = request.args.get('sort')
            if self.sort_field not in session:
                all_query += self.sort_query['default']
                session[self.sort_field] = 'default'
            else:
                all_query += self.sort_query[session[self.sort_field]]
            temp_query=''
            if request.args.get('next'):
                temp_query = ' OFFSET %s*10 '%(request.args.get('next'))
                all_query += temp_query
                next = int(request.args.get('next')) + 1
                prev = int(request.args.get('next')) - 1 if int(request.args.get('next')) >= 2 else 1
            if request.args.get('prev'):
                temp_query = ' OFFSET %s*10 '%(request.args.get('prev'))
                all_query += temp_query
                next = int(request.args.get('prev')) + 1
                prev = int(request.args.get('prev')) - 1 if int(request.args.get('prev')) >= 2 else 1
            data = {}
            for item in self.get_query_objects():
                data[item[0]] = query_db(item[1])
            print(all_query)
            data['list'] = query_db(all_query)
            if data['list']:
                data['prev'] = prev                
                data['next'] = next

            self.result['data'] = data
        
        
        except (Exception, psycopg2.Error) as e:
            self.result['error'] = True
            self.result['message'] = e

        return render_template(self.template_name, c_module=self.c_module, result=self.result)



class DeleteView(BaseView):
    methods = ['GET']
    delete_query=None
    redirect_url=None

    def dispatch_request(self, id):
        self.reset_result()
        try:
            query_db(self.delete_query, (id,))
            return redirect(url_for(self.redirect_url))
        
        except (Exception, psycopg2.Error) as e:
            self.result['error'] = True
            self.result['message'] = e
            return render_template(self.template_name, c_module=self.c_module, result=self.result)


class DetailUpdateView(BaseView):
    methods = ['GET', 'POST']
    update_query=None
    detail_query=None

    def dispatch_request(self, id):
        self.reset_result()
        try:
            data = {}
           
            if request.method == 'POST':
                form_args = []
                for key in self.get_form_names():
                    form_args.append(request.form[key])
                form_args.append(id)
                query_db(self.update_query, tuple(form_args))
                self.result['success'] = True
                self.result['message'] = 'Updated'
            data['item'] = query_db(self.detail_query,(id,), True)
            for item in self.get_query_objects():
                data[item[0]] = query_db(item[1])
            self.result['data'] = data
                
        except (Exception, psycopg2.Error) as e:
            self.result['error'] = True
            self.result['message'] = e

        return render_template(self.template_name, c_module=self.c_module, result=self.result)


class AddView(BaseView):
    methods = ['GET', 'POST']
    insert_query=None

    def dispatch_request(self):
        self.reset_result()
        try:
            data = {}
            for item in self.get_query_objects():
                data[item[0]] = query_db(item[1])
            self.result['data'] = data
            if request.method == 'POST':
                form_args = []
                for key in self.get_form_names():
                    if request.form[key] == '':
                        form_args.append(None)
                        continue
                    form_args.append(request.form[key])
                query_db(self.insert_query, tuple(form_args))
                self.result['success'] = True
                self.result['message'] = 'Success'
        except (Exception, psycopg2.Error) as e:
            self.result['error'] = True
            self.result['message'] = e

        return render_template(self.template_name, c_module=self.c_module, result=self.result)

    def get_query_objects(self):
        return NotImplementedError()

    def get_form_names(self):
        return NotImplementedError()