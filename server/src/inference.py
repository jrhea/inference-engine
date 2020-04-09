import scipy
import numpy as np
import caffe
import os.path
import sys
import time
from PIL import Image
import io
import base64

#caffe.set_mode_cpu()

def initialize_model(model_file,pretrained_file,labels_file):
    """
    Load caffe.Net model with layers
    """

    # Load model files from user collections
    #model_file = "models/20180724_epoch_60/deploy.prototxt"
    #pretrained_file = "models/20180724_epoch_60/snapshot_iter_6540.caffemodel"
    #labels_file = "models/20180724_epoch_60/labels.txt"

    # Create net and load weights
    net = caffe.Classifier(model_file,pretrained_file);
    
    labels  =  open(labels_file).read().split('\n');

    return net,labels;



def top_k(elements, labels, k = 5): 
    top = elements.argsort()[-k:][::-1];
    probs = elements[top];
    return zip(probs, np.array(labels)[top]);
    
# API calls will begin at the apply() method, with the request body passed as 'input'
def detect(net,labels,input_file):
    """
    Input is an image file
    """
    #image = np.moveaxis(np.array(scipy.misc.imread(input_file), dtype=np.int), 2, 0);
    image_bytes = io.BytesIO(base64.b64decode(input_file));
    image = np.moveaxis(np.array(Image.open(image_bytes)), 2, 0);
    out = net.forward(data=np.asarray([image]));
    prob = net.blobs['softmax'].data[0];
    foo = top_k(prob, labels, k = 2);
    output = [];
    for prob, label in foo:
        result = {};
        result['label'] = label;
        result['confidence'] = str(prob);
        output.append(result);
    
    return output;

if __name__== "__main__":
    result = "";
    
    # Load model files from user collections
    model_file = sys.argv[1]
    pretrained_file = sys.argv[2]
    labels_file = sys.argv[3]
    
    net,labels=initialize_model(model_file,pretrained_file,labels_file);
    
    while True:
        user_input = raw_input("Please provide the path to a new image (Press q to exit):")
        print user_input
        start = time.time()
        
        
        
        if user_input != 'q':
            result = detect(net,labels,user_input);
            end = time.time()
            print "Elapsed: ", str(end-start)
            print result
        else:
            break;
