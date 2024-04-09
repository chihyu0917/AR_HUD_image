from multiprocessing import Process,Manager
import time
import json
import socket

import jetson.utils
import argparse
import sys

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

# parse the command line
parser = argparse.ArgumentParser(description="draw something", 
                           formatter_class=argparse.RawTextHelpFormatter)



parser.add_argument("--width", type=int, default=1280, help="display window width")
parser.add_argument("--height", type=int, default=720, help="display window height")
parser.add_argument("--win_x", type=int, default=0, help="display window start x(xmin)")
parser.add_argument("--win_y", type=int, default=0, help="display window start y(ymin)")
parser.add_argument("--if_no_title", type=bool, default=True, help="True : window with no title; False : window with title")

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


try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)


if __name__ == '__main__':
    manager = Manager()
    shared_dict = manager.dict()

    # draw the canvas
    display = jetson.utils.glDisplay(win_x,win_y,width,height,if_no_title)
    img_start_x=0
    img_start_y=0

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
            'A2_B': './png/W_A2_R_B.png', 'A2_L': './png/W_A2_R_L.png', 'A2_R': './png/W_A2_R_R.png', # A2
            'A3_SF': './png/W_A3_SF.png', 'A3_BL': './png/W_A3_BL.png', 'A3_MH': './png/W_A3_MH.png', 'A3_MS': './png/W_A3_MS.png', 'A3_BF': './png/W_A3_BF.png', # A3
            'A4_S': './png/N_A4_S.png', 'A4_TR': './png/N_A4_TR.png', 'A4_TL': './png/N_A4_TL.png', 'A4_KR': './png/N_A4_KR.png', 
            'A4_KL': './png/N_A4_KL.png', 'A4_TA': './png/N_A4_TA.png', 'A4_D': './png/N_A4_D.png', # A4
            'A5': './png/W_A5_A.png', # A5
            'B5': './png/A_B5_LBIN.png', 'B6': './png/A_B6_RBIN.png', # B5, B6
            'B1_S': './png/N_B1_S.png', 'B1_S_1': './png/N_B1_S_1.png', 'B1_S_2': './png/N_B1_S_2.png', 'B1_S_3': './png/N_B1_S_3.png', 'B1_S_4': './png/N_B1_S_4.png', # B1
            'B1_FTR': './png/N_B1_FTR.png', 'B1_FTL': './png/N_B1_FTL.png', 'B1_FTA': './png/N_B1_FTA.png',
            'B1_NTR_001': './png/N_B1_NTR_001.png', 'B1_NTR_004': './png/N_B1_NTR_004.png', 'B1_NTR_011': './png/N_B1_NTR_011.png', 'B1_NTR_015': './png/N_B1_NTR_015.png', 
            'B1_NTR_022': './png/N_B1_NTR_022.png', 'B1_NTR_028': './png/N_B1_NTR_028.png', 'B1_NTR_034': './png/N_B1_NTR_034.png',
            'B1_NTR_037': './png/N_B1_NTR_037.png', 'B1_NTR_040': './png/N_B1_NTR_040.png', 'B1_NTR_043': './png/N_B1_NTR_043.png', 'B1_NTR_046': './png/N_B1_NTR_046.png',
            'B1_NTL_001': './png/N_B1_NTL_001.png', 'B1_NTL_004': './png/N_B1_NTL_004.png', 'B1_NTL_011': './png/N_B1_NTL_011.png', 'B1_NTL_015': './png/N_B1_NTL_015.png',
            'B1_NTL_022': './png/N_B1_NTL_022.png', 'B1_NTL_028': './png/N_B1_NTL_028.png', 'B1_NTL_034': './png/N_B1_NTL_034.png',
            'B1_NTL_037': './png/N_B1_NTL_037.png', 'B1_NTL_040': './png/N_B1_NTL_040.png', 'B1_NTL_043': './png/N_B1_NTL_043.png', 'B1_NTL_046': './png/N_B1_NTL_046.png',
            'B1_NTA_001': './png/N_B1_NTA_001.png', 'B1_NTA_004': './png/N_B1_NTA_004.png', 'B1_NTA_011': './png/N_B1_NTA_011.png', 'B1_NTA_015': './png/N_B1_NTA_015.png',
            'B1_NTA_022': './png/N_B1_NTA_022.png', 'B1_NTA_028': './png/N_B1_NTA_028.png', 'B1_NTA_034': './png/N_B1_NTA_034.png',
            'B1_NTA_037': './png/N_B1_NTA_037.png', 'B1_NTA_040': './png/N_B1_NTA_040.png', 'B1_NTA_043': './png/N_B1_NTA_043.png', 'B1_NTA_046': './png/N_B1_NTA_046.png',
            'B1_KR_1': './png/N_B1_KR_1.png', 'B1_KR_2': './png/N_B1_KR_2.png', 'B1_KR_3': './png/N_B1_KR_3.png', 'B1_KR_4': './png/N_B1_KR_4.png', 
            'B1_KL_1': './png/N_B1_KL_1.png', 'B1_KL_2': './png/N_B1_KL_2.png', 'B1_KL_3': './png/N_B1_KL_3.png', 'B1_KL_4': './png/N_B1_KL_4.png',
            'B2_NTR_050': './png/N_B1_NTR_050.png', 'B2_NTR_052': './png/N_B1_NTR_052.png', 'B2_NTR_055': './png/N_B1_NTR_055.png', 'B2_NTR_062': './png/N_B1_NTR_062.png',
            'B2_NTR_079': './png/N_B1_NTR_079.png', 'B2_NTR_085': './png/N_B1_NTR_085.png', 'B2_NTR_091': './png/N_B1_NTR_091.png', 'B2_NTR_097': './png/N_B1_NTR_097.png',
            'B2_NTR_104': './png/N_B1_NTR_104.png', 'B2_NTR_110': './png/N_B1_NTR_110.png', 'B2_NTR_116': './png/N_B1_NTR_116.png',
            'B2_NTL_050': './png/N_B1_NTL_050.png', 'B2_NTL_052': './png/N_B1_NTL_052.png', 'B2_NTL_055': './png/N_B1_NTL_055.png', 'B2_NTL_062': './png/N_B1_NTL_062.png',
            'B2_NTL_079': './png/N_B1_NTL_079.png', 'B2_NTL_085': './png/N_B1_NTL_085.png', 'B2_NTL_091': './png/N_B1_NTL_091.png', 'B2_NTL_097': './png/N_B1_NTL_097.png',
            'B2_NTL_104': './png/N_B1_NTL_104.png', 'B2_NTL_110': './png/N_B1_NTL_110.png', 'B2_NTL_116': './png/N_B1_NTL_116.png',
            'B2_NTA_050': './png/N_B1_NTA_050.png', 'B2_NTA_052': './png/N_B1_NTA_052.png', 'B2_NTA_055': './png/N_B1_NTA_055.png', 'B2_NTA_062': './png/N_B1_NTA_062.png',
            'B2_NTA_079': './png/N_B1_NTA_079.png', 'B2_NTA_085': './png/N_B1_NTA_085.png', 'B2_NTA_091': './png/N_B1_NTA_091.png', 'B2_NTA_097': './png/N_B1_NTA_097.png',
            'B2_NTA_104': './png/N_B1_NTA_104.png', 'B2_NTA_110': './png/N_B1_NTA_110.png', 'B2_NTA_116': './png/N_B1_NTA_116.png', 'B2_NTA_122': './png/N_B1_NTA_122.png',
            'B3_FCWA': './png/A_B3_FCWA.png', 'B3_FCW_B': './png/A_B3_FCW_B.png', 'B3_FCWB_2': './png/A_B3_FCWB_002.png', # B3
            'B3_PDWA': './png/A_B3_PDWA.png', 'B3_PDWB_2': './png/A_B3_PDWB_002.png', 'B3_PDW_1': './png/A_B3_PDW_1.png', 'B3_PDW_2': './png/A_B3_PDW_2.png', 'B3_PDW_3': './png/A_B3_PDW_3.png', 'B3_PDW_4': './png/A_B3_PDW_4.png',
            'B4_R_B': './png/A_B4_RLDW_B.png', 'B4_R_R': './png/A_B4_RLDW_R.png', 'B4_BL': './png/A_B4_BL.png', 'B4_L_B': './png/A_B4_LLDW_B.png', 'B4_L_R': './png/A_B4_LLDW_R.png' # B4
        }
        
        images = {}
        for key, path in images_path.items():
            images[key] = jetson.utils.loadImageRGBA(path)
            
        return images
    
    images = loadImages()
    for key in images.keys():
        img, img_width, img_height = images[key]


    A1 = attributes(images['A1'][0], images['A1'][1], images['A1'][2], 0, 80, 387) # A1
    
    A2_B = attributes(images['A2_B'][0], images['A2_B'][1], images['A2_B'][2], 0, 265, 390) # A2
    A2_L = attributes(images['A2_L'][0], images['A2_L'][1], images['A2_L'][2], 0, 265, 390)
    A2_R = attributes(images['A2_R'][0], images['A2_R'][1], images['A2_R'][2], 0, 265, 390)

    A3_SF = attributes(images['A3_SF'][0], images['A3_SF'][1], images['A3_SF'][2], 0, 560, 417) # A3
    A3_BL = attributes(images['A3_BL'][0], images['A3_BL'][1], images['A3_BL'][2], 0, 560, 403)
    A3_MH = attributes(images['A3_MH'][0], images['A3_MH'][1], images['A3_MH'][2], 0, 560, 401)
    A3_MS = attributes(images['A3_MS'][0], images['A3_MS'][1], images['A3_MS'][2], 0, 560, 422)
    A3_BF = attributes(images['A3_BF'][0], images['A3_BF'][1], images['A3_BF'][2], 0, 560, 398)
    
    A4_S = attributes(images['A4_S'][0], images['A4_S'][1], images['A4_S'][2], 0, 782, 404) # A4
    A4_TR = attributes(images['A4_TR'][0], images['A4_TR'][1], images['A4_TR'][2], 0, 770, 404)
    A4_TL = attributes(images['A4_TL'][0], images['A4_TL'][1], images['A4_TL'][2], 0, 770, 404)
    A4_KR = attributes(images['A4_KR'][0], images['A4_KR'][1], images['A4_KR'][2], 0, 770, 404)
    A4_KL = attributes(images['A4_KL'][0], images['A4_KL'][1], images['A4_KL'][2], 0, 770, 404)
    A4_TA = attributes(images['A4_TA'][0], images['A4_TA'][1], images['A4_TA'][2], 0, 776, 404)
    A4_D = attributes(images['A4_D'][0], images['A4_D'][1], images['A4_D'][2], 0, 785, 419)
    
    A5 = attributes(images['A5'][0], images['A5'][1], images['A5'][2], 0, 1045, 407) # A5

    B5 = attributes(images['B5'][0], images['B5'][1], images['B5'][2], 0, 70, 155) # B5
    B6 = attributes(images['B6'][0], images['B6'][1], images['B6'][2], 0, 1128, 155) # B6
    
    B1_S = attributes(images['B1_S'][0], images['B1_S'][1], images['B1_S'][2], 0, 585, 260)
    B1_S_1 = attributes(images['B1_S_1'][0], images['B1_S_1'][1], images['B1_S_1'][2], 0, 585, 260)
    B1_S_2 = attributes(images['B1_S_2'][0], images['B1_S_2'][1], images['B1_S_2'][2], 0, 585, 260)
    B1_S_3 = attributes(images['B1_S_3'][0], images['B1_S_3'][1], images['B1_S_3'][2], 0, 585, 260)
    B1_S_4 = attributes(images['B1_S_4'][0], images['B1_S_4'][1], images['B1_S_4'][2], 0, 585, 260)
    
    B1_FTR = attributes(images['B1_FTR'][0], images['B1_FTR'][1], images['B1_FTR'][2], 0, 585, 175)
    B1_FTL = attributes(images['B1_FTL'][0], images['B1_FTL'][1], images['B1_FTL'][2], 0, 513, 175)
    B1_FTA = attributes(images['B1_FTA'][0], images['B1_FTA'][1], images['B1_FTA'][2], 0, 585, 175)
    
    B1_NTR_001 = attributes(images['B1_NTR_001'][0], images['B1_NTR_001'][1], images['B1_NTR_001'][2], 0, 70, 155)
    B1_NTR_004 = attributes(images['B1_NTR_004'][0], images['B1_NTR_004'][1], images['B1_NTR_004'][2], 0, 70, 155)
    B1_NTR_011 = attributes(images['B1_NTR_011'][0], images['B1_NTR_011'][1], images['B1_NTR_011'][2], 0, 70, 155)
    B1_NTR_015 = attributes(images['B1_NTR_015'][0], images['B1_NTR_015'][1], images['B1_NTR_015'][2], 0, 70, 155)
    B1_NTR_022 = attributes(images['B1_NTR_022'][0], images['B1_NTR_022'][1], images['B1_NTR_022'][2], 0, 70, 155)
    B1_NTR_028 = attributes(images['B1_NTR_028'][0], images['B1_NTR_028'][1], images['B1_NTR_028'][2], 0, 70, 155)
    B1_NTR_034 = attributes(images['B1_NTR_034'][0], images['B1_NTR_034'][1], images['B1_NTR_034'][2], 0, 70, 155)
    B1_NTR_037 = attributes(images['B1_NTR_037'][0], images['B1_NTR_037'][1], images['B1_NTR_037'][2], 0, 70, 155)
    B1_NTR_040 = attributes(images['B1_NTR_040'][0], images['B1_NTR_040'][1], images['B1_NTR_040'][2], 0, 70, 155)
    B1_NTR_043 = attributes(images['B1_NTR_043'][0], images['B1_NTR_043'][1], images['B1_NTR_043'][2], 0, 70, 155)
    B1_NTR_046 = attributes(images['B1_NTR_046'][0], images['B1_NTR_046'][1], images['B1_NTR_046'][2], 0, 70, 155)
    
    B1_NTL_001 = attributes(images['B1_NTL_001'][0], images['B1_NTL_001'][1], images['B1_NTL_001'][2], 0, 70, 155)
    B1_NTL_004 = attributes(images['B1_NTL_004'][0], images['B1_NTL_004'][1], images['B1_NTL_004'][2], 0, 70, 155)
    B1_NTL_011 = attributes(images['B1_NTL_011'][0], images['B1_NTL_011'][1], images['B1_NTL_011'][2], 0, 70, 155)
    B1_NTL_015 = attributes(images['B1_NTL_015'][0], images['B1_NTL_015'][1], images['B1_NTL_015'][2], 0, 70, 155)
    B1_NTL_022 = attributes(images['B1_NTL_022'][0], images['B1_NTL_022'][1], images['B1_NTL_022'][2], 0, 70, 155)
    B1_NTL_028 = attributes(images['B1_NTL_028'][0], images['B1_NTL_028'][1], images['B1_NTL_028'][2], 0, 70, 155)
    B1_NTL_034 = attributes(images['B1_NTL_034'][0], images['B1_NTL_034'][1], images['B1_NTL_034'][2], 0, 70, 155)
    B1_NTL_037 = attributes(images['B1_NTL_037'][0], images['B1_NTL_037'][1], images['B1_NTL_037'][2], 0, 70, 155)
    B1_NTL_040 = attributes(images['B1_NTL_040'][0], images['B1_NTL_040'][1], images['B1_NTL_040'][2], 0, 70, 155)
    B1_NTL_043 = attributes(images['B1_NTL_043'][0], images['B1_NTL_043'][1], images['B1_NTL_043'][2], 0, 70, 155)
    B1_NTL_046 = attributes(images['B1_NTL_046'][0], images['B1_NTL_046'][1], images['B1_NTL_046'][2], 0, 70, 155)
    
    B1_NTA_001 = attributes(images['B1_NTA_001'][0], images['B1_NTA_001'][1], images['B1_NTA_001'][2], 0, 70, 155)
    B1_NTA_004 = attributes(images['B1_NTA_004'][0], images['B1_NTA_004'][1], images['B1_NTA_004'][2], 0, 70, 155)
    B1_NTA_011 = attributes(images['B1_NTA_011'][0], images['B1_NTA_011'][1], images['B1_NTA_011'][2], 0, 70, 155)
    B1_NTA_015 = attributes(images['B1_NTA_015'][0], images['B1_NTA_015'][1], images['B1_NTA_015'][2], 0, 70, 155)
    B1_NTA_022 = attributes(images['B1_NTA_022'][0], images['B1_NTA_022'][1], images['B1_NTA_022'][2], 0, 70, 155)
    B1_NTA_028 = attributes(images['B1_NTA_028'][0], images['B1_NTA_028'][1], images['B1_NTA_028'][2], 0, 70, 155)
    B1_NTA_034 = attributes(images['B1_NTA_034'][0], images['B1_NTA_034'][1], images['B1_NTA_034'][2], 0, 70, 155)
    B1_NTA_037 = attributes(images['B1_NTA_037'][0], images['B1_NTA_037'][1], images['B1_NTA_037'][2], 0, 70, 155)
    B1_NTA_040 = attributes(images['B1_NTA_040'][0], images['B1_NTA_040'][1], images['B1_NTA_040'][2], 0, 70, 155)
    B1_NTA_043 = attributes(images['B1_NTA_043'][0], images['B1_NTA_043'][1], images['B1_NTA_043'][2], 0, 70, 155)
    B1_NTA_046 = attributes(images['B1_NTA_046'][0], images['B1_NTA_046'][1], images['B1_NTA_046'][2], 0, 70, 155)
    
    B1_KR_1 = attributes(images['B1_KR_1'][0], images['B1_KR_1'][1], images['B1_KR_1'][2], 0, 586, 261)
    B1_KR_2 = attributes(images['B1_KR_2'][0], images['B1_KR_2'][1], images['B1_KR_2'][2], 0, 586, 261)
    B1_KR_3 = attributes(images['B1_KR_3'][0], images['B1_KR_3'][1], images['B1_KR_3'][2], 0, 586, 261)
    B1_KR_4 = attributes(images['B1_KR_4'][0], images['B1_KR_4'][1], images['B1_KR_4'][2], 0, 586, 261)
    
    B1_KL_1 = attributes(images['B1_KL_1'][0], images['B1_KL_1'][1], images['B1_KL_1'][2], 0, 540, 261)
    B1_KL_2 = attributes(images['B1_KL_2'][0], images['B1_KL_2'][1], images['B1_KL_2'][2], 0, 540, 261)
    B1_KL_3 = attributes(images['B1_KL_3'][0], images['B1_KL_3'][1], images['B1_KL_3'][2], 0, 540, 261)
    B1_KL_4 = attributes(images['B1_KL_4'][0], images['B1_KL_4'][1], images['B1_KL_4'][2], 0, 540, 261)
     
    B2_NTR_050 = attributes(images['B2_NTR_050'][0], images['B2_NTR_050'][1], images['B2_NTR_050'][2], 0, 70, 155)
    B2_NTR_052 = attributes(images['B2_NTR_052'][0], images['B2_NTR_052'][1], images['B2_NTR_052'][2], 0, 70, 155)
    B2_NTR_055 = attributes(images['B2_NTR_055'][0], images['B2_NTR_055'][1], images['B2_NTR_055'][2], 0, 70, 155)
    B2_NTR_062 = attributes(images['B2_NTR_062'][0], images['B2_NTR_062'][1], images['B2_NTR_062'][2], 0, 70, 155)
    B2_NTR_079 = attributes(images['B2_NTR_079'][0], images['B2_NTR_079'][1], images['B2_NTR_079'][2], 0, 70, 155)
    B2_NTR_085 = attributes(images['B2_NTR_085'][0], images['B2_NTR_085'][1], images['B2_NTR_085'][2], 0, 70, 155)
    B2_NTR_091 = attributes(images['B2_NTR_091'][0], images['B2_NTR_091'][1], images['B2_NTR_091'][2], 0, 70, 155)
    B2_NTR_097 = attributes(images['B2_NTR_097'][0], images['B2_NTR_097'][1], images['B2_NTR_097'][2], 0, 70, 155)
    B2_NTR_104 = attributes(images['B2_NTR_104'][0], images['B2_NTR_104'][1], images['B2_NTR_104'][2], 0, 70, 155)
    B2_NTR_110 = attributes(images['B2_NTR_110'][0], images['B2_NTR_110'][1], images['B2_NTR_110'][2], 0, 70, 155)
    B2_NTR_116 = attributes(images['B2_NTR_116'][0], images['B2_NTR_116'][1], images['B2_NTR_116'][2], 0, 70, 155)
    B2_NTL_050 = attributes(images['B2_NTL_050'][0], images['B2_NTL_050'][1], images['B2_NTL_050'][2], 0, 70, 155)
    B2_NTL_052 = attributes(images['B2_NTL_052'][0], images['B2_NTL_052'][1], images['B2_NTL_052'][2], 0, 70, 155)
    B2_NTL_055 = attributes(images['B2_NTL_055'][0], images['B2_NTL_055'][1], images['B2_NTL_055'][2], 0, 70, 155)
    B2_NTL_062 = attributes(images['B2_NTL_062'][0], images['B2_NTL_062'][1], images['B2_NTL_062'][2], 0, 70, 155)
    B2_NTL_079 = attributes(images['B2_NTL_079'][0], images['B2_NTL_079'][1], images['B2_NTL_079'][2], 0, 70, 155)
    B2_NTL_085 = attributes(images['B2_NTL_085'][0], images['B2_NTL_085'][1], images['B2_NTL_085'][2], 0, 70, 155)
    B2_NTL_091 = attributes(images['B2_NTL_091'][0], images['B2_NTL_091'][1], images['B2_NTL_091'][2], 0, 70, 155)
    B2_NTL_097 = attributes(images['B2_NTL_097'][0], images['B2_NTL_097'][1], images['B2_NTL_097'][2], 0, 70, 155)
    B2_NTL_104 = attributes(images['B2_NTL_104'][0], images['B2_NTL_104'][1], images['B2_NTL_104'][2], 0, 70, 155)
    B2_NTL_110 = attributes(images['B2_NTL_110'][0], images['B2_NTL_110'][1], images['B2_NTL_110'][2], 0, 70, 155)
    B2_NTL_116 = attributes(images['B2_NTL_116'][0], images['B2_NTL_116'][1], images['B2_NTL_116'][2], 0, 70, 155)
    
    B2_NTA_050 = attributes(images['B2_NTA_050'][0], images['B2_NTA_050'][1], images['B2_NTA_050'][2], 0, 70, 155)
    B2_NTA_052 = attributes(images['B2_NTA_052'][0], images['B2_NTA_052'][1], images['B2_NTA_052'][2], 0, 70, 155)
    B2_NTA_055 = attributes(images['B2_NTA_055'][0], images['B2_NTA_055'][1], images['B2_NTA_055'][2], 0, 70, 155)
    B2_NTA_062 = attributes(images['B2_NTA_062'][0], images['B2_NTA_062'][1], images['B2_NTA_062'][2], 0, 70, 155)
    B2_NTA_079 = attributes(images['B2_NTA_079'][0], images['B2_NTA_079'][1], images['B2_NTA_079'][2], 0, 70, 155)
    B2_NTA_085 = attributes(images['B2_NTA_085'][0], images['B2_NTA_085'][1], images['B2_NTA_085'][2], 0, 70, 155)
    B2_NTA_091 = attributes(images['B2_NTA_091'][0], images['B2_NTA_091'][1], images['B2_NTA_091'][2], 0, 70, 155)
    B2_NTA_097 = attributes(images['B2_NTA_097'][0], images['B2_NTA_097'][1], images['B2_NTA_097'][2], 0, 70, 155)
    B2_NTA_104 = attributes(images['B2_NTA_104'][0], images['B2_NTA_104'][1], images['B2_NTA_104'][2], 0, 70, 155)
    B2_NTA_110 = attributes(images['B2_NTA_110'][0], images['B2_NTA_110'][1], images['B2_NTA_110'][2], 0, 70, 155)
    B2_NTA_116 = attributes(images['B2_NTA_116'][0], images['B2_NTA_116'][1], images['B2_NTA_116'][2], 0, 70, 155)
    B2_NTA_122 = attributes(images['B2_NTA_122'][0], images['B2_NTA_122'][1], images['B2_NTA_122'][2], 0, 70, 155)
    
    B3_FCWA = attributes(images['B3_FCWA'][0], images['B3_FCWA'][1], images['B3_FCWA'][2], 0, 310, 175)
    B3_FCW_B = attributes(images['B3_FCW_B'][0], images['B3_FCW_B'][1], images['B3_FCW_B'][2], 0, 310, 175)
    B3_FCWB_2 = attributes(images['B3_FCWB_2'][0], images['B3_FCWB_2'][1], images['B3_FCWB_2'][2], 0, 362, 181)
    B3_PDWA = attributes(images['B3_PDWA'][0], images['B3_PDWA'][1], images['B3_PDWA'][2], 0, 310, 175)
    B3_PDWB_2 = attributes(images['B3_PDWB_2'][0], images['B3_PDWB_2'][1], images['B3_PDWB_2'][2], 0, 362, 181)
    B3_PDW_1 = attributes(images['B3_PDW_1'][0], images['B3_PDW_1'][1], images['B3_PDW_1'][2], 0, 310, 175)
    B3_PDW_2 = attributes(images['B3_PDW_2'][0], images['B3_PDW_2'][1], images['B3_PDW_2'][2], 0, 310, 175)
    B3_PDW_3 = attributes(images['B3_PDW_3'][0], images['B3_PDW_3'][1], images['B3_PDW_3'][2], 0, 310, 175)
    B3_PDW_4 = attributes(images['B3_PDW_4'][0], images['B3_PDW_4'][1], images['B3_PDW_4'][2], 0, 310, 175)
    
    B4_R_B = attributes(images['B4_R_B'][0], images['B4_R_B'][1], images['B4_R_B'][2], 0, 311, 161)
    B4_R_R = attributes(images['B4_R_R'][0], images['B4_R_R'][1], images['B4_R_R'][2], 0, 311, 161)
    B4_BL = attributes(images['B4_BL'][0], images['B4_BL'][1], images['B4_BL'][2], 0, 630, 80)
    B4_L_B = attributes(images['B4_L_B'][0], images['B4_L_B'][1], images['B4_L_B'][2], 0, 311, 161)
    B4_L_R = attributes(images['B4_L_R'][0], images['B4_L_R'][1], images['B4_L_R'][2], 0, 311, 161)

    bg_img,bg_img_width,bg_img_height=jetson.utils.loadImageRGBA("background.png")

    test_txt_x=100
    test_txt_y=435
    test_txt_size=250
    test_txt_R,test_txt_G,test_txt_B,test_txt_A=(255,0,0,255)

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

    # render pattern
    count = 0
    start = 0
    fps = 30
    f = round(1000 / fps) / 1000

    def renderPattern(img, x, y, width, height, alpha, min_alpha, max_alpha, step, base, period, remain, count):
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, img, x, y, width, height, alpha)
        if (count // step) % period == remain:
            alpha = min(alpha + base, max_alpha)
        else:
            alpha = max(alpha - base, min_alpha)
        return alpha


    while True:
    # while display.IsOpen():
        #---------------get detection result of this frame-----------------
        #data, address = sock_recv_detection.recvfrom(port)
        #detection_this_frame=data.decode('utf8')
        #---------------get detection result of this frame-----------------

        #---------------get current can info-----------
        can_this_frame=shared_dict
        #---------------get current can info-----------

        # display functions
        def A1_display():
            A1.alpha = renderPattern(A1.img, A1.img_x, A1.img_y, A1.img_width, A1.img_height, A1.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def A2_B_display():
            A2_B.alpha = renderPattern(A2_B.img, A2_B.img_x, A2_B.img_y, A2_B.img_width, A2_B.img_height, A2_B.alpha, 50, 255, fps/2, 400/fps, 2, 0, count) # 1 Hz
            
        def A2_L_display():
            A2_L.alpha = renderPattern(A2_L.img, A2_L.img_x, A2_L.img_y, A2_L.img_width, A2_L.img_height, A2_L.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)
        
        def A2_R_display():
            A2_R.alpha = renderPattern(A2_R.img, A2_R.img_x, A2_R.img_y, A2_R.img_width, A2_R.img_height, A2_R.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)
            
        def A3_SF_display():
            A3_SF.alpha = renderPattern(A3_SF.img, A3_SF.img_x, A3_SF.img_y, A3_SF.img_width, A3_SF.img_height, A3_SF.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)
            
        def A3_BL_display():
            A3_BL.alpha = renderPattern(A3_BL.img, A3_BL.img_x, A3_BL.img_y, A3_BL.img_width, A3_BL.img_height, A3_BL.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)
        
        def A3_MH_display():
            A3_MH.alpha = renderPattern(A3_MH.img, A3_MH.img_x, A3_MH.img_y, A3_MH.img_width, A3_MH.img_height, A3_MH.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)
            
        def A3_MS_display():
            A3_MS.alpha = renderPattern(A3_MS.img, A3_MS.img_x, A3_MS.img_y, A3_MS.img_width, A3_MS.img_height, A3_MS.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)
            
        def A3_BF_display():
            A3_BF.alpha = renderPattern(A3_BF.img, A3_BF.img_x, A3_BF.img_y, A3_BF.img_width, A3_BF.img_height, A3_BF.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)
            
        def A4_S_display():
            A4_S.alpha = renderPattern(A4_S.img, A4_S.img_x, A4_S.img_y, A4_S.img_width, A4_S.img_height, A4_S.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def A4_TR_display():
            A4_TR.alpha = renderPattern(A4_TR.img, A4_TR.img_x, A4_TR.img_y, A4_TR.img_width, A4_TR.img_height, A4_TR.alpha, 255, 255, 1, 255, 1, 0, count)
        
        def A4_TL_display():
            A4_TL.alpha = renderPattern(A4_TL.img, A4_TL.img_x, A4_TL.img_y, A4_TL.img_width, A4_TL.img_height, A4_TL.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def A4_KR_display():
            A4_KR.alpha = renderPattern(A4_KR.img, A4_KR.img_x, A4_KR.img_y, A4_KR.img_width, A4_KR.img_height, A4_KR.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def A4_KL_display():
            A4_KL.alpha = renderPattern(A4_KL.img, A4_KL.img_x, A4_KL.img_y, A4_KL.img_width, A4_KL.img_height, A4_KL.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def A4_TA_display():
            A4_TA.alpha = renderPattern(A4_TA.img, A4_TA.img_x, A4_TA.img_y, A4_TA.img_width, A4_TA.img_height, A4_TA.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def A4_D_display():
            A4_D.alpha = renderPattern(A4_D.img, A4_D.img_x, A4_D.img_y, A4_D.img_width, A4_D.img_height, A4_D.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def A5_display():
            A5.alpha = renderPattern(A5.img, A5.img_x, A5.img_y, A5.img_width, A5.img_height, A5.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def B5_display():
            B5.alpha = renderPattern(B5.img, B5.img_x, B5.img_y, B5.img_width, B5.img_height, B5.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)
            
        def B6_display():
            B6.alpha = renderPattern(B6.img, B6.img_x, B6.img_y, B6.img_width, B6.img_height, B6.alpha, 50, 255, fps/2, 400/fps, 2, 0, count)  
        
        def B1_S_display(): # go straight
            B1_S_1.alpha = renderPattern(B1_S_1.img, B1_S_1.img_x, B1_S_1.img_y, B1_S_1.img_width, B1_S_1.img_height,B1_S_1.alpha, 50, 255, fps/2, 400/fps, 4, 0, count) 
            B1_S_2.alpha = renderPattern(B1_S_2.img, B1_S_2.img_x, B1_S_2.img_y, B1_S_2.img_width, B1_S_2.img_height,B1_S_2.alpha, 50, 255, fps/2, 400/fps, 4, 1, count)
            B1_S_3.alpha = renderPattern(B1_S_3.img, B1_S_3.img_x, B1_S_3.img_y, B1_S_3.img_width, B1_S_3.img_height,B1_S_3.alpha, 50, 255, fps/2, 400/fps, 4, 2, count)
            B1_S_4.alpha = renderPattern(B1_S_4.img, B1_S_4.img_x, B1_S_4.img_y, B1_S_4.img_width, B1_S_4.img_height,B1_S_4.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
            
        def B1_R_Far_display(): # turn right
            B1_S_1.alpha = renderPattern(B1_S_1.img, B1_S_1.img_x, B1_S_1.img_y, B1_S_1.img_width, B1_S_1.img_height,B1_S_1.alpha, 50, 255, fps/2, 400/fps, 4, 0, count) 
            B1_S_2.alpha = renderPattern(B1_S_2.img, B1_S_2.img_x, B1_S_2.img_y, B1_S_2.img_width, B1_S_2.img_height,B1_S_2.alpha, 50, 255, fps/2, 400/fps, 4, 1, count)
            B1_S_3.alpha = renderPattern(B1_S_3.img, B1_S_3.img_x, B1_S_3.img_y, B1_S_3.img_width, B1_S_3.img_height,B1_S_3.alpha, 50, 255, fps/2, 400/fps, 4, 2, count)
            B1_S_4.alpha = renderPattern(B1_S_4.img, B1_S_4.img_x, B1_S_4.img_y, B1_S_4.img_width, B1_S_4.img_height,B1_S_4.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
            
            B1_FTR.alpha = renderPattern(B1_FTR.img, B1_FTR.img_x, B1_FTR.img_y, B1_FTR.img_width, B1_FTR.img_height,B1_FTR.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
            
        def B1_L_Far_display(): # turn left
            B1_S_1.alpha = renderPattern(B1_S_1.img, B1_S_1.img_x, B1_S_1.img_y, B1_S_1.img_width, B1_S_1.img_height,B1_S_1.alpha, 50, 255, fps/2, 400/fps, 4, 0, count) 
            B1_S_2.alpha = renderPattern(B1_S_2.img, B1_S_2.img_x, B1_S_2.img_y, B1_S_2.img_width, B1_S_2.img_height,B1_S_2.alpha, 50, 255, fps/2, 400/fps, 4, 1, count)
            B1_S_3.alpha = renderPattern(B1_S_3.img, B1_S_3.img_x, B1_S_3.img_y, B1_S_3.img_width, B1_S_3.img_height,B1_S_3.alpha, 50, 255, fps/2, 400/fps, 4, 2, count)
            B1_S_4.alpha = renderPattern(B1_S_4.img, B1_S_4.img_x, B1_S_4.img_y, B1_S_4.img_width, B1_S_4.img_height,B1_S_4.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
            
            B1_FTL.alpha = renderPattern(B1_FTL.img, B1_FTL.img_x, B1_FTL.img_y, B1_FTL.img_width, B1_FTL.img_height, B1_FTL.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
        
        def B1_A_Far_display(): # turn around
            B1_S_1.alpha = renderPattern(B1_S_1.img, B1_S_1.img_x, B1_S_1.img_y, B1_S_1.img_width, B1_S_1.img_height,B1_S_1.alpha, 50, 255, fps/2, 400/fps, 4, 0, count)
            B1_S_2.alpha = renderPattern(B1_S_2.img, B1_S_2.img_x, B1_S_2.img_y, B1_S_2.img_width, B1_S_2.img_height,B1_S_2.alpha, 50, 255, fps/2, 400/fps, 4, 1, count)
            B1_S_3.alpha = renderPattern(B1_S_3.img, B1_S_3.img_x, B1_S_3.img_y, B1_S_3.img_width, B1_S_3.img_height,B1_S_3.alpha, 50, 255, fps/2, 400/fps, 4, 2, count)
            B1_S_4.alpha = renderPattern(B1_S_4.img, B1_S_4.img_x, B1_S_4.img_y, B1_S_4.img_width, B1_S_4.img_height,B1_S_4.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
            
            B1_FTA.alpha = renderPattern(B1_FTA.img, B1_FTA.img_x, B1_FTA.img_y, B1_FTA.img_width, B1_FTA.img_height, B1_FTA.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
            
        def B1_R_Near_display(start): # turn right
            if count < start + 12:
                B1_NTR_001.alpha = renderPattern(B1_NTR_001.img, B1_NTR_001.img_x, B1_NTR_001.img_y, B1_NTR_001.img_width, B1_NTR_001.img_height, B1_NTR_001.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 25:
                B1_NTR_004.alpha = renderPattern(B1_NTR_004.img, B1_NTR_004.img_x, B1_NTR_004.img_y, B1_NTR_004.img_width, B1_NTR_004.img_height, B1_NTR_004.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 50:
                B1_NTR_011.alpha = renderPattern(B1_NTR_011.img, B1_NTR_011.img_x, B1_NTR_011.img_y, B1_NTR_011.img_width, B1_NTR_011.img_height, B1_NTR_011.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 62:
                B1_NTR_015.alpha = renderPattern(B1_NTR_015.img, B1_NTR_015.img_x, B1_NTR_015.img_y, B1_NTR_015.img_width, B1_NTR_015.img_height, B1_NTR_015.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 75:
                B1_NTR_022.alpha = renderPattern(B1_NTR_022.img, B1_NTR_022.img_x, B1_NTR_022.img_y, B1_NTR_022.img_width, B1_NTR_022.img_height, B1_NTR_022.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 87:
                B1_NTR_028.alpha = renderPattern(B1_NTR_028.img, B1_NTR_028.img_x, B1_NTR_028.img_y, B1_NTR_028.img_width, B1_NTR_028.img_height, B1_NTR_028.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 100:
                B1_NTR_034.alpha = renderPattern(B1_NTR_034.img, B1_NTR_034.img_x, B1_NTR_034.img_y, B1_NTR_034.img_width, B1_NTR_034.img_height, B1_NTR_034.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 112:
                B1_NTR_037.alpha = renderPattern(B1_NTR_037.img, B1_NTR_037.img_x, B1_NTR_037.img_y, B1_NTR_037.img_width, B1_NTR_037.img_height, B1_NTR_037.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 125:
                B1_NTR_040.alpha = renderPattern(B1_NTR_040.img, B1_NTR_040.img_x, B1_NTR_040.img_y, B1_NTR_040.img_width, B1_NTR_040.img_height, B1_NTR_040.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 137:
                B1_NTR_043.alpha = renderPattern(B1_NTR_043.img, B1_NTR_043.img_x, B1_NTR_043.img_y, B1_NTR_043.img_width, B1_NTR_043.img_height, B1_NTR_043.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 150:
                B1_NTR_046.alpha = renderPattern(B1_NTR_046.img, B1_NTR_046.img_x, B1_NTR_046.img_y, B1_NTR_046.img_width, B1_NTR_046.img_height, B1_NTR_046.alpha, 255, 255, 1, 255, 1, 0, count)
            
            elif count < start + 155:
                B2_NTR_050.alpha = renderPattern(B2_NTR_050.img, B2_NTR_050.img_x, B2_NTR_050.img_y, B2_NTR_050.img_width, B2_NTR_050.img_height, B2_NTR_050.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 160:
                B2_NTR_052.alpha = renderPattern(B2_NTR_052.img, B2_NTR_052.img_x, B2_NTR_052.img_y, B2_NTR_052.img_width, B2_NTR_052.img_height, B2_NTR_052.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 165:
                B2_NTR_055.alpha = renderPattern(B2_NTR_055.img, B2_NTR_055.img_x, B2_NTR_055.img_y, B2_NTR_055.img_width, B2_NTR_055.img_height, B2_NTR_055.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 170:
                B2_NTR_062.alpha = renderPattern(B2_NTR_062.img, B2_NTR_062.img_x, B2_NTR_062.img_y, B2_NTR_062.img_width, B2_NTR_062.img_height, B2_NTR_062.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 175:
                B2_NTR_079.alpha = renderPattern(B2_NTR_079.img, B2_NTR_079.img_x, B2_NTR_079.img_y, B2_NTR_079.img_width, B2_NTR_079.img_height, B2_NTR_079.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 185:
                B2_NTR_085.alpha = renderPattern(B2_NTR_085.img, B2_NTR_085.img_x, B2_NTR_085.img_y, B2_NTR_085.img_width, B2_NTR_085.img_height, B2_NTR_085.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 190:
                B2_NTR_091.alpha = renderPattern(B2_NTR_091.img, B2_NTR_091.img_x, B2_NTR_091.img_y, B2_NTR_091.img_width, B2_NTR_091.img_height, B2_NTR_091.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 200:
                B2_NTR_097.alpha = renderPattern(B2_NTR_097.img, B2_NTR_097.img_x, B2_NTR_097.img_y, B2_NTR_097.img_width, B2_NTR_097.img_height, B2_NTR_097.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 205:
                B2_NTR_104.alpha = renderPattern(B2_NTR_104.img, B2_NTR_104.img_x, B2_NTR_104.img_y, B2_NTR_104.img_width, B2_NTR_104.img_height, B2_NTR_104.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 210:
                B2_NTR_110.alpha = renderPattern(B2_NTR_110.img, B2_NTR_110.img_x, B2_NTR_110.img_y, B2_NTR_110.img_width, B2_NTR_110.img_height, B2_NTR_110.alpha, 255, 255, 1, 255, 1, 0, count)
            else:
                B2_NTR_116.alpha = renderPattern(B2_NTR_116.img, B2_NTR_116.img_x, B2_NTR_116.img_y, B2_NTR_116.img_width, B2_NTR_116.img_height, B2_NTR_116.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def B1_L_Near_display(start): # turn left
            if count < start + 12:
                B1_NTL_001.alpha = renderPattern(B1_NTL_001.img, B1_NTL_001.img_x, B1_NTL_001.img_y, B1_NTL_001.img_width, B1_NTL_001.img_height, B1_NTL_001.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 25:
                B1_NTL_004.alpha = renderPattern(B1_NTL_004.img, B1_NTL_004.img_x, B1_NTL_004.img_y, B1_NTL_004.img_width, B1_NTL_004.img_height, B1_NTL_004.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 50:
                B1_NTL_011.alpha = renderPattern(B1_NTL_011.img, B1_NTL_011.img_x, B1_NTL_011.img_y, B1_NTL_011.img_width, B1_NTL_011.img_height, B1_NTL_011.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 62:
                B1_NTL_015.alpha = renderPattern(B1_NTL_015.img, B1_NTL_015.img_x, B1_NTL_015.img_y, B1_NTL_015.img_width, B1_NTL_015.img_height, B1_NTL_015.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 75:
                B1_NTL_022.alpha = renderPattern(B1_NTL_022.img, B1_NTL_022.img_x, B1_NTL_022.img_y, B1_NTL_022.img_width, B1_NTL_022.img_height, B1_NTL_022.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 87:
                B1_NTL_028.alpha = renderPattern(B1_NTL_028.img, B1_NTL_028.img_x, B1_NTL_028.img_y, B1_NTL_028.img_width, B1_NTL_028.img_height, B1_NTL_028.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 100:
                B1_NTL_034.alpha = renderPattern(B1_NTL_034.img, B1_NTL_034.img_x, B1_NTL_034.img_y, B1_NTL_034.img_width, B1_NTL_034.img_height, B1_NTL_034.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 112:
                B1_NTL_037.alpha = renderPattern(B1_NTL_037.img, B1_NTL_037.img_x, B1_NTL_037.img_y, B1_NTL_037.img_width, B1_NTL_037.img_height, B1_NTL_037.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 125:
                B1_NTL_040.alpha = renderPattern(B1_NTL_040.img, B1_NTL_040.img_x, B1_NTL_040.img_y, B1_NTL_040.img_width, B1_NTL_040.img_height, B1_NTL_040.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 137:
                B1_NTL_043.alpha = renderPattern(B1_NTL_043.img, B1_NTL_043.img_x, B1_NTL_043.img_y, B1_NTL_043.img_width, B1_NTL_043.img_height, B1_NTL_043.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 150:
                B1_NTL_046.alpha = renderPattern(B1_NTL_046.img, B1_NTL_046.img_x, B1_NTL_046.img_y, B1_NTL_046.img_width, B1_NTL_046.img_height, B1_NTL_046.alpha, 255, 255, 1, 255, 1, 0, count)
            
            elif count < start + 155:
                B2_NTL_050.alpha = renderPattern(B2_NTL_050.img, B2_NTL_050.img_x, B2_NTL_050.img_y, B2_NTL_050.img_width, B2_NTL_050.img_height, B2_NTL_050.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 160:
                B2_NTL_052.alpha = renderPattern(B2_NTL_052.img, B2_NTL_052.img_x, B2_NTL_052.img_y, B2_NTL_052.img_width, B2_NTL_052.img_height, B2_NTL_052.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 165:
                B2_NTL_055.alpha = renderPattern(B2_NTL_055.img, B2_NTL_055.img_x, B2_NTL_055.img_y, B2_NTL_055.img_width, B2_NTL_055.img_height, B2_NTL_055.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 170:
                B2_NTL_062.alpha = renderPattern(B2_NTL_062.img, B2_NTL_062.img_x, B2_NTL_062.img_y, B2_NTL_062.img_width, B2_NTL_062.img_height, B2_NTL_062.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 175:
                B2_NTL_079.alpha = renderPattern(B2_NTL_079.img, B2_NTL_079.img_x, B2_NTL_079.img_y, B2_NTL_079.img_width, B2_NTL_079.img_height, B2_NTL_079.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 185:
                B2_NTL_085.alpha = renderPattern(B2_NTL_085.img, B2_NTL_085.img_x, B2_NTL_085.img_y, B2_NTL_085.img_width, B2_NTL_085.img_height, B2_NTL_085.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 190:
                B2_NTL_091.alpha = renderPattern(B2_NTL_091.img, B2_NTL_091.img_x, B2_NTL_091.img_y, B2_NTL_091.img_width, B2_NTL_091.img_height, B2_NTL_091.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 200:
                B2_NTL_097.alpha = renderPattern(B2_NTL_097.img, B2_NTL_097.img_x, B2_NTL_097.img_y, B2_NTL_097.img_width, B2_NTL_097.img_height, B2_NTL_097.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 205:
                B2_NTL_104.alpha = renderPattern(B2_NTL_104.img, B2_NTL_104.img_x, B2_NTL_104.img_y, B2_NTL_104.img_width, B2_NTL_104.img_height, B2_NTL_104.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 210:
                B2_NTL_110.alpha = renderPattern(B2_NTL_110.img, B2_NTL_110.img_x, B2_NTL_110.img_y, B2_NTL_110.img_width, B2_NTL_110.img_height, B2_NTL_110.alpha, 255, 255, 1, 255, 1, 0, count)
            else:
                B2_NTL_116.alpha = renderPattern(B2_NTL_116.img, B2_NTL_116.img_x, B2_NTL_116.img_y, B2_NTL_116.img_width, B2_NTL_116.img_height, B2_NTL_116.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def B1_A_Near_display(start): # turn around
            if count < start + 12:
                B1_NTA_001.alpha = renderPattern(B1_NTA_001.img, B1_NTA_001.img_x, B1_NTA_001.img_y, B1_NTA_001.img_width, B1_NTA_001.img_height, B1_NTA_001.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 25:
                B1_NTA_004.alpha = renderPattern(B1_NTA_004.img, B1_NTA_004.img_x, B1_NTA_004.img_y, B1_NTA_004.img_width, B1_NTA_004.img_height, B1_NTA_004.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 50:
                B1_NTA_011.alpha = renderPattern(B1_NTA_011.img, B1_NTA_011.img_x, B1_NTA_011.img_y, B1_NTA_011.img_width, B1_NTA_011.img_height, B1_NTA_011.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 62:
                B1_NTA_015.alpha = renderPattern(B1_NTA_015.img, B1_NTA_015.img_x, B1_NTA_015.img_y, B1_NTA_015.img_width, B1_NTA_015.img_height, B1_NTA_015.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 75:
                B1_NTA_022.alpha = renderPattern(B1_NTA_022.img, B1_NTA_022.img_x, B1_NTA_022.img_y, B1_NTA_022.img_width, B1_NTA_022.img_height, B1_NTA_022.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 87:
                B1_NTA_028.alpha = renderPattern(B1_NTA_028.img, B1_NTA_028.img_x, B1_NTA_028.img_y, B1_NTA_028.img_width, B1_NTA_028.img_height, B1_NTA_028.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 100:
                B1_NTA_034.alpha = renderPattern(B1_NTA_034.img, B1_NTA_034.img_x, B1_NTA_034.img_y, B1_NTA_034.img_width, B1_NTA_034.img_height, B1_NTA_034.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 112:
                B1_NTA_037.alpha = renderPattern(B1_NTA_037.img, B1_NTA_037.img_x, B1_NTA_037.img_y, B1_NTA_037.img_width, B1_NTA_037.img_height, B1_NTA_037.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 125:
                B1_NTA_040.alpha = renderPattern(B1_NTA_040.img, B1_NTA_040.img_x, B1_NTA_040.img_y, B1_NTA_040.img_width, B1_NTA_040.img_height, B1_NTA_040.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 137:
                B1_NTA_043.alpha = renderPattern(B1_NTA_043.img, B1_NTA_043.img_x, B1_NTA_043.img_y, B1_NTA_043.img_width, B1_NTA_043.img_height, B1_NTA_043.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 150:
                B1_NTA_046.alpha = renderPattern(B1_NTA_046.img, B1_NTA_046.img_x, B1_NTA_046.img_y, B1_NTA_046.img_width, B1_NTA_046.img_height, B1_NTA_046.alpha, 255, 255, 1, 255, 1, 0, count) 
            
            elif count < start + 155:
                B2_NTA_050.alpha = renderPattern(B2_NTA_050.img, B2_NTA_050.img_x, B2_NTA_050.img_y, B2_NTA_050.img_width, B2_NTA_050.img_height, B2_NTA_050.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 160:
                B2_NTA_052.alpha = renderPattern(B2_NTA_052.img, B2_NTA_052.img_x, B2_NTA_052.img_y, B2_NTA_052.img_width, B2_NTA_052.img_height, B2_NTA_052.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 165:
                B2_NTA_055.alpha = renderPattern(B2_NTA_055.img, B2_NTA_055.img_x, B2_NTA_055.img_y, B2_NTA_055.img_width, B2_NTA_055.img_height, B2_NTA_055.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 170:
                B2_NTA_062.alpha = renderPattern(B2_NTA_062.img, B2_NTA_062.img_x, B2_NTA_062.img_y, B2_NTA_062.img_width, B2_NTA_062.img_height, B2_NTA_062.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 175:
                B2_NTA_079.alpha = renderPattern(B2_NTA_079.img, B2_NTA_079.img_x, B2_NTA_079.img_y, B2_NTA_079.img_width, B2_NTA_079.img_height, B2_NTA_079.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 185:
                B2_NTA_085.alpha = renderPattern(B2_NTA_085.img, B2_NTA_085.img_x, B2_NTA_085.img_y, B2_NTA_085.img_width, B2_NTA_085.img_height, B2_NTA_085.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 190:
                B2_NTA_091.alpha = renderPattern(B2_NTA_091.img, B2_NTA_091.img_x, B2_NTA_091.img_y, B2_NTA_091.img_width, B2_NTA_091.img_height, B2_NTA_091.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 200:
                B2_NTA_097.alpha = renderPattern(B2_NTA_097.img, B2_NTA_097.img_x, B2_NTA_097.img_y, B2_NTA_097.img_width, B2_NTA_097.img_height, B2_NTA_097.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 205:
                B2_NTA_104.alpha = renderPattern(B2_NTA_104.img, B2_NTA_104.img_x, B2_NTA_104.img_y, B2_NTA_104.img_width, B2_NTA_104.img_height, B2_NTA_104.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 210:
                B2_NTA_110.alpha = renderPattern(B2_NTA_110.img, B2_NTA_110.img_x, B2_NTA_110.img_y, B2_NTA_110.img_width, B2_NTA_110.img_height, B2_NTA_110.alpha, 255, 255, 1, 255, 1, 0, count)
            elif count < start + 215:
                B2_NTA_116.alpha = renderPattern(B2_NTA_116.img, B2_NTA_116.img_x, B2_NTA_116.img_y, B2_NTA_116.img_width, B2_NTA_116.img_height, B2_NTA_116.alpha, 255, 255, 1, 255, 1, 0, count)
            else:
                B2_NTA_122.alpha = renderPattern(B2_NTA_122.img, B2_NTA_122.img_x, B2_NTA_122.img_y, B2_NTA_122.img_width, B2_NTA_122.img_height, B2_NTA_122.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def B1_KR_display():
            B1_KR_1.alpha = renderPattern(B1_KR_1.img, B1_KR_1.img_x, B1_KR_1.img_y, B1_KR_1.img_width, B1_KR_1.img_height, B1_KR_1.alpha, 50, 255, fps/2, 400/fps, 4, 0, count) 
            B1_KR_2.alpha = renderPattern(B1_KR_2.img, B1_KR_2.img_x, B1_KR_2.img_y, B1_KR_2.img_width, B1_KR_2.img_height, B1_KR_2.alpha, 50, 255, fps/2, 400/fps, 4, 1, count)
            B1_KR_3.alpha = renderPattern(B1_KR_3.img, B1_KR_3.img_x, B1_KR_3.img_y, B1_KR_3.img_width, B1_KR_3.img_height, B1_KR_3.alpha, 50, 255, fps/2, 400/fps, 4, 2, count)
            B1_KR_4.alpha = renderPattern(B1_KR_4.img, B1_KR_4.img_x, B1_KR_4.img_y, B1_KR_4.img_width, B1_KR_4.img_height, B1_KR_4.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
        
        def B1_KL_display():
            B1_KL_1.alpha = renderPattern(B1_KL_1.img, B1_KL_1.img_x, B1_KL_1.img_y, B1_KL_1.img_width, B1_KL_1.img_height, B1_KL_1.alpha, 50, 255, fps/2, 400/fps, 4, 0, count) 
            B1_KL_2.alpha = renderPattern(B1_KL_2.img, B1_KL_2.img_x, B1_KL_2.img_y, B1_KL_2.img_width, B1_KL_2.img_height, B1_KL_2.alpha, 50, 255, fps/2, 400/fps, 4, 1, count)
            B1_KL_3.alpha = renderPattern(B1_KL_3.img, B1_KL_3.img_x, B1_KL_3.img_y, B1_KL_3.img_width, B1_KL_3.img_height, B1_KL_3.alpha, 50, 255, fps/2, 400/fps, 4, 2, count)
            B1_KL_4.alpha = renderPattern(B1_KL_4.img, B1_KL_4.img_x, B1_KL_4.img_y, B1_KL_4.img_width, B1_KL_4.img_height, B1_KL_4.alpha, 50, 255, fps/2, 400/fps, 4, 3, count)
        
        # def B2_R_Now_display(start): # turn right
        #     if count < start + 5:
        #         B2_NTR_050.alpha = renderPattern(B2_NTR_050.img, B2_NTR_050.img_x, B2_NTR_050.img_y, B2_NTR_050.img_width, B2_NTR_050.img_height, B2_NTR_050.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 10:
        #         B2_NTR_052.alpha = renderPattern(B2_NTR_052.img, B2_NTR_052.img_x, B2_NTR_052.img_y, B2_NTR_052.img_width, B2_NTR_052.img_height, B2_NTR_052.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 15:
        #         B2_NTR_055.alpha = renderPattern(B2_NTR_055.img, B2_NTR_055.img_x, B2_NTR_055.img_y, B2_NTR_055.img_width, B2_NTR_055.img_height, B2_NTR_055.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 20:
        #         B2_NTR_062.alpha = renderPattern(B2_NTR_062.img, B2_NTR_062.img_x, B2_NTR_062.img_y, B2_NTR_062.img_width, B2_NTR_062.img_height, B2_NTR_062.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 25:
        #         B2_NTR_079.alpha = renderPattern(B2_NTR_079.img, B2_NTR_079.img_x, B2_NTR_079.img_y, B2_NTR_079.img_width, B2_NTR_079.img_height, B2_NTR_079.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 35:
        #         B2_NTR_085.alpha = renderPattern(B2_NTR_085.img, B2_NTR_085.img_x, B2_NTR_085.img_y, B2_NTR_085.img_width, B2_NTR_085.img_height, B2_NTR_085.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 40:
        #         B2_NTR_091.alpha = renderPattern(B2_NTR_091.img, B2_NTR_091.img_x, B2_NTR_091.img_y, B2_NTR_091.img_width, B2_NTR_091.img_height, B2_NTR_091.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 50:
        #         B2_NTR_097.alpha = renderPattern(B2_NTR_097.img, B2_NTR_097.img_x, B2_NTR_097.img_y, B2_NTR_097.img_width, B2_NTR_097.img_height, B2_NTR_097.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 55:
        #         B2_NTR_104.alpha = renderPattern(B2_NTR_104.img, B2_NTR_104.img_x, B2_NTR_104.img_y, B2_NTR_104.img_width, B2_NTR_104.img_height, B2_NTR_104.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 60:
        #         B2_NTR_110.alpha = renderPattern(B2_NTR_110.img, B2_NTR_110.img_x, B2_NTR_110.img_y, B2_NTR_110.img_width, B2_NTR_110.img_height, B2_NTR_110.alpha, 255, 255, 1, 255, 1, 0, count)
        #     else:
        #         B2_NTR_116.alpha = renderPattern(B2_NTR_116.img, B2_NTR_116.img_x, B2_NTR_116.img_y, B2_NTR_116.img_width, B2_NTR_116.img_height, B2_NTR_116.alpha, 255, 255, 1, 255, 1, 0, count)
            
        # def B2_L_Now_display(start): # turn left
        #     if count < start + 5:
        #         B2_NTL_050.alpha = renderPattern(B2_NTL_050.img, B2_NTL_050.img_x, B2_NTL_050.img_y, B2_NTL_050.img_width, B2_NTL_050.img_height, B2_NTL_050.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 10:
        #         B2_NTL_052.alpha = renderPattern(B2_NTL_052.img, B2_NTL_052.img_x, B2_NTL_052.img_y, B2_NTL_052.img_width, B2_NTL_052.img_height, B2_NTL_052.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 15:
        #         B2_NTL_055.alpha = renderPattern(B2_NTL_055.img, B2_NTL_055.img_x, B2_NTL_055.img_y, B2_NTL_055.img_width, B2_NTL_055.img_height, B2_NTL_055.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 20:
        #         B2_NTL_062.alpha = renderPattern(B2_NTL_062.img, B2_NTL_062.img_x, B2_NTL_062.img_y, B2_NTL_062.img_width, B2_NTL_062.img_height, B2_NTL_062.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 25:
        #         B2_NTL_079.alpha = renderPattern(B2_NTL_079.img, B2_NTL_079.img_x, B2_NTL_079.img_y, B2_NTL_079.img_width, B2_NTL_079.img_height, B2_NTL_079.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 35:
        #         B2_NTL_085.alpha = renderPattern(B2_NTL_085.img, B2_NTL_085.img_x, B2_NTL_085.img_y, B2_NTL_085.img_width, B2_NTL_085.img_height, B2_NTL_085.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 40:
        #         B2_NTL_091.alpha = renderPattern(B2_NTL_091.img, B2_NTL_091.img_x, B2_NTL_091.img_y, B2_NTL_091.img_width, B2_NTL_091.img_height, B2_NTL_091.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 50:
        #         B2_NTL_097.alpha = renderPattern(B2_NTL_097.img, B2_NTL_097.img_x, B2_NTL_097.img_y, B2_NTL_097.img_width, B2_NTL_097.img_height, B2_NTL_097.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 55:
        #         B2_NTL_104.alpha = renderPattern(B2_NTL_104.img, B2_NTL_104.img_x, B2_NTL_104.img_y, B2_NTL_104.img_width, B2_NTL_104.img_height, B2_NTL_104.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 60:
        #         B2_NTL_110.alpha = renderPattern(B2_NTL_110.img, B2_NTL_110.img_x, B2_NTL_110.img_y, B2_NTL_110.img_width, B2_NTL_110.img_height, B2_NTL_110.alpha, 255, 255, 1, 255, 1, 0, count)
        #     else:
        #         B2_NTL_116.alpha = renderPattern(B2_NTL_116.img, B2_NTL_116.img_x, B2_NTL_116.img_y, B2_NTL_116.img_width, B2_NTL_116.img_height, B2_NTL_116.alpha, 255, 255, 1, 255, 1, 0, count)
            
        # def B2_A_Now_display(start): # turn around
        #     if count < start + 5:
        #         B2_NTA_050.alpha = renderPattern(B2_NTA_050.img, B2_NTA_050.img_x, B2_NTA_050.img_y, B2_NTA_050.img_width, B2_NTA_050.img_height, B2_NTA_050.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 10:
        #         B2_NTA_052.alpha = renderPattern(B2_NTA_052.img, B2_NTA_052.img_x, B2_NTA_052.img_y, B2_NTA_052.img_width, B2_NTA_052.img_height, B2_NTA_052.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 15:
        #         B2_NTA_055.alpha = renderPattern(B2_NTA_055.img, B2_NTA_055.img_x, B2_NTA_055.img_y, B2_NTA_055.img_width, B2_NTA_055.img_height, B2_NTA_055.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 20:
        #         B2_NTA_062.alpha = renderPattern(B2_NTA_062.img, B2_NTA_062.img_x, B2_NTA_062.img_y, B2_NTA_062.img_width, B2_NTA_062.img_height, B2_NTA_062.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 25:
        #         B2_NTA_079.alpha = renderPattern(B2_NTA_079.img, B2_NTA_079.img_x, B2_NTA_079.img_y, B2_NTA_079.img_width, B2_NTA_079.img_height, B2_NTA_079.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 35:
        #         B2_NTA_085.alpha = renderPattern(B2_NTA_085.img, B2_NTA_085.img_x, B2_NTA_085.img_y, B2_NTA_085.img_width, B2_NTA_085.img_height, B2_NTA_085.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 40:
        #         B2_NTA_091.alpha = renderPattern(B2_NTA_091.img, B2_NTA_091.img_x, B2_NTA_091.img_y, B2_NTA_091.img_width, B2_NTA_091.img_height, B2_NTA_091.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 50:
        #         B2_NTA_097.alpha = renderPattern(B2_NTA_097.img, B2_NTA_097.img_x, B2_NTA_097.img_y, B2_NTA_097.img_width, B2_NTA_097.img_height, B2_NTA_097.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 55:
        #         B2_NTA_104.alpha = renderPattern(B2_NTA_104.img, B2_NTA_104.img_x, B2_NTA_104.img_y, B2_NTA_104.img_width, B2_NTA_104.img_height, B2_NTA_104.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 60:
        #         B2_NTA_110.alpha = renderPattern(B2_NTA_110.img, B2_NTA_110.img_x, B2_NTA_110.img_y, B2_NTA_110.img_width, B2_NTA_110.img_height, B2_NTA_110.alpha, 255, 255, 1, 255, 1, 0, count)
        #     elif count < start + 65:
        #         B2_NTA_116.alpha = renderPattern(B2_NTA_116.img, B2_NTA_116.img_x, B2_NTA_116.img_y, B2_NTA_116.img_width, B2_NTA_116.img_height, B2_NTA_116.alpha, 255, 255, 1, 255, 1, 0, count)
        #     else:
        #         B2_NTA_122.alpha = renderPattern(B2_NTA_122.img, B2_NTA_122.img_x, B2_NTA_122.img_y, B2_NTA_122.img_width, B2_NTA_122.img_height, B2_NTA_122.alpha, 255, 255, 1, 255, 1, 0, count)
            
        def B3_F_L1_display():
            B3_FCW_B.alpha = renderPattern(B3_FCW_B.img, B3_FCW_B.img_x, B3_FCW_B.img_y, B3_FCW_B.img_width, B3_FCW_B.img_height, B3_FCW_B.alpha, 255, 255, 1, 255, 1, 0, count)
            B3_FCWB_2.alpha = renderPattern(B3_FCWB_2.img, B3_FCWB_2.img_x, B3_FCWB_2.img_y, B3_FCWB_2.img_width, B3_FCWB_2.img_height, B3_FCWB_2.alpha, 50, 255, fps/4, 800/fps, 2, 0, count) # 0.5 Hz
        
        def B3_F_L2_display():
            B3_FCWA.alpha = renderPattern(B3_FCWA.img, B3_FCWA.img_x, B3_FCWA.img_y, B3_FCWA.img_width, B3_FCWA.img_height, B3_FCWA.alpha, 255, 255, 1, 255, 1, 0, count)
        
        def B3_P_L1_display():
            B3_FCW_B.alpha = renderPattern(B3_FCW_B.img, B3_FCW_B.img_x, B3_FCW_B.img_y, B3_FCW_B.img_width, B3_FCW_B.img_height, B3_FCW_B.alpha, 255, 255, 1, 255, 1, 0, count)
            B3_PDWB_2.alpha = renderPattern(B3_PDWB_2.img, B3_PDWB_2.img_x, B3_PDWB_2.img_y, B3_PDWB_2.img_width, B3_PDWB_2.img_height, B3_PDWB_2.alpha, 50, 255, fps/4, 800/fps, 2, 0, count) # 0.5 Hz
        
        def B3_P_L2_display():
            B3_PDWA.alpha = renderPattern(B3_PDWA.img, B3_PDWA.img_x, B3_PDWA.img_y, B3_PDWA.img_width, B3_PDWA.img_height, B3_PDWA.alpha, 255, 255, 1, 255, 1, 0, count)
        
        def B3_P_display(start):
            B3_FCW_B.alpha = renderPattern(B3_FCW_B.img, B3_FCW_B.img_x, B3_FCW_B.img_y, B3_FCW_B.img_width, B3_FCW_B.img_height, B3_FCW_B.alpha, 255, 255, 1, 255, 1, 0, count)
            if count < start + 20:
                B3_PDW_1.alpha = renderPattern(B3_PDW_1.img, B3_PDW_1.img_x, B3_PDW_1.img_y, B3_PDW_1.img_width, B3_PDW_1.img_height, B3_PDW_1.alpha, 50, 255, fps/4, 800/fps, 2, 0, count) # 0.5 Hz
            elif count < start + 40:
                B3_PDW_2.alpha = renderPattern(B3_PDW_2.img, B3_PDW_2.img_x, B3_PDW_2.img_y, B3_PDW_2.img_width, B3_PDW_2.img_height, B3_PDW_2.alpha, 50, 255, fps/4, 800/fps, 2, 0, count)
            elif count < start + 60:
                B3_PDW_3.alpha = renderPattern(B3_PDW_3.img, B3_PDW_3.img_x, B3_PDW_3.img_y, B3_PDW_3.img_width, B3_PDW_3.img_height, B3_PDW_3.alpha, 50, 255, fps/4, 800/fps, 2, 0, count)
            elif count < start + 80:
                B3_PDW_4.alpha = renderPattern(B3_PDW_4.img, B3_PDW_4.img_x, B3_PDW_4.img_y, B3_PDW_4.img_width, B3_PDW_4.img_height, B3_PDW_4.alpha, 50, 255, fps/4, 800/fps, 2, 0, count)
        
        def B4_R_display():
            B4_R_B.alpha = renderPattern(B4_R_B.img, B4_R_B.img_x, B4_R_B.img_y, B4_R_B.img_width, B4_R_B.img_height, B4_R_B.alpha, 255, 255, 1, 255, 1, 0, count)
            B4_R_R.alpha = renderPattern(B4_R_R.img, B4_R_R.img_x, B4_R_R.img_y, B4_R_R.img_width, B4_R_R.img_height, B4_R_R.alpha, 255, 255, 1, 255, 1, 0, count)
            for i in range(0, 8):
                if (count//2)%8==i:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B4_BL.img, B4_BL.img_x+i*20, B4_BL.img_y, B4_BL.img_width, B4_BL.img_height)
        
        def B4_L_display():
            B4_L_B.alpha = renderPattern(B4_L_B.img, B4_L_B.img_x, B4_L_B.img_y, B4_L_B.img_width, B4_L_B.img_height, B4_L_B.alpha, 255, 255, 1, 255, 1, 0, count)
            B4_L_R.alpha = renderPattern(B4_L_R.img, B4_L_R.img_x, B4_L_R.img_y, B4_L_R.img_width, B4_L_R.img_height, B4_L_R.alpha, 255, 255, 1, 255, 1, 0, count)
            for i in range(0, 8):
                if (count//2)%8==i:
                    jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B4_BL.img, B4_BL.img_x-280-i*20, B4_BL.img_y, B4_BL.img_width, B4_BL.img_height)


        jetson.utils.Overlay_all(bg_img, bg_img_width, bg_img_height, 0,0,0,255)

        p = 3
        a = 0

        A1_display()

        if can_this_frame['VehicleDirection'] == 'rear':
            A2_B_display()
        elif can_this_frame['VehicleDirection'] == 'left':
            A2_L_display()
        elif can_this_frame['VehicleDirection'] == 'right':
            A2_R_display()
        
        if can_this_frame['SystemError']:
            A3_SF_display()
            p = 1
        elif can_this_frame['BatteryError']:
            A3_BL_display()
            p = 1
        elif can_this_frame['MotorOverHeat'] or can_this_frame['ControllerOverHeat']:
            A3_MH_display()
            p = 1
        elif can_this_frame['MotorOverSpeed']:
            A3_MS_display()
            p = 1
        elif can_this_frame['BrakeError']:
            A3_BF_display()
            p = 1

        if can_this_frame['ObjectDirection'] == 'left':
            B5_display()
        elif can_this_frame['ObjectDirection'] == 'right':
            B6_display()

        if can_this_frame['FrontCollisionLevel'] == 'level1' and can_this_frame['FrontCollisionType'] == 'vehicle warning':
            B3_F_L1_display()
            p = 1
            a = 1
        elif can_this_frame['FrontCollisionLevel'] == 'level1' and can_this_frame['FrontCollisionType'] == 'none vehicle/pedestrian warning':
            B3_P_L1_display()
            p = 1
            a = 1
        elif can_this_frame['FrontCollisionLevel'] == 'level2' and can_this_frame['FrontCollisionType'] == 'vehicle warning':
            B3_F_L2_display()
            p = 1
            a = 1
        elif can_this_frame['FrontCollisionLevel'] == 'level2' and can_this_frame['FrontCollisionType'] == 'none vehicle/pedestrian warning':
            B3_P_L2_display()
            p = 1
            a = 1
        
        if can_this_frame['LDW_Left'] == 'warning' and (p >= 2 or a != 1):
            B4_L_display()
            p = 2
        elif can_this_frame['LDW_Right'] == 'warning' and (p >= 2 or a != 1):
            B4_R_display()
            p = 2


        a3_number = int(can_this_frame['DistanceValue']*0.1)
        unit = can_this_frame['DistanceUnit']
        if unit == '0.1m' or unit =='0.1km':
            unit = unit[3:] 
            if a3_number >= 1000 and unit == 'm':
                a3_number = int(a3_number * 0.001)
                unit = 'km'

        a4_number = int(can_this_frame['NavigationDestinationValue']*0.1)
        dUnit = can_this_frame['NavigationDestinationUnit']
        if dUnit == '0.1m' or dUnit =='0.1km':
            dUnit = dUnit[3:] 
            if a4_number >= 1000 and dUnit == 'm':
                a4_number = int(a4_number * 0.001)
                dUnit = 'km'
        
        if dUnit == 'm' or dUnit == 'km':
            A4_D_display()
        elif can_this_frame['NavigationDirection'] == 'go straight':
            A4_S_display()
        elif can_this_frame['NavigationDirection'] == 'turn left' or can_this_frame['NavigationDirection'] == 'left front' or can_this_frame['NavigationDirection'] == 'left rear':
            A4_TL_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = count
                B1_L_Near_display(start)
            elif p == 3 and unit == 'm':
                B1_L_Near_display(start)
            elif p == 3:
                B1_L_Far_display()
        elif can_this_frame['NavigationDirection'] == 'turn right' or can_this_frame['NavigationDirection'] == 'right front' or can_this_frame['NavigationDirection'] == 'right rear':
            A4_TR_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = count
                B1_R_Near_display(start)
            elif p == 3 and unit == 'm':
                B1_R_Near_display(start)
            elif p == 3:
                B1_R_Far_display()
        elif can_this_frame['NavigationDirection'] == 'U-turn':
            A4_TA_display()
            if p == 3 and unit == 'm' and a3_number < 50 and start == 0:
                start = count
                B1_A_Near_display(start)
            elif p == 3 and unit == 'm':
                B1_A_Near_display(start)
            elif p == 3:
                B1_A_Far_display()
        # elif dUnit == 'm' or dUnit == 'km':
        #     A4_D_display()

        if unit == 'm' and a3_number == 0:
            start = 0
        

        #FCW_warning_level,FCW_main_obj_class,PDW_right_near,PDW_right_far,PDW_left_near,PDW_left_far=fcw_warning.update(detection_this_frame,can_this_frame["Speed"],can_this_frame["BrakeSignal"],can_this_frame["LeftSignal"],can_this_frame["RightSignal"])
        #FCW_warning_level:0=normal,1=blue,2=red ; FCW_main_obj_class=['Sedan', 'Truck', 'Bus', 'Motorcycle', 'Person'] ; PDW_X_X:0=normal,1=warning

        # print(can_this_frame)
        # print(can_this_frame['DistanceValue'], can_this_frame['DistanceUnit'])
        # print('A3: ', can_this_frame['SystemError'], can_this_frame['BatteryError'], can_this_frame['MotorOverHeat'], can_this_frame['MotorOverSpeed'], can_this_frame['BrakeError'])
        print(can_this_frame['NavigationDirection'])
        print(can_this_frame['DistanceValue'], can_this_frame['DistanceUnit'])
        print(can_this_frame['NavigationDestinationValue'], can_this_frame['NavigationDestinationUnit'])

        a1_number = can_this_frame['SpeedLimit']
        if a1_number >= 100:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a1_number), test_txt_x,test_txt_y,80,0,255,255,255)
        elif a1_number >= 10:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a1_number), test_txt_x+18,test_txt_y,80,0,255,255,255)
        elif a1_number > 0:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a1_number), test_txt_x+36,test_txt_y,80,0,255,255,255)

        a2_number = int(can_this_frame['Speed'])
        if a2_number >= 100:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+230,test_txt_y-37,80,0,255,255,255)
        elif a2_number >= 10:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+248,test_txt_y-37,80,0,255,255,255)
        elif a2_number > 0:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+266,test_txt_y-37,80,0,255,255,255)

       
        if dUnit == 'm' or dUnit == 'km':
            if a4_number >= 100:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+740,test_txt_y+40,80,0,255,255,255)
            elif a4_number >= 10:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+758,test_txt_y+40,80,0,255,255,255)
            elif a4_number > 0:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+776,test_txt_y+40,80,0,255,255,255)
        elif unit == 'm' or unit =='km':
            # unit = unit[3:] 
            # if a3_number >= 1000 and unit == 'm':
            #     a3_number = int(a3_number * 0.001)
            #     unit = 'km'
            if a3_number >= 100:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number)+unit, test_txt_x+740,test_txt_y+40,80,0,255,255,255)
            elif a3_number >= 10:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number)+unit, test_txt_x+758,test_txt_y+40,80,0,255,255,255)
            elif a3_number > 0:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number)+unit, test_txt_x+776,test_txt_y+40,80,0,255,255,255)
        # elif dUnit == 'm' or dUnit == 'km':
        #     if a4_number >= 100:
        #         jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+740,test_txt_y+40,80,0,255,255,255)
        #     elif a4_number >= 10:
        #         jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+758,test_txt_y+40,80,0,255,255,255)
        #     elif a4_number > 0:
        #         jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a4_number)+dUnit, test_txt_x+776,test_txt_y+40,80,0,255,255,255)    


        display.RenderOnce(bg_img, bg_img_width, bg_img_height,img_start_x,img_start_y)

        count=count+1

        time.sleep(f) # fps
        # time.sleep(0.033) # 30fps
        # time.sleep(0.2) # 5fps


