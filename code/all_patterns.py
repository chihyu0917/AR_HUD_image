from multiprocessing import Process,Manager
import time
import json
import socket
import struct
import numpy as np
import cv2
import jetson.utils
import argparse
import sys
import faulthandler
faulthandler.enable()
class_name_list=['Sedan', 'Truck', 'Bus', 'Motorcycle', 'Person']

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
                if key == "SpeedLimit" and "FindSpeedLimit" in dict_received:
                    continue
                else:
                    shared_dict[key]=dict_received[key]


class FCWarningAlgorithm:
    def __init__(self, self_name="rav4"):
        self.self_name=self_name
        self.cameraMatrix,self.distCoeffs,self.transformationMat,self.origin_point=self.get_camera_parameters(self.self_name)
        self.warning_ttc_near=1.5
        self.warning_ttc_far=2.5
        
        self.FCW_warning_x_range=100   #1.75m
        self.PDW_warning_x_range=350   #FCW_warning_x_range < PDW <=3.5m

        self.FCW_level_change_buffer=30
        self.FCW_main_obj_class="None"
        self.FCW_warning_level=0
        self.PDW_level_change_buffer_list=[30,30,30,30]
        self.PDW_flag_list=[False,False,False,False]

    def update(self,detection_this_frame,self_speed,self_brake,self_leftsigal,self_rightsignal):
        obj_points=[]
        obj_classes=[]
        for obj_dict in detection_this_frame["object"]:
            obj_points.append((obj_dict["xmin"]+0.5*obj_dict["width"],obj_dict["ymin"]+obj_dict["height"]))
            obj_classes.append(class_name_list[obj_dict["class_id"]])

        #----------estimate distance--------------
        if obj_points:
            obj_points=np.array(obj_points,dtype=np.float32)
            reshape_obj_points=obj_points.reshape(-1,1,2)
            undist_points=cv2.undistortPoints(reshape_obj_points, self.cameraMatrix, self.distCoeffs,None,self.cameraMatrix)
            undist_points=np.array(np.squeeze(undist_points),dtype=int)
            undist_points_T=undist_points.transpose().reshape(2,-1)
            mul_result=np.matmul(np.linalg.inv(self.transformationMat) ,np.vstack((undist_points_T,np.ones(undist_points_T.shape[1],dtype=int))))
            out_points=np.vstack((np.around(mul_result[0]/mul_result[2]).astype(int),np.around(mul_result[1]/mul_result[2]).astype(int))).transpose()
        else:
            out_points=[]
        #----------estimate distance--------------

        #----------simple FCW--------------
        xdis_list,ydis_list=[],[]
        front_min_ydis=100000
        target_index=-1
        for i in range(len(out_points)):
            xdis=out_points[i][0]-self.origin_point[0]
            ydis=self.origin_point[1]-out_points[i][1]
            xdis_list.append(xdis)
            ydis_list.append(ydis)
            if abs(xdis)<=self.FCW_warning_x_range and ydis<front_min_ydis and ydis>400:    #reflect
                front_min_ydis=ydis
                target_index=i
        if target_index==-1 or self_speed==0:
            new_FCW_warning_level=0
            new_FCW_main_obj_class="None"
        else:
            target_xdis=xdis_list[target_index]
            target_ydis=ydis_list[target_index]
            ttc_self_speed=max(self_speed,7)
            ttc_from_self_speed=target_ydis/ttc_self_speed*0.036    #speed*1000*100/60/60
            if ttc_from_self_speed<self.warning_ttc_near:
                new_FCW_warning_level=2
                new_FCW_main_obj_class=obj_classes[target_index]
            elif ttc_from_self_speed<self.warning_ttc_far:
                new_FCW_warning_level=1
                new_FCW_main_obj_class=obj_classes[target_index]
            else:
                new_FCW_warning_level=0
                new_FCW_main_obj_class="None"

        if new_FCW_warning_level<self.FCW_warning_level:
            self.FCW_level_change_buffer=self.FCW_level_change_buffer-1   #30/(31-1)
        elif new_FCW_warning_level>self.FCW_warning_level:    
            self.FCW_level_change_buffer=self.FCW_level_change_buffer-15  #30/(3-1)
        else:
            self.FCW_level_change_buffer=min(30,self.FCW_level_change_buffer+7)

        if self.FCW_level_change_buffer<0:
            self.FCW_warning_level=new_FCW_warning_level
            self.FCW_main_obj_class=new_FCW_main_obj_class
            self.FCW_level_change_buffer=30
        elif self.FCW_warning_level>0 and new_FCW_main_obj_class!="None":
            self.FCW_main_obj_class=new_FCW_main_obj_class

        #----------simple FCW--------------

        #----------simple PDW--------------
        new_PDW_flag_list=[False,False,False,False]
        for i in range(len(xdis_list)):
            if obj_classes[i]!="Person":
                continue
            this_xdis=xdis_list[i]
            this_ydis=ydis_list[i]
            if self_speed==0:
                continue
            ttc_from_self_speed=this_ydis/self_speed*0.036    #speed*1000*100/60/60
            if this_xdis>self.FCW_warning_x_range and this_xdis<=self.PDW_warning_x_range:
                if ttc_from_self_speed<self.warning_ttc_near:
                    new_PDW_flag_list[0]=True   #new_PDW_right_near
                elif ttc_from_self_speed<self.warning_ttc_far:
                    new_PDW_flag_list[1]=True   #new_PDW_right_far
            elif this_xdis<-self.FCW_warning_x_range and this_xdis>=-self.PDW_warning_x_range:
                if ttc_from_self_speed<self.warning_ttc_near:
                    new_PDW_flag_list[2]=True   #new_PDW_left_near
                elif ttc_from_self_speed<self.warning_ttc_far:
                    new_PDW_flag_list[3]=True   #new_PDW_left_far

        for i in range(len(self.PDW_flag_list)):    #PDW_right_near,PDW_right_far,PDW_left_near,PDW_left_far
            if new_PDW_flag_list[i]!=self.PDW_flag_list[i]:
                self.PDW_level_change_buffer_list[i]=self.PDW_level_change_buffer_list[i]-6   #30/(6-1)
            else:
                self.PDW_level_change_buffer_list[i]=min(30,self.PDW_level_change_buffer_list[i]+7)

            if self.PDW_level_change_buffer_list[i]<0:
                self.PDW_flag_list[i]=new_PDW_flag_list[i]
                self.PDW_level_change_buffer_list[i]=30
            
        #----------simple PDW--------------

        return self.FCW_warning_level,self.FCW_main_obj_class,self.PDW_flag_list[0],self.PDW_flag_list[1],self.PDW_flag_list[2],self.PDW_flag_list[3]

    def get_camera_parameters(self,self_name):
        if self_name=="rav4":
            alpha_angle=3.8
            beta_angle=1.4
            gamma_angle=-2.7
            cam_height=165
            img_width=640
            img_height=512
            cameraMatrix=np.array([ [5.1591477494842707e+02,0., 3.3191212988723413e+02],
                                    [0., 5.1574907447682267e+02 ,2.5254243342505606e+02],
                                    [0., 0.,   1.]],np.float64)
            distCoeffs=np.array([ -4.6350770880023096e-01, 2.9316382549931186e-01,-1.8465945457083347e-03, -4.7112165736109326e-04,-1.0767973540548396e-01 ],np.float64)
        else:
            print(self_name," not support")

        alpha=(alpha_angle -90) * np.pi/180
        beta=(beta_angle) * np.pi/180
        gamma =(gamma_angle) * np.pi/180
        cam_height=cam_height
        
        cameraMatrix_expand=np.pad(cameraMatrix, ((0,0),(0,1)), 'constant')

        h_=img_height
        w_=img_width
        h=float(h_)
        w=float(w_)
            
        dist=abs(cam_height/np.cos(alpha))
        
        # Projecion matrix 2D -> 3D
        A1=np.array([[1, 0, -w/2],
                     [0, 1, -h/2],
                     [0, 0, 0],
                     [0, 0, 1]],np.float32)
        
        # Rotation matrices Rx, Ry, Rz
        RX=np.array([[1, 0, 0, 0],
                     [0, np.cos(alpha), -np.sin(alpha), 0],
                     [0, np.sin(alpha), np.cos(alpha), 0],
                     [0, 0, 0, 1]],np.float32)
        RY=np.array([[np.cos(beta), 0, np.sin(beta), 0],
                     [0, 1, 0, 0],
                     [-np.sin(beta), 0, np.cos(beta), 0],
                     [0, 0, 0, 1]],np.float32)
        RZ=np.array([[np.cos(gamma), -np.sin(gamma), 0, 0],
                     [np.sin(gamma), np.cos(gamma), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]],np.float32)
        
        
        
        # R - rotation matrix
        R = RX.dot(RY).dot(RZ)
        
        # T - translation matrix
        T=np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, dist],
                    [0, 0, 0, 1]],np.float32)
        
        # K - intrinsic matrix
        K=cameraMatrix_expand
        turn=np.array([[-1 , 0 , w ],
                       [ 0 ,-1 ,2*h],
                       [ 0 , 0 , 1 ]],np.float32)
        # K * (T * (R * A1))
        transformationMat=K.dot(T.dot(R.dot(A1)))

        origin_point=(int(round(w/2-cam_height*(-np.cos(alpha)*np.sin(beta)*np.cos(gamma)+np.sin(alpha)*np.sin(gamma))/(np.cos(alpha)*np.cos(beta)))),int(round(h/2-cam_height*(np.cos(alpha)*np.sin(beta)*np.sin(gamma)+np.sin(alpha)*np.cos(gamma))/(np.cos(alpha)*np.cos(beta)))))
        return cameraMatrix,distCoeffs,transformationMat,origin_point

# parse the command line
parser = argparse.ArgumentParser(description="draw something", 
                           formatter_class=argparse.RawTextHelpFormatter)



parser.add_argument("--width", type=int, default=1280, help="display window width")
parser.add_argument("--height", type=int, default=720, help="display window height")
parser.add_argument("--win_x", type=int, default=0, help="display window start x(xmin)")
parser.add_argument("--win_y", type=int, default=0, help="display window start y(ymin)")
parser.add_argument("--if_no_title", type=bool, default=True, help="True : window with no title; False : window with title")
parser.add_argument("--if_transparent_window", type=bool, default=True, help="True : transparent window; False : black window ")

try:
    opt=parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)
    
