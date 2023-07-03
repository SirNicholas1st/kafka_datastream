import random
import sys
import json
from datetime import datetime
from time import sleep
from cassandra.cluster import Cluster
from kafka import KafkaProducer

CASSANDRA_PORT = 9042
CASSANDRA_KEYSPACE = "kafka_datastream"
CASSANDRA_TABLE = "datastream_table"
KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC = "kafka-datastream"

try:
    # connection to kafka
    kafka_producer = KafkaProducer(bootstrap_servers = KAFKA_HOST, value_serializer = lambda v: json.dumps(v).encode("utf-8"))
    # connection to cassandra
    cassandra_cluster = Cluster(port = CASSANDRA_PORT)
    cassandra_session = cassandra_cluster.connect(keyspace = CASSANDRA_KEYSPACE)

except Exception as e:
    print(f"Error --> {e}")
    sys.exit()

create_table_query = f"CREATE TABLE IF NOT EXISTS {CASSANDRA_TABLE} (sensor_id TEXT, timestamp TIMESTAMP, temperature INT, rh FLOAT, PRIMARY KEY(sensor_id, timestamp));"
cassandra_session.execute(create_table_query)

while True:

    timestamp = datetime.utcnow().isoformat()

    sensor_1 = {
        "timestamp": timestamp,
        "temperature": random.randint(15, 30),
        "rh": round(random.random(), 2)
    }

    sensor_2 = {
        "timestamp": timestamp,
        "temperature": random.randint(20, 35),
        "rh": round(random.random(), 2)
    }

    kafka_producer.send(topic = KAFKA_TOPIC, key = b"sensor_1", value = sensor_1)
    kafka_producer.send(topic = KAFKA_TOPIC, key = b"sensor_2", value = sensor_2)
    sleep(random.randint(2, 4))
    