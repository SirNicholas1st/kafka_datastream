import json
import sys
from cassandra.cluster import Cluster
from kafka import KafkaConsumer

CASSANDRA_PORT = 9042
CASSANDRA_KEYSPACE = "kafka_datastream"
CASSANDRA_TABLE = "datastream_table"
KAFKA_HOST = "localhost:9092"
KAFKA_TOPIC = "kafka-datastream"

try:
    # kafka connection
    kafka_consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers = KAFKA_HOST,
                            value_deserializer = lambda v: json.loads(v.decode("utf-8")))
    # cassandra connection
    cassandra_cluster = Cluster(port = CASSANDRA_PORT)
    cassandra_session = cassandra_cluster.connect(keyspace = CASSANDRA_KEYSPACE)
    
except Exception as e:
    print(f"Error --> {e}")
    sys.exit()

for message in kafka_consumer:
    sensor_id = message.key.decode("utf-8")
    message_values = message.value
    timestamp, temperature, rh = message_values["timestamp"], message_values["temperature"], message_values["rh"]
    
    insert_query = f"INSERT INTO {CASSANDRA_TABLE} (sensor_id, timestamp, temperature, rh) VALUES ('{sensor_id}', '{timestamp}', {temperature}, {rh});"
    cassandra_session.execute(insert_query)
