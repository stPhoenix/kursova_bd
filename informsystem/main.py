import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from informsystem.db import get_db

bp = Blueprint('main', __name__)

@bp.route('/', methods=('GET', 'POST'))
def main():
    return render_template('main.html')