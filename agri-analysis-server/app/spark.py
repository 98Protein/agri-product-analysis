import yaml
from pyspark import SparkConf
from pyspark.sql import SparkSession

app_name = "agri-analysis-spark"
master = "local[*]"

conf = SparkConf().setAppName(app_name).setMaster(master)
spark = SparkSession.builder.config(conf=conf).getOrCreate()
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")


mysql_config = {}
mysql_url = ""


def init_sql(config_name):
    global mysql_config
    global mysql_url
    mysql_config = yaml.load(open('app/config/database.secret.yml'),
                             Loader=yaml.SafeLoader)[config_name]['database']
    mysql_url = f"{mysql_config['jdbc']}://{mysql_config['host']}:{mysql_config['port']}/{mysql_config['database']}"


def df_reader(table, column=None, lower_bound=None, upper_bound=None, num_partitions=None,
              predicates=None):
    global mysql_config
    global mysql_url
    return spark.read.jdbc(
        url=mysql_url,
        table=table,
        column=column,
        lowerBound=lower_bound,
        upperBound=upper_bound,
        numPartitions=num_partitions,
        predicates=predicates,
        properties={
            'user': mysql_config['username'],
            'password': mysql_config['password']
        }
    )
