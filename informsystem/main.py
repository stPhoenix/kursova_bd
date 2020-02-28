import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, request
)

from informsystem.db import get_db, query_db

import sqlite3

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def main():
    return render_template('main.html')

@bp.route('/query', methods=('GET', 'POST'))
def query():
    result = {'success': False, 'error': False, 'message': None, 'data': None}
    if request.method == 'POST':
        try:
            result['data'] = query_db(request.form['query'])
            result['success'] = True
            result['message'] = 'Success'
        
        except sqlite3.Error as e:
            result['error'] = True
            result['message'] = e.args[0]


    return render_template('query.html', result=result, c_module='query')