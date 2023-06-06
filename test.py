from retransmission_contorole import RTO, RETRANSMISSION_CONTROLE
import random
import pylab
import threading
import socket 

def rto_tests():
    rto_func = RTO()

    random_time_max = [random.uniform(0.01, 0.8) for i in range(100)]
    random_time_min = [random.uniform(0.01, 0.4) for i in range(100)]
    
    random_time_max = random_time_max + random_time_min
    

    his = []
    c = 0
    for t in random_time_max:
        rto_func.resolve_srtt(t)
        resolve = rto_func.resolve_rto()
         
        his.append(resolve)
    
    
    print(his)
    pylab.plot(his)
    pylab.show()



def retransmission_contorole_t():
    dstaddr = ("127.0.0.1", 1234)

    sockdg = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockdg2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    func = RETRANSMISSION_CONTROLE(sockdg, dstaddr)
    func2 = RETRANSMISSION_CONTROLE(sockdg2, dstaddr)

    func2_th = threading.Thread(target=func2.retr_ctl_recv)
    func2_th.start() 

    for _ in range(100):
        func.retr_ctl_send()
    return 

retransmission_contorole_t()
