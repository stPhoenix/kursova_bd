#import sqlite3
import psycopg2
import psycopg2.extras


import click
from flask import current_app, g
from flask.cli import with_appcontext

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_tmm_command)
    app.cli.add_command(init_entity_command)
    app.cli.add_command(init_sales_command)

def get_db():
    if 'db' not in g:
        # g.db = sqlite3.connect(
        #     current_app.config['DATABASE'],
        #     detect_types=sqlite3.PARSE_DECLTYPES
        # )
        # g.db.execute("PRAGMA foreign_keys = 1")
        # g.db.row_factory = sqlite3.Row

        g.db = psycopg2.connect(user=current_app.config['DBUSER'],
                                password=current_app.config['DBPASS'],
                                database=current_app.config['DBNAME'],
                                host=current_app.config['DBHOST'],
                                port=current_app.config['DBPORT']).cursor(cursor_factory=psycopg2.extras.DictCursor)
#        g.db.execute("PRAGMA foreign_keys = 1")
 #       g.db.row_factory = sqlite3.Row
    
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        #db.executescript(f.read().decode('utf8'))
        db.execute(f.read().decode('utf8'))
        db.connection.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('init-tmm')
@with_appcontext
def init_tmm_command():
    db = get_db()

    with current_app.open_resource('../queries/tmm.sql') as f:
        db.execute(f.read().decode('utf8'))
        db.connection.commit()

    click.echo('Initialized the tmm.')

@click.command('init-entity')
@with_appcontext
def init_entity_command():
    db = get_db()

    with current_app.open_resource('../queries/entity.sql') as f:
        db.execute(f.read().decode('utf8'))
        db.connection.commit()

    click.echo('Initialized the entity.')

@click.command('init-sales')
@with_appcontext
def init_sales_command():
    db = get_db()

    with current_app.open_resource('../queries/sales.sql') as f:
        db.execute(f.read().decode('utf8'))
        db.connection.commit()

    click.echo('Initialized the sales.')

def query_db(query, args=(), one=False):
    cur = get_db()
    cur.execute(query, args)
    if 'INSERT' in query or 'DELETE' in query or 'CREATE' in query or 'UPDATE' in query or 'DROP' in query:
       cur.connection.commit()
       return
    if 'insert' in query or 'delete' in query or 'create' in query or 'update' in query or 'drop' in query:
       cur.connection.commit()
       return

    rv = cur.fetchall()    
    #cur.close()
    return (rv[0] if rv else None) if one else rv
