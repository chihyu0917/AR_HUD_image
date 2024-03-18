import time
import jetson.utils

import argparse
import sys

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
    display = jetson.utils.glDisplay(win_x,win_y,width,height,if_no_title)
    img_start_x=0
    img_start_y=0
    
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
            'pat1': './png/W_A1_SL.png', # A1
            'pat2': './png/W_A2_R_B.png', 'pat3': './png/W_A2_R_L.png', 'pat4': './png/W_A2_R_R.png', # A2
            'pat5': './png/W_A3_SF.png', 'pat6': './png/W_A3_BL.png', 'pat7': './png/W_A3_MH.png', 'pat8': './png/W_A3_MS.png', 'pat9': './png/W_A3_BF.png', # A3
            'pat10': './png/N_A4_S.png', 'pat11': './png/N_A4_TR.png', 'pat12': './png/N_A4_TL.png', 'pat13': './png/N_A4_KR.png', 
            'pat14': './png/N_A4_KL.png', 'pat15': './png/N_A4_TA.png', 'pat16': './png/N_A4_D.png', # A4
            'pat17': './png/W_A5_A.png', # A5
            'pat18': './png/A_B5_LBIN.png', 'pat19': './png/A_B6_RBIN.png', # B5, B6
            'pat20': './png/N_B1_S.png', 'pat21': './png/N_B1_S_1.png', 'pat22': './png/N_B1_S_2.png', 'pat23': './png/N_B1_S_3.png', 'pat24': './png/N_B1_S_4.png', # B1
            'pat25': './png/N_B1_FTR.png', 'pat26': './png/N_B1_NTR_2.png', 'pat27': './png/N_B1_NTR_4.png', 'pat28': './png/N_B1_NTR_3.png', 'pat29': './png/N_B1_NTR_1.png',
            'pat30': './png/N_B2_TRI_1.png', 'pat51': './png/N_B2_TRI_2_d.png', 'pat31': './png/N_B2_TRI_2_a.png', 'pat52': './png/N_B2_TRI_2_e.png', # B2
            'pat32': './png/N_B2_TRI_2_b.png', 'pat53': './png/N_B2_TRI_2_f.png', 'pat33': './png/N_B2_TRI_2_c.png', 'pat54': './png/N_B2_TRI_2_g.png', 'pat34': './png/N_B2_TRI_2.png', 
            'pat35': './png/N_B2_TRI_3_a.png', 'pat36': './png/N_B2_TRI_3_b.png', 'pat37': './png/N_B2_TRI_3_c.png', 'pat38': './png/N_B2_TRI_3_d.png',
            'pat39': './png/A_B3_FCW_B.png', 'pat40': './png/A_B3_FCW_BA.png', 'pat41': './png/A_B3_FCW_R.png', 'pat42': './png/A_B3_PDW_1.png', # B3
            'pat43': './png/A_B3_PDW_2.png', 'pat44': './png/A_B3_PDW_3.png', 'pat45': './png/A_B3_PDW_4.png',
            'pat46': './png/A_B4_RLDW_B.png', 'pat47': './png/A_B4_RLDW_R.png', 'pat48': './png/A_B4_RLDW_BL.png', 'pat49': './png/A_B4_LLDW_B.png', 'pat50': './png/A_B4_LLDW_R.png' # B4
        }
        
        images = {}
        for key, path in images_path.items():
            images[key] = jetson.utils.loadImageRGBA(path)
            
        return images
    
    images = loadImages()
    for key in images.keys():
        img, img_width, img_height = images[key]


    pat1 = attributes(images['pat1'][0], images['pat1'][1], images['pat1'][2], 0, 80, 387) # A1
    
    pat2 = attributes(images['pat2'][0], images['pat2'][1], images['pat2'][2], 0, 265, 390) # A2
    pat3 = attributes(images['pat3'][0], images['pat3'][1], images['pat3'][2], 0, 265, 390)
    pat4 = attributes(images['pat4'][0], images['pat4'][1], images['pat4'][2], 0, 265, 390)

    pat5 = attributes(images['pat5'][0], images['pat5'][1], images['pat5'][2], 0, 560, 417) # A3
    pat6 = attributes(images['pat6'][0], images['pat6'][1], images['pat6'][2], 0, 560, 403)
    pat7 = attributes(images['pat7'][0], images['pat7'][1], images['pat7'][2], 0, 560, 401)
    pat8 = attributes(images['pat8'][0], images['pat8'][1], images['pat8'][2], 0, 560, 422)
    pat9 = attributes(images['pat9'][0], images['pat9'][1], images['pat9'][2], 0, 560, 398)

    pat10 = attributes(images['pat10'][0], images['pat10'][1], images['pat10'][2], 0, 782, 404) # A4
    pat11 = attributes(images['pat11'][0], images['pat11'][1], images['pat11'][2], 0, 770, 404)
    pat12 = attributes(images['pat12'][0], images['pat12'][1], images['pat12'][2], 0, 770, 404)
    pat13 = attributes(images['pat13'][0], images['pat13'][1], images['pat13'][2], 0, 770, 404)
    pat14 = attributes(images['pat14'][0], images['pat14'][1], images['pat14'][2], 0, 770, 404)
    pat15 = attributes(images['pat15'][0], images['pat15'][1], images['pat15'][2], 0, 776, 404)
    pat16 = attributes(images['pat16'][0], images['pat16'][1], images['pat16'][2], 0, 785, 419)
    
    pat17 = attributes(images['pat17'][0], images['pat17'][1], images['pat17'][2], 0, 1045, 407) # A5
    
    pat18 = attributes(images['pat18'][0], images['pat18'][1], images['pat18'][2], 0, 70, 155) # B5
    pat19 = attributes(images['pat19'][0], images['pat19'][1], images['pat19'][2], 0, 1128, 155) # B6
    
    pat20 = attributes(images['pat20'][0], images['pat20'][1], images['pat20'][2], 0, 585, 260) # B1
    pat21 = attributes(images['pat21'][0], images['pat21'][1], images['pat21'][2], 0, 585, 260)
    pat22 = attributes(images['pat22'][0], images['pat22'][1], images['pat22'][2], 0, 585, 260)
    pat23 = attributes(images['pat23'][0], images['pat23'][1], images['pat23'][2], 0, 585, 260)
    pat24 = attributes(images['pat24'][0], images['pat24'][1], images['pat24'][2], 0, 585, 260)
    
    pat25 = attributes(images['pat25'][0], images['pat25'][1], images['pat25'][2], 0, 585, 175)
    
    pat26 = attributes(images['pat26'][0], images['pat26'][1], images['pat26'][2], 0, 550, 415)
    pat27 = attributes(images['pat27'][0], images['pat27'][1], images['pat27'][2], 0, 580, 315)
    pat28 = attributes(images['pat28'][0], images['pat28'][1], images['pat28'][2], 0, 610, 235)
    pat29 = attributes(images['pat29'][0], images['pat29'][1], images['pat29'][2], 0, 640, 175)
    
    pat30 = attributes(images['pat30'][0], images['pat30'][1], images['pat30'][2], 0, 560, 232) # B2
    pat51 = attributes(images['pat51'][0], images['pat51'][1], images['pat51'][2], 0, 540, 226)
    pat31 = attributes(images['pat31'][0], images['pat31'][1], images['pat31'][2], 0, 520, 220)
    pat52 = attributes(images['pat52'][0], images['pat52'][1], images['pat52'][2], 0, 500, 214)
    pat32 = attributes(images['pat32'][0], images['pat32'][1], images['pat32'][2], 0, 480, 207)
    pat53 = attributes(images['pat53'][0], images['pat53'][1], images['pat53'][2], 0, 460, 201)
    pat33 = attributes(images['pat33'][0], images['pat33'][1], images['pat33'][2], 0, 440, 195)
    pat54 = attributes(images['pat54'][0], images['pat54'][1], images['pat54'][2], 0, 420, 189)
    
    pat34 = attributes(images['pat34'][0], images['pat34'][1], images['pat34'][2], 0, 400, 182)
    pat35 = attributes(images['pat35'][0], images['pat35'][1], images['pat35'][2], 0, 400, 182)
    pat36 = attributes(images['pat36'][0], images['pat36'][1], images['pat36'][2], 0, 400, 182)
    pat37 = attributes(images['pat37'][0], images['pat37'][1], images['pat37'][2], 0, 400, 182)
    pat38 = attributes(images['pat38'][0], images['pat38'][1], images['pat38'][2], 0, 400, 182)
    
    pat39 = attributes(images['pat39'][0], images['pat39'][1], images['pat39'][2], 0, 310, 175) # B3
    pat40 = attributes(images['pat40'][0], images['pat40'][1], images['pat40'][2], 0, 310, 175)
    pat41 = attributes(images['pat41'][0], images['pat41'][1], images['pat41'][2], 0, 310, 175)
    pat42 = attributes(images['pat42'][0], images['pat42'][1], images['pat42'][2], 0, 310, 175)
    pat43 = attributes(images['pat43'][0], images['pat43'][1], images['pat43'][2], 0, 310, 175)
    pat44 = attributes(images['pat44'][0], images['pat44'][1], images['pat44'][2], 0, 310, 175)
    pat45 = attributes(images['pat45'][0], images['pat45'][1], images['pat45'][2], 0, 310, 175)
    
    pat46 = attributes(images['pat46'][0], images['pat46'][1], images['pat46'][2], 0, 311, 161) # B4
    pat47 = attributes(images['pat47'][0], images['pat47'][1], images['pat47'][2], 0, 311, 161)
    pat48 = attributes(images['pat48'][0], images['pat48'][1], images['pat48'][2], 0, 770, 161)
    pat49 = attributes(images['pat49'][0], images['pat49'][1], images['pat49'][2], 0, 311, 161)
    pat50 = attributes(images['pat50'][0], images['pat50'][1], images['pat50'][2], 0, 311, 161)
    


    bg_img,bg_img_width,bg_img_height=jetson.utils.loadImageRGBA("background.png")
    # # pat1_img,pat1_img_width,pat1_img_height=jetson.utils.loadImageRGBA("logo.png")
    # pat1_img,pat1_img_width,pat1_img_height=jetson.utils.loadImageRGBA("./png/W_A1_SL.png") # A1

    # pat2_img,pat2_img_width,pat2_img_height=jetson.utils.loadImageRGBA("./png/W_A2_R_B.png") #A2
    # pat3_img,pat3_img_width,pat3_img_height=jetson.utils.loadImageRGBA("./png/W_A2_R_L.png")
    # pat4_img,pat4_img_width,pat4_img_height=jetson.utils.loadImageRGBA("./png/W_A2_R_R.png")

    # pat5_img,pat5_img_width,pat5_img_height=jetson.utils.loadImageRGBA("./png/W_A3_SF.png") # A3
    # pat6_img,pat6_img_width,pat6_img_height=jetson.utils.loadImageRGBA("./png/W_A3_BL.png")
    # pat7_img,pat7_img_width,pat7_img_height=jetson.utils.loadImageRGBA("./png/W_A3_MH.png")
    # pat8_img,pat8_img_width,pat8_img_height=jetson.utils.loadImageRGBA("./png/W_A3_MS.png")
    # pat9_img,pat9_img_width,pat9_img_height=jetson.utils.loadImageRGBA("./png/W_A3_BF.png")

    # pat10_img,pat10_img_width,pat10_img_height=jetson.utils.loadImageRGBA('./png/N_A4_S.png') # A4
    # pat11_img,pat11_img_width,pat11_img_height=jetson.utils.loadImageRGBA('./png/N_A4_TR.png')
    # pat12_img,pat12_img_width,pat12_img_height=jetson.utils.loadImageRGBA('./png/N_A4_TL.png')
    # pat13_img,pat13_img_width,pat13_img_height=jetson.utils.loadImageRGBA('./png/N_A4_KR.png')
    # pat14_img,pat14_img_width,pat14_img_height=jetson.utils.loadImageRGBA('./png/N_A4_KL.png')
    # pat15_img,pat15_img_width,pat15_img_height=jetson.utils.loadImageRGBA('./png/N_A4_TA.png')
    # pat16_img,pat16_img_width,pat16_img_height=jetson.utils.loadImageRGBA('./png/N_A4_D.png')

    # pat17_img,pat17_img_width,pat17_img_height=jetson.utils.loadImageRGBA("./png/W_A5_A.png") # A5

    # pat18_img,pat18_img_width,pat18_img_height=jetson.utils.loadImageRGBA("./png/A_B5_LBIN.png") # B5

    # pat19_img,pat19_img_width,pat19_img_height=jetson.utils.loadImageRGBA("./png/A_B6_RBIN.png") # B6

    # pat20_img,pat20_img_width,pat20_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S.png") # B1
    # pat21_img,pat21_img_width,pat21_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S_1.png")
    # pat22_img,pat22_img_width,pat22_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S_2.png")
    # pat23_img,pat23_img_width,pat23_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S_3.png")
    # pat24_img,pat24_img_width,pat24_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S_4.png")
    # pat25_img,pat25_img_width,pat25_img_height=jetson.utils.loadImageRGBA("./png/N_B1_FTR.png")
    # pat26_img,pat26_img_width,pat26_img_height=jetson.utils.loadImageRGBA("./png/N_B1_NTR_2.png")
    # pat27_img,pat27_img_width,pat27_img_height=jetson.utils.loadImageRGBA("./png/N_B1_NTR_4.png")
    # pat28_img,pat28_img_width,pat28_img_height=jetson.utils.loadImageRGBA("./png/N_B1_NTR_3.png")
    # pat29_img,pat29_img_width,pat29_img_height=jetson.utils.loadImageRGBA("./png/N_B1_NTR_1.png")

    # pat30_img,pat30_img_width,pat30_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_1.png") # B2
    # pat51_img,pat51_img_width,pat51_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_d.png")
    # pat31_img,pat31_img_width,pat31_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_a.png")
    # pat52_img,pat52_img_width,pat52_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_e.png")
    # pat32_img,pat32_img_width,pat32_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_b.png")
    # pat53_img,pat53_img_width,pat53_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_f.png")
    # pat33_img,pat33_img_width,pat33_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_c.png")
    # pat54_img,pat54_img_width,pat54_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_g.png")
    # pat34_img,pat34_img_width,pat34_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2.png")
    # pat35_img,pat35_img_width,pat35_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_3_a.png")
    # pat36_img,pat36_img_width,pat36_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_3_b.png")
    # pat37_img,pat37_img_width,pat37_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_3_c.png")
    # pat38_img,pat38_img_width,pat38_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_3_d.png")

    # pat39_img,pat39_img_width,pat39_img_height=jetson.utils.loadImageRGBA("./png/A_B3_FCW_B.png") # B3
    # pat40_img,pat40_img_width,pat40_img_height=jetson.utils.loadImageRGBA("./png/A_B3_FCW_BA.png")
    # pat41_img,pat41_img_width,pat41_img_height=jetson.utils.loadImageRGBA("./png/A_B3_FCW_R.png")
    # pat42_img,pat42_img_width,pat42_img_height=jetson.utils.loadImageRGBA("./png/A_B3_PDW_1.png")
    # pat43_img,pat43_img_width,pat43_img_height=jetson.utils.loadImageRGBA("./png/A_B3_PDW_2.png")
    # pat44_img,pat44_img_width,pat44_img_height=jetson.utils.loadImageRGBA("./png/A_B3_PDW_3.png")
    # pat45_img,pat45_img_width,pat45_img_height=jetson.utils.loadImageRGBA("./png/A_B3_PDW_4.png")

    # pat46_img,pat46_img_width,pat46_img_height=jetson.utils.loadImageRGBA("./png/A_B4_RLDW_B.png") # B4
    # pat47_img,pat47_img_width,pat47_img_height=jetson.utils.loadImageRGBA("./png/A_B4_RLDW_R.png")
    # pat48_img,pat48_img_width,pat48_img_height=jetson.utils.loadImageRGBA("./png/A_B4_RLDW_BL.png")
    # pat49_img,pat49_img_width,pat49_img_height=jetson.utils.loadImageRGBA("./png/A_B4_LLDW_B.png")
    # pat50_img,pat50_img_width,pat50_img_height=jetson.utils.loadImageRGBA("./png/A_B4_LLDW_R.png")

    # image position

    # pat1_alpha=0
    # pat1_img_x=133
    # pat1_img_y=0
    # pat1_img_width=268
    # pat1_img_height=268
    
    # pat1_img, pat1_img_width, pat1_img_height = images['pat1']
    # pat1.alpha, pat1.img_x, pat1.img_y = 0, 80, 387

    
    
    
    
    
    # pat1_alpha, pat1_img_x, pat1_img_y, pat1_img_width, pat1_img_height = 0, 80, 387, 150, 150 # A1

    # pat2_alpha, pat2_img_x, pat2_img_y, pat2_img_width, pat2_img_height = 0, 265, 390, 240, 145 # A2
    # pat3_alpha, pat3_img_x, pat3_img_y, pat3_img_width, pat3_img_height = 0, 265, 390, 240, 145
    # pat4_alpha, pat4_img_x, pat4_img_y, pat4_img_width, pat4_img_height = 0, 265, 390, 240, 145
    
    # pat5_alpha, pat5_img_x, pat5_img_y, pat5_img_width, pat5_img_height = 0, 560, 417, 160, 90 # A3
    # pat6_alpha, pat6_img_x, pat6_img_y, pat6_img_width, pat6_img_height = 0, 560, 403, 160, 118
    # pat7_alpha, pat7_img_x, pat7_img_y, pat7_img_width, pat7_img_height = 0, 560, 401, 160, 123
    # pat8_alpha, pat8_img_x, pat8_img_y, pat8_img_width, pat8_img_height = 0, 560, 422, 160, 80
    # pat9_alpha, pat9_img_x, pat9_img_y, pat9_img_width, pat9_img_height = 0, 560, 398, 160, 128

    # pat10_alpha, pat10_img_x, pat10_img_y, pat10_img_width, pat10_img_height = 0, 782, 404, 219, 120 # A4
    # pat11_alpha, pat11_img_x, pat11_img_y, pat11_img_width, pat11_img_height = 0, 770, 404, 231, 120
    # pat12_alpha, pat12_img_x, pat12_img_y, pat12_img_width, pat12_img_height = 0, 770, 404, 230,120
    # pat13_alpha, pat13_img_x, pat13_img_y, pat13_img_width, pat13_img_height = 0, 770, 404, 215, 115
    # pat14_alpha, pat14_img_x, pat14_img_y, pat14_img_width, pat14_img_height = 0, 770, 404, 215, 115
    # pat15_alpha, pat15_img_x, pat15_img_y, pat15_img_width, pat15_img_height = 0, 776, 404, 230, 95
    # pat16_alpha, pat16_img_x, pat16_img_y, pat16_img_width, pat16_img_height = 0, 785, 419, 221, 96

    # pat17_alpha, pat17_img_x, pat17_img_y, pat17_img_width, pat17_img_height = 0, 1045, 407, 160, 122 # A5

    # pat18_alpha, pat18_img_x, pat18_img_y, pat18_img_width, pat18_img_height = 0, 70, 155, 82, 164 # B5
    # pat19_alpha, pat19_img_x, pat19_img_y, pat19_img_width, pat19_img_height = 0, 1128, 155, 82, 164 # B6

    # pat20_alpha, pat20_img_x, pat20_img_y, pat20_img_width, pat20_img_height = 0, 585, 260, 110, 285 # B1
    # pat21_alpha, pat21_img_x, pat21_img_y, pat21_img_width, pat21_img_height = 0, 585, 260, 110, 285
    # pat22_alpha, pat22_img_x, pat22_img_y, pat22_img_width, pat22_img_height = 0, 585, 260, 110, 285
    # pat23_alpha, pat23_img_x, pat23_img_y, pat23_img_width, pat23_img_height = 0, 585, 260, 110, 285
    # pat24_alpha, pat24_img_x, pat24_img_y, pat24_img_width, pat24_img_height = 0, 585, 260, 110, 285
    
    # pat25_alpha, pat25_img_x, pat25_img_y, pat25_img_width, pat25_img_height = 0, 585, 175, 183, 370 
    
    # pat26_alpha, pat26_img_x, pat26_img_y, pat26_img_width, pat26_img_height = 0, 550, 415, 180, 130
    # pat27_alpha, pat27_img_x, pat27_img_y, pat27_img_width, pat27_img_height = 0, 580, 315, 126, 91
    # pat28_alpha, pat28_img_x, pat28_img_y, pat28_img_width, pat28_img_height = 0, 610, 235, 113, 82
    # pat29_alpha, pat29_img_x, pat29_img_y, pat29_img_width, pat29_img_height = 0, 640, 175, 80, 57

    # pat30_alpha, pat30_img_x, pat30_img_y, pat30_img_width, pat30_img_height = 0, 560, 232, 160, 50 # B2
    # pat51_alpha, pat51_img_x, pat51_img_y, pat51_img_width, pat51_img_height = 0, 540, 226, 200, 63
    # pat31_alpha, pat31_img_x, pat31_img_y, pat31_img_width, pat31_img_height = 0, 520, 220, 240, 75
    # pat52_alpha, pat52_img_x, pat52_img_y, pat52_img_width, pat52_img_height = 0, 500, 214, 280, 88
    # pat32_alpha, pat32_img_x, pat32_img_y, pat32_img_width, pat32_img_height = 0, 480, 207, 320, 100
    # pat53_alpha, pat53_img_x, pat53_img_y, pat53_img_width, pat53_img_height = 0, 460, 201, 360, 113
    # pat33_alpha, pat33_img_x, pat33_img_y, pat33_img_width, pat33_img_height = 0, 440, 195, 400, 125
    # pat54_alpha, pat54_img_x, pat54_img_y, pat54_img_width, pat54_img_height = 0, 420, 189, 440, 138

    # pat34_alpha, pat34_img_x, pat34_img_y, pat34_img_width, pat34_img_height = 0, 400, 182, 480, 150
    # pat35_alpha, pat35_img_x, pat35_img_y, pat35_img_width, pat35_img_height = 0, 400, 182, 480, 150
    # pat36_alpha, pat36_img_x, pat36_img_y, pat36_img_width, pat36_img_height = 0, 400, 182, 480, 150
    # pat37_alpha, pat37_img_x, pat37_img_y, pat37_img_width, pat37_img_height = 0, 400, 182, 480, 150
    # pat38_alpha, pat38_img_x, pat38_img_y, pat38_img_width, pat38_img_height = 0, 400, 182, 480, 150
    
    # pat39_alpha, pat39_img_x, pat39_img_y, pat39_img_width, pat39_img_height = 0, 310, 175, 660, 159 # B3
    # pat40_alpha, pat40_img_x, pat40_img_y, pat40_img_width, pat40_img_height = 0, 310, 175, 660, 159
    # pat41_alpha, pat41_img_x, pat41_img_y, pat41_img_width, pat41_img_height = 0, 310, 175, 660, 159
    # pat42_alpha, pat42_img_x, pat42_img_y, pat42_img_width, pat42_img_height = 0, 310, 175, 660, 159
    # pat43_alpha, pat43_img_x, pat43_img_y, pat43_img_width, pat43_img_height = 0, 310, 175, 660, 159
    # pat44_alpha, pat44_img_x, pat44_img_y, pat44_img_width, pat44_img_height = 0, 310, 175, 660, 159
    # pat45_alpha, pat45_img_x, pat45_img_y, pat45_img_width, pat45_img_height = 0, 310, 175, 660, 159

    # pat46_alpha, pat46_img_x, pat46_img_y, pat46_img_width, pat46_img_height = 0, 311, 161, 629, 179 # B4
    # pat47_alpha, pat47_img_x, pat47_img_y, pat47_img_width, pat47_img_height = 0, 311, 161, 629, 179
    # pat48_alpha, pat48_img_x, pat48_img_y, pat48_img_width, pat48_img_height = 0, 770, 161, 27, 179
    # pat49_alpha, pat49_img_x, pat49_img_y, pat49_img_width, pat49_img_height = 0, 311, 161, 629, 179
    # pat50_alpha, pat50_img_x, pat50_img_y, pat50_img_width, pat50_img_height = 0, 311, 161, 629, 179
    

    # text position
    test_txt_x=100
    test_txt_y=435
    test_txt_size=250
    test_txt_R,test_txt_G,test_txt_B,test_txt_A=(255,0,0,255)

    count=0

    def renderPattern(img, x, y, width, height, alpha, min_alpha, max_alpha, step, base, period, remain, count):
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, img, x, y, width, height, alpha)
        if (count // step) % period == remain:
            alpha = min(alpha + base, max_alpha)
        else:
            alpha = max(alpha - base, min_alpha)
        return alpha


    while display.IsOpen():
        jetson.utils.Overlay_all(bg_img, bg_img_width, bg_img_height, 0,0,0,255)
        
        # A1
        if count < 460:
            # pat1_alpha = renderPattern(pat1_img, pat1_img_x, pat1_img_y, pat1_img_width, pat1_img_height, pat1_alpha, 255, 255, 1, 255, 1, 0, count)
            pat1.alpha = renderPattern(pat1.img, pat1.img_x, pat1.img_y, pat1.img_width, pat1.img_height, pat1.alpha, 255, 255, 1, 255, 1, 0, count)
        # if (count//15)%2==0:
        #     pat1_alpha=min(pat1_alpha+17,255)
        # else:
        #     pat1_alpha=max(pat1_alpha-17,0)

        # A2
        if count < 120:
            # pat2_alpha = renderPattern(pat2_img, pat2_img_x, pat2_img_y, pat2_img_width, pat2_img_height,pat2_alpha, 0, 255, 10, 25, 2, 0, count) # 1 Hz
            pat2.alpha = renderPattern(pat2.img, pat2.img_x, pat2.img_y, pat2.img_width, pat2.img_height,pat2.alpha, 0, 255, 10, 25, 2, 0, count) # 1 Hz
        if count > 120 and count < 240:
            # pat3_alpha = renderPattern(pat3_img, pat3_img_x, pat3_img_y, pat3_img_width, pat3_img_height,pat3_alpha, 0, 255, 10, 25, 2, 0, count)
            pat3.alpha = renderPattern(pat3.img, pat3.img_x, pat3.img_y, pat3.img_width, pat3.img_height,pat3.alpha, 0, 255, 10, 25, 2, 0, count)
        if count > 240 and count < 360:
            # pat4_alpha = renderPattern(pat4_img, pat4_img_x, pat4_img_y, pat4_img_width, pat4_img_height,pat4_alpha, 0, 255, 10, 25, 2, 0, count)
            pat4.alpha = renderPattern(pat4.img, pat4.img_x, pat4.img_y, pat4.img_width, pat4.img_height,pat4.alpha, 0, 255, 10, 25, 2, 0, count)

        # A3
        if count < 120:
            if count < 24:
                # pat5_alpha = renderPattern(pat5_img, pat5_img_x, pat5_img_y, pat5_img_width, pat5_img_height,pat5_alpha, 0, 255, 10, 25, 2, 0, count)
                pat5.alpha = renderPattern(pat5.img, pat5.img_x, pat5.img_y, pat5.img_width, pat5.img_height,pat5.alpha, 0, 255, 10, 25, 2, 0, count)
            if count > 24 and count < 48:
                # pat6_alpha = renderPattern(pat6_img, pat6_img_x, pat6_img_y, pat6_img_width, pat6_img_height,pat6_alpha, 0, 255, 10, 25, 2, 0, count)
                pat6.alpha = renderPattern(pat6.img, pat6.img_x, pat6.img_y, pat6.img_width, pat6.img_height,pat6.alpha, 0, 255, 10, 25, 2, 0, count)
            if count > 48 and count < 72:
                # pat7_alpha = renderPattern(pat7_img, pat7_img_x, pat7_img_y, pat7_img_width, pat7_img_height,pat7_alpha, 0, 255, 10, 25, 2, 0, count)
                pat7.alpha = renderPattern(pat7.img, pat7.img_x, pat7.img_y, pat7.img_width, pat7.img_height,pat7.alpha, 0, 255, 10, 25, 2, 0, count)
            if count > 72 and count < 96:
                # pat8_alpha = renderPattern(pat8_img, pat8_img_x, pat8_img_y, pat8_img_width, pat8_img_height,pat8_alpha, 0, 255, 10, 25, 2, 0, count)
                pat8.alpha = renderPattern(pat8.img, pat8.img_x, pat8.img_y, pat8.img_width, pat8.img_height,pat8.alpha, 0, 255, 10, 25, 2, 0, count)
            if count > 96 and count < 120:
                # pat9_alpha = renderPattern(pat9_img, pat9_img_x, pat9_img_y, pat9_img_width, pat9_img_height,pat9_alpha, 0, 255, 10, 25, 2, 0, count)
                pat9.alpha = renderPattern(pat9.img, pat9.img_x, pat9.img_y, pat9.img_width, pat9.img_height,pat9.alpha, 0, 255, 10, 25, 2, 0, count)

        # A4
        if count < 120:
            if count < 20:
                # pat10_alpha = renderPattern(pat10_img, pat10_img_x, pat10_img_y, pat10_img_width, pat10_img_height,pat10_alpha, 255, 255, 1, 255, 1, 0, count)
                pat10.alpha = renderPattern(pat10.img, pat10.img_x, pat10.img_y, pat10.img_width, pat10.img_height,pat10.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 20 and count < 40:
                # pat12_alpha = renderPattern(pat12_img, pat12_img_x, pat12_img_y, pat12_img_width, pat12_img_height,pat12_alpha, 255, 255, 1, 255, 1, 0, count)
                pat12.alpha = renderPattern(pat12.img, pat12.img_x, pat12.img_y, pat12.img_width, pat12.img_height,pat12.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 40 and count < 60:
                # pat13_alpha = renderPattern(pat13_img, pat13_img_x, pat13_img_y, pat13_img_width, pat13_img_height,pat13_alpha, 255, 255, 1, 255, 1, 0, count)
                pat13.alpha = renderPattern(pat13.img, pat13.img_x, pat13.img_y, pat13.img_width, pat13.img_height,pat13.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 60 and count < 80:
                # pat14_alpha = renderPattern(pat14_img, pat14_img_x, pat14_img_y, pat14_img_width, pat14_img_height,pat14_alpha, 255, 255, 1, 255, 1, 0, count)
                pat14.alpha = renderPattern(pat14.img, pat14.img_x, pat14.img_y, pat14.img_width, pat14.img_height,pat14.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 80 and count < 100:
                # pat15_alpha = renderPattern(pat15_img, pat15_img_x, pat15_img_y, pat15_img_width, pat15_img_height,pat15_alpha, 255, 255, 1, 255, 1, 0, count)
                pat15.alpha = renderPattern(pat15.img, pat15.img_x, pat15.img_y, pat15.img_width, pat15.img_height,pat15.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 100 and count < 120:
                # pat16_alpha = renderPattern(pat16_img, pat16_img_x, pat16_img_y, pat16_img_width, pat16_img_height,pat16_alpha, 255, 255, 1, 255, 1, 0, count)
                pat16.alpha = renderPattern(pat16.img, pat16.img_x, pat16.img_y, pat16.img_width, pat16.img_height,pat16.alpha, 255, 255, 1, 255, 1, 0, count)

        if count > 120 and count < 460:
            # pat11_alpha = renderPattern(pat11_img, pat11_img_x, pat11_img_y, pat11_img_width, pat11_img_height,pat11_alpha, 255, 255, 1, 255, 1, 0, count)
            pat11.alpha = renderPattern(pat11.img, pat11.img_x, pat11.img_y, pat11.img_width, pat11.img_height,pat11.alpha, 255, 255, 1, 255, 1, 0, count)

        # A5
        if count < 460:
            # pat17_alpha = renderPattern(pat17_img, pat17_img_x, pat17_img_y, pat17_img_width, pat17_img_height,pat17_alpha, 255, 255, 1, 255, 1, 0, count)
            pat17.alpha = renderPattern(pat17.img, pat17.img_x, pat17.img_y, pat17.img_width, pat17.img_height,pat17.alpha, 255, 255, 1, 255, 1, 0, count)

        # B5
        if count < 120:
            # pat18_alpha = renderPattern(pat18_img, pat18_img_x, pat18_img_y, pat18_img_width, pat18_img_height,pat18_alpha, 0, 255, 15, 17, 2, 0, count)
            pat18.alpha = renderPattern(pat18.img, pat18.img_x, pat18.img_y, pat18.img_width, pat18.img_height,pat18.alpha, 0, 255, 15, 17, 2, 0, count)

        # B6
        if count > 120:
            # pat19_alpha = renderPattern(pat19_img, pat19_img_x, pat19_img_y, pat19_img_width, pat19_img_height,pat19_alpha, 0, 255, 15, 17, 2, 0, count)
            pat19.alpha = renderPattern(pat19.img, pat19.img_x, pat19.img_y, pat19.img_width, pat19.img_height,pat19.alpha, 0, 255, 15, 17, 2, 0, count)

        # B1
        if count > 120 and count < 240:
            # pat21_alpha = renderPattern(pat21_img, pat21_img_x, pat21_img_y, pat21_img_width, pat21_img_height,pat21_alpha, 50, 255, 7, 36, 4, 0, count)
            # pat22_alpha = renderPattern(pat22_img, pat22_img_x, pat22_img_y, pat22_img_width, pat22_img_height,pat22_alpha, 50, 255, 7, 36, 4, 1, count)
            # pat23_alpha = renderPattern(pat23_img, pat23_img_x, pat23_img_y, pat23_img_width, pat23_img_height,pat23_alpha, 50, 255, 7, 36, 4, 2, count)
            # pat24_alpha = renderPattern(pat24_img, pat24_img_x, pat24_img_y, pat24_img_width, pat24_img_height,pat24_alpha, 50, 255, 7, 36, 4, 3, count)
            pat21.alpha = renderPattern(pat21.img, pat21.img_x, pat21.img_y, pat21.img_width, pat21.img_height,pat21.alpha, 50, 255, 7, 36, 4, 0, count)
            pat22.alpha = renderPattern(pat22.img, pat22.img_x, pat22.img_y, pat22.img_width, pat22.img_height,pat22.alpha, 50, 255, 7, 36, 4, 1, count)
            pat23.alpha = renderPattern(pat23.img, pat23.img_x, pat23.img_y, pat23.img_width, pat23.img_height,pat23.alpha, 50, 255, 7, 36, 4, 2, count)
            pat24.alpha = renderPattern(pat24.img, pat24.img_x, pat24.img_y, pat24.img_width, pat24.img_height,pat24.alpha, 50, 255, 7, 36, 4, 3, count)

        if count > 180 and count < 240:
            # pat25_alpha = renderPattern(pat25_img, pat25_img_x, pat25_img_y, pat25_img_width, pat25_img_height,pat25_alpha, 0, 255, 7, 36, 4, 3, count)
            pat25.alpha = renderPattern(pat25.img, pat25.img_x, pat25.img_y, pat25.img_width, pat25.img_height,pat25.alpha, 0, 255, 7, 36, 4, 3, count)

        
        if count > 240 and count < 280:
            if count > 240 and count < 250:
                # pat26_alpha = renderPattern(pat26_img, pat26_img_x, pat26_img_y, pat26_img_width, pat26_img_height, pat26_alpha, 255, 255, 1, 255, 1, 0, count)
                pat26.alpha = renderPattern(pat26.img, pat26.img_x, pat26.img_y, pat26.img_width, pat26.img_height, pat26.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 250 and count < 260:
                # pat26_alpha = renderPattern(pat26_img, pat26_img_x, pat26_img_y, pat26_img_width, pat26_img_height, pat26_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat27_alpha = renderPattern(pat27_img, pat27_img_x, pat27_img_y, pat27_img_width, pat27_img_height, pat27_alpha, 255, 255, 1, 255, 1, 0, count)
                pat26.alpha = renderPattern(pat26.img, pat26.img_x, pat26.img_y, pat26.img_width, pat26.img_height, pat26.alpha, 0, 255, 15, 17, 2, 50, count)
                pat27.alpha = renderPattern(pat27.img, pat27.img_x, pat27.img_y, pat27.img_width, pat27.img_height, pat27.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 260 and count < 270:
                # pat26_alpha = renderPattern(pat26_img, pat26_img_x, pat26_img_y, pat26_img_width, pat26_img_height, pat26_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat27_alpha = renderPattern(pat27_img, pat27_img_x, pat27_img_y, pat27_img_width, pat27_img_height, pat27_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat28_alpha = renderPattern(pat28_img, pat28_img_x, pat28_img_y, pat28_img_width, pat28_img_height, pat28_alpha, 255, 255, 1, 255, 1, 0, count)
                pat26.alpha = renderPattern(pat26.img, pat26.img_x, pat26.img_y, pat26.img_width, pat26.img_height, pat26.alpha, 0, 255, 15, 17, 2, 50, count)
                pat27.alpha = renderPattern(pat27.img, pat27.img_x, pat27.img_y, pat27.img_width, pat27.img_height, pat27.alpha, 0, 255, 15, 17, 2, 50, count)
                pat28.alpha = renderPattern(pat28.img, pat28.img_x, pat28.img_y, pat28.img_width, pat28.img_height, pat28.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 270 and count < 275:
                # pat27_alpha = renderPattern(pat27_img, pat27_img_x, pat27_img_y, pat27_img_width, pat27_img_height, pat27_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat28_alpha = renderPattern(pat28_img, pat28_img_x, pat28_img_y, pat28_img_width, pat28_img_height, pat28_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat29_alpha = renderPattern(pat29_img, pat29_img_x, pat29_img_y, pat29_img_width, pat29_img_height, pat29_alpha, 255, 255, 1, 255, 1, 0, count)
                pat27.alpha = renderPattern(pat27.img, pat27.img_x, pat27.img_y, pat27.img_width, pat27.img_height, pat27.alpha, 0, 255, 15, 17, 2, 50, count)
                pat28.alpha = renderPattern(pat28.img, pat28.img_x, pat28.img_y, pat28.img_width, pat28.img_height, pat28.alpha, 0, 255, 15, 17, 2, 50, count)
                pat29.alpha = renderPattern(pat29.img, pat29.img_x, pat29.img_y, pat29.img_width, pat29.img_height, pat29.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 275 and count < 280:
                # pat29_alpha = renderPattern(pat29_img, pat29_img_x-40, pat29_img_y+54, pat29_img_width, pat29_img_height, pat29_alpha, 0, 255, 15, 17, 2, 50, count)
                pat29.alpha = renderPattern(pat29.img, pat29.img_x-40, pat29.img_y+54, pat29.img_width, pat29.img_height, pat29.alpha, 0, 255, 15, 17, 2, 50, count)
        
        # B2    
        if count > 280 and count < 380:
            if count > 280 and count < 285:
                # pat30_alpha = renderPattern(pat30_img, pat30_img_x, pat30_img_y, pat30_img_width, pat30_img_height, pat30_alpha, 255, 255, 1, 255, 1, 0, count)
                pat30.alpha = renderPattern(pat30.img, pat30.img_x, pat30.img_y, pat30.img_width, pat30.img_height, pat30.alpha, 255, 255, 1, 255, 1, 0, count)
            # if count >= 282 and count < 285:
            #     pat30_alpha = renderPattern(pat30_img, pat30_img_x, pat30_img_y, pat30_img_width, pat30_img_height, pat30_alpha, 100, 255, 15, 17, 2, 50, count)
            if count >= 285 and count < 280:
                # pat51_alpha = renderPattern(pat51_img, pat51_img_x, pat51_img_y, pat51_img_width, pat51_img_height, pat51_alpha, 255, 255, 1, 255, 1, 0, count)
                pat51.alpha = renderPattern(pat51.img, pat51.img_x, pat51.img_y, pat51.img_width, pat51.img_height, pat51.alpha, 255, 255, 1, 255, 1, 0, count)
            # if count >= 287 and count < 290:
            #     pat49_alpha = renderPattern(pat49_img, pat49_img_x, pat49_img_y, pat49_img_width, pat49_img_height, pat49_alpha, 100, 255, 15, 17, 2, 50, count)
            if count >= 290 and count < 295:
                # pat31_alpha = renderPattern(pat31_img, pat31_img_x, pat31_img_y, pat31_img_width, pat31_img_height, pat31_alpha, 255, 255, 1, 255, 1, 0, count)
                pat31.alpha = renderPattern(pat31.img, pat31.img_x, pat31.img_y, pat31.img_width, pat31.img_height, pat31.alpha, 255, 255, 1, 255, 1, 0, count)
            # if count >= 292 and count < 295:
            #     pat31_alpha = renderPattern(pat31_img, pat31_img_x, pat31_img_y, pat31_img_width, pat31_img_height, pat31_alpha, 100, 255, 15, 17, 2, 50, count)
            if count >= 295 and count < 300:
                # pat52_alpha = renderPattern(pat52_img, pat52_img_x, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 255, 255, 1, 255, 1, 0, count)
                pat52.alpha = renderPattern(pat52.img, pat52.img_x, pat52.img_y, pat52.img_width, pat52.img_height, pat52.alpha, 255, 255, 1, 255, 1, 0, count)
            # if count >= 297 and count < 300:
            #     pat50_alpha = renderPattern(pat50_img, pat50_img_x, pat50_img_y, pat50_img_width, pat50_img_height, pat50_alpha, 100, 255, 15, 17, 2, 50, count)
            if count >= 300 and count < 305:
                # pat32_alpha = renderPattern(pat32_img, pat32_img_x, pat32_img_y, pat32_img_width, pat32_img_height, pat32_alpha, 255, 255, 1, 255, 1, 0, count)
                pat32.alpha = renderPattern(pat32.img, pat32.img_x, pat32.img_y, pat32.img_width, pat32.img_height, pat32.alpha, 255, 255, 1, 255, 1, 0, count)
            # if count >= 302 and count < 305:
            #     pat32_alpha = renderPattern(pat32_img, pat32_img_x, pat32_img_y, pat32_img_width, pat32_img_height, pat32_alpha, 100, 255, 15, 17, 2, 50, count)
            if count >= 305 and count < 310:
                # pat53_alpha = renderPattern(pat53_img, pat53_img_x, pat53_img_y, pat53_img_width, pat53_img_height, pat53_alpha, 255, 255, 1, 255, 1, 0, count)
                pat53.alpha = renderPattern(pat53.img, pat53.img_x, pat53.img_y, pat53.img_width, pat53.img_height, pat53.alpha, 255, 255, 1, 255, 1, 0, count)
            # if count >= 307 and count < 310:
            #     pat51_alpha = renderPattern(pat51_img, pat51_img_x, pat51_img_y, pat51_img_width, pat51_img_height, pat51_alpha, 100, 255, 15, 17, 2, 50, count)
            if count >= 310 and count < 315:
                # pat33_alpha = renderPattern(pat33_img, pat33_img_x, pat33_img_y, pat33_img_width, pat33_img_height, pat33_alpha, 255, 255, 1, 255, 1, 0, count)
                pat33.alpha = renderPattern(pat33.img, pat33.img_x, pat33.img_y, pat33.img_width, pat33.img_height, pat33.alpha, 255, 255, 1, 255, 1, 0, count)
            # if count >= 312 and count < 315:
            #     pat33_alpha = renderPattern(pat33_img, pat33_img_x, pat33_img_y, pat33_img_width, pat33_img_height, pat33_alpha, 100, 255, 15, 17, 2, 50, count)
            if count >= 315 and count < 320:
                # pat54_alpha = renderPattern(pat54_img, pat54_img_x, pat54_img_y, pat54_img_width, pat54_img_height, pat54_alpha, 255, 255, 1, 255, 1, 0, count)
                pat54.alpha = renderPattern(pat54.img, pat54.img_x, pat54.img_y, pat54.img_width, pat54.img_height, pat54.alpha, 255, 255, 1, 255, 1, 0, count)
            # if count >= 317 and count < 320:
            #     pat52_alpha = renderPattern(pat52_img, pat52_img_x, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 100, 255, 15, 17, 2, 50, count)
            if count >= 320 and count < 330:
                # pat34_alpha = renderPattern(pat34_img, pat34_img_x, pat34_img_y, pat34_img_width, pat34_img_height, pat34_alpha, 255, 255, 1, 255, 1, 0, count)
                pat34.alpha = renderPattern(pat34.img, pat34.img_x, pat34.img_y, pat34.img_width, pat34.img_height, pat34.alpha, 255, 255, 1, 255, 1, 0, count)
            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat30_img, pat30_img_x, pat30_img_y, pat30_img_width, pat30_img_height,pat30_alpha)
            # if count > 280 and count < 290:
            #     pat30_alpha=255
            # else:
            #     pat30_alpha=max(pat30_alpha-30,0)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat31_img, pat31_img_x, pat31_img_y, pat31_img_width, pat31_img_height,pat31_alpha)
            # if count > 290 and count < 300:
            #     pat31_alpha=255
            # else:
            #     pat31_alpha=max(pat31_alpha-30,0)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat32_img, pat32_img_x, pat32_img_y, pat32_img_width, pat32_img_height,pat32_alpha)
            # if count > 300 and count < 310:
            #     pat32_alpha=255
            # else:
            #     pat32_alpha=max(pat32_alpha-30,0)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat33_img, pat33_img_x, pat33_img_y, pat33_img_width, pat33_img_height,pat33_alpha)
            # if count > 310 and count < 320:
            #     pat33_alpha=255
            # else:
            #     pat33_alpha=max(pat33_alpha-30,0)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat34_img, pat34_img_x, pat34_img_y, pat34_img_width, pat34_img_height,pat34_alpha)
            # if count > 320 and count < 330:
            #     pat34_alpha=255
            # else:
            #     pat34_alpha=max(pat34_alpha-30,0)

            if count > 330 and count < 350:
                # pat35_alpha = renderPattern(pat35_img, pat35_img_x, pat35_img_y, pat35_img_width, pat35_img_height, pat35_alpha, 255, 255, 1, 255, 1, 0, count)
                pat35.alpha = renderPattern(pat35.img, pat35.img_x, pat35.img_y, pat35.img_width, pat35.img_height, pat35.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 350 and count < 360:
                # pat35_alpha = renderPattern(pat35_img, pat35_img_x, pat35_img_y, pat35_img_width, pat35_img_height, pat35_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat36_alpha = renderPattern(pat36_img, pat36_img_x, pat36_img_y, pat36_img_width, pat36_img_height, pat36_alpha, 255, 255, 1, 255, 1, 0, count)
                pat35.alpha = renderPattern(pat35.img, pat35.img_x, pat35.img_y, pat35.img_width, pat35.img_height, pat35.alpha, 0, 255, 15, 17, 2, 50, count)
                pat36.alpha = renderPattern(pat36.img, pat36.img_x, pat36.img_y, pat36.img_width, pat36.img_height, pat36.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 360 and count < 370:
                # pat35_alpha = renderPattern(pat35_img, pat35_img_x, pat35_img_y, pat35_img_width, pat35_img_height, pat35_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat36_alpha = renderPattern(pat36_img, pat36_img_x, pat36_img_y, pat36_img_width, pat36_img_height, pat36_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat37_alpha = renderPattern(pat37_img, pat37_img_x, pat37_img_y, pat37_img_width, pat37_img_height, pat37_alpha, 255, 255, 1, 255, 1, 0, count)
                pat35.alpha = renderPattern(pat35.img, pat35.img_x, pat35.img_y, pat35.img_width, pat35.img_height, pat35.alpha, 0, 255, 15, 17, 2, 50, count)
                pat36.alpha = renderPattern(pat36.img, pat36.img_x, pat36.img_y, pat36.img_width, pat36.img_height, pat36.alpha, 0, 255, 15, 17, 2, 50, count)
                pat37.alpha = renderPattern(pat37.img, pat37.img_x, pat37.img_y, pat37.img_width, pat37.img_height, pat37.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 370 and count < 380:
                # pat36_alpha = renderPattern(pat36_img, pat36_img_x, pat36_img_y, pat36_img_width, pat36_img_height, pat36_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat37_alpha = renderPattern(pat37_img, pat37_img_x, pat37_img_y, pat37_img_width, pat37_img_height, pat37_alpha, 0, 255, 15, 17, 2, 50, count)
                # pat38_alpha = renderPattern(pat38_img, pat38_img_x, pat38_img_y, pat38_img_width, pat38_img_height, pat38_alpha, 255, 255, 1, 255, 1, 0, count)
                pat36.alpha = renderPattern(pat36.img, pat36.img_x, pat36.img_y, pat36.img_width, pat36.img_height, pat36.alpha, 0, 255, 15, 17, 2, 50, count)
                pat37.alpha = renderPattern(pat37.img, pat37.img_x, pat37.img_y, pat37.img_width, pat37.img_height, pat37.alpha, 0, 255, 15, 17, 2, 50, count)
                pat38.alpha = renderPattern(pat38.img, pat38.img_x, pat38.img_y, pat38.img_width, pat38.img_height, pat38.alpha, 255, 255, 1, 255, 1, 0, count)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat35_img, pat35_img_x, pat35_img_y, pat35_img_width, pat35_img_height,pat35_alpha)
            # if count > 330 and count < 340:
            #     pat35_alpha=255
            # else:
            #     pat35_alpha=max(pat35_alpha-15,0)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat35_img, pat35_img_x, pat35_img_y, pat35_img_width, pat35_img_height,pat35_alpha)
            # if count > 340 and count < 350:
            #     pat35_alpha=255
            # else:
            #     pat35_alpha=max(pat35_alpha-15,0)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat36_img, pat36_img_x, pat36_img_y, pat36_img_width, pat36_img_height,pat36_alpha)
            # if count > 350 and count < 360:
            #     pat36_alpha=255
            # else:
            #     pat36_alpha=max(pat36_alpha-15,0)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat37_img, pat37_img_x, pat37_img_y, pat37_img_width, pat37_img_height,pat37_alpha)
            # if count > 360 and count < 370:
            #     pat37_alpha=255
            # else:
            #     pat37_alpha=max(pat37_alpha-15,0)

            # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat38_img, pat38_img_x, pat38_img_y, pat38_img_width, pat38_img_height,pat38_alpha)
            # if count > 370 and count < 380:
            #     pat38_alpha=255
            # else:
            #     pat38_alpha=max(pat38_alpha-15,0)  


        # B3
        if count < 120:
            # pat39_alpha = renderPattern(pat39_img, pat39_img_x, pat39_img_y, pat39_img_width, pat39_img_height, pat39_alpha, 255, 255, 1, 255, 1, 0, count)
            pat39.alpha = renderPattern(pat39.img, pat39.img_x, pat39.img_y, pat39.img_width, pat39.img_height, pat39.alpha, 255, 255, 1, 255, 1, 0, count)
            if count < 40:
                # pat40_alpha = renderPattern(pat40_img, pat40_img_x, pat40_img_y, pat40_img_width, pat40_img_height, pat40_alpha, 255, 255, 1, 255, 1, 0, count)
                # pat41_alpha = renderPattern(pat41_img, pat41_img_x, pat41_img_y, pat41_img_width, pat41_img_height, pat41_alpha, 0, 255, 15, 17, 2, 0, count)
                pat40.alpha = renderPattern(pat40.img, pat40.img_x, pat40.img_y, pat40.img_width, pat40.img_height, pat40.alpha, 255, 255, 1, 255, 1, 0, count)
                pat41.alpha = renderPattern(pat41.img, pat41.img_x, pat41.img_y, pat41.img_width, pat41.img_height, pat41.alpha, 0, 255, 15, 17, 2, 0, count)
            if count > 40 and count < 60:
                # pat42_alpha = renderPattern(pat42_img, pat42_img_x, pat42_img_y, pat42_img_width, pat42_img_height, pat42_alpha, 0, 255, 5, 51, 2, 0, count) # 0.5 Hz
                pat42.alpha = renderPattern(pat42.img, pat42.img_x, pat42.img_y, pat42.img_width, pat42.img_height, pat42.alpha, 0, 255, 5, 51, 2, 0, count) # 0.5 Hz
            if count > 60 and count < 80:
                # pat43_alpha = renderPattern(pat43_img, pat43_img_x, pat43_img_y, pat43_img_width, pat43_img_height, pat43_alpha, 0, 255, 5, 51, 2, 0, count)
                pat43.alpha = renderPattern(pat43.img, pat43.img_x, pat43.img_y, pat43.img_width, pat43.img_height, pat43.alpha, 0, 255, 5, 51, 2, 0, count)
            if count > 80 and count < 100:
                # pat44_alpha = renderPattern(pat44_img, pat44_img_x, pat44_img_y, pat44_img_width, pat44_img_height, pat44_alpha, 0, 255, 5, 51, 2, 0, count)
                pat44.alpha = renderPattern(pat44.img, pat44.img_x, pat44.img_y, pat44.img_width, pat44.img_height, pat44.alpha, 0, 255, 5, 51, 2, 0, count)
            if count > 100 and count < 120:
                # pat45_alpha = renderPattern(pat45_img, pat45_img_x, pat45_img_y, pat45_img_width, pat45_img_height, pat45_alpha, 0, 255, 5, 51, 2, 0, count)
                pat45.alpha = renderPattern(pat45.img, pat45.img_x, pat45.img_y, pat45.img_width, pat45.img_height, pat45.alpha, 0, 255, 5, 51, 2, 0, count)

        # B4
        if count > 380:
            if count > 380 and count < 460:
                # pat46_alpha = renderPattern(pat46_img, pat46_img_x, pat46_img_y, pat46_img_width, pat46_img_height, pat46_alpha, 255, 255, 1, 255, 1, 0, count)
                # pat47_alpha = renderPattern(pat47_img, pat47_img_x, pat47_img_y, pat47_img_width, pat47_img_height, pat47_alpha, 255, 255, 1, 255, 1, 0, count)
                pat46.alpha = renderPattern(pat46.img, pat46.img_x, pat46.img_y, pat46.img_width, pat46.img_height, pat46.alpha, 255, 255, 1, 255, 1, 0, count)
                pat47.alpha = renderPattern(pat47.img, pat47.img_x, pat47.img_y, pat47.img_width, pat47.img_height, pat47.alpha, 255, 255, 1, 255, 1, 0, count)
                for i in range(0, 8):
                    if (count//2)%8==i:
                        # pat48_alpha = renderPattern(pat48_img, pat48_img_x+i*20, pat48_img_y, pat48_img_width, pat48_img_height, pat48_alpha, 200, 200, 1, 255, 1, 0, count)
                        pat48.alpha = renderPattern(pat48.img, pat48.img_x+i*20, pat48.img_y, pat48.img_width, pat48.img_height, pat48.alpha, 200, 200, 1, 255, 1, 0, count)
                # if (count//2)%8==0:
                #     pat52_alpha = renderPattern(pat52_img, pat52_img_x, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 200, 200, 1, 255, 1, 0, count)
                # elif (count//2)%8==1:
                #     pat52_alpha = renderPattern(pat52_img, pat52_img_x+20, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 200, 200, 1, 255, 1, 0, count)
                # elif (count//2)%8==2:
                #     pat52_alpha = renderPattern(pat52_img, pat52_img_x+40, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 200, 200, 1, 255, 1, 0, count)
                # elif (count//2)%8==3:
                #     pat52_alpha = renderPattern(pat52_img, pat52_img_x+60, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 200, 200, 1, 255, 1, 0, count)
                # elif (count//2)%8==4:
                #     pat52_alpha = renderPattern(pat52_img, pat52_img_x+80, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 200, 200, 1, 255, 1, 0, count)
                # elif (count//2)%8==5:
                #     pat52_alpha = renderPattern(pat52_img, pat52_img_x+100, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 200, 200, 1, 255, 1, 0, count)
                # elif (count//2)%8==6:
                #     pat52_alpha = renderPattern(pat52_img, pat52_img_x+120, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 200, 200, 1, 255, 1, 0, count)
                # elif (count//2)%8==7:
                #     pat52_alpha = renderPattern(pat52_img, pat52_img_x+140, pat52_img_y, pat52_img_width, pat52_img_height, pat52_alpha, 200, 200, 1, 255, 1, 0, count)
            # if count > 460 and count < 540:
            if count > 460 and count < 540:
                # pat49_alpha = renderPattern(pat49_img, pat49_img_x, pat49_img_y, pat49_img_width, pat49_img_height, pat49_alpha, 255, 255, 1, 255, 1, 0, count)
                # pat50_alpha = renderPattern(pat50_img, pat50_img_x, pat50_img_y, pat50_img_width, pat50_img_height, pat50_alpha, 255, 255, 1, 255, 1, 0, count)
                pat49.alpha = renderPattern(pat49.img, pat49.img_x, pat49.img_y, pat49.img_width, pat49.img_height, pat49.alpha, 255, 255, 1, 255, 1, 0, count)
                pat50.alpha = renderPattern(pat50.img, pat50.img_x, pat50.img_y, pat50.img_width, pat50.img_height, pat50.alpha, 255, 255, 1, 255, 1, 0, count)
                for i in range(0, 8):
                    if (count//2)%8==i:
                        # pat48_alpha = renderPattern(pat48_img, pat48_img_x-314-i*20, pat48_img_y, pat48_img_width, pat48_img_height, pat48_alpha, 200, 200, 1, 255, 1, 0, count)
                        pat48.alpha = renderPattern(pat48.img, pat48.img_x-314-i*20, pat48.img_y, pat48.img_width, pat48.img_height, pat48.alpha, 200, 200, 1, 255, 1, 0, count)


        # print(count)

        # if (count//150)%2==0:
        #     jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, "60", test_txt_x,test_txt_y,test_txt_size,test_txt_R,test_txt_G,test_txt_B,test_txt_A)
        if count < 460:
            a1_number=110-(count//20)
            if a1_number >= 100:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a1_number), test_txt_x,test_txt_y,80,0,255,255,255)
            else:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a1_number), test_txt_x+18,test_txt_y,80,0,255,255,255)

            if (count//15)%3==0:
                a2_number=80-(count//20)
            if a2_number >= 100:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+230,test_txt_y-37,80,0,255,255,255)
            else:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a2_number), test_txt_x+248,test_txt_y-37,80,0,255,255,255)

            a3_number=100-(count//10)
            if a3_number >= 100:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number), test_txt_x+740,test_txt_y+40,80,0,255,255,255)
            elif a3_number > 0:
                jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number)+'m', test_txt_x+758,test_txt_y+40,80,0,255,255,255)
    
        display.RenderOnce(bg_img, bg_img_width, bg_img_height,img_start_x,img_start_y)

        count=count+1
        
        # time.sleep(0.03)
        time.sleep(0.05)

