import json
import common
import numpy
import socket
import threading

def StorePose(pose, humans):

    list0 = list()
    dict0 = dict()
    dict1 = dict()

    # Init dict1
    try:
        with open('tf-openpose/pose_data.json', 'r') as fpr:
            dict1 = json.load(fpr)
            
    except:
        dict1[pose] = list()

    for i in range(common.CocoPart.Background.value):
        if i not in humans[0].body_parts.keys():
            continue
        
        list0.append(humans[0].body_parts[i].x)
        list0.append(humans[0].body_parts[i].y)
        dict0[i] = list0
        list0 = list()

    dict1[pose].append(dict0)

    # Store
    with open('tf-openpose/pose_data.json', 'w') as fpw:

        json.dump(dict1, fpw, sort_keys=True, indent=4)

        
def CalCorrel(pose, humans, filePath):

    with open(filePath, 'r') as fpr:
        dict1 = json.load(fpr)

    list0 = list()
    list1 = list()
    list2 = list()
    list3 = list()

    correl = 0

    # Return correlation 0 while no human detected
    if not len(humans):
        print('No person in sight')
        return 0
    
    for item in dict1[pose]:
        for key in range(common.CocoPart.Background.value):
            
            if key not in humans[0].body_parts.keys() or str(key) not in item.keys():
                continue

            # Add x,y coordinate
            list0.append(item[str(key)][0])
            list1.append(humans[0].body_parts[key].x)
            list2.append(item[str(key)][1])
            list3.append(humans[0].body_parts[key].y)

        # Get value from these two-dimensional arrays
        correlX = numpy.corrcoef(list0, list1)[0][1]
        correlY = numpy.corrcoef(list2, list3)[0][1]
        tmpCorrel = min(abs(correlX), abs(correlY))
        correl = max(tmpCorrel, correl)

        # Reinitiate lists
        list0 = list()
        list1 = list()
        list2 = list()
        list3 = list()
        
    print(correl)

    return correl


def InitTCPServer():
    
    host = '127.0.0.1'
    port = 12345
    sockIns = socket.socket()

    # Allow reuse tcp port
    sockIns.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sockIns.bind((host, port))
    sockIns.listen(1)

    # Start tcp server thread
    threading.Thread(target=StartTCPServ, args=(sockIns,)).start()


def StartTCPServ(sockIns):

    global ifMMWave
    global processDone
    
    print('TCP server started, waiting for mmwave ...')
    while True:
        conn, addr = sockIns.accept()

        with conn:
            data = conn.recv(1024)
            if data.decode() == 'mmwave_true':

                print('MMWave OK!')

                # Set ifMMWave to 1
                ifMMWave = 1

                # Block if process isn't done
                while not processDone:
                    # time.sleep(0.1)
                    pass
                
                # Feedback to mmwave
                conn.send('OK'.encode())

                # Fallback ifMMWave
                ifMMWave = 0


import argparse
import logging
import time

import cv2
import numpy as np

from estimator import TfPoseEstimator
from networks import get_graph_path, model_wh

logger = logging.getLogger('TfPoseEstimator-WebCam')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

fps_time = 0

# Bool variable for reminding by mmwave
global ifMMWave
ifMMWave = 0

# If process done
global processDone
processDone = 0

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='tf-pose-estimation realtime webcam')
    parser.add_argument('--camera', type=int, default=0)
    parser.add_argument('--zoom', type=float, default=1.0)
    parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin')
    parser.add_argument('--show-process', type=bool, default=False,help='for debug purpose, if enabled, speed for inference is dropped.')
    parser.add_argument('--pose', type=str, default='extend', help='specify pose to record')
    parser.add_argument('--operation', type=str, default='calc', help='specify if store pose data or calculate correlation')
    args = parser.parse_args()

    logger.debug('initialization %s : %s' % (args.model, get_graph_path(args.model)))
    w, h = model_wh(args.resolution)
    e = TfPoseEstimator(get_graph_path(args.model), target_size=(w, h))
    cam = cv2.VideoCapture(args.camera)

    # Set camera properties
    # cam.set(3, 432)
    # cam.set(4, 368)

    # Initial tcp server
    InitTCPServer()

    while True:

        # Block while no signal comes from mmwave
        while not ifMMWave:
            # time.sleep(0.01)
            pass

        # Fallback to previos value
        ifMMWave = 0

        logger.debug('cam read+')
        ret_val, image = cam.read()
        logger.info('cam image=%dx%d' % (image.shape[1], image.shape[0]))
        logger.debug('image preprocess+')
        if args.zoom < 1.0:
            canvas = np.zeros_like(image)
            img_scaled = cv2.resize(image, None, fx=args.zoom, fy=args.zoom, interpolation=cv2.INTER_LINEAR)
            dx = (canvas.shape[1] - img_scaled.shape[1]) // 2
            dy = (canvas.shape[0] - img_scaled.shape[0]) // 2
            canvas[dy:dy + img_scaled.shape[0], dx:dx + img_scaled.shape[1]] = img_scaled
            image = canvas
        elif args.zoom > 1.0:
            img_scaled = cv2.resize(image, None, fx=args.zoom, fy=args.zoom, interpolation=cv2.INTER_LINEAR)
            dx = (img_scaled.shape[1] - image.shape[1]) // 2
            dy = (img_scaled.shape[0] - image.shape[0]) // 2
            image = img_scaled[dy:image.shape[0], dx:image.shape[1]]

        logger.debug('image process+')
        humans = e.inference(image)


        # Custom cy
        if cv2.waitKey(1) == ord('s'):
            
            # Decide if store pose data or calculate correlation
            if args.operation == 'store':
            
                # Store pose data
                StorePose(args.pose, humans)
                print('Pose stored!')

        if args.operation== 'calc':

            # Calculate correlation, judgement
            correl = CalCorrel(args.pose, humans, 'tf-openpose/pose_data.json')
            if correl > 0.8:
                # PushToCloud(image)
                print('A person tumbled, pushing to cloud!')
                for num in range(10):
                    print('*****************************')
                    print()
                time.sleep(4)

        logger.debug('postprocess+')
        image = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        logger.debug('show+')
        print('FPS: ', (1.0 / (time.time() - fps_time)))

        '''
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        '''
        
        # cv2.imshow('tf-pose-estimation result', image)
        
        fps_time = time.time()
        
        if cv2.waitKey(1) == 27:
            break

        # Process done
        processDone = 1
        
        logger.debug('finished+')

    # cv2.destroyAllWindows()
