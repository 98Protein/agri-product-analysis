import json
import subprocess

from flask import Blueprint, jsonify, request

from app.models.market import Market
from app.models.product import Product
from app.models.type import Type
from app.models.variety import Variety
from app.spark import df_reader

bp = Blueprint('monitor_bp', __name__, url_prefix='/monitor')


@bp.route('/basic', methods=['GET'])
def basic_info():
    return jsonify({
        'marketTotal': Market.query.count(),
        'typeTotal': Type.query.count(),
        'varietyTotal': Variety.query.count(),
        'productTotal': Product.query.count(),
    })


@bp.route('/crawls', methods=['POST'])
def get_crawls():
    data = json.loads(request.data)

    t_product = df_reader('t_product')
    t_variety = df_reader('t_variety')
    t_type = df_reader('t_type')

    count_df = t_product.filter(
        (t_product.date >= data['dateRange'][0]) & (t_product.date <= data['dateRange'][1])
        & (t_product.market_id == data['market'])) \
        .join(t_variety, t_product.variety_id == t_variety.id, 'left_outer') \
        .join(t_type, t_variety.type_id == t_type.id).groupby('date', "type_id").count()

    count_df = count_df.select("date", "type_id", "count")

    return jsonify(count_df.toJSON().map(lambda x: json.loads(x)).collect())


@bp.route('/scrapy', methods=['POST'])
def run_scrapy():
    data = json.loads(request.data)  # 获取请求数据
    start_date = data['timeRange'][0]
    end_date = data['timeRange'][1]

    if not start_date or not end_date:  # 检查是否接收到正确的数据
        return jsonify({'success': False, 'message': 'Missing start or end date'}), 400

    # 构造 scrapy 命令
    cmd = f'. venv/bin/activate && scrapy crawl all_product -a start={start_date} -a end={end_date}'

    try:
        # 使用 Popen 启动进程，并保存进程对象
        subprocess.Popen(cmd, shell=True, cwd='../agri-analysis-spider')
        return jsonify({'success': True, 'message': 'Scrapy command ran successfully'}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'message': f'Scrapy command failed: {str(e)}'}), 500


@bp.route('/stop_scrapy', methods=['POST'])
def stop_scrapy():
    try:
        while True:
            result = subprocess.run(['pkill', '-f', 'agri-analysis-spider'], capture_output=True)
            if result.returncode != 0:
                break
        return jsonify({'success': True, 'message': 'Scrapy command stopped successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Failed to stop scrapy command: {str(e)}'}), 500
