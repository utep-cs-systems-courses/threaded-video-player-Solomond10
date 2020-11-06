#!/usr/bin/env python3

import cv2
import os
import time
import threading
import queue

def extract(clipFileName, q1, maxFramesToLoad=9999):

    # initialize frame count
    count = 0
    
    # open the video clip
    vidcap = cv2.VideoCapture(clipFileName)

    # read one frame
    success,image = vidcap.read()

    print(f'Reading frame {count} {success}')

    while success and count < maxFramesToLoad:
            
            success, jpgImage = cv2.imencode('.jpg', image)

            # add the frame to queue 1
            put(q1,image)
            success,image = vidcap.read()
            print(f'Reading frame {count} {success}')
            count += 1

    print("Extraction Complete")
    
def convert(q1, q2, maxFramesToLoad=9999):

    # initialize frame count
    count = 0
   
    while q1 is not None and count < maxFramesToLoad:
    
        print(f'Converting frame {count}')
        
        # convert the image to grayscale

        grayscaleFrame = cv2.cvtColor(get(q1), cv2.COLOR_BGR2GRAY)
            
        # Get next frame
        count += 1
    
        # Queue 2 is written to
        put(q2,grayscaleFrame)
        
        
    print("Conversion Complete")
    
def display(q2):

    # initialize frame count
    count = 0

    while q2 is not None:
    
        frame = get(q2)
        
        print(f'Displaying frame {count}')        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if (cv2.waitKey(42) and 0xFF == ord("q")) or q2.empty() is True:
            break
         
        count += 1

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()
        
    print("Display Complete")

def put(queue,item):

    if queue == queue1:
        emptyQ1.acquire()
        mutexQ1.acquire()
        queue.put(item)
        mutexQ1.release()
        fullQ1.release()


    else:
        emptyQ2.acquire()
        mutexQ2.acquire()
        queue.put(item)
        mutexQ2.release()
        fullQ2.release()
        
def get(queue):

    if queue == queue1:
        fullQ1.acquire()
        mutexQ1.acquire()
        im = queue.get()
        mutexQ1.release()
        emptyQ1.release()
        
    else:
        fullQ2.acquire()
        mutexQ2.acquire()
        im = queue.get()
        mutexQ2.release()
        emptyQ2.release()

    return im

mutexQ1 = threading.Lock()
mutexQ2 = threading.Lock()

emptyQ1 = threading.BoundedSemaphore(24)
fullQ1 = threading.Semaphore(0)
emptyQ2 = threading.BoundedSemaphore(24)
fullQ2 = threading.Semaphore(0)

fileName = 'clip.mp4'
framesToLoad = 400

queue1 = queue.Queue()
queue2 = queue.Queue()

thread1 = threading.Thread(target = extract, args = (fileName, queue1, framesToLoad))
thread2 = threading.Thread(target = convert, args = (queue1, queue2, framesToLoad))
thread3 = threading.Thread(target = display, args = (queue2,))

thread1.start()
thread2.start()
thread3.start()
