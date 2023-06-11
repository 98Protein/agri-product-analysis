import json

import pyspark.sql.functions as f
from flask import Blueprint, jsonify, request

from app.spark import df_reader

bp = Blueprint('region_bp', __name__, url_prefix='/region')


@bp.route('/country', methods=['POST'])
def get_country_data():
    data = json.loads(request.data)

    t_product = df_reader('t_product')
    t_market = df_reader('t_market')
    t_city = df_reader('t_city')
    t_province = df_reader('t_province')

    avg_df = t_product.filter((t_product.date == data['date']) & (t_product.variety_id == data['varietyId'])) \
        .join(t_market, t_product.market_id == t_market.id, 'left_outer') \
        .join(t_city, t_market.city_id == t_city.id, 'left_outer') \
        .join(t_province, t_city.province_id == t_province.id, 'left_outer') \
        .groupby("province_id") \
        .agg(f.avg('price').alias('avg_price'))

    avg_df = avg_df.join(t_province, avg_df.province_id == t_province.id).select("id", "name", "avg_price")

    return jsonify(avg_df.toJSON().map(lambda x: json.loads(x)).collect())


@bp.route('/province/<province_id>', methods=['POST'])
def get_province_data(province_id):
    data = json.loads(request.data)

    t_product = df_reader('t_product')
    t_market = df_reader('t_market')
    t_city = df_reader('t_city')

    avg_df = t_product.filter((t_product.date == data['date']) & (t_product.variety_id == data['varietyId'])) \
        .join(t_market, t_product.market_id == t_market.id, 'left_outer') \
        .join(t_city, t_market.city_id == t_city.id, 'left_outer') \
        .where(t_city.province_id == province_id) \
        .groupby("city_id") \
        .agg(f.avg('price').alias('avg_price'))

    avg_df = avg_df.join(t_city, avg_df.city_id == t_city.id).select("id", "name", "avg_price")

    return jsonify(avg_df.toJSON().map(lambda x: json.loads(x)).collect())


@bp.route('/city/<city_id>', methods=['POST'])
def get_city_data(city_id):
    data = json.loads(request.data)

    t_product = df_reader('t_product')
    t_market = df_reader('t_market')

    avg_df = t_product.filter((t_product.date == data['date']) & (t_product.variety_id == data['varietyId'])) \
        .join(t_market, t_product.market_id == t_market.id, 'left_outer') \
        .where(t_market.city_id == city_id) \
        .groupby("market_id") \
        .agg(f.avg('price').alias('avg_price'))

    avg_df = avg_df.join(t_market, avg_df.market_id == t_market.id).select("id", "name", "avg_price")

    return jsonify(avg_df.toJSON().map(lambda x: json.loads(x)).collect())
