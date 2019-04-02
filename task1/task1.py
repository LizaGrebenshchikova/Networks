from threading import Thread
import time
import random
    
buffer = [None] * 128
busy = False
clock_time = 51.2 * 10 ** -6

def send_frame(idx, frame):
    global buffer, busy, clock_time
    
    sent = False
    attempt = 1    
    while not sent:
        while busy:
            time.sleep(clock_time)
            
        busy = True            
        print('agent', idx, 'starts sending frame at time', time.time())              
        byte = 0
        while byte < len(frame):
            if frame[: byte] == buffer[: byte]:
                buffer[byte] = frame[byte]
                byte += 1
            else:
                if attempt > 15:
                    print('run out of attempts')
                    return
                
                for i in range(random.randint(0, 16)):
                    time.sleep(clock_time)
                attempt += 1
                break
        else:                
            sent = True
            print('agent', idx, 'ends sending frame at time', time.time())        
            busy = False

if __name__ == '__main__':
    threads = []
    for i in range(4):
        frame = 'Frame for agent ' + str(i)
        thread = Thread(target=send_frame, args=(i, list(frame)))
        threads.append(thread)
        thread.start()
        
    for i in range(4):
        threads[i].join()