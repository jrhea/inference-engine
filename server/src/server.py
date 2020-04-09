from flask import Flask,request,Response,jsonify
from flask_cors import CORS
import subprocess
import os
import sys
import errno
import time
from multiprocessing import Pool
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Webserver is running';

@app.route('/inference/<model>',methods=['POST'])
def inference(model):
    commands = ['output','input']
    fifos = ['./tmp/' + model + '-output','./tmp/' + model + '-input'];
    image = request.json['image'];
    images = [None,image];
    params = [[commands[0],fifos[0],images[0]],[commands[1],fifos[1],images[1]]];
    pool = Pool();
    result = pool.map(doIO,params)[0];
    pool.close()
    pool.join()
    #return Response(json.loads(result.replace('\'','\"')),mimetype='application/json');
    return jsonify(result);

def doIO(params):
    result = '';
    command = params[0];
    fifo = params[1];
    image = params[2];
    if command == 'output':
        result = readOutput(fifo);
    elif command == 'input':
        result = sendInput(fifo,image);
    return result;

def sendInput(fifo,image):
    #time.sleep(.500);
    with open(fifo,'w') as f:
        f.write(image+'\n');
    return None;

def readOutput(fifo):
    result = [];
    bufferSize = 1000;
    pipe = os.open(fifo,os.O_RDONLY | os.O_NONBLOCK);
    
    while 1:
        try:
            #pipe = os.open(fifo,os.O_RDONLY | os.O_NONBLOCK);
            data = os.read(pipe,bufferSize).decode('utf-8');
            if len(data) > 1 and "confidence" in data:
                data = data.split('\r\n');
                result = [i for i,s in enumerate(data) if "confidence" in s];
                result = data[result[0]];
                
        except OSError as err:
            if err.errno != 11:
                raise err;
        #os.close(pipe)       
        
        if len(result)  > 0:
            break;
        
    return result






if __name__== "__main__":
    app.run(host="0.0.0.0",port="8080", threaded=True);
#    cwd = os.getcwd();
#    model='wind';
#    image = './tests/%(model)s/havey_damage_tl_1.png' % {'model':model};
#    result = inference(model,image);
#    print(result);
