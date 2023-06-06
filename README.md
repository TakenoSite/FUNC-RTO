# FUNC-RTO

RFC793  RTO計算概要


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
