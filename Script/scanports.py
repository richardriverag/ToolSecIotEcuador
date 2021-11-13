
import threading
from queue import Queue
import time
import socket
  
# a print_lock is used to prevent "double"
# modification of shared variables this is
# used so that while one thread is using a
# variable others cannot access it Once it
# is done, the thread releases the print_lock.
# In order to use it, we want to specify a
# print_lock per thing you wish to print_lock.
print_lock = threading.Lock()
  
PortList = [22, 23, 25, 53, 80, 81, 110, 180, 443, 873, 2323, 5000, 5001, 5094, 5150, 5160, 7547, 8080, 8100, 8443, 8883, 49152, 52869, 56000,
                        1728, 3001, 8008, 8009, 10001, 223, 1080, 1935, 2332, 8888, 9100, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 21, 554, 888, 1159, 1160, 1161,
                        1435, 1518, 3389, 4550, 5005, 5400, 5550, 6550, 7000, 8000, 8081, 8090, 8150, 8866, 9000, 9650, 9999, 10000, 18004, 25001, 30001, 34567, 37777,
                        69, 135, 161, 162, 4786, 5431, 8291, 37215, 53413]

# ip = socket.gethostbyname(target)
target = 'localhost'
  
def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target, port))
        with print_lock:
            print('port is open', port)
        con.close()
    except:
        print('port is close', port)
  
  
# The threader thread pulls a worker 
# from a queue and processes it
def threader():
    while True:
        # gets a worker from the queue
        worker = q.get()
  
        # Run the example job with the available 
        # worker in queue (thread)
        portscan(worker)
  
        # completed with the job
        q.task_done()
  
  
# Creating the queue and threader
q = Queue()
  
# number of threads are we going to allow for
for x in range(4):
    t = threading.Thread(target=threader)
  
    # classifying as a daemon, so they it will
    # die when the main dies
    t.daemon = True
  
    # begins, must come after daemon definition
    t.start()
  
  
start = time.time()
  
# 10 jobs assigned.
for worker in PortList:
    q.put(worker)
  
# wait till the thread terminates.
q.join()