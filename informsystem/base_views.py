from flask.views import View

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import sqlite3


class ListView(View):
    methods = ['GET', 'POST']
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    template_name=None
    list_query=None
    c_module=None
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
        for item in form.getlist(key):
            keys_copy = keys.copy()
            temp_query = ''
            if head:
                temp_query += query+' AND e.%s=%s '%(key, item)
                qs = []
                self.filter_query(keys_copy, form, temp_query, False, qs)
            else:
                temp_query+=query+' AND e.%s=%s '% (key, item)
                self.filter_query(keys_copy, form, temp_query, False, results)    
        if head:
            return ' UNION '.join(qs)


    def dispatch_request(self):
        all_query = self.list_query
        try:
            if request.method == 'POST':
                session[self.filter_field] = request.form
            if request.args.get('reset_filter'):
                session.pop(self.filter_field, None)
            if self.filter_field in session:
                keys = list(request.form.keys())
                all_query = self.filter_query(keys, request.form)
            if request.args.get('sort'):
                all_query += self.sort_query[request.args.get('sort')]
                session[self.sort_field] = request.args.get('sort')
            if self.sort_field not in session:
                all_query += self.sort_query['default']
                session[self.sort_field] = 'default'
            temp_query=''
            if request.args.get('next'):
                temp_query = self.page_next_query[session[self.sort_field]]%(request.args.get('next'))
                all_query += temp_query + self.sort_query[session[self.sort_field]]
            if request.args.get('prev'):
                temp_query = self.page_next_query[session[self.sort_field]]%(request.args.get('prev'))
                all_query += temp_query + self.sort_query[session[self.sort_field]]
            if request.method == 'GET' and not request.args.get('next') and not request.args.get('prev') and not request.args.get('sort'):
                all_query += self.sort_query[session[self.sort_field]]
            data = {}
            for item in self.get_query_objects():
                data[item[0]] = query_db(item[1])
            data['list'] = query_db(all_query)
            data['prev'] = data['list'][0][self.id_field] if request.args.get('next') else 0                
            data['next'] = data['list'][-1][self.id_field]

            self.result['data'] = data
        
        
        except sqlite3.Error as e:
            self.result['error'] = True
            self.result['message'] = e.args[0]

        return render_template(self.template_name, c_module=self.c_module, result=self.result)


    def get_query_objects(self):
        raise NotImplementedError()


class DeleteView(View):
    methods = ['GET']
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    template_name=None
    c_module=None
    delete_query=None

    def dispatch_request(self, id):
        try:
            query_db(self.delete_query, (id,))
            return redirect(url_for('entity_list'))
        
        except sqlite3.Error as e:
            self.result['error'] = True
            self.result['message'] = e.args[0]
            return render_template(self.template_name, c_module=self.c_module, result=self.result)


class DetailUpdateView(View):
    methods = ['GET', 'POST']
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    template_name=None
    c_module=None
    update_query=None
    detail_query=None

    def dispatch_request(self, id):
        try:
            data = {}
            data['item'] = query_db(self.detail_query,(id,), True)
            for item in self.get_query_objects():
                data[item[0]] = query_db(item[1])
            self.result['data'] = data
            if request.method == 'POST':
                form_args = []
                for key in self.get_form_names():
                    form_args.append(request.form[key])
                form_args.append(id)
                query_db(self.update_query, tuple(form_args))
                self.result['success'] = True
                self.result['message'] = 'Updated'
        except sqlite3.Error as e:
            self.result['error'] = True
            self.result['message'] = e.args[0]

        return render_template(self.template_name, c_module=self.c_module, result=self.result)

    def get_query_objects(self):
        return NotImplementedError()

    def get_form_names(self):
        return NotImplementedError()


class AddView(View):
    methods = ['GET', 'POST']
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    template_name=None
    c_module=None
    insert_query=None

    def dispatch_request(self):
        try:
            data = {}
            for item in self.get_query_objects():
                data[item[0]] = query_db(item[1])
            self.result['data'] = data
            if request.method == 'POST':
                form_args = []
                for key in self.get_form_names():
                    form_args.append(request.form[key])
                query_db(self.insert_query, tuple(form_args))
                self.result['success'] = True
                self.result['message'] = 'Success'
        except sqlite3.Error as e:
            self.result['error'] = True
            self.result['message'] = e.args[0]

        return render_template(self.template_name, c_module=self.c_module, result=self.result)

    def get_query_objects(self):
        return NotImplementedError()

    def get_form_names(self):
        return NotImplementedError()