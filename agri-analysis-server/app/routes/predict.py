import json

import pandas
from flask import Blueprint, request, jsonify
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from prophet import Prophet
from app.spark import df_reader

bp = Blueprint('predict_bp', __name__)


@bp.route('/predict', methods=['POST'])
def get_predict_data():
    data = json.loads(request.get_data())

    t_product = df_reader('t_product').alias('t_product')
    total_df = t_product.filter(
        (t_product.date >= data['dateRange'][0]) & (t_product.date <=
                                                    (parse(data['dateRange'][1], fuzzy=True) + relativedelta(
                                                        days=10)).strftime('%Y-%m-%d')) & (
                t_product.market_id == data['marketId'])
        & (t_product.variety_id == data['varietyId'])).select('date', 'price') \
        .withColumnRenamed('date', 'ds').withColumnRenamed('price', 'y')
    history_df = total_df.filter(total_df.ds <= data['dateRange'][1])
    if history_df.count() == 0:
        return jsonify({
            'history': [],
            'predict': []
        })

    model = Prophet(
        growth='linear',
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=False,
        seasonality_mode='multiplicative'
    )

    model.fit(history_df.toPandas())

    future_pd = model.make_future_dataframe(
        periods=data['predictDays'],
        freq='d',
        include_history=False
    )

    forecast_pd = pandas.DataFrame(model.predict(future_pd), columns=['ds', 'yhat'])
    return jsonify({
        'history': total_df.toJSON().map(lambda x: json.loads(x)).collect(),
        'predict': json.loads(forecast_pd.to_json(orient='records'))
    })
