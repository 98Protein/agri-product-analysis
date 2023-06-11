import json
from functools import reduce

import pyspark.sql.functions as f
from flask import Blueprint, jsonify, request

from app.spark import df_reader

bp = Blueprint('compare_bp', __name__, url_prefix='/compare')


@bp.route('/price', methods=['POST'])
def get_compare_data():
    data = json.loads(request.data)
    if data.get('items', None) is None or len(data['items']) == 0:
        return '[]'
    if data.get('dateRange', None) is None:
        return '[]'

    t_product = df_reader('t_product').alias('t_product')
    t_variety = df_reader('t_variety').withColumnRenamed("name", "variety_name").alias('t_variety')
    t_market = df_reader('t_market').withColumnRenamed("name", "market_name").alias('t_market')
    count_df = t_product.filter((t_product.date >= data['dateRange'][0]) & (t_product.date <= data['dateRange'][1]))

    count_df = count_df.filter(
        reduce(
            lambda x, y: x | y,
            [
                ((f.col('market_id') == item['marketId']) & (f.col('variety_id') == item['varietyId']))
                for item in data['items']
            ]
        )
    )

    count_df = count_df.join(t_variety, t_product.variety_id == t_variety.id, 'left_outer') \
        .join(t_market, t_product.market_id == t_market.id, 'left_outer') \
        .select("t_product.id", "t_product.variety_id", "t_product.market_id", "t_product.price", "t_product.date",\
                "t_market.market_name", "t_variety.variety_name")

    return jsonify(count_df.toJSON().map(lambda x: json.loads(x)).collect())
