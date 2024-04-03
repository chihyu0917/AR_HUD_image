from multiprocessing import Process,Manager
import time
import json
import socket

def udp_receiver(ip,port,shared_dict):
    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = (ip, port)
    s.bind(server_address)
    print("Do Ctrl+c to exit the program !!")
    print("####### Server is listening #######")
    

    while True:
    
        data, address = s.recvfrom(1024)
        raw=data.decode()
        raw = raw.replace('\'', '"')
        dict_received = json.loads(raw)
        for key in dict_received:
            if not key=="Id":
                if key not in shared_dict:
                    print(key," not in shared_dict")
                shared_dict[key]=dict_received[key]
if __name__ == '__main__':
    manager = Manager()
    shared_dict = manager.dict()

    #----------------------------------------------------shared_dict initialization-------------------------------------------------------------
    int_varaible=["BatteryError", "MotorOverHeat", "ControllerOverHeat", "MotorOverSpeed", "BrakeError", "SystemError", "NavigationDestinationValue", "DistanceValue", "Speedlimit", "FrontCollisionX", "FrontCollisionY", "FrontCollisionVerticalDistance", "FrontCollisionHorizontalDistance", "SpeedLimit", "PedestrianCount", "PedestrianNumber", "PedestrianX", "PedestrianY", "PedestrianVerticalDistance", "PedestrianHorizontalDistance", "ObjectCount", "ObjectNumber", "ObjectX", "ObjectY", "VehicleCount", "VehicleNumber", "VehicleX", "VehicleY", "VehicleVerticalDistance", "VehicleHorizontalDistance", "LaneCount", "LaneNumber", "LaneFunctionCoefficientA", "LaneFunctionCoefficientB", "LaneFunctionCoefficientC", "LaneFunctionCoefficientD"]
    for var in int_varaible:
        shared_dict[var]=0
    shared_dict["Speed"]=0.0
    for var in ["LeftSignal", "RightSignal", "BrakeSignal"]:
        shared_dict[var]="off"
    shared_dict["DataValid"]="data invalid"
    for var in ["NavigationDestinationUnit", "DistanceUnit"]:
        shared_dict[var]="invalid"
    shared_dict["NavigationDirection"]="go straight"
    for var in ["LDW_Left", "LDW_Right"]:
        shared_dict[var]="normal"
    shared_dict["FindSpeedLimit"]="not found"
    shared_dict["FrontCollisionType"]="normal"
    shared_dict["FrontCollisionLevel"]="normal"
    shared_dict["ObjectDirection"]="left"
    shared_dict["VehicleDirection"]="front"
    #----------------------------------------------------shared_dict initialization-------------------------------------------------------------
    
    can_recv_ip="127.0.0.1"
    can_recv_port=17414
    #sock_recv_detection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    #server_address = (ip_detection, port_detection)
    #sock_recv_detection.bind(server_address)   # Bind the socket to the port

    #fcw_warning=FCWarningAlgorithm(bus_name)

    
    p = Process(target=udp_receiver, args=(can_recv_ip,can_recv_port,shared_dict,))
    p.start()

    while True:
        #---------------get detection result of this frame-----------------
        #data, address = sock_recv_detection.recvfrom(port)
        #detection_this_frame=data.decode('utf8')
        #---------------get detection result of this frame-----------------

        #---------------get current can info-----------
        can_this_frame=shared_dict
        #---------------get current can info-----------

        
        #FCW_warning_level,FCW_main_obj_class,PDW_right_near,PDW_right_far,PDW_left_near,PDW_left_far=fcw_warning.update(detection_this_frame,can_this_frame["Speed"],can_this_frame["BrakeSignal"],can_this_frame["LeftSignal"],can_this_frame["RightSignal"])
        #FCW_warning_level:0=normal,1=blue,2=red ; FCW_main_obj_class=['Sedan', 'Truck', 'Bus', 'Motorcycle', 'Person'] ; PDW_X_X:0=normal,1=warning

        #print(can_this_frame)

        







        time.sleep(0.033)


