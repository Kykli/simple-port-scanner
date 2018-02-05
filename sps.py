import sys
import socket
import threading
import time
from datetime import datetime
from queue import Queue

print_lock = threading.Lock()

try:
    print("[#] ----------Simple-Port-Scanner----------")
    print("[#]\n[#] 1. Scan")
    print("[#] 0. Exit")
    choice = input("[#]\n[#] What do you want to do?: ")

    if choice == "1":
        target = input("[#]\n[#] Enter Target Host Address: ")
        startp = int(input("[#] Enter Starting Port: "))
        endp = int(input("[#] Enter Ending Port: "))
        print("[#]\n[#] Scanning:\n[#]")

        def portscan(port):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                connection = s.connect((target,port))
                with print_lock:
                    print("[#] Port",port,"is open!")
                connection.close()
            except:
                pass

        def threader():
            while True:
                worker = q.get()
                portscan(worker)
                q.task_done()

        q = Queue()

        for x in range(30):
            t = threading.Thread(target=threader)
            t.daemon = True
            t.start()

        start_time = datetime.now()

        for worker in range(startp, endp):
            q.put(worker)

        q.join()

        stop_time = datetime.now()
        total_time = stop_time - start_time
        print("\n[#] Scanning Finished At", time.strftime("%a, %d %b %Y %H:%M:%S"))
        print("[#] Scanning Duration:", total_time)

    elif choice == "0":
        sys.exit(0)

except KeyboardInterrupt:
    print("\n[#] Aborting!")
    sys.exit(0)
