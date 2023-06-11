import json

import pyspark.sql.functions as f
from flask import Blueprint, jsonify, request

from app.spark import df_reader

bp = Blueprint('sell_bp', __name__, url_prefix='/sell')


@bp.route('/year', methods=['POST'])
def get_year_sell_date():
    data = json.loads(request.get_data())

    t_product = df_reader('t_product')
    df = t_product.filter((t_product.date >= data['dateRange'][0]) & (t_product.date <= data['dateRange'][1])
                          & (t_product.variety_id == data['varietyId'])
                          & (t_product.market_id == data['marketId'])).withColumn('year', f.year(t_product.date)) \
        .groupby('year').agg(f.sum('sell_number').alias('sum'))

    return jsonify(df.toJSON().map(lambda x: json.loads(x)).collect())


@bp.route('/month', methods=['POST'])
def get_month_sell_date():
    data = json.loads(request.get_data())

    t_product = df_reader('t_product')
    df = t_product.filter((t_product.date >= data['dateRange'][0]) & (t_product.date <= data['dateRange'][1])
                          & (t_product.variety_id == data['varietyId'])
                          & (t_product.market_id == data['marketId'])).withColumn('year', f.year(t_product.date))\
        .withColumn('month', f.month(t_product.date)) \
        .groupby('month', 'year').agg(f.sum('sell_number').alias('sum'))

    return jsonify(df.toJSON().map(lambda x: json.loads(x)).collect())


@bp.route('/day', methods=['POST'])
def get_day_sell_date():
    data = json.loads(request.get_data())

    t_product = df_reader('t_product')
    df = t_product.filter((t_product.date >= data['dateRange'][0]) & (t_product.date <= data['dateRange'][1])
                          & (t_product.variety_id == data['varietyId'])
                          & (t_product.market_id == data['marketId']))
    return jsonify(df.toJSON().map(lambda x: json.loads(x)).collect())
