from flask import Flask, request
from datetime import datetime
import json 

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


app = Flask(__name__)

token = "b7VLnKqmR_ggkwmgMVKTHOp1tXY10X5I10srY6huoSH8t-XBnpPtcX3Mj592ZTZpVcUFDSB7uFlMYzXpXaOmYA=="
org = "my-org"
bucket = "testing-bucket"

client = InfluxDBClient(url="http://localhost:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

@app.route('/', methods = ['GET','POST'])
def index():
    value = request.json
 #   f = open('data.json',)
    data = value
    column_name = next(iter(data))

    word_list=[]

    word = ''

    for i in range(len(data[column_name])):
        for k, v in data[column_name][i].items():
            part = k + "=" + v + ' '
            word = word + part
        word = column_name + ',' + word
        word_list.append(word)
        word = ''

    sequence = word_list

    print(sequence)

    isi = []

    for i in range(len(data[column_name])):
        isi.append(data[column_name][i])


    #sequence = ['baru3,host=host1 used_percent=23.43234543 ',
    #            'baru3,host=host1 available_percent=15.856523 ']
 
    write_api.write(bucket, org, sequence)

    return "Success \n " + column_name + "," + str(isi)

if __name__ == '__main__':
    app.run(debug=True)