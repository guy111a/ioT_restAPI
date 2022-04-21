# distance calculation

import math
import time
import flask
from flask import Flask
import requests
from flask import request, jsonify
from pymysql import *
import sys
import pandas as pd
from flask import send_file
from flask import render_template

#apiUrl='http://xaviercat.com:8089/temperature?key=2022&act=&timeStamp=&temp='
apiKey = '2022'
db_name = "guy_temps"
port = '8094'
chart_template = 'chart_line.html'

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#db_opts = {'user': 'root', 'password': 'pass2014', 'host': '172.17.0.3', 'database': 'temprature'}


@app.route('/', methods=['GET'])
def home():
    return '<h1>Temperature data restAPI</1><p><a href="http://xaviercat.com:8094/temperature?key=2022&act=chart&act=chart&day=1"><h4>Take a look</h></a><p><h3> for details, contact &nbsp&nbsp<a href="mailto:guy@xaviercat.com">guy@xaviercat.com</a></p></h3><p>'


@app.route('/temperature', methods=['GET'])   # df2 = df["Fee"].mean()
def calculate():
    if 'key' in request.args:
        if str(request.args['key']) == apiKey:
            if 'act' in request.args:

                if str(request.args['act']) == 'avg':
                    connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                    with connection.cursor() as cursor:
                        if 'from' in request.args:
                            if 'to'  in request.args:
                                sql = f'select * from {db_name} where time_stamp between {str(request.args["from"])} and {str(request.args["to"])}'
                            else:
                                return 'Missing TO'
                        else:                         
                            sql = f"SELECT * FROM {db_name}"
                        cursor.execute(sql)
                        df = pd.read_sql(sql, connection)
                        print(df)
                        df2 = df["temp"].mean()
                        avg_value = str(df2)
                        connection.close()
                    return f'average value of Temp : {avg_value}'
                
                if str(request.args['act']) == 'min':
                    connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                    with connection.cursor() as cursor:
                        if 'from' in request.args:
                            if 'to'  in request.args:
                                sql = f'select min(temp), time_stamp, humid from {db_name} where time_stamp between {str(request.args["from"])} and {str(request.args["to"])}'
                            else:
                                return 'Missing TO'
                        else:                         
                            sql = f"SELECT   min(temp), time_stamp, humid FROM {db_name}"
                        result = cursor.execute(sql)
                        connection.commit()
                        r = []
                        for row in cursor:
                            r.append(row)
                            '''
                        df = pd.read_sql(sql, connection)
                        column = df["temp"]
                        index = df['temp'].idxmin()
                        min_value = str([index+1, column.min()]) '''
                        connection.close()
                    return str(r)
                
                if str(request.args['act']) == 'max':
                    connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                    with connection.cursor() as cursor:
                        if 'from' in request.args:
                            if 'to'  in request.args:
                                sql = f'select max(temp), time_stamp, humid from {db_name} where time_stamp between {str(request.args["from"])} and {str(request.args["to"])}'
                            else:
                                return 'Missing TO'
                        else:                         
                            sql = f"SELECT  max(temp), time_stamp, humid FROM {db_name}"
                        
                        result = cursor.execute(sql)
                        connection.commit()
                        r = []
                        for row in cursor:
                            r.append(row)
                            '''
                        df = pd.read_sql(sql, connection)
                        column = df["temp"]
                        timeStamp = df['time_stamp']
                        index = df['temp'].idxmax()
                        max_value = str([index+1, column.max()]) '''
                        connection.close()
                    return str(r)
                
                if str(request.args['act']) == 'save2file':
                    csv_file_path = f'/tmp/temp_data_{time.time()}.csv'
                    connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                    with connection.cursor() as cursor:
                        if 'from' in request.args:
                            if 'to'  in request.args:
                                sql = f'select * from {db_name} where time_stamp between {str(request.args["from"])} and {str(request.args["to"])}'
                            else:
                                return 'Missing TO'
                        else:                                
                            sql = f"SELECT * FROM {db_name}"
                            cursor.execute(sql)
                            df = pd.read_sql(sql, connection)
                            #print(df)
                            #data = '[{x:1, y:1}, {x:5, y:2}, {x:10, y:3}]'
                            df.to_csv(csv_file_path, sep=',', encoding='utf-8',index=False)                    
                            file_obj =csv_file_path
                            connection.close()
                    return send_file(file_obj, mimetype="text/csv", attachment_filename=csv_file_path, )
                
                if str(request.args['act']) == 'count':
                    r=[]
                    connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                    with connection.cursor() as cursor:
                        sql = f"SELECT count(*) FROM {db_name} ;"
                        result = cursor.execute(sql)
                        connection.commit()
                        for row in cursor:
                            r.append(row)
                        connection.close()
                    return str(r)
                
                if str(request.args['act']) == 'read':
                    r=[]
                    connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                    with connection.cursor() as cursor:
                        if 'day' in request.args:
                            days = request.args["day"]
                            timeStampTo = int(time.time())
                            timeStampFrom = int(timeStampTo)-(86413*int(days))
                            sql = f'select time_stamp, temp, humid from {db_name} where time_stamp between {str(timeStampFrom)} and {str(timeStampTo)} ORDER BY ID DESC ;'
                        else:
                            sql = f"SELECT * FROM {db_name} ORDER BY ID DESC LIMIT 1 ;"
                        print(sql)
                        result = cursor.execute(sql)
                        connection.commit()
                        for row in cursor:
                            r.append(f'<br>{row}')
                    connection.close()                    
                    return str(r)

                if str(request.args['act']) == 'readall':
                    r=[]
                    connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                    with connection.cursor() as cursor:
                        if 'from' in request.args:
                            if 'to'  in request.args:
                                sql = f'select * from {db_name} where time_stamp between {str(request.args["from"])} and {str(request.args["to"])}'
                            else:
                                return 'Missing TO'
                        else:
                             sql = f"SELECT * FROM {db_name} ;"
                        result = cursor.execute(sql)
                        connection.commit()
                        for row in cursor:
                            r.append(f'{row}<br>')
                        connection.close()
                    return str(r)
                
                if str(request.args['act']) == 'chart':
                    timeLine = []
                    tData = []
                    hData = []
                    connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                    with connection.cursor() as cursor:
                        if 'day' in request.args:
                            days = request.args["day"]
                            timeStampTo = int(time.time())
                            timeStampFrom = int(timeStampTo)-(86413*int(days))
                            sql = f'select time_stamp, temp, humid from {db_name} where time_stamp between {str(timeStampFrom)} and {str(timeStampTo)}'
                        else:
                            if 'from' in request.args:
                                if 'to'  in request.args:
                                    timeStampFrom =str(request.args["from"])
                                    timeStampTo = str(request.args["to"])
                                    sql = f'select time_stamp, temp, humid from {db_name} where time_stamp between {str(request.args["from"])} and {str(request.args["to"])}'
                                    max_x =str(request.args["from"])
                                    min_x = str(request.args["to"])
                                else:
                                    return 'Missing [TO]'
                            else:
                                 sql = f"SELECT temp, time_stamp, humid FROM {db_name} ;"
                        print(sql)
                        result = cursor.execute(sql)
                        rows = cursor.fetchall()
                        for row in rows:
                            # add a check, if temp is not bigger or smaller that 25% of AVG, else remove
                            timeLine.append(row["time_stamp"])
                            tData.append(row['temp'])
                            hData.append(row['humid'])
                            
                        df = pd.read_sql(sql, connection)
                        timeStampFrom = int(df['time_stamp'].min())
                        timeStampTo = int(df['time_stamp'].max())
                        print(f' timeStampFrom => {timeStampFrom}, timeStampTo => {timeStampTo}')
                        cold = df['temp'].min()
                        hot = df['temp'].max()
                    
                        sql = f"SELECT humid, temp FROM {db_name} ORDER BY ID DESC LIMIT 1 ;"
                        result = cursor.execute(sql)
                        connection.commit()
                        for row in cursor:
                            currentHumid = str((row['humid']))
                            currentTemp = str((row['temp']))
                        connection.close()

                    return render_template(chart_template, members=timeLine,  temp_values=tData, \
                                           humid_values=hData, max_x=timeStampTo, min_x=timeStampFrom,\
                                           min_y=str(cold), max_y=str(hot), sTime=str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timeStampFrom)))), \
                                           eTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(timeStampTo))), currentT=str(currentTemp), \
                                           currentH=str(currentHumid), currentTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))))
                
                if str(request.args['act']) == 'write':
                    if 'timeStamp' in request.args:
                        timeStamp =  str(request.args['timeStamp'])
                    if 'temp' in request.args:
                        temp = str(request.args['temp'])
                        if 'humid' in request.args:
                            humid = str(request.args['humid'])
                            connection = connect(host='172.17.0.3', user='root', password='pass2014', db='temprature', cursorclass=cursors.DictCursor)
                            with connection.cursor() as cursor:
                                sql = "INSERT INTO {} (temp, time_stamp, humid) VALUES (\'{}\', \'{}\', \'{}\')".format(db_name, temp, timeStamp, humid)
                                cursor.execute(sql)
                                connection.commit()
                    connection.close()
                    return 'Saved to DB'
            else:
                return 'Missing Action'
    else:
        return 'Missing Key'

app.run(host='0.0.0.0', port=port)
# app.run(host='0.0.0.0', port='8094')
c