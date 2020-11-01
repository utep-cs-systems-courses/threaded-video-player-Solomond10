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

            semaphore.acquire()
            
            success, jpgImage = cv2.imencode('.jpg', image)

            # add the frame to queue 1
            q1.put(image)

            success,image = vidcap.read()
            print(f'Reading frame {count} {success}')
            count += 1

            semaphore.release()

    print("Extraction Complete")
    
def convert(q1, q2, maxFramesToLoad=9999):

    # initialize frame count
    count = 0
   
    while q1 is not None and count < maxFramesToLoad:

        semaphore.acquire()
        print(f'Converting frame {count}')
        
        # convert the image to grayscale
        grayscaleFrame = cv2.cvtColor(q1.get(), cv2.COLOR_BGR2GRAY)
        # Get next frame
        count += 1
    
        # Queue 2 is written to
        q2.put(grayscaleFrame)
        semaphore.release()
        
    print("Conversion Complete")
    
def display(q2):

    # initialize frame count
    count = 0

    while q2 is not None:
        semaphore.acquire()
        # get the next frame
        frame = q2.get()

        print(f'Displaying frame {count}')        

        # display the image in a window called "video" and wait 42ms
        # before displaying the next frame
        cv2.imshow('Video', frame)
        if (cv2.waitKey(42) and 0xFF == ord("q")) or q2.empty() is True:
            break
        
        semaphore.release()
    
        count += 1

    # make sure we cleanup the windows, otherwise we might end up with a mess
    cv2.destroyAllWindows()
        
    print("Display Complete")

#Bounded Semaphore ensures that there is a limit on the amount of stuff placed inside the queue
#and that an empty queue is never read from   
semaphore = threading.BoundedSemaphore(3)
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
