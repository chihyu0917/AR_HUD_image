
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
            if abs(xdis)<=self.FCW_warning_x_range and ydis<front_min_ydis and ydis>400:	#reflect
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


