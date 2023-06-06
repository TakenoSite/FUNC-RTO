import socket 
import struct
import threading
import time
import random

"""
  RFC 793 
                     RANSMISSION CONTROL PROTOCOL

                         DARPA INTERNET PROGRAM

                         PROTOCOL SPECIFICATION

  
  acknowledgment it advances SND.UNA.  The extent to which the values of
  these variables differ is a measure of the delay in the communication.
  The amount by which the variables are advanced is the length of the
  data in the segment.  Note that once in the ESTABLISHED state all
  segments must carry current acknowledgment information.

  The CLOSE user call implies a push function, as does the FIN control
  flag in an incoming segment.

  Retransmission Timeout

  Because of the variability of the networks that compose an
  internetwork system and the wide range of uses of TCP connections the
  retransmission timeout must be dynamically determined.  One procedure
  for determining a retransmission time out is given here as an
  illustration.

    An Example Retransmission Timeout Procedure

      Measure the elapsed time between sending a data octet with a
      particular sequence number and receiving an acknowledgment that
      covers that sequence number (segments sent do not have to match
      segments received).  This measured elapsed time is the Round Trip
      Time (RTT).  Next compute a Smoothed Round Trip Time (SRTT) as:

        SRTT = ( ALPHA * SRTT ) + ((1-ALPHA) * RTT) 

      and based on this, compute the retransmission timeout (RTO) as:

        RTO = min[UBOUND,max[LBOUND,(BETA*SRTT)]]

      where UBOUND is an upper bound on the timeout (e.g., 1 minute),
      LBOUND is a lower bound on the timeout (e.g., 1 second), ALPHA is
      a smoothing factor (e.g., .8 to .9), and BETA is a delay variance
      factor (e.g., 1.3 to 2.0).

  The Communication of Urgent Information

  The objective of the TCP urgent mechanism is to allow the sending user
  to stimulate the receiving user to accept some urgent data and to
  permit the receiving TCP to indicate to the receiving user when all
  the currently known urgent data has been received by the user.

  This mechanism permits a point in the data stream to be designated as
  the end of urgent information.  Whenever this point is in advance of
  the receive sequence number (RCV.NXT) at the receiving TCP, that TCP
  must tell the user to go into "urgent mode"; when the receive sequence
  number catches up to the urgent pointer, the TCP must tell user to go
    

   +---------------------------------SAMPLE-----------------------------------------+

   
    alpha = 0.8   # ALPHA is a smoothing factor (e.g., .8 to .9), 
    beta = 2.0    # 
    ubound = 3    # UBOUND is an upper bound on the timeout (e.g., 1 minute),
    lbound = 0.01 # LBOUND is a lower bound on the timeout (e.g., 1 second)
    
    rtt = [random.uniform(0.01, 0.8) for i in range(1000)] # dummy response time
    srtt = [0.0]
    for i in range(1, 1000):
        srtt.append(alpha * srtt[i-1] + ((1 - alpha) * rtt[i]))
    
    rto = [round(min(ubound, max(lbound, beta*srtt[i])), 3) for i in range(1000)]
    
 +---------------------------------------------------------------------------------+
 
"""


class RTO:
    def __init__(self):
        self.rto = 0
        self.alpha = 0.8
        self.beta = 2.0
        self.ubound = 10
        self.lbound = 1.0e-04
    
        self.rtt = []
        self.rtt_len = 0
        self.srtt = [0.1, 0.1]

    def resolve_srtt(self, t:float)->float:
        self.rtt.append(t)
        self.rtt_len = len(self.rtt)
        
        if self.rtt_len < 2:
            return  
        
        self.srtt.append(self.alpha * self.srtt[-2] + ((1 - self.alpha) * self.rtt[-1]))

        if self.rtt_len > 100: 
            del self.rtt[0]

    def resolve_rto(self)->float:
        
        if self.rtt_len < 2:
            rto = 1
            return rto

        rto = min(self.ubound, max(self.lbound, self.beta*self.srtt[-1]))
        return rto



class RETRANSMISSION_CONTROLE():
    
    payloads = b"messages"
    ack_msg = struct.pack("!3s", b"ack") 
     
    def __init__(self, sockdg, addr:list):
        self.s = sockdg 
        self.dstaddr = addr
        self.rto_func = RTO()

    def retr_ctl_send(self):
        
        set_error_limit = 10
        error_count = 0
        
        while error_count < set_error_limit: 
            
            start_time = time.time()
            rto = self.rto_func.resolve_rto()
            self.s.settimeout(rto) # widnow size : 1
            self.s.sendto(self.payloads, self.dstaddr)
            
            try:
                data,addr = self.s.recvfrom(0xff)
            except:
                error_count +=1
                continue
             
            end_time = time.time()
            response_time =  round((end_time - start_time), 4)
            self.rto_func.resolve_srtt(response_time)
            
            return 0 
            
        return -1   


    def retr_ctl_recv(self):
        self.s.bind(self.dstaddr)
        while True:
            data,addr = self.s.recvfrom(0xff)
            self.s.sendto(self.ack_msg, addr)
            
            print(data)
        return
