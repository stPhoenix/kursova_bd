import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'informsystem.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import main, entity
    from informsystem.entity import EntityList, EntityDelete, EntityDetailUpdate, EntityAdd
    from informsystem.f_type import F_TypeList, F_TypeDelete, F_TypeDetailUpdate, F_TypeAdd
    from informsystem.f_maker import F_MakerList, F_MakerDelete, F_MakerDetailUpdate, F_MakerAdd, F_MakerSearch
    from informsystem.f_material import F_MaterialList, F_MaterialDelete, F_MaterialDetailUpdate, F_MaterialAdd
    from informsystem.f_set import F_SetList, F_SetDelete, F_SetDetailUpdate, F_SetAdd
    from informsystem.f_sales import F_SalesList, F_SalesDelete, F_SalesDetailUpdate, F_SalesAdd
    from informsystem.f_sets import F_SetsList, F_SetsDelete, F_SetsDetailUpdate, F_SetsAdd




    app.register_blueprint(main.bp)
    app.add_url_rule('/entity/list', view_func=EntityList.as_view('entity_list'))
    app.add_url_rule('/entity/delete/<id>', view_func=EntityDelete.as_view('entity_delete'))
    app.add_url_rule('/entity/detail/<id>', view_func=EntityDetailUpdate.as_view('entity_detail'))
    app.add_url_rule('/entity/add', view_func=EntityAdd.as_view('entity_add'))
    app.add_url_rule('/f_type/list', view_func=F_TypeList.as_view('f_type_list'))
    app.add_url_rule('/f_type/delete/<id>', view_func=F_TypeDelete.as_view('f_type_delete'))
    app.add_url_rule('/f_type/detail/<id>', view_func=F_TypeDetailUpdate.as_view('f_type_detail'))
    app.add_url_rule('/f_type/add', view_func=F_TypeAdd.as_view('f_type_add'))
    app.add_url_rule('/f_maker/list', view_func=F_MakerList.as_view('f_maker_list'))
    app.add_url_rule('/f_maker/delete/<id>', view_func=F_MakerDelete.as_view('f_maker_delete'))
    app.add_url_rule('/f_maker/detail/<id>', view_func=F_MakerDetailUpdate.as_view('f_maker_detail'))
    app.add_url_rule('/f_maker/add', view_func=F_MakerAdd.as_view('f_maker_add'))
    app.add_url_rule('/f_maker/search', view_func=F_MakerSearch.as_view('f_maker_search'))
    app.add_url_rule('/f_material/list', view_func=F_MaterialList.as_view('f_material_list'))
    app.add_url_rule('/f_material/delete/<id>', view_func=F_MaterialDelete.as_view('f_material_delete'))
    app.add_url_rule('/f_material/detail/<id>', view_func=F_MaterialDetailUpdate.as_view('f_material_detail'))
    app.add_url_rule('/f_material/add', view_func=F_MaterialAdd.as_view('f_material_add'))
    app.add_url_rule('/f_set/list', view_func=F_SetList.as_view('f_set_list'))
    app.add_url_rule('/f_set/delete/<id>', view_func=F_SetDelete.as_view('f_set_delete'))
    app.add_url_rule('/f_set/detail/<id>', view_func=F_SetDetailUpdate.as_view('f_set_detail'))
    app.add_url_rule('/f_set/add', view_func=F_SetAdd.as_view('f_set_add'))
    app.add_url_rule('/f_sales/list', view_func=F_SalesList.as_view('f_sales_list'))
    app.add_url_rule('/f_sales/delete/<id>', view_func=F_SalesDelete.as_view('f_sales_delete'))
    app.add_url_rule('/f_sales/detail/<id>', view_func=F_SalesDetailUpdate.as_view('f_sales_detail'))
    app.add_url_rule('/f_sales/add', view_func=F_SalesAdd.as_view('f_sales_add'))
    app.add_url_rule('/f_sets/list', view_func=F_SetsList.as_view('f_sets_list'))
    app.add_url_rule('/f_sets/delete/<s_id>/<e_id>', view_func=F_SetsDelete.as_view('f_sets_delete'))
    app.add_url_rule('/f_sets/detail/<s_id>/<e_id>', view_func=F_SetsDetailUpdate.as_view('f_sets_detail'))
    app.add_url_rule('/f_sets/add', view_func=F_SetsAdd.as_view('f_sets_add'))
    
    return app