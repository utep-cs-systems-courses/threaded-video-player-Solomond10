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
            print("Q!")
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

        print("We're in Q1 - PUT")
        emptyQ1.acquire()
        mutex.acquire()
        queue.put(item)
        mutex.release()
        fullQ1.release()


    else:
        print("We're in Q2 - PUT")
        emptyQ2.acquire()
        mutex.acquire()
        queue.put(item)
        mutex.release()
        fullQ2.release()
        
def get(queue):

    if queue == queue1:

        print("We're in Q1 - GET")
        emptyQ1.acquire()
        mutex.acquire()
        queue.get()
        mutex.release()
        fullQ1.release()

    else:
        print("We're in Q2 - GET")
        emptyQ2.acquire()
        mutex.acquire()
        queue.get()
        mutex.release()
        fullQ2.release()
    
#Bounded Semaphore ensures that there is a limit on the amount of stuff placed inside the queue
#and that an empty queue is never read from   

mutex = threading.Lock()
emptyQ1 = threading.BoundedSemaphore(24)
fullQ1 = threading.BoundedSemaphore(0)
emptyQ2 = threading.BoundedSemaphore(24)
fullQ2 = threading.BoundedSemaphore(0)

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
