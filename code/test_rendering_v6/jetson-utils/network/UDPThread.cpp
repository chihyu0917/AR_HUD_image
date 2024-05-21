/*
 * UDPThread.cpp
 *
 *  Created on: 2015. 3. 3.
 *      Author: youngmok
 */

#include "UDPThread.h"
#include "strings.h"
#include "string.h"
#include <unistd.h>
UDP_Thread::UDP_Thread (int cam) {

	// variable initialization
	for(int i=0;i<3;i++) 
        {
          speed_data[i] = 0.0;
          breaking_data[i] = 0.0;
          gas_pedal_data[i] = 0.0;
          dir_light_data[i] = 0.0;
          gyro_data[i] = 0.0;
          gear_data[i] = 0.0;
          fake_data[i] = 0.0;
        }
        
	// pthread initialization
	_thread = pthread_self(); // get pthread ID
	pthread_setschedprio(_thread, SCHED_FIFO); // setting priority
        // log file initialization
	if ( UDP_FILE_LOG_FLAG == 1)	ofp = fopen("sensordata.txt", "w");
        udp_cam = cam;
        std::cout << "UDP for CAM : " << cam << endl;  
        port =32570 + cam;             
	// udp initialization
	sockfd=socket(AF_INET,SOCK_DGRAM,0);
	bzero(&servaddr,sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr=htonl(INADDR_ANY);
	servaddr.sin_port=htons(port);
	bind(sockfd,(struct sockaddr *)&servaddr,sizeof(servaddr));

}
UDP_Thread::~UDP_Thread() {

	pthread_join(_thread, NULL); 	// close the thread
	close(sockfd); 					// close UDP socket
	fclose(ofp);					// close log file
}

// string_to_vector_array (double) 
std::vector<double> UDP_Thread:: d_udp_csv(string s)
{
    std::vector<double> arr;
    istringstream delim(s); // string to stream
    string token_csv;
    double token;
    int c = 0;
    while (getline(delim, token_csv, ','))        
    {

       token = ::atof(token_csv.c_str());
 
     arr.push_back(token);                
     c++;                                           
    }
    return  arr;
    arr.clear();
    std::vector<double>().swap(arr);
}

double UDP_Thread::getTimeElapsed(struct timeval end, struct timeval start)
{
    return (end.tv_sec - start.tv_sec) + (end.tv_usec - start.tv_usec) / 1000000.00;
}

void UDP_Thread::get_port(int cam)
{    
    port = 32570 + cam;
    std::cout << "UDP PORT : " << port << endl; 
}

/** Returns true if the thread was successfully started, false if there was an error starting the thread */
bool UDP_Thread::StartInternalThread()
{
	return (pthread_create(&_thread, NULL, InternalThreadEntryFunc, this) == 0);
}

/** Will not return until the internal thread has exited. */
void UDP_Thread::WaitForInternalThreadToExit()
{
	(void) pthread_join(_thread, NULL);
}

void UDP_Thread::InternalThreadEntry(){

	gettimeofday(&tvalInit, NULL);

	for (;;)
	{

		len = sizeof(cliaddr);
		n = recvfrom(sockfd,mesg,20,0,(struct sockaddr *)&cliaddr,&len);

		mesg[n] = 0;

		string str_sensor_data(mesg);
		stringstream stream(str_sensor_data);

		//cout << "Thread : str_sensor_data " << str_sensor_data << "from CAM" << udp_cam << endl;

                std::vector<double> c_token = d_udp_csv(str_sensor_data);
        	//cout << "size=" << c_token.size() << endl;
        	//for (int ii = 0; ii < c_token.size(); ii++)
        	//{
            	//	cout << c_token[ii] << ",";
        	//}
        	//cout << endl;
        	//========================
                //mUDPCanData.push_back(c_token);

                //std::cout << "The c_token vector size is " << c_token.size() << " and its " << "capacity is " << c_token.capacity() << endl;               
                /*
		for(int i=0;i<3;i++){
			stream >> sensor_data[i]; 
                        cout << "sensor_data[" << i <<"]= "<< sensor_data[i] << endl;                      
		}
                */

                if (c_token[0]==1)
                {   
                    double* speed_i = &c_token[0];
                    for(int i=0;i<3;i++){
                           speed_data[i] = speed_i[i];
                    }            	    
                }
        	else if (c_token[0]==2)
                {
                    double* breaking_i = &c_token[0]; 
            	    for(int i=0;i<3;i++){
			   breaking_data[i] = breaking_i[i];                         
		    }
                }
        	else if (c_token[0]==3)
                {
                    double* gas_pedal_i = &c_token[0];
            	    for(int i=0;i<3;i++){
			   gas_pedal_data[i] = gas_pedal_i[i];                        
		    }
                }
        	else if (c_token[0]==5)
                {
                    double* dir_light_i = &c_token[0];
            	    for(int i=0;i<3;i++){
			   dir_light_data[i] = dir_light_i[i];                       
		    }
                }
        	else if (c_token[0]==6)
                {
                    double* gyro_i = &c_token[0];
            	    for(int i=0;i<3;i++){
			   gyro_data[i] = gyro_i[i];                       
		    }
                }
                else if (c_token[0]==9)
                {
                    double* gear_i = &c_token[0];
            	    for(int i=0;i<3;i++){
			   gear_data[i] = gear_i[i];                       
		    }
                }
                else if (c_token[0]==99)
                {
                    double* fake_i = &c_token[0];
            	    for(int i=0;i<3;i++){
			   fake_data[i] = fake_i[i];                       
		    }
                }
                c_token.clear();
                std::vector<double>().swap(c_token);

		if ( UDP_FILE_LOG_FLAG == 1) {
			gettimeofday(&tvalNow, NULL);
			double time_elapsed = getTimeElapsed(tvalNow, tvalInit);
			fprintf(ofp, "%lf\t%s\n", time_elapsed,mesg);
		}
	}

};


void * UDP_Thread::InternalThreadEntryFunc(void * This) {
	((UDP_Thread *)This)->InternalThreadEntry(); return NULL;
}

