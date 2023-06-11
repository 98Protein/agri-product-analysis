import json

from flask import Blueprint, jsonify, request, abort
from sqlalchemy import text

from app.models import db
from app.models.product import Product
from app.utils.serialize import serialize

bp = Blueprint('product_bp', __name__, url_prefix='/')


def list_products():
    data = json.loads(request.get_data())

    query = Product.query
    print(data)

    # search
    search_obj = data.get('searchObj', None)
    if search_obj is not None:
        if search_obj.get('variety_id', None) is not None:
            query = query.filter(Product.variety_id == search_obj['variety_id'])
        if search_obj.get('market_id', None) is not None:
            query = query.filter(Product.market_id == search_obj['market_id'])
        if search_obj.get('date', None) is not None:
            query = query.filter((Product.date >= search_obj['date'][0]) & (Product.date <= search_obj['date'][1]))
        if search_obj.get('price', None) is not None:
            if search_obj['price'][0] is not None:
                query = query.filter(Product.price >= search_obj['price'][0])
            if search_obj['price'][1] is not None:
                query = query.filter(Product.price <= search_obj['price'][1])

    # sort
    sort_info = data.get('sortInfo', None)
    if sort_info is not None:
        if sort_info['order'] == 'ascending':
            query = query.order_by(text(sort_info['column']))
        else:
            query = query.order_by(text("-" + sort_info['column']))

    # pagination
    page_info = data.get('pagination', {
        'pageNo': 1,
        'pageSize': 10
    })
    page_no = page_info['pageNo']
    page_size = page_info['pageSize']
    query = query.paginate(page_no, per_page=page_size, error_out=False)

    items = serialize(query.items)
    return jsonify({
        "pageCount": query.pages,
        "pageNo": query.page,
        "pageSize": query.per_page,
        "total": query.total,
        "list": items
    })


def insert_product():
    data = json.loads(request.get_data())
    db.session.add(Product(**data))
    db.session.commit()
    return ""


def delete_products():
    data = json.loads(request.get_data())
    Product.query.filter(Product.id.in_(data)).delete()
    db.session.commit()
    return ""


def modify_product():
    data = json.loads(request.get_data())
    Product.query.filter_by(id=data["id"]).update({
        'id': data['id'],
        'variety_id': data['variety_id'],
        'market_id': data['market_id'],
        'price': data['price'],
        'date': data['date'],
        'sell_number': data['sell_number']
    })
    db.session.commit()
    return ""


@bp.route('/product', methods=['PUT', 'DELETE', 'POST', 'PATCH'])
def index():
    if request.method == 'POST':
        return list_products()
    elif request.method == 'PUT':
        return insert_product()
    elif request.method == 'DELETE':
        return delete_products()
    elif request.method == 'PATCH':
        return modify_product()
    else:
        abort(404)