width=opt.width
height=opt.height
win_x=opt.win_x
win_y=opt.win_y
if_no_title=opt.if_no_title
if_transparent_window=opt.if_transparent_window

try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)


if __name__ == '__main__':
    manager = Manager()
    shared_dict = manager.dict()


    # load images 
    class attributes:
        def __init__(self, img, img_width, img_height, img_alpha, img_x, img_y):
            self.img = img
            self.img_width = img_width
            self.img_height = img_height
            self.alpha = 0
            self.img_x = img_x
            self.img_y = img_y

    def loadImages():
        images_path = {
            'bg': 'background.png', 
            'A1': './png/W_A1_SL.png', # A1
            'A2_B': './png/W_A2_R_003.png', 'A2_L': './png/W_A2_R_001.png', 'A2_R': './png/W_A2_R_002.png', # A2
            'A3_SF': './png/W_A3_SF.png', 'A3_BL': './png/W_A3_BL.png', 'A3_MH': './png/W_A3_MH.png', 'A3_MS': './png/W_A3_MS.png', 'A3_BF': './png/W_A3_BF.png', # A3
            'A4_S': './png/N_A4_S.png', 'A4_TR': './png/N_A4_TR.png', 'A4_TL': './png/N_A4_TL.png', 'A4_KR': './png/N_A4_KR.png', 
            'A4_KL': './png/N_A4_KL.png', 'A4_TA': './png/N_A4_TA.png', 'A4_D': './png/N_A4_D.png', # A4

            # 'B5_001': './png/A_B5_LBIN_001.png', 'B5_002': './png/A_B5_LBIN_002.png', 'B5_003': './png/A_B5_LBIN_003.png', # B5
            # 'B6_001': './png/A_B6_RBIN_001.png', 'B6_002': './png/A_B6_RBIN_002.png', 'B6_003': './png/A_B6_RBIN_003.png', # B6
            # 'B1_S_031': './png/N_B1_S_031.png', 'B1_S_037': './png/N_B1_S_037.png', 'B1_S_043': './png/N_B1_S_043.png', 'B1_S_049': './png/N_B1_S_049.png', 'B1_S_055': './png/N_B1_S_055.png', # B1
            # 'B1_FTL_001': './png/N_B1_FTL_001.png', 'B1_FTL_010': './png/N_B1_FTL_010.png', 'B1_FTL_019': './png/N_B1_FTL_019.png', 'B1_FTL_028': './png/N_B1_FTL_028.png',
            # 'B1_FTR_001': './png/N_B1_FTR_001.png', 'B1_FTR_010': './png/N_B1_FTR_010.png', 'B1_FTR_019': './png/N_B1_FTR_019.png', 'B1_FTR_028': './png/N_B1_FTR_028.png',
            # 'B1_FTA_001': './png/N_B1_FTA_001.png', 'B1_FTA_010': './png/N_B1_FTA_010.png', 'B1_FTA_019': './png/N_B1_FTA_019.png', 'B1_FTA_028': './png/N_B1_FTA_028.png',
            
            'B1_NTR_001': './png/N_B1_NTR_001.png', 'B1_NTR_004': './png/N_B1_NTR_004.png', 'B1_NTR_007': './png/N_B1_NTR_007.png', 'B1_NTR_010': './png/N_B1_NTR_010.png', 'B1_NTR_013': './png/N_B1_NTR_013.png', 'B1_NTR_016': './png/N_B1_NTR_016.png',
            'B1_NTR_019': './png/N_B1_NTR_019.png', 'B1_NTR_022': './png/N_B1_NTR_022.png', 'B1_NTR_025': './png/N_B1_NTR_025.png', 'B1_NTR_028': './png/N_B1_NTR_028.png', 'B1_NTR_031': './png/N_B1_NTR_031.png', 'B1_NTR_034': './png/N_B1_NTR_034.png',
            'B1_NTR_037': './png/N_B1_NTR_037.png', 'B1_NTR_040': './png/N_B1_NTR_040.png', 'B1_NTR_043': './png/N_B1_NTR_043.png', 'B1_NTR_046': './png/N_B1_NTR_046.png',
            
            'B1_NTL_001': './png/N_B1_NTL_001.png', 'B1_NTL_004': './png/N_B1_NTL_004.png', 'B1_NTL_007': './png/N_B1_NTL_007.png', 'B1_NTL_010': './png/N_B1_NTL_010.png', 'B1_NTL_013': './png/N_B1_NTL_013.png', 'B1_NTL_016': './png/N_B1_NTL_016.png',
            'B1_NTL_019': './png/N_B1_NTL_019.png', 'B1_NTL_022': './png/N_B1_NTL_022.png', 'B1_NTL_025': './png/N_B1_NTL_025.png', 'B1_NTL_028': './png/N_B1_NTL_028.png', 'B1_NTL_031': './png/N_B1_NTL_031.png', 'B1_NTL_034': './png/N_B1_NTL_034.png',
            'B1_NTL_037': './png/N_B1_NTL_037.png', 'B1_NTL_040': './png/N_B1_NTL_040.png', 'B1_NTL_043': './png/N_B1_NTL_043.png', 'B1_NTL_046': './png/N_B1_NTL_046.png',
            
            'B1_NTA_001': './png/N_B1_NTA_001.png', 'B1_NTA_004': './png/N_B1_NTA_004.png', 'B1_NTA_007': './png/N_B1_NTA_007.png', 'B1_NTA_010': './png/N_B1_NTA_010.png', 'B1_NTA_013': './png/N_B1_NTA_013.png', 'B1_NTA_016': './png/N_B1_NTA_016.png',
            'B1_NTA_019': './png/N_B1_NTA_019.png', 'B1_NTA_022': './png/N_B1_NTA_022.png', 'B1_NTA_025': './png/N_B1_NTA_025.png', 'B1_NTA_028': './png/N_B1_NTA_028.png', 'B1_NTA_031': './png/N_B1_NTA_031.png', 'B1_NTA_034': './png/N_B1_NTA_034.png',
            'B1_NTA_037': './png/N_B1_NTA_037.png', 'B1_NTA_040': './png/N_B1_NTA_040.png', 'B1_NTA_043': './png/N_B1_NTA_043.png', 'B1_NTA_046': './png/N_B1_NTA_046.png',
            
            'B2_NTR_049': './png/N_B1_NTR_049.png', 'B2_NTR_052': './png/N_B1_NTR_052.png', 'B2_NTR_055': './png/N_B1_NTR_055.png', 'B2_NTR_058': './png/N_B1_NTR_058.png', 'B2_NTR_061': './png/N_B1_NTR_061.png', 'B2_NTR_064': './png/N_B1_NTR_064.png',
            'B2_NTR_067': './png/N_B1_NTR_067.png', 'B2_NTR_070': './png/N_B1_NTR_070.png', 'B2_NTR_073': './png/N_B1_NTR_073.png', 'B2_NTR_076': './png/N_B1_NTR_076.png', 'B2_NTR_079': './png/N_B1_NTR_079.png', 'B2_NTR_082': './png/N_B1_NTR_082.png',
            'B2_NTR_085': './png/N_B1_NTR_085.png', 'B2_NTR_088': './png/N_B1_NTR_088.png', 'B2_NTR_091': './png/N_B1_NTR_091.png', 'B2_NTR_094': './png/N_B1_NTR_094.png', 'B2_NTR_097': './png/N_B1_NTR_097.png', 'B2_NTR_100': './png/N_B1_NTR_100.png',
            'B2_NTR_103': './png/N_B1_NTR_103.png', 'B2_NTR_106': './png/N_B1_NTR_106.png', 'B2_NTR_109': './png/N_B1_NTR_109.png', 'B2_NTR_112': './png/N_B1_NTR_112.png', 'B2_NTR_115': './png/N_B1_NTR_115.png',
            
            'B2_NTL_049': './png/N_B1_NTL_049.png', 'B2_NTL_052': './png/N_B1_NTL_052.png', 'B2_NTL_055': './png/N_B1_NTL_055.png', 'B2_NTL_058': './png/N_B1_NTL_058.png', 'B2_NTL_061': './png/N_B1_NTL_061.png', 'B2_NTL_064': './png/N_B1_NTL_064.png',
            'B2_NTL_067': './png/N_B1_NTL_067.png', 'B2_NTL_070': './png/N_B1_NTL_070.png', 'B2_NTL_073': './png/N_B1_NTL_073.png', 'B2_NTL_076': './png/N_B1_NTL_076.png', 'B2_NTL_079': './png/N_B1_NTL_079.png', 'B2_NTL_082': './png/N_B1_NTL_082.png',
            'B2_NTL_085': './png/N_B1_NTL_085.png', 'B2_NTL_088': './png/N_B1_NTL_088.png', 'B2_NTL_091': './png/N_B1_NTL_091.png', 'B2_NTL_094': './png/N_B1_NTL_094.png', 'B2_NTL_097': './png/N_B1_NTL_097.png', 'B2_NTL_100': './png/N_B1_NTL_100.png',
            'B2_NTL_103': './png/N_B1_NTL_103.png', 'B2_NTL_106': './png/N_B1_NTL_106.png', 'B2_NTL_109': './png/N_B1_NTL_109.png', 'B2_NTL_112': './png/N_B1_NTL_112.png', 'B2_NTL_115': './png/N_B1_NTL_115.png',
            
            'B2_NTA_049': './png/N_B1_NTA_049.png', 'B2_NTA_052': './png/N_B1_NTA_052.png', 'B2_NTA_055': './png/N_B1_NTA_055.png', 'B2_NTA_058': './png/N_B1_NTA_058.png', 'B2_NTA_061': './png/N_B1_NTA_061.png', 'B2_NTA_064': './png/N_B1_NTA_064.png',
            'B2_NTA_067': './png/N_B1_NTA_067.png', 'B2_NTA_070': './png/N_B1_NTA_070.png', 'B2_NTA_073': './png/N_B1_NTA_073.png', 'B2_NTA_076': './png/N_B1_NTA_076.png', 'B2_NTA_079': './png/N_B1_NTA_079.png', 'B2_NTA_082': './png/N_B1_NTA_082.png',
            'B2_NTA_085': './png/N_B1_NTA_085.png', 'B2_NTA_088': './png/N_B1_NTA_088.png', 'B2_NTA_091': './png/N_B1_NTA_091.png', 'B2_NTA_094': './png/N_B1_NTA_094.png', 'B2_NTA_097': './png/N_B1_NTA_097.png', 'B2_NTA_100': './png/N_B1_NTA_100.png',
            'B2_NTA_103': './png/N_B1_NTA_103.png', 'B2_NTA_106': './png/N_B1_NTA_106.png', 'B2_NTA_109': './png/N_B1_NTA_109.png', 'B2_NTA_112': './png/N_B1_NTA_112.png', 'B2_NTA_115': './png/N_B1_NTA_115.png', 'B2_NTA_118': './png/N_B1_NTA_118.png', 'B2_NTA_121': './png/N_B1_NTA_121.png',
            
            'B3_FCWA': './png/A_B3_FCWA.png', 'B3_FCW_B': './png/A_B3_FCWB_001.png', 'B3_FCWB_2': './png/A_B3_FCWB_002.png', # B3
            'B3_PDWA': './png/A_B3_PDWA.png', 'B3_PDWB_2': './png/A_B3_PDWB_002.png', 'B3_PDW_1': './png/A_B3_PDW_1.png', 'B3_PDW_2': './png/A_B3_PDW_2.png', 'B3_PDW_3': './png/A_B3_PDW_3.png', 'B3_PDW_4': './png/A_B3_PDW_4.png',
            # 'B4_LLDW_001': './png/A_B4_LLDW_001.png', 'B4_LLDW_002': './png/A_B4_LLDW_002.png', 'B4_LLDW_003': './png/A_B4_LLDW_003.png', 'B4_LLDW_004': './png/A_B4_LLDW_004.png', 'B4_LLDW_005': './png/A_B4_LLDW_005.png', # B4
            # 'B4_RLDW_001': './png/A_B4_RLDW_001.png', 'B4_RLDW_002': './png/A_B4_RLDW_002.png', 'B4_RLDW_003': './png/A_B4_RLDW_003.png', 'B4_RLDW_004': './png/A_B4_RLDW_004.png', 'B4_RLDW_005': './png/A_B4_RLDW_005.png',
        }
        #---------------------
        B5_images_path = {'B5_{:03d}'.format(i): './png/A_B5_LBIN_{:03d}.png'.format(i) for i in range(1, 37)}
        B6_images_path = {'B6_{:03d}'.format(i): './png/A_B6_RBIN_{:03d}.png'.format(i) for i in range(1, 37)}
        S_images_path = {'B1_S_{:03d}'.format(i): './png/N_B1_S_{:03d}.png'.format(i) for i in range(1, 151)}
        FTL_images_path = {'B1_FTL_{:03d}'.format(i): './png/N_B1_FTL_{:03d}.png'.format(i) for i in range(1, 37)}
        FTR_images_path = {'B1_FTR_{:03d}'.format(i): './png/N_B1_FTR_{:03d}.png'.format(i) for i in range(1, 37)}
        FTA_images_path = {'B1_FTA_{:03d}'.format(i): './png/N_B1_FTA_{:03d}.png'.format(i) for i in range(1, 37)}
        B4_LLDW_images_path = {'B4_LLDW_{:03d}'.format(i): './png/A_B4_LLDW_{:03d}.png'.format(i) for i in range(1, 31)}
        B4_RLDW_images_path = {'B4_RLDW_{:03d}'.format(i): './png/A_B4_RLDW_{:03d}.png'.format(i) for i in range(1, 31)}
        images_path.update(B5_images_path)
        images_path.update(B6_images_path)
        images_path.update(S_images_path)
        images_path.update(FTL_images_path)
        images_path.update(FTR_images_path)
        images_path.update(FTA_images_path)
        images_path.update(B4_LLDW_images_path)
        images_path.update(B4_RLDW_images_path)
        #----------------------


        images = {}
        for key, path in images_path.items():
            images[key] = jetson.utils.loadImageRGBA(path)
            
        return images
    
    images = loadImages()
    for key in images.keys():
        img, img_width, img_height = images[key]


    A1 = attributes(images['A1'][0], images['A1'][1], images['A1'][2], 0, 80, 387) # A1
    
    A2_B = attributes(images['A2_B'][0], images['A2_B'][1], images['A2_B'][2], 0, 341, 512) # A2
    A2_L = attributes(images['A2_L'][0], images['A2_L'][1], images['A2_L'][2], 0, 255, 399)
    A2_R = attributes(images['A2_R'][0], images['A2_R'][1], images['A2_R'][2], 0, 482, 399)


    A3_SF = attributes(images['A3_SF'][0], images['A3_SF'][1], images['A3_SF'][2], 0, 560, 417) # A3
    A3_BL = attributes(images['A3_BL'][0], images['A3_BL'][1], images['A3_BL'][2], 0, 560, 403)
    A3_MH = attributes(images['A3_MH'][0], images['A3_MH'][1], images['A3_MH'][2], 0, 560, 401)
    A3_MS = attributes(images['A3_MS'][0], images['A3_MS'][1], images['A3_MS'][2], 0, 560, 422)
    A3_BF = attributes(images['A3_BF'][0], images['A3_BF'][1], images['A3_BF'][2], 0, 560, 398)
    
    # A4_S = attributes(images['A4_S'][0], images['A4_S'][1], images['A4_S'][2], 0, 782, 404) # A4
    # A4_TR = attributes(images['A4_TR'][0], images['A4_TR'][1], images['A4_TR'][2], 0, 770, 404)
    # A4_TL = attributes(images['A4_TL'][0], images['A4_TL'][1], images['A4_TL'][2], 0, 770, 404)
    # A4_KR = attributes(images['A4_KR'][0], images['A4_KR'][1], images['A4_KR'][2], 0, 770, 404)
    # A4_KL = attributes(images['A4_KL'][0], images['A4_KL'][1], images['A4_KL'][2], 0, 770, 404)
    # A4_TA = attributes(images['A4_TA'][0], images['A4_TA'][1], images['A4_TA'][2], 0, 770, 425)
    # A4_D = attributes(images['A4_D'][0], images['A4_D'][1], images['A4_D'][2], 0, 785, 425) 
    A4_S = attributes(images['A4_S'][0], images['A4_S'][1], images['A4_S'][2], 0, 777, 400) # A4
    A4_TR = attributes(images['A4_TR'][0], images['A4_TR'][1], images['A4_TR'][2], 0, 770, 394)
    A4_TL = attributes(images['A4_TL'][0], images['A4_TL'][1], images['A4_TL'][2], 0, 770, 394)
    A4_KR = attributes(images['A4_KR'][0], images['A4_KR'][1], images['A4_KR'][2], 0, 775, 410)
    A4_KL = attributes(images['A4_KL'][0], images['A4_KL'][1], images['A4_KL'][2], 0, 783, 410)
    A4_TA = attributes(images['A4_TA'][0], images['A4_TA'][1], images['A4_TA'][2], 0, 770, 425)
    A4_D = attributes(images['A4_D'][0], images['A4_D'][1], images['A4_D'][2], 0, 775, 424)

    # B5_001 = attributes(images['B5_001'][0], images['B5_001'][1], images['B5_001'][2], 0, 70, 155) # B5
    # B5_002 = attributes(images['B5_002'][0], images['B5_002'][1], images['B5_002'][2], 0, 70, 155)
    # B5_003 = attributes(images['B5_003'][0], images['B5_003'][1], images['B5_003'][2], 0, 70, 155)
    
    B5_attributes = []
    for i in range(1, 37):
        key = f'B5_{str(i).zfill(3)}'
        B5_attributes.append(attributes(images[key][0], images[key][1], images[key][2], 0, 70, 155))


    # B6_001 = attributes(images['B6_001'][0], images['B6_001'][1], images['B6_001'][2], 0, 1128, 155) # B6
    # B6_002 = attributes(images['B6_002'][0], images['B6_002'][1], images['B6_002'][2], 0, 1128, 155)
    # B6_003 = attributes(images['B6_003'][0], images['B6_003'][1], images['B6_003'][2], 0, 1128, 155)
    B6_attributes = []
    for i in range(1, 37):
        key = f'B6_{str(i).zfill(3)}'
        B6_attributes.append(attributes(images[key][0], images[key][1], images[key][2], 0, 1128, 155))

    
    # B1_S_031 = attributes(images['B1_S_031'][0], images['B1_S_031'][1], images['B1_S_031'][2], 0, 70, 155)
    # B1_S_037 = attributes(images['B1_S_037'][0], images['B1_S_037'][1], images['B1_S_037'][2], 0, 70, 155)
    # B1_S_043 = attributes(images['B1_S_043'][0], images['B1_S_043'][1], images['B1_S_043'][2], 0, 70, 155)
    # B1_S_049 = attributes(images['B1_S_049'][0], images['B1_S_049'][1], images['B1_S_049'][2], 0, 70, 155)
    # B1_S_055 = attributes(images['B1_S_055'][0], images['B1_S_055'][1], images['B1_S_055'][2], 0, 70, 155)
    B1_S_attributes = []
    for i in range(1, 151):
        key = f'B1_S_{str(i).zfill(3)}'
        B1_S_attributes.append(attributes(images[key][0], images[key][1], images[key][2], 0, 70, 155))
    
    # B1_FTL_001 = attributes(images['B1_FTL_001'][0], images['B1_FTL_001'][1], images['B1_FTL_001'][2], 0, 70, 155)
    # B1_FTL_010 = attributes(images['B1_FTL_010'][0], images['B1_FTL_010'][1], images['B1_FTL_010'][2], 0, 70, 155)
    # B1_FTL_019 = attributes(images['B1_FTL_019'][0], images['B1_FTL_019'][1], images['B1_FTL_019'][2], 0, 70, 155)
    # B1_FTL_028 = attributes(images['B1_FTL_028'][0], images['B1_FTL_028'][1], images['B1_FTL_028'][2], 0, 70, 155)
    B1_FTL_attributes = []
    for i in range(1, 37):
        key = f'B1_FTL_{str(i).zfill(3)}'
        B1_FTL_attributes.append(attributes(images[key][0], images[key][1], images[key][2], 0, 70, 155))
    
    # B1_FTR_001 = attributes(images['B1_FTR_001'][0], images['B1_FTR_001'][1], images['B1_FTR_001'][2], 0, 70, 155)
    # B1_FTR_010 = attributes(images['B1_FTR_010'][0], images['B1_FTR_010'][1], images['B1_FTR_010'][2], 0, 70, 155)
    # B1_FTR_019 = attributes(images['B1_FTR_019'][0], images['B1_FTR_019'][1], images['B1_FTR_019'][2], 0, 70, 155)
    # B1_FTR_028 = attributes(images['B1_FTR_028'][0], images['B1_FTR_028'][1], images['B1_FTR_028'][2], 0, 70, 155)
    B1_FTR_attributes = []
    for i in range(1, 37):
        key = f'B1_FTR_{str(i).zfill(3)}'
        B1_FTR_attributes.append(attributes(images[key][0], images[key][1], images[key][2], 0, 70, 155))
    
    # B1_FTA_001 = attributes(images['B1_FTA_001'][0], images['B1_FTA_001'][1], images['B1_FTA_001'][2], 0, 70, 155)
    # B1_FTA_010 = attributes(images['B1_FTA_010'][0], images['B1_FTA_010'][1], images['B1_FTA_010'][2], 0, 70, 155)
    # B1_FTA_019 = attributes(images['B1_FTA_019'][0], images['B1_FTA_019'][1], images['B1_FTA_019'][2], 0, 70, 155)
    # B1_FTA_028 = attributes(images['B1_FTA_028'][0], images['B1_FTA_028'][1], images['B1_FTA_028'][2], 0, 70, 155)
    B1_FTA_attributes = []
    for i in range(1, 37):
        key = f'B1_FTA_{str(i).zfill(3)}'
        B1_FTA_attributes.append(attributes(images[key][0], images[key][1], images[key][2], 0, 70, 155))
    
    B1_NTR_001 = attributes(images['B1_NTR_001'][0], images['B1_NTR_001'][1], images['B1_NTR_001'][2], 0, 70, 155)
    B1_NTR_004 = attributes(images['B1_NTR_004'][0], images['B1_NTR_004'][1], images['B1_NTR_004'][2], 0, 70, 155)
    B1_NTR_007 = attributes(images['B1_NTR_007'][0], images['B1_NTR_007'][1], images['B1_NTR_007'][2], 0, 70, 155)
    B1_NTR_010 = attributes(images['B1_NTR_010'][0], images['B1_NTR_010'][1], images['B1_NTR_010'][2], 0, 70, 155)
    B1_NTR_013 = attributes(images['B1_NTR_013'][0], images['B1_NTR_013'][1], images['B1_NTR_013'][2], 0, 70, 155)
    B1_NTR_016 = attributes(images['B1_NTR_016'][0], images['B1_NTR_016'][1], images['B1_NTR_016'][2], 0, 70, 155)
    B1_NTR_019 = attributes(images['B1_NTR_019'][0], images['B1_NTR_019'][1], images['B1_NTR_019'][2], 0, 70, 155)
    B1_NTR_022 = attributes(images['B1_NTR_022'][0], images['B1_NTR_022'][1], images['B1_NTR_022'][2], 0, 70, 155)
    B1_NTR_025 = attributes(images['B1_NTR_025'][0], images['B1_NTR_025'][1], images['B1_NTR_025'][2], 0, 70, 155)
    B1_NTR_028 = attributes(images['B1_NTR_028'][0], images['B1_NTR_028'][1], images['B1_NTR_028'][2], 0, 70, 155)
    B1_NTR_031 = attributes(images['B1_NTR_031'][0], images['B1_NTR_031'][1], images['B1_NTR_031'][2], 0, 70, 155)
    B1_NTR_034 = attributes(images['B1_NTR_034'][0], images['B1_NTR_034'][1], images['B1_NTR_034'][2], 0, 70, 155)
    B1_NTR_037 = attributes(images['B1_NTR_037'][0], images['B1_NTR_037'][1], images['B1_NTR_037'][2], 0, 70, 155)
    B1_NTR_040 = attributes(images['B1_NTR_040'][0], images['B1_NTR_040'][1], images['B1_NTR_040'][2], 0, 70, 155)
    B1_NTR_043 = attributes(images['B1_NTR_043'][0], images['B1_NTR_043'][1], images['B1_NTR_043'][2], 0, 70, 155)
    B1_NTR_046 = attributes(images['B1_NTR_046'][0], images['B1_NTR_046'][1], images['B1_NTR_046'][2], 0, 70, 155)
    
    B1_NTL_001 = attributes(images['B1_NTL_001'][0], images['B1_NTL_001'][1], images['B1_NTL_001'][2], 0, 70, 155)
    B1_NTL_004 = attributes(images['B1_NTL_004'][0], images['B1_NTL_004'][1], images['B1_NTL_004'][2], 0, 70, 155)
    B1_NTL_007 = attributes(images['B1_NTL_007'][0], images['B1_NTL_007'][1], images['B1_NTL_007'][2], 0, 70, 155)
    B1_NTL_010 = attributes(images['B1_NTL_010'][0], images['B1_NTL_010'][1], images['B1_NTL_010'][2], 0, 70, 155)
    B1_NTL_013 = attributes(images['B1_NTL_013'][0], images['B1_NTL_013'][1], images['B1_NTL_013'][2], 0, 70, 155)
    B1_NTL_016 = attributes(images['B1_NTL_016'][0], images['B1_NTL_016'][1], images['B1_NTL_016'][2], 0, 70, 155)
    B1_NTL_019 = attributes(images['B1_NTL_019'][0], images['B1_NTL_019'][1], images['B1_NTL_019'][2], 0, 70, 155)
    B1_NTL_022 = attributes(images['B1_NTL_022'][0], images['B1_NTL_022'][1], images['B1_NTL_022'][2], 0, 70, 155)
    B1_NTL_025 = attributes(images['B1_NTL_025'][0], images['B1_NTL_025'][1], images['B1_NTL_025'][2], 0, 70, 155)
    B1_NTL_028 = attributes(images['B1_NTL_028'][0], images['B1_NTL_028'][1], images['B1_NTL_028'][2], 0, 70, 155)
    B1_NTL_031 = attributes(images['B1_NTL_031'][0], images['B1_NTL_031'][1], images['B1_NTL_031'][2], 0, 70, 155)
    B1_NTL_034 = attributes(images['B1_NTL_034'][0], images['B1_NTL_034'][1], images['B1_NTL_034'][2], 0, 70, 155)
    B1_NTL_037 = attributes(images['B1_NTL_037'][0], images['B1_NTL_037'][1], images['B1_NTL_037'][2], 0, 70, 155)
    B1_NTL_040 = attributes(images['B1_NTL_040'][0], images['B1_NTL_040'][1], images['B1_NTL_040'][2], 0, 70, 155)
    B1_NTL_043 = attributes(images['B1_NTL_043'][0], images['B1_NTL_043'][1], images['B1_NTL_043'][2], 0, 70, 155)
    B1_NTL_046 = attributes(images['B1_NTL_046'][0], images['B1_NTL_046'][1], images['B1_NTL_046'][2], 0, 70, 155)
    
    B1_NTA_001 = attributes(images['B1_NTA_001'][0], images['B1_NTA_001'][1], images['B1_NTA_001'][2], 0, 70, 155)
    B1_NTA_004 = attributes(images['B1_NTA_004'][0], images['B1_NTA_004'][1], images['B1_NTA_004'][2], 0, 70, 155)
    B1_NTA_007 = attributes(images['B1_NTA_007'][0], images['B1_NTA_007'][1], images['B1_NTA_007'][2], 0, 70, 155)
    B1_NTA_010 = attributes(images['B1_NTA_010'][0], images['B1_NTA_010'][1], images['B1_NTA_010'][2], 0, 70, 155)
    B1_NTA_013 = attributes(images['B1_NTA_013'][0], images['B1_NTA_013'][1], images['B1_NTA_013'][2], 0, 70, 155)
    B1_NTA_016 = attributes(images['B1_NTA_016'][0], images['B1_NTA_016'][1], images['B1_NTA_016'][2], 0, 70, 155)
    B1_NTA_019 = attributes(images['B1_NTA_019'][0], images['B1_NTA_019'][1], images['B1_NTA_019'][2], 0, 70, 155)
    B1_NTA_022 = attributes(images['B1_NTA_022'][0], images['B1_NTA_022'][1], images['B1_NTA_022'][2], 0, 70, 155)
    B1_NTA_025 = attributes(images['B1_NTA_025'][0], images['B1_NTA_025'][1], images['B1_NTA_025'][2], 0, 70, 155)
    B1_NTA_028 = attributes(images['B1_NTA_028'][0], images['B1_NTA_028'][1], images['B1_NTA_028'][2], 0, 70, 155)
    B1_NTA_031 = attributes(images['B1_NTA_031'][0], images['B1_NTA_031'][1], images['B1_NTA_031'][2], 0, 70, 155)
    B1_NTA_034 = attributes(images['B1_NTA_034'][0], images['B1_NTA_034'][1], images['B1_NTA_034'][2], 0, 70, 155)
    B1_NTA_037 = attributes(images['B1_NTA_037'][0], images['B1_NTA_037'][1], images['B1_NTA_037'][2], 0, 70, 155)
    B1_NTA_040 = attributes(images['B1_NTA_040'][0], images['B1_NTA_040'][1], images['B1_NTA_040'][2], 0, 70, 155)
    B1_NTA_043 = attributes(images['B1_NTA_043'][0], images['B1_NTA_043'][1], images['B1_NTA_043'][2], 0, 70, 155)
    B1_NTA_046 = attributes(images['B1_NTA_046'][0], images['B1_NTA_046'][1], images['B1_NTA_046'][2], 0, 70, 155)
    
    B2_NTR_049 = attributes(images['B2_NTR_049'][0], images['B2_NTR_049'][1], images['B2_NTR_049'][2], 0, 70, 155)
    B2_NTR_052 = attributes(images['B2_NTR_052'][0], images['B2_NTR_052'][1], images['B2_NTR_052'][2], 0, 70, 155)
    B2_NTR_055 = attributes(images['B2_NTR_055'][0], images['B2_NTR_055'][1], images['B2_NTR_055'][2], 0, 70, 155)
    B2_NTR_058 = attributes(images['B2_NTR_058'][0], images['B2_NTR_058'][1], images['B2_NTR_058'][2], 0, 70, 155)
    B2_NTR_061 = attributes(images['B2_NTR_061'][0], images['B2_NTR_061'][1], images['B2_NTR_061'][2], 0, 70, 155)
    B2_NTR_064 = attributes(images['B2_NTR_064'][0], images['B2_NTR_064'][1], images['B2_NTR_064'][2], 0, 70, 155)
    B2_NTR_067 = attributes(images['B2_NTR_067'][0], images['B2_NTR_067'][1], images['B2_NTR_067'][2], 0, 70, 155)
    B2_NTR_070 = attributes(images['B2_NTR_070'][0], images['B2_NTR_070'][1], images['B2_NTR_070'][2], 0, 70, 155)
    B2_NTR_073 = attributes(images['B2_NTR_073'][0], images['B2_NTR_073'][1], images['B2_NTR_073'][2], 0, 70, 155)
    B2_NTR_076 = attributes(images['B2_NTR_076'][0], images['B2_NTR_076'][1], images['B2_NTR_076'][2], 0, 70, 155)
    B2_NTR_079 = attributes(images['B2_NTR_079'][0], images['B2_NTR_079'][1], images['B2_NTR_079'][2], 0, 70, 155)
    B2_NTR_082 = attributes(images['B2_NTR_082'][0], images['B2_NTR_082'][1], images['B2_NTR_082'][2], 0, 70, 155)
    B2_NTR_085 = attributes(images['B2_NTR_085'][0], images['B2_NTR_085'][1], images['B2_NTR_085'][2], 0, 70, 155)
    B2_NTR_088 = attributes(images['B2_NTR_088'][0], images['B2_NTR_088'][1], images['B2_NTR_088'][2], 0, 70, 155)
    B2_NTR_091 = attributes(images['B2_NTR_091'][0], images['B2_NTR_091'][1], images['B2_NTR_091'][2], 0, 70, 155)
    B2_NTR_094 = attributes(images['B2_NTR_094'][0], images['B2_NTR_094'][1], images['B2_NTR_094'][2], 0, 70, 155)
    B2_NTR_097 = attributes(images['B2_NTR_097'][0], images['B2_NTR_097'][1], images['B2_NTR_097'][2], 0, 70, 155)
    B2_NTR_100 = attributes(images['B2_NTR_100'][0], images['B2_NTR_100'][1], images['B2_NTR_100'][2], 0, 70, 155)
    B2_NTR_103 = attributes(images['B2_NTR_103'][0], images['B2_NTR_103'][1], images['B2_NTR_103'][2], 0, 70, 155)
    B2_NTR_106 = attributes(images['B2_NTR_106'][0], images['B2_NTR_106'][1], images['B2_NTR_106'][2], 0, 70, 155)
    B2_NTR_109 = attributes(images['B2_NTR_109'][0], images['B2_NTR_109'][1], images['B2_NTR_109'][2], 0, 70, 155)
    B2_NTR_112 = attributes(images['B2_NTR_112'][0], images['B2_NTR_112'][1], images['B2_NTR_112'][2], 0, 70, 155)
    B2_NTR_115 = attributes(images['B2_NTR_115'][0], images['B2_NTR_115'][1], images['B2_NTR_115'][2], 0, 70, 155)
    
    B2_NTL_049 = attributes(images['B2_NTL_049'][0], images['B2_NTL_049'][1], images['B2_NTL_049'][2], 0, 70, 155)
    B2_NTL_052 = attributes(images['B2_NTL_052'][0], images['B2_NTL_052'][1], images['B2_NTL_052'][2], 0, 70, 155)
    B2_NTL_055 = attributes(images['B2_NTL_055'][0], images['B2_NTL_055'][1], images['B2_NTL_055'][2], 0, 70, 155)
    B2_NTL_058 = attributes(images['B2_NTL_058'][0], images['B2_NTL_058'][1], images['B2_NTL_058'][2], 0, 70, 155)
    B2_NTL_061 = attributes(images['B2_NTL_061'][0], images['B2_NTL_061'][1], images['B2_NTL_061'][2], 0, 70, 155)
    B2_NTL_064 = attributes(images['B2_NTL_064'][0], images['B2_NTL_064'][1], images['B2_NTL_064'][2], 0, 70, 155)
    B2_NTL_067 = attributes(images['B2_NTL_067'][0], images['B2_NTL_067'][1], images['B2_NTL_067'][2], 0, 70, 155)
    B2_NTL_070 = attributes(images['B2_NTL_070'][0], images['B2_NTL_070'][1], images['B2_NTL_070'][2], 0, 70, 155)
    B2_NTL_073 = attributes(images['B2_NTL_073'][0], images['B2_NTL_073'][1], images['B2_NTL_073'][2], 0, 70, 155)
    B2_NTL_076 = attributes(images['B2_NTL_076'][0], images['B2_NTL_076'][1], images['B2_NTL_076'][2], 0, 70, 155)
    B2_NTL_079 = attributes(images['B2_NTL_079'][0], images['B2_NTL_079'][1], images['B2_NTL_079'][2], 0, 70, 155)
    B2_NTL_082 = attributes(images['B2_NTL_082'][0], images['B2_NTL_082'][1], images['B2_NTL_082'][2], 0, 70, 155)
    B2_NTL_085 = attributes(images['B2_NTL_085'][0], images['B2_NTL_085'][1], images['B2_NTL_085'][2], 0, 70, 155)
    B2_NTL_088 = attributes(images['B2_NTL_088'][0], images['B2_NTL_088'][1], images['B2_NTL_088'][2], 0, 70, 155)
    B2_NTL_091 = attributes(images['B2_NTL_091'][0], images['B2_NTL_091'][1], images['B2_NTL_091'][2], 0, 70, 155)
    B2_NTL_094 = attributes(images['B2_NTL_094'][0], images['B2_NTL_094'][1], images['B2_NTL_094'][2], 0, 70, 155)
    B2_NTL_097 = attributes(images['B2_NTL_097'][0], images['B2_NTL_097'][1], images['B2_NTL_097'][2], 0, 70, 155)
    B2_NTL_100 = attributes(images['B2_NTL_100'][0], images['B2_NTL_100'][1], images['B2_NTL_100'][2], 0, 70, 155)
    B2_NTL_103 = attributes(images['B2_NTL_103'][0], images['B2_NTL_103'][1], images['B2_NTL_103'][2], 0, 70, 155)
    B2_NTL_106 = attributes(images['B2_NTL_106'][0], images['B2_NTL_106'][1], images['B2_NTL_106'][2], 0, 70, 155)
    B2_NTL_109 = attributes(images['B2_NTL_109'][0], images['B2_NTL_109'][1], images['B2_NTL_109'][2], 0, 70, 155)
    B2_NTL_112 = attributes(images['B2_NTL_112'][0], images['B2_NTL_112'][1], images['B2_NTL_112'][2], 0, 70, 155)
    B2_NTL_115 = attributes(images['B2_NTL_115'][0], images['B2_NTL_115'][1], images['B2_NTL_115'][2], 0, 70, 155)
    
    B2_NTA_049 = attributes(images['B2_NTA_049'][0], images['B2_NTA_049'][1], images['B2_NTA_049'][2], 0, 70, 155)
    B2_NTA_052 = attributes(images['B2_NTA_052'][0], images['B2_NTA_052'][1], images['B2_NTA_052'][2], 0, 70, 155)
    B2_NTA_055 = attributes(images['B2_NTA_055'][0], images['B2_NTA_055'][1], images['B2_NTA_055'][2], 0, 70, 155)
    B2_NTA_058 = attributes(images['B2_NTA_058'][0], images['B2_NTA_058'][1], images['B2_NTA_058'][2], 0, 70, 155)
    B2_NTA_061 = attributes(images['B2_NTA_061'][0], images['B2_NTA_061'][1], images['B2_NTA_061'][2], 0, 70, 155)
    B2_NTA_064 = attributes(images['B2_NTA_064'][0], images['B2_NTA_064'][1], images['B2_NTA_064'][2], 0, 70, 155)
    B2_NTA_067 = attributes(images['B2_NTA_067'][0], images['B2_NTA_067'][1], images['B2_NTA_067'][2], 0, 70, 155)
    B2_NTA_070 = attributes(images['B2_NTA_070'][0], images['B2_NTA_070'][1], images['B2_NTA_070'][2], 0, 70, 155)
    B2_NTA_073 = attributes(images['B2_NTA_073'][0], images['B2_NTA_073'][1], images['B2_NTA_073'][2], 0, 70, 155)
    B2_NTA_076 = attributes(images['B2_NTA_076'][0], images['B2_NTA_076'][1], images['B2_NTA_076'][2], 0, 70, 155)
    B2_NTA_079 = attributes(images['B2_NTA_079'][0], images['B2_NTA_079'][1], images['B2_NTA_079'][2], 0, 70, 155)
    B2_NTA_082 = attributes(images['B2_NTA_082'][0], images['B2_NTA_082'][1], images['B2_NTA_082'][2], 0, 70, 155)
    B2_NTA_085 = attributes(images['B2_NTA_085'][0], images['B2_NTA_085'][1], images['B2_NTA_085'][2], 0, 70, 155)
    B2_NTA_088 = attributes(images['B2_NTA_088'][0], images['B2_NTA_088'][1], images['B2_NTA_088'][2], 0, 70, 155)
    B2_NTA_091 = attributes(images['B2_NTA_091'][0], images['B2_NTA_091'][1], images['B2_NTA_091'][2], 0, 70, 155)
    B2_NTA_094 = attributes(images['B2_NTA_094'][0], images['B2_NTA_094'][1], images['B2_NTA_094'][2], 0, 70, 155)
    B2_NTA_097 = attributes(images['B2_NTA_097'][0], images['B2_NTA_097'][1], images['B2_NTA_097'][2], 0, 70, 155)
    B2_NTA_100 = attributes(images['B2_NTA_100'][0], images['B2_NTA_100'][1], images['B2_NTA_100'][2], 0, 70, 155)
    B2_NTA_103 = attributes(images['B2_NTA_103'][0], images['B2_NTA_103'][1], images['B2_NTA_103'][2], 0, 70, 155)
    B2_NTA_106 = attributes(images['B2_NTA_106'][0], images['B2_NTA_106'][1], images['B2_NTA_106'][2], 0, 70, 155)
    B2_NTA_109 = attributes(images['B2_NTA_109'][0], images['B2_NTA_109'][1], images['B2_NTA_109'][2], 0, 70, 155)
    B2_NTA_112 = attributes(images['B2_NTA_112'][0], images['B2_NTA_112'][1], images['B2_NTA_112'][2], 0, 70, 155)
    B2_NTA_115 = attributes(images['B2_NTA_115'][0], images['B2_NTA_115'][1], images['B2_NTA_115'][2], 0, 70, 155)
    B2_NTA_118 = attributes(images['B2_NTA_118'][0], images['B2_NTA_118'][1], images['B2_NTA_118'][2], 0, 70, 155)
    B2_NTA_121 = attributes(images['B2_NTA_121'][0], images['B2_NTA_121'][1], images['B2_NTA_121'][2], 0, 70, 155)
    
    B3_FCWA = attributes(images['B3_FCWA'][0], images['B3_FCWA'][1], images['B3_FCWA'][2], 0, 310, 175)
    B3_FCW_B = attributes(images['B3_FCW_B'][0], images['B3_FCW_B'][1], images['B3_FCW_B'][2], 0, 310, 175)
    B3_FCWB_2 = attributes(images['B3_FCWB_2'][0], images['B3_FCWB_2'][1], images['B3_FCWB_2'][2], 0, 362, 181)
    B3_PDWA = attributes(images['B3_PDWA'][0], images['B3_PDWA'][1], images['B3_PDWA'][2], 0, 310, 175)
    B3_PDWB_2 = attributes(images['B3_PDWB_2'][0], images['B3_PDWB_2'][1], images['B3_PDWB_2'][2], 0, 362, 181)
    B3_PDW_1 = attributes(images['B3_PDW_1'][0], images['B3_PDW_1'][1], images['B3_PDW_1'][2], 0, 310, 175)
    B3_PDW_2 = attributes(images['B3_PDW_2'][0], images['B3_PDW_2'][1], images['B3_PDW_2'][2], 0, 310, 175)
    B3_PDW_3 = attributes(images['B3_PDW_3'][0], images['B3_PDW_3'][1], images['B3_PDW_3'][2], 0, 310, 175)
    B3_PDW_4 = attributes(images['B3_PDW_4'][0], images['B3_PDW_4'][1], images['B3_PDW_4'][2], 0, 310, 175)
    
    # B4_LLDW_001 = attributes(images['B4_LLDW_001'][0], images['B4_LLDW_001'][1], images['B4_LLDW_001'][2], 0, 190, 155)
    # B4_LLDW_002 = attributes(images['B4_LLDW_002'][0], images['B4_LLDW_002'][1], images['B4_LLDW_002'][2], 0, 190, 155)
    # B4_LLDW_003 = attributes(images['B4_LLDW_003'][0], images['B4_LLDW_003'][1], images['B4_LLDW_003'][2], 0, 190, 155)
    # B4_LLDW_004 = attributes(images['B4_LLDW_004'][0], images['B4_LLDW_004'][1], images['B4_LLDW_004'][2], 0, 190, 155)
    # B4_LLDW_005 = attributes(images['B4_LLDW_005'][0], images['B4_LLDW_005'][1], images['B4_LLDW_005'][2], 0, 190, 155)
    # B4_RLDW_001 = attributes(images['B4_RLDW_001'][0], images['B4_RLDW_001'][1], images['B4_RLDW_001'][2], 0, 190, 155)
    # B4_RLDW_002 = attributes(images['B4_RLDW_002'][0], images['B4_RLDW_002'][1], images['B4_RLDW_002'][2], 0, 190, 155)
    # B4_RLDW_003 = attributes(images['B4_RLDW_003'][0], images['B4_RLDW_003'][1], images['B4_RLDW_003'][2], 0, 190, 155)
    # B4_RLDW_004 = attributes(images['B4_RLDW_004'][0], images['B4_RLDW_004'][1], images['B4_RLDW_004'][2], 0, 190, 155)
    # B4_RLDW_005 = attributes(images['B4_RLDW_005'][0], images['B4_RLDW_005'][1], images['B4_RLDW_005'][2], 0, 190, 155)
    
    B4_LLDW_attributes = []
    for i in range(1, 31):
        key = f'B4_LLDW_{str(i).zfill(3)}'
        B4_LLDW_attributes.append(attributes(images[key][0], images[key][1], images[key][2], 0, 190, 155))
        
    B4_RLDW_attributes = []
    for i in range(1, 31):
        key = f'B4_RLDW_{str(i).zfill(3)}'
        B4_RLDW_attributes.append(attributes(images[key][0], images[key][1], images[key][2], 0, 190, 155))
        
    


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
    ip_detection="127.0.0.1"
    port_detection=32770

    sock_recv_detection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    server_address = (ip_detection, port_detection)
    sock_recv_detection.bind(server_address)   # Bind the socket to the port

    fcw_warning=FCWarningAlgorithm()

    if_no_title=True
    display = jetson.utils.glDisplay(0,0,1280,720,if_no_title,False)
    # display = jetson.utils.glDisplay(0,0,1280,720,if_no_title,True)
    img_start_x=0
    img_start_y=0
    bg_img,bg_img_width,bg_img_height=jetson.utils.loadImageRGBA("background.png")
    test_txt_x=100
    test_txt_y=435
    test_txt_size=250
    test_txt_R,test_txt_G,test_txt_B,test_txt_A=(255,0,0,255)

    p = Process(target=udp_receiver, args=(can_recv_ip,can_recv_port,shared_dict,))
    p.start()

    # render pattern
    count = 0
    startTime = time.time()
    start, now = 0, 0
    fps = 30
    f = round(1000 / fps) / 1000
    lastTime = time.time()
    lastB3B4, lastA4, last_unit, last_dUnit = '', '', '', ''
    last_a3_number, last_a4_number = 0, 0
    # a2_number, a3_number, a4_number = 70, 100, 20
    # dUnit, unit = '', ''


    while True:
    # while display.IsOpen():
        #---------------get detection result of this frame-----------------
        data, address = sock_recv_detection.recvfrom(8192)
        detection_this_frame=json.loads(data.decode('utf8'))
        #---------------get detection result of this frame-----------------

        #---------------get current can info-----------
        can_this_frame=shared_dict
        #---------------get current can info-----------

        FCW_warning_level,FCW_main_obj_class,PDW_right_near,PDW_right_far,PDW_left_near,PDW_left_far =fcw_warning.update(detection_this_frame, can_this_frame["Speed"], can_this_frame["BrakeSignal"], can_this_frame["LeftSignal"], can_this_frame["RightSignal"])
        #FCW_warning_level:0=normal,1=blue,2=red ; FCW_main_obj_class=['Sedan', 'Truck', 'Bus', 'Motorcycle', 'Person'] ; PDW_X_X:0=normal,1=warning

        #--------------difference---------------
        count += 1
        dif = time.time() - startTime
        lastTime = time.time()
        #--------------frame count---------------

        # display functions
        def A1_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, A1.img, A1.img_x, A1.img_y, A1.img_width, A1.img_height)
            
        def A2_B_display():
            tDif = dif * 1000
            frame = 500
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, A2_B.img, A2_B.img_x, A2_B.img_y, A2_B.img_width, A2_B.img_height, A2_B.alpha)
            if (tDif//frame)%2== 0:
                A2_B.alpha = min(A2_B.alpha + 80, 255)
            else:
                A2_B.alpha = max(A2_B.alpha - 80, 50)
            
        def A2_L_display():
            tDif = dif * 1000
            frame = 500
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, A2_L.img, A2_L.img_x, A2_L.img_y, A2_L.img_width, A2_L.img_height, A2_L.alpha)
            if (tDif//frame)%2== 0:
                A2_L.alpha = min(A2_L.alpha + 80, 255)
            else:
                A2_L.alpha = max(A2_L.alpha - 80, 50)
        
        def A2_R_display():
            tDif = dif * 1000
            frame = 500
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, A2_R.img, A2_R.img_x, A2_R.img_y, A2_R.img_width, A2_R.img_height, A2_R.alpha)
            if (tDif//frame)%2== 0:
                A2_R.alpha = min(A2_R.alpha + 80, 255)
            else:
                A2_R.alpha = max(A2_R.alpha - 80, 50)
            
        def A3_SF_display():
            tDif = dif * 1000
            frame = 500
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, A3_SF.img, A3_SF.img_x, A3_SF.img_y, A3_SF.img_width, A3_SF.img_height, A3_SF.alpha)
            if (tDif//frame)%2== 0:
                A3_SF.alpha = min(A3_SF.alpha + 80, 255)
            else:
                A3_SF.alpha = max(A3_SF.alpha - 80, 50)
            
        def A3_BL_display():
            tDif = dif * 1000
            frame = 500
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, A3_BL.img, A3_BL.img_x, A3_BL.img_y, A3_BL.img_width, A3_BL.img_height, A3_BL.alpha)
            if (tDif//frame)%2== 0:
                A3_BL.alpha = min(A3_BL.alpha + 80, 255)
            else:
                A3_BL.alpha = max(A3_BL.alpha - 80, 50)
        
        def A3_MH_display():
            tDif = dif * 1000
            frame = 500
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, A3_MH.img, A3_MH.img_x, A3_MH.img_y, A3_MH.img_width, A3_MH.img_height, A3_MH.alpha)
            if (tDif//frame)%2== 0:
                A3_MH.alpha = min(A3_MH.alpha + 80, 255)
            else:
                A3_MH.alpha = max(A3_MH.alpha - 80, 50)
            
        def A3_MS_display():
            tDif = dif * 1000
            frame = 500
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, A3_MS.img, A3_MS.img_x, A3_MS.img_y, A3_MS.img_width, A3_MS.img_height, A3_MS.alpha)
            if (tDif//frame)%2== 0:
                A3_MS.alpha = min(A3_MS.alpha + 80, 255)
            else:
                A3_MS.alpha = max(A3_MS.alpha - 80, 50)
            
        def A3_BF_display():
            tDif = dif * 1000
            frame = 500
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, A3_BF.img, A3_BF.img_x, A3_BF.img_y, A3_BF.img_width, A3_BF.img_height, A3_BF.alpha)
            if (tDif//frame)%2== 0:
                A3_BF.alpha = min(A3_BF.alpha + 80, 255)
            else:
                A3_BF.alpha = max(A3_BF.alpha - 80, 50)
            
        def A4_S_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, A4_S.img, A4_S.img_x, A4_S.img_y, A4_S.img_width, A4_S.img_height)
            
        def A4_TR_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, A4_TR.img, A4_TR.img_x, A4_TR.img_y, A4_TR.img_width, A4_TR.img_height)
        
        def A4_TL_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, A4_TL.img, A4_TL.img_x, A4_TL.img_y, A4_TL.img_width, A4_TL.img_height)
            
        # def A4_KR_display():
        #     A4_KR.alpha = renderPattern(A4_KR.img, A4_KR.img_x, A4_KR.img_y, A4_KR.img_width, A4_KR.img_height, A4_KR.alpha, 255, 255, 1, 255, 1, 0, count)
            
        # def A4_KL_display():
        #     A4_KL.alpha = renderPattern(A4_KL.img, A4_KL.img_x, A4_KL.img_y, A4_KL.img_width, A4_KL.img_height, A4_KL.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def A4_TA_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, A4_TA.img, A4_TA.img_x, A4_TA.img_y, A4_TA.img_width, A4_TA.img_height)
            
        def A4_D_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, A4_D.img, A4_D.img_x, A4_D.img_y, A4_D.img_width, A4_D.img_height)
            
        # def A5_display():
        #     A5.alpha = renderPattern(A5.img, A5.img_x, A5.img_y, A5.img_width, A5.img_height, A5.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def B5_display():
            # frame = 200 
            # tDif = dif * 1000
            # B5_images = [B5_001, B5_002, B5_003, B5_002, B5_001]
            # i = 0
            # for i in range(len(B5_images)):
            #     if (tDif//frame)%5 == i%5:
            #         jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B5_images[i%5].img, B5_images[i%5].img_x, B5_images[i%5].img_y, B5_images[i%5].img_width, B5_images[i%5].img_height)
            #         break
            frame = 33 
            tDif = dif * 1000
            B5_images = B5_attributes
            # B5_images = [B5_001, B5_002, B5_003, B5_004, B5_005, B5_006, B5_007, B5_008, B5_009, B5_010, B5_011, B5_012, B5_013, B5_014, B5_015, B5_016, B5_017, B5_018, B5_019, B5_020, B5_021, B5_022, B5_023, B5_024, B5_025, B5_026, B5_027, B5_028, B5_029, B5_030, B5_031, B5_032, B5_033, B5_034, B5_035, B5_036]
            i = 0
            for i in range(len(B5_images)):
                if (tDif//frame)%36 == i%36:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B5_images[i%36].img, B5_images[i%36].img_x, B5_images[i%36].img_y, B5_images[i%36].img_width, B5_images[i%36].img_height)
                    break
            

        def B6_display():
            # frame = 200 
            # tDif = dif * 1000
            # B6_images = [B6_001, B6_002, B6_003, B6_002, B6_001]
            # i = 0
            # for i in range(len(B6_images)):
            #     if (tDif//frame)%5 == i%5:
            #         jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B6_images[i%5].img, B6_images[i%5].img_x, B6_images[i%5].img_y, B6_images[i%5].img_width, B6_images[i%5].img_height)
            #         break
            frame = 33 
            tDif = dif * 1000
            B6_images = B6_attributes
            i = 0
            for i in range(len(B6_images)):
                if (tDif//frame)%36 == i%36:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B6_images[i%36].img, B6_images[i%36].img_x, B6_images[i%36].img_y, B6_images[i%36].img_width, B6_images[i%36].img_height)
                    break
        
        def B1_S_display(): # go straight
            # frame = 200 
            # tDif = dif * 1000
            # S_images = [B1_S_031, B1_S_037, B1_S_043, B1_S_049, B1_S_055]
            # i = 0
            # for i in range(len(S_images)):
            #     if (tDif//frame)%5 == i%5:
            #         jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, S_images[i%5].img, S_images[i%5].img_x, S_images[i%5].img_y, S_images[i%5].img_width, S_images[i%5].img_height)
            #         break
            frame = 33 
            tDif = dif * 1000
            S_images = B1_S_attributes
            i = 0
            for i in range(len(S_images)):
                if (tDif//frame)%150 == i%150:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, S_images[i%150].img, S_images[i%150].img_x, S_images[i%150].img_y, S_images[i%150].img_width, S_images[i%150].img_height)
                    break
            
            
        def B1_R_Far_display(): # turn right
            # frame = 250 
            # tDif = dif * 1000
            # FTR_images = [B1_FTR_001, B1_FTR_010, B1_FTR_019, B1_FTR_028]
            # i = 0
            # for i in range(len(FTR_images)):
            #     if (tDif//frame)%4 == i%4:
            #         jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, FTR_images[i%4].img, FTR_images[i%4].img_x, FTR_images[i%4].img_y, FTR_images[i%4].img_width, FTR_images[i%4].img_height)
            #         break
            frame = 33 
            tDif = dif * 1000
            FTR_images = B1_FTR_attributes
            i = 0
            for i in range(len(FTR_images)):
                if (tDif//frame)%36 == i%36:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, FTR_images[i%36].img, FTR_images[i%36].img_x, FTR_images[i%36].img_y, FTR_images[i%36].img_width, FTR_images[i%36].img_height)
                    break

                       
        def B1_L_Far_display(): # turn left
            # frame = 250 
            # tDif = dif * 1000
            # FTL_images = [B1_FTL_001, B1_FTL_010, B1_FTL_019, B1_FTL_028]
            # i = 0
            # for i in range(len(FTL_images)):
            #     if (tDif//frame)%4 == i%4:
            #         jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, FTL_images[i%4].img, FTL_images[i%4].img_x, FTL_images[i%4].img_y, FTL_images[i%4].img_width, FTL_images[i%4].img_height)
            #         break
            frame = 33 
            tDif = dif * 1000
            FTL_images = B1_FTL_attributes
            i = 0
            for i in range(len(FTL_images)):
                if (tDif//frame)%36 == i%36:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, FTL_images[i%36].img, FTL_images[i%36].img_x, FTL_images[i%36].img_y, FTL_images[i%36].img_width, FTL_images[i%36].img_height)
                    break
        
        def B1_A_Far_display(): # turn around
            # frame = 250
            # tDif = dif * 1000
            # FTA_images = [B1_FTA_001, B1_FTA_010, B1_FTA_019, B1_FTA_028]
            # i = 0
            # for i in range(len(FTA_images)):
            #     if (tDif//frame)%4 == i%4:
            #         jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, FTA_images[i%4].img, FTA_images[i%4].img_x, FTA_images[i%4].img_y, FTA_images[i%4].img_width, FTA_images[i%4].img_height)
            #         break
            frame = 33 
            tDif = dif * 1000
            FTA_images = B1_FTA_attributes
            i = 0
            for i in range(len(FTA_images)):
                if (tDif//frame)%36 == i%36:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, FTA_images[i%36].img, FTA_images[i%36].img_x, FTA_images[i%36].img_y, FTA_images[i%36].img_width, FTA_images[i%36].img_height)
                    break
                
            
        def B1_R_Near_display(start): # turn right
            tDif = dif * 1000
            NTR_images_B1 = [B1_NTR_001, B1_NTR_004, B1_NTR_007, B1_NTR_010, B1_NTR_013, B1_NTR_016, B1_NTR_019, B1_NTR_022, B1_NTR_025, B1_NTR_028, B1_NTR_031, B1_NTR_034, B1_NTR_037, B1_NTR_040, B1_NTR_043, B1_NTR_046]
            NTR_images_B2 = [B2_NTR_049, B2_NTR_052, B2_NTR_055, B2_NTR_058, B2_NTR_061, B2_NTR_064, B2_NTR_067, B2_NTR_070, B2_NTR_073, B2_NTR_076, B2_NTR_079, B2_NTR_082, B2_NTR_085, B2_NTR_088, B2_NTR_091, B2_NTR_094, B2_NTR_097, B2_NTR_100, B2_NTR_103, B2_NTR_106, B2_NTR_109, B2_NTR_112, B2_NTR_115]
            NTR_images = NTR_images_B1 + NTR_images_B2
            frame = 150 
            i = 0
            for i in range((len(NTR_images)*frame)):
                image = NTR_images[int(i/frame)]
                if tDif < start + i:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
                    break
                if i == (len(NTR_images)*frame)-1:
                    image = NTR_images[-1]
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
            
            
        def B1_L_Near_display(start): # turn left
            tDif = dif * 1000
            NTL_images_B1 = [B1_NTL_001, B1_NTL_004, B1_NTL_007, B1_NTL_010, B1_NTL_013, B1_NTL_016, B1_NTL_019, B1_NTL_022, B1_NTL_025, B1_NTL_028, B1_NTL_031, B1_NTL_034, B1_NTL_037, B1_NTL_040, B1_NTL_043, B1_NTL_046]
            NTL_images_B2 = [B2_NTL_049, B2_NTL_052, B2_NTL_055, B2_NTL_058, B2_NTL_061, B2_NTL_064, B2_NTL_067, B2_NTL_070, B2_NTL_073, B2_NTL_076, B2_NTL_079, B2_NTL_082, B2_NTL_085, B2_NTL_088, B2_NTL_091, B2_NTL_094, B2_NTL_097, B2_NTL_100, B2_NTL_103, B2_NTL_106, B2_NTL_109, B2_NTL_112, B2_NTL_115]
            NTL_images = NTL_images_B1 + NTL_images_B2
            frame = 150 
            i = 0
            for i in range((len(NTL_images)*frame)):
                image = NTL_images[int(i/frame)]
                if tDif < start + i:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
                    break
                if i == (len(NTL_images)*frame)-1:
                    image = NTL_images[-1]
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
                
            
        def B1_A_Near_display(start): # turn around
            tDif = dif * 1000
            NTA_images_B1 = [B1_NTA_001, B1_NTA_004, B1_NTA_007, B1_NTA_010, B1_NTA_013, B1_NTA_016, B1_NTA_019, B1_NTA_022, B1_NTA_025, B1_NTA_028, B1_NTA_031, B1_NTA_034, B1_NTA_037, B1_NTA_040, B1_NTA_043, B1_NTA_046]
            NTA_images_B2 = [B2_NTA_049, B2_NTA_052, B2_NTA_055, B2_NTA_058, B2_NTA_061, B2_NTA_064, B2_NTA_067, B2_NTA_070, B2_NTA_073, B2_NTA_076, B2_NTA_079, B2_NTA_082, B2_NTA_085, B2_NTA_088, B2_NTA_091, B2_NTA_094, B2_NTA_097, B2_NTA_100, B2_NTA_103, B2_NTA_106, B2_NTA_109, B2_NTA_112, B2_NTA_115, B2_NTA_118, B2_NTA_121]
            NTA_images = NTA_images_B1 + NTA_images_B2
            frame = 150 
            i = 0
            for i in range((len(NTA_images)*frame)):
                image = NTA_images[int(i/frame)]
                if tDif < start + i:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
                    break
                if i == (len(NTA_images)*frame)-1:
                    image = NTA_images[-1]
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
    
            
        def B3_F_L1_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B3_FCW_B.img, B3_FCW_B.img_x, B3_FCW_B.img_y, B3_FCW_B.img_width, B3_FCW_B.img_height)
            tDif = dif * 1000
            frame = 1000
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, B3_FCWB_2.img, B3_FCWB_2.img_x, B3_FCWB_2.img_y, B3_FCWB_2.img_width, B3_FCWB_2.img_height, B3_FCWB_2.alpha)
            if (tDif//frame)%2== 0:
                B3_FCWB_2.alpha = min(B3_FCWB_2.alpha + 40, 255)
            else:
                B3_FCWB_2.alpha = max(B3_FCWB_2.alpha - 40, 50)
            
        
        def B3_F_L2_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B3_FCWA.img, B3_FCWA.img_x, B3_FCWA.img_y, B3_FCWA.img_width, B3_FCWA.img_height)
        
        def B3_P_L1_display():
            jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B3_FCW_B.img, B3_FCW_B.img_x, B3_FCW_B.img_y, B3_FCW_B.img_width, B3_FCW_B.img_height)
            tDif = dif * 1000
            frame = 1000
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, B3_PDWB_2.img, B3_PDWB_2.img_x, B3_PDWB_2.img_y, B3_PDWB_2.img_width, B3_PDWB_2.img_height, B3_PDWB_2.alpha)
            if (tDif//frame)%2== 0:
                B3_PDWB_2.alpha = min(B3_PDWB_2.alpha + 40, 255)
            else:
                B3_PDWB_2.alpha = max(B3_PDWB_2.alpha - 40, 50)
        
        def B3_P_L2_display():
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, B3_PDWA.img, B3_PDWA.img_x, B3_PDWA.img_y, B3_PDWA.img_width, B3_PDWA.img_height, 255)
        
        def B3_P_display(PNum):
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, B3_FCW_B.img, B3_FCW_B.img_x, B3_FCW_B.img_y, B3_FCW_B.img_width, B3_FCW_B.img_height, 255)
            P_images = [B3_PDW_1, B3_PDW_2, B3_PDW_3, B3_PDW_4]
            tDif = dif * 1000
            frame = 1000
            for i in range(len(P_images)):
                if i+1 == PNum:
                    image = P_images[i]
                    jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height, image.alpha)
                    if (tDif//frame)%2== 0:
                        image.alpha = min(image.alpha + 40, 255)
                    else:
                        image.alpha = max(image.alpha - 40, 50)
        
        def B4_R_display():
            # B4_R_images = [B4_RLDW_001, B4_RLDW_002, B4_RLDW_003, B4_RLDW_004, B4_RLDW_005]
            # tDif = dif * 1000
            # frame = 200
            # for i in range(len(B4_R_images)):
            #     if (tDif//frame)%5 == i%5:
            #         image = B4_R_images[i]
            #         jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
            #         break
            tDif = dif * 1000
            frame = 33
            B4_R_images = B4_RLDW_attributes
            for i in range(len(B4_R_images)):
                if (tDif//frame)%30 == i%30:
                    image = B4_R_images[i]
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
                    break
            
            
        
        def B4_L_display():
            # B4_L_images = [B4_LLDW_001, B4_LLDW_002, B4_LLDW_003, B4_LLDW_004, B4_LLDW_005]
            # tDif = dif * 1000
            # frame = 200
            # for i in range(len(B4_L_images)):
            #     if (tDif//frame)%5 == i%5:
            #         image = B4_L_images[i]
            #         jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
            #         break
            tDif = dif * 1000
            frame = 33
            B4_L_images = B4_LLDW_attributes
            for i in range(len(B4_L_images)):
                if (tDif//frame)%30 == i%30:
                    image = B4_L_images[i]
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, image.img, image.img_x, image.img_y, image.img_width, image.img_height)
                    break
        

        jetson.utils.Overlay_all(bg_img, bg_img_width, bg_img_height, 0,0,0,255)

        p = 3 # priority
        a = 0 # collision alert

        a2_number, a3_number, a4_number = 70, 100, 20
        dUnit, unit = '', ''
        # A1--------------------------
        A1_display()
        # for testing-----------
        if (dif//10) % 2 == 0:
            a1_number = 120 # for testing
        else:
            a1_number = 80
        # A1--------------------------

        # A2--------------------------
        # for testing-----------
        if a2_number < 120:
            a2_number = 70 + int(dif)%50
        else:
            a2_number = 70
        if (dif//10) % 3 == 0:
            A2_L_display() # for testing
        elif (dif//10) % 3 == 1:
            A2_R_display()
        else:
            A2_B_display()
        # for testing-----------
        # A2---------------------------
        
        # A3---------------------------
        # for testing-----------
        if dif < 10:
            pass
        elif dif < 20:
            A3_MH_display()
        elif dif < 30:
            A3_MS_display()
        elif dif < 40:
            A3_SF_display()
        elif dif < 50:
            A3_BL_display()
        elif dif < 60:
            A3_BF_display()
        if dif >= 10 and dif < 60:
            p = 1
        # for testing-----------
        # A3----------------------------

        # B5/B6-------------------------
        # for testing-----------
        if (dif//10) % 2 == 0:
            B5_display()
        else:
            B6_display() # for testing
        # for testing-----------
        # B5/B6-------------------------

        # B3----------------------------------
        # for testing------------------
        if dif < 10:
            pass
        elif dif< 15:
            B3_P_display(1)
        elif dif < 20:
            B3_P_display(2)
        elif dif < 25:
            B3_P_display(3)
        elif dif < 30:
            B3_P_display(4)
        elif dif < 35:
            B3_F_L1_display()
        elif dif < 40:
            B3_F_L2_display()
        elif dif < 45:
            B3_P_L1_display()
        elif dif < 50:
            B3_P_L2_display()
        if dif >= 10 and dif < 50:  
            p = 1
            a = 1
        # for testing------------------
        # B3----------------------------------

        # B4----------------------------------
        # for testing---------------
        if dif >= 50 and dif < 60:
            B4_L_display()
            p = 2
        elif dif >= 60 and dif < 70:
            B4_R_display()
            p = 2
        # for testing---------------
        # B4----------------------------------

        # A4 value----------------------------
        # for testing-------------
        if a3_number > 1:
            a3_number = 100 - 3*(int(dif)%33)
            a4_number = a3_number
            unit = 'm'
        elif a3_number >= 0:
            a3_number = -1
            a4_number = 0
            dUnit = 'm'
        else:
            a3_number = 100
            a4_number = a3_number
            unit = 'm'

        # for testing-------------
        # A4 value----------------------------

        # A4 pattern--------------------------
        # for testing-------------
        if dif < 70:
            pass
        elif dif < 80:
            if lastA4 != 'S':
                start = 0
            lastA4 = 'S'
            A4_S_display()
            if p == 3:
                B1_S_display()
        elif dif < 99:
            if lastA4 != 'TL':
                start = 0
            lastA4 = 'TL'
            A4_TL_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = dif * 1000
                B1_L_Near_display(start)
            elif p == 3 and unit == 'm' and a3_number < 50:
                B1_L_Near_display(start)
            elif p == 3:
                B1_L_Far_display()
        elif dif < 132:
            if lastA4 != 'TR':
                start = 0
            lastA4 = 'TR'
            A4_TR_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = dif * 1000
                B1_R_Near_display(start)
            elif p == 3 and unit == 'm' and a3_number < 50:
                B1_R_Near_display(start)
            elif p == 3:
                B1_R_Far_display()
        elif dif < 165:
            if lastA4 != 'TA':
                start = 0
            lastA4 = 'TA'
            A4_TA_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = dif * 1000
                B1_A_Near_display(start)
            elif p == 3 and unit == 'm' and a3_number < 50:
                B1_A_Near_display(start)
            elif p == 3:
                B1_A_Far_display()
        # for testing-------------
        # A4 pattern--------------------------



        print(dif)

        if a1_number >= 100:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a1_number), test_txt_x,test_txt_y,80,0,255,255,255)
        elif a1_number >= 10:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a1_number), test_txt_x+18,test_txt_y,80,0,255,255,255)
        elif a1_number >= 0:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a1_number), test_txt_x+36,test_txt_y,80,0,255,255,255)

        if a2_number >= 100:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+230,test_txt_y-15,80,0,255,255,255)
        elif a2_number >= 10:
            # jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+248,test_txt_y-15,80,0,255,255,255) 
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, '0', test_txt_x+230,test_txt_y-15,80,0,255,255,50)
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+273,test_txt_y-15,80,0,255,255,255)
        elif a2_number >= 0:
            # jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+266,test_txt_y-15,80,0,255,255,255) 
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, '00', test_txt_x+230,test_txt_y-15,80,0,255,255,50)
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+315,test_txt_y-15,80,0,255,255,255)

       
        if dUnit == 'm' and a4_number == 0:
            # if a4_number >= 100:
            #     jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+750,test_txt_y+40,80,0,255,255,255)
            # elif a4_number >= 10:
            #     jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+758,test_txt_y+40,80,0,255,255,255)
            # elif a4_number >= 0:
            #     jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+776,test_txt_y+40,80,0,255,255,255)
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, '00', test_txt_x+770,test_txt_y+40,80,0,255,255,50)
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number), test_txt_x+855,test_txt_y+40,80,0,255,255,255)
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, dUnit, test_txt_x+895,test_txt_y+65,50,0,255,255,255)
        elif unit == 'm' or unit =='km':
            if a3_number >= 100:
                # jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number)+unit, test_txt_x+750,test_txt_y+40,80,0,255,255,255)
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number), test_txt_x+770,test_txt_y+40,80,0,255,255,255)
            elif a3_number >= 10:
                # jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number)+unit, test_txt_x+758,test_txt_y+40,80,0,255,255,255)
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, '0', test_txt_x+770,test_txt_y+40,80,0,255,255,50)
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number), test_txt_x+812,test_txt_y+40,80,0,255,255,255)
            elif a3_number >= 0:
                # jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number)+unit, test_txt_x+776,test_txt_y+40,80,0,255,255,255) 
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, '00', test_txt_x+770,test_txt_y+40,80,0,255,255,50)
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number), test_txt_x+855,test_txt_y+40,80,0,255,255,255)
            if unit == 'm':
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, unit, test_txt_x+895,test_txt_y+65,50,0,255,255,255)
            elif unit =='km':
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, unit, test_txt_x+895,test_txt_y+50,50,0,255,255,255)


        display.RenderOnce(bg_img, bg_img_width, bg_img_height,img_start_x,img_start_y)