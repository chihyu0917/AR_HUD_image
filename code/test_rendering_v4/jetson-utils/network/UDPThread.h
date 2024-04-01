/*
 * UDPThread.h
 *
 *  Created on: 2015. 3. 3.
 *      Author: youngmok
 */

#ifndef UDPTHREAD_H_
#define UDPTHREAD_H_

#define UDP_FILE_LOG_FLAG 0

#include <iostream> 		// cout
#include <sstream>  		// parsing
#include <sys/socket.h>	// for UDP
#include <netinet/in.h>	// for UDP
#include <stdio.h>			// for File output
#include <sys/time.h>		// Time measurement
#include <vector>
using namespace std;

class UDP_Thread {

private:

	FILE *ofp;				// File log
	pthread_t _thread;		// thread
	int sockfd,n;			// UDP
	struct sockaddr_in servaddr,cliaddr; 	// UDP
	socklen_t len;			// UDP
	char mesg[20];		// UDP

	struct timeval tvalNow, tvalInit;	// for time stamp
	double getTimeElapsed(struct timeval end, struct timeval start); // For time stamp


protected:
	void InternalThreadEntry();
        
public:
        int port;
        int udp_cam;
	double sensor_data[3];
        double speed_data[3];
        double breaking_data[3];
        double gas_pedal_data[3];
        double dir_light_data[3];
        double gyro_data[3];
        double gear_data[3];
        double fake_data[3];
	bool StartInternalThread();
	void WaitForInternalThreadToExit();
	static void * InternalThreadEntryFunc(void * This);
        void get_port(int cam);
        std::vector<double> d_udp_csv(string s);
        std::vector< std::vector<double> > mUDPCanData;
	UDP_Thread(int cam);
	~UDP_Thread();


};

#endif /* UDPTHREAD_H_ */
