import mysql.connector
import json
import pandas as pd

cnx = mysql.connector.connect(user='Kan_1962', password='7SPxJWFE',
                              host='api.awareframework.com',
                              database='Kan_1962')

cursor = cnx.cursor()

device_id = "'2bb0b3f1-23db-4e57-a8bb-a5cdc03d784d'"

query = ("SELECT timestamp, data FROM ball_game WHERE device_id = {}".format(device_id))
cursor.execute(query)
lista = [(item[0], json.loads(item[1])["gamedata"][0]["score"]) for item in cursor]

query = ("SELECT timestamp FROM medication WHERE device_id = {}".format(device_id))
cursor.execute(query)
cnx.close()

lista2 = [item[0] for item in cursor]

df = pd.DataFrame(lista).rename(columns={0: "timestamp", 1: "score"})
df = df.join(pd.DataFrame(lista2, columns=["timestamp_medication"]))
df["timestamp"] = pd.to_datetime(df['timestamp'],unit='ms')
df["timestamp"] = df["timestamp"] + pd.Timedelta(hours=2)
df["timestamp_medication"] = pd.to_datetime(df['timestamp_medication'],unit='ms')
df["timestamp_medication"] = df["timestamp_medication"] + pd.Timedelta(hours=2)

#iplot([go.Scatter(x=df["timestamp"], y=df["score"])])