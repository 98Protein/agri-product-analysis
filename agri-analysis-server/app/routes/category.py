from flask import Blueprint, jsonify, request

from app.models.city import City
from app.models.market import Market
from app.models.province import Province
from app.models.type import Type
from app.models.variety import Variety
from app.utils.serialize import serialize

bp = Blueprint('category_bp', __name__, url_prefix='/')


@bp.route('/province', methods=['GET'])
def get_province_list():
    return jsonify(serialize(Province.query.all()))


@bp.route('/city', methods=['GET'])
def get_city_list():
    province_id = request.args['province']
    return jsonify(serialize(City.query.filter_by(province_id=province_id).all()))


@bp.route('/market', methods=['GET'])
def get_market_list():
    city_id = request.args['city']
    return jsonify(serialize(Market.query.filter_by(city_id=city_id).all()))


@bp.route('/market/<market_id>', methods=['GET'])
def get_market(market_id):
    return jsonify(serialize(Market.query.filter_by(id=market_id).one()))


@bp.route('/type', methods=['GET'])
def get_type_list():
    return jsonify(serialize(Type.query.all()))


@bp.route('/variety', methods=['GET'])
def get_variety_list():
    type_id = request.args['type']
    return jsonify(serialize(Variety.query.filter_by(type_id=type_id).all()))


@bp.route('/variety/<variety_id>', methods=['GET'])
def get_variety(variety_id):
    return jsonify(serialize(Variety.query.filter_by(id=variety_id).one()))
