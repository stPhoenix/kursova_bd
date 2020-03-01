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
                keys = list(request.form.keys())
                all_query = self.filter_query(keys, request.form) 
            if request.args.get('sort'):
                all_query += self.sort_query[request.args.get('sort')]
            data = {}
            for item in self.get_query_objects():
                print(item)
                data[item[0]] = query_db(item[1])
            data['list'] = query_db(all_query)

            self.result['data'] = data
        
        
        except sqlite3.Error as e:
            self.result['error'] = True
            self.result['message'] = e.args[0]

        return render_template(self.template_name, c_module=self.c_module, result=self.result)


    def get_query_objects(self):
        raise NotImplementedError()
    