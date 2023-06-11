source venv/bin/activate
# 启动 hadoop 和 Spark
start-all.sh
/usr/local/spark/sbin/start-all.sh
export FLASK_APP=app
export FLASK_ENV=development
# 启动后端项目
flask run
