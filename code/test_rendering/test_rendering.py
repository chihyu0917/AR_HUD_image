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

    bg_img,bg_img_width,bg_img_height=jetson.utils.loadImageRGBA("background.png")
    # pat1_img,pat1_img_width,pat1_img_height=jetson.utils.loadImageRGBA("logo.png")
    pat1_img,pat1_img_width,pat1_img_height=jetson.utils.loadImageRGBA("./png/W_A1_SL.png")
    pat2_img,pat2_img_width,pat2_img_height=jetson.utils.loadImageRGBA("./png/W_A2_R_B.png")
    pat3_img,pat3_img_width,pat3_img_height=jetson.utils.loadImageRGBA("./png/W_A2_R_L.png")
    pat4_img,pat4_img_width,pat4_img_height=jetson.utils.loadImageRGBA("./png/W_A2_R_R.png")
    pat5_img,pat5_img_width,pat5_img_height=jetson.utils.loadImageRGBA("./png/W_A3_SF.png")
    pat6_img,pat6_img_width,pat6_img_height=jetson.utils.loadImageRGBA("./png/W_A3_BL.png")
    pat7_img,pat7_img_width,pat7_img_height=jetson.utils.loadImageRGBA("./png/W_A3_MH.png")
    pat8_img,pat8_img_width,pat8_img_height=jetson.utils.loadImageRGBA("./png/W_A3_MS.png")
    pat9_img,pat9_img_width,pat9_img_height=jetson.utils.loadImageRGBA("./png/W_A3_BF.png")
    pat10_img,pat10_img_width,pat10_img_height=jetson.utils.loadImageRGBA('./png/N_A4_S.png')
    pat11_img,pat11_img_width,pat11_img_height=jetson.utils.loadImageRGBA('./png/N_A4_TR.png')
    pat12_img,pat12_img_width,pat12_img_height=jetson.utils.loadImageRGBA('./png/N_A4_TL.png')
    pat13_img,pat13_img_width,pat13_img_height=jetson.utils.loadImageRGBA('./png/N_A4_KR.png')
    pat14_img,pat14_img_width,pat14_img_height=jetson.utils.loadImageRGBA('./png/N_A4_KL.png')
    pat15_img,pat15_img_width,pat15_img_height=jetson.utils.loadImageRGBA('./png/N_A4_TA.png')
    pat16_img,pat16_img_width,pat16_img_height=jetson.utils.loadImageRGBA('./png/N_A4_D.png')
    pat17_img,pat17_img_width,pat17_img_height=jetson.utils.loadImageRGBA("./png/W_A5_A.png")
    pat18_img,pat18_img_width,pat18_img_height=jetson.utils.loadImageRGBA("./png/A_B5_LBIN.png")
    pat19_img,pat19_img_width,pat19_img_height=jetson.utils.loadImageRGBA("./png/A_B6_RBIN.png")
    pat20_img,pat20_img_width,pat20_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S.png")
    pat21_img,pat21_img_width,pat21_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S_1.png")
    pat22_img,pat22_img_width,pat22_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S_2.png")
    pat23_img,pat23_img_width,pat23_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S_3.png")
    pat24_img,pat24_img_width,pat24_img_height=jetson.utils.loadImageRGBA("./png/N_B1_S_4.png")
    pat25_img,pat25_img_width,pat25_img_height=jetson.utils.loadImageRGBA("./png/N_B1_FTR.png")
    pat26_img,pat26_img_width,pat26_img_height=jetson.utils.loadImageRGBA("./png/N_B1_NTR_2.png")
    pat27_img,pat27_img_width,pat27_img_height=jetson.utils.loadImageRGBA("./png/N_B1_NTR_4.png")
    pat28_img,pat28_img_width,pat28_img_height=jetson.utils.loadImageRGBA("./png/N_B1_NTR_3.png")
    pat29_img,pat29_img_width,pat29_img_height=jetson.utils.loadImageRGBA("./png/N_B1_NTR_1.png")
    pat30_img,pat30_img_width,pat30_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_1.png")
    pat31_img,pat31_img_width,pat31_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_a.png")
    pat32_img,pat32_img_width,pat32_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_b.png")
    pat33_img,pat33_img_width,pat33_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2_c.png")
    pat34_img,pat34_img_width,pat34_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_2.png")
    pat35_img,pat35_img_width,pat35_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_3_a.png")
    pat36_img,pat36_img_width,pat36_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_3_b.png")
    pat37_img,pat37_img_width,pat37_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_3_c.png")
    pat38_img,pat38_img_width,pat38_img_height=jetson.utils.loadImageRGBA("./png/N_B2_TRI_3_d.png")
    pat39_img,pat39_img_width,pat39_img_height=jetson.utils.loadImageRGBA("./png/A_B3_FCW_B.png")
    pat40_img,pat40_img_width,pat40_img_height=jetson.utils.loadImageRGBA("./png/A_B3_FCW_BA.png")
    pat41_img,pat41_img_width,pat41_img_height=jetson.utils.loadImageRGBA("./png/A_B3_FCW_R.png")
    pat42_img,pat42_img_width,pat42_img_height=jetson.utils.loadImageRGBA("./png/A_B3_PDW_1.png")
    pat43_img,pat43_img_width,pat43_img_height=jetson.utils.loadImageRGBA("./png/A_B3_PDW_2.png")
    pat44_img,pat44_img_width,pat44_img_height=jetson.utils.loadImageRGBA("./png/A_B3_PDW_3.png")
    pat45_img,pat45_img_width,pat45_img_height=jetson.utils.loadImageRGBA("./png/A_B3_PDW_4.png")


    # image position

    # pat1_alpha=0
    # pat1_img_x=133
    # pat1_img_y=0
    # pat1_img_width=268
    # pat1_img_height=268

    pat1_alpha, pat1_img_x, pat1_img_y, pat1_img_width, pat1_img_height = 0, 80, 387, 150, 150

    pat2_alpha, pat2_img_x, pat2_img_y, pat2_img_width, pat2_img_height = 0, 265, 390, 240, 145
    pat3_alpha, pat3_img_x, pat3_img_y, pat3_img_width, pat3_img_height = 0, 265, 390, 240, 145
    pat4_alpha, pat4_img_x, pat4_img_y, pat4_img_width, pat4_img_height = 0, 265, 390, 240, 145
    
    pat5_alpha, pat5_img_x, pat5_img_y, pat5_img_width, pat5_img_height = 0, 560, 417, 160, 90
    pat6_alpha, pat6_img_x, pat6_img_y, pat6_img_width, pat6_img_height = 0, 560, 403, 160, 118
    pat7_alpha, pat7_img_x, pat7_img_y, pat7_img_width, pat7_img_height = 0, 560, 401, 160, 123
    pat8_alpha, pat8_img_x, pat8_img_y, pat8_img_width, pat8_img_height = 0, 560, 422, 160, 80
    pat9_alpha, pat9_img_x, pat9_img_y, pat9_img_width, pat9_img_height = 0, 560, 398, 160, 128

    pat10_alpha, pat10_img_x, pat10_img_y, pat10_img_width, pat10_img_height = 0, 782, 404, 219, 120
    pat11_alpha, pat11_img_x, pat11_img_y, pat11_img_width, pat11_img_height = 0, 770, 404, 231, 120
    pat12_alpha, pat12_img_x, pat12_img_y, pat12_img_width, pat12_img_height = 0, 770, 404, 230,120
    pat13_alpha, pat13_img_x, pat13_img_y, pat13_img_width, pat13_img_height = 0, 770, 404, 215, 115
    pat14_alpha, pat14_img_x, pat14_img_y, pat14_img_width, pat14_img_height = 0, 770, 404, 215, 115
    pat15_alpha, pat15_img_x, pat15_img_y, pat15_img_width, pat15_img_height = 0, 776, 404, 230, 95
    pat16_alpha, pat16_img_x, pat16_img_y, pat16_img_width, pat16_img_height = 0, 785, 419, 221, 96

    pat17_alpha, pat17_img_x, pat17_img_y, pat17_img_width, pat17_img_height = 0, 1045, 407, 160, 122

    pat18_alpha, pat18_img_x, pat18_img_y, pat18_img_width, pat18_img_height = 0, 70, 155, 82, 164
    pat19_alpha, pat19_img_x, pat19_img_y, pat19_img_width, pat19_img_height = 0, 1128, 155, 82, 164

    pat20_alpha, pat20_img_x, pat20_img_y, pat20_img_width, pat20_img_height = 0, 585, 260, 110, 285
    pat21_alpha, pat21_img_x, pat21_img_y, pat21_img_width, pat21_img_height = 0, 585, 260, 110, 285
    pat22_alpha, pat22_img_x, pat22_img_y, pat22_img_width, pat22_img_height = 0, 585, 260, 110, 285
    pat23_alpha, pat23_img_x, pat23_img_y, pat23_img_width, pat23_img_height = 0, 585, 260, 110, 285
    pat24_alpha, pat24_img_x, pat24_img_y, pat24_img_width, pat24_img_height = 0, 585, 260, 110, 285
    
    pat25_alpha, pat25_img_x, pat25_img_y, pat25_img_width, pat25_img_height = 0, 585, 175, 183, 370
    
    pat26_alpha, pat26_img_x, pat26_img_y, pat26_img_width, pat26_img_height = 0, 550, 415, 180, 130
    pat27_alpha, pat27_img_x, pat27_img_y, pat27_img_width, pat27_img_height = 0, 580, 315, 126, 91
    pat28_alpha, pat28_img_x, pat28_img_y, pat28_img_width, pat28_img_height = 0, 610, 235, 113, 82
    pat29_alpha, pat29_img_x, pat29_img_y, pat29_img_width, pat29_img_height = 0, 640, 175, 80, 57

    pat30_alpha, pat30_img_x, pat30_img_y, pat30_img_width, pat30_img_height = 0, 560, 232, 160, 50
    pat31_alpha, pat31_img_x, pat31_img_y, pat31_img_width, pat31_img_height = 0, 520, 220, 240, 75
    pat32_alpha, pat32_img_x, pat32_img_y, pat32_img_width, pat32_img_height = 0, 480, 207, 320, 100
    pat33_alpha, pat33_img_x, pat33_img_y, pat33_img_width, pat33_img_height = 0, 440, 195, 400, 125

    pat34_alpha, pat34_img_x, pat34_img_y, pat34_img_width, pat34_img_height = 0, 400, 182, 480, 150
    pat35_alpha, pat35_img_x, pat35_img_y, pat35_img_width, pat35_img_height = 0, 400, 182, 480, 150
    pat36_alpha, pat36_img_x, pat36_img_y, pat36_img_width, pat36_img_height = 0, 400, 182, 480, 150
    pat37_alpha, pat37_img_x, pat37_img_y, pat37_img_width, pat37_img_height = 0, 400, 182, 480, 150
    pat38_alpha, pat38_img_x, pat38_img_y, pat38_img_width, pat38_img_height = 0, 400, 182, 480, 150
    
    pat39_alpha, pat39_img_x, pat39_img_y, pat39_img_width, pat39_img_height = 0, 310, 175, 660, 159
    pat40_alpha, pat40_img_x, pat40_img_y, pat40_img_width, pat40_img_height = 0, 310, 175, 660, 159
    pat41_alpha, pat41_img_x, pat41_img_y, pat41_img_width, pat41_img_height = 0, 310, 175, 660, 159
    pat42_alpha, pat42_img_x, pat42_img_y, pat42_img_width, pat42_img_height = 0, 310, 175, 660, 159
    pat43_alpha, pat43_img_x, pat43_img_y, pat43_img_width, pat43_img_height = 0, 310, 175, 660, 159
    pat44_alpha, pat44_img_x, pat44_img_y, pat44_img_width, pat44_img_height = 0, 310, 175, 660, 159
    pat45_alpha, pat45_img_x, pat45_img_y, pat45_img_width, pat45_img_height = 0, 310, 175, 660, 159


    # text position
    test_txt_x=100
    test_txt_y=435
    test_txt_size=250
    test_txt_R,test_txt_G,test_txt_B,test_txt_A=(255,0,0,255)

    count=0
    while display.IsOpen():
        
        # overlay the image
        jetson.utils.Overlay_all(bg_img, bg_img_width, bg_img_height, 0,0,0,255)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat1_img, pat1_img_x, pat1_img_y, pat1_img_width, pat1_img_height,pat1_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat2_img, pat2_img_x, pat2_img_y, pat2_img_width, pat2_img_height,pat2_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat3_img, pat3_img_x, pat3_img_y, pat3_img_width, pat3_img_height,pat3_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat4_img, pat4_img_x, pat4_img_y, pat4_img_width, pat4_img_height,pat4_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat5_img, pat5_img_x, pat5_img_y, pat5_img_width, pat5_img_height,pat5_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat6_img, pat6_img_x, pat6_img_y, pat6_img_width, pat6_img_height,pat6_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat7_img, pat7_img_x, pat7_img_y, pat7_img_width, pat7_img_height,pat7_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat8_img, pat8_img_x, pat8_img_y, pat8_img_width, pat8_img_height,pat8_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat9_img, pat9_img_x, pat9_img_y, pat9_img_width, pat9_img_height,pat9_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat10_img, pat10_img_x, pat10_img_y, pat10_img_width, pat10_img_height,pat10_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat11_img, pat11_img_x, pat11_img_y, pat11_img_width, pat11_img_height,pat11_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat12_img, pat12_img_x, pat12_img_y, pat12_img_width, pat12_img_height,pat12_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat13_img, pat13_img_x, pat13_img_y, pat13_img_width, pat13_img_height,pat13_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat14_img, pat14_img_x, pat14_img_y, pat14_img_width, pat14_img_height,pat14_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat15_img, pat15_img_x, pat15_img_y, pat15_img_width, pat15_img_height,pat15_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat16_img, pat16_img_x, pat16_img_y, pat16_img_width, pat16_img_height,pat16_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat17_img, pat17_img_x, pat17_img_y, pat17_img_width, pat17_img_height,pat17_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat18_img, pat18_img_x, pat18_img_y, pat18_img_width, pat18_img_height,pat18_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat19_img, pat19_img_x, pat19_img_y, pat19_img_width, pat19_img_height,pat19_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat20_img, pat20_img_x, pat20_img_y, pat20_img_width, pat20_img_height,pat20_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat21_img, pat21_img_x, pat21_img_y, pat21_img_width, pat21_img_height,pat21_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat22_img, pat22_img_x, pat22_img_y, pat22_img_width, pat22_img_height,pat22_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat23_img, pat23_img_x, pat23_img_y, pat23_img_width, pat23_img_height,pat23_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat24_img, pat24_img_x, pat24_img_y, pat24_img_width, pat24_img_height,pat24_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat25_img, pat25_img_x, pat25_img_y, pat25_img_width, pat25_img_height,pat25_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat26_img, pat26_img_x, pat26_img_y, pat26_img_width, pat26_img_height,pat26_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat27_img, pat27_img_x, pat27_img_y, pat27_img_width, pat27_img_height,pat27_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat28_img, pat28_img_x, pat28_img_y, pat28_img_width, pat28_img_height,pat28_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat29_img, pat29_img_x, pat29_img_y, pat29_img_width, pat29_img_height,pat29_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat30_img, pat30_img_x, pat30_img_y, pat30_img_width, pat30_img_height,pat30_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat31_img, pat31_img_x, pat31_img_y, pat31_img_width, pat31_img_height,pat31_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat32_img, pat32_img_x, pat32_img_y, pat32_img_width, pat32_img_height,pat32_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat33_img, pat33_img_x, pat33_img_y, pat33_img_width, pat33_img_height,pat33_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat34_img, pat34_img_x, pat34_img_y, pat34_img_width, pat34_img_height,pat34_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat35_img, pat35_img_x, pat35_img_y, pat35_img_width, pat35_img_height,pat35_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat36_img, pat36_img_x, pat36_img_y, pat36_img_width, pat36_img_height,pat36_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat37_img, pat37_img_x, pat37_img_y, pat37_img_width, pat37_img_height,pat37_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat38_img, pat38_img_x, pat38_img_y, pat38_img_width, pat38_img_height,pat38_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat39_img, pat39_img_x, pat39_img_y, pat39_img_width, pat39_img_height,pat39_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat40_img, pat40_img_x, pat40_img_y, pat40_img_width, pat40_img_height,pat40_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat41_img, pat41_img_x, pat41_img_y, pat41_img_width, pat41_img_height,pat41_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat42_img, pat42_img_x, pat42_img_y, pat42_img_width, pat42_img_height,pat42_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat43_img, pat43_img_x, pat43_img_y, pat43_img_width, pat43_img_height,pat43_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat44_img, pat44_img_x, pat44_img_y, pat44_img_width, pat44_img_height,pat44_alpha)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat45_img, pat45_img_x, pat45_img_y, pat45_img_width, pat45_img_height,pat45_alpha)
        
        
        # condition to change the alpha value 
        
        # if (count//15)%2==0:
        #     pat1_alpha=min(pat1_alpha+17,255)
        # else:
        #     pat1_alpha=max(pat1_alpha-17,0)
        pat1_alpha = 255

        if (count//15)%3==0:
            pat2_alpha=min(pat2_alpha+17,255)
        else:
            pat2_alpha=max(pat2_alpha-17,0)

        if (count//15)%3==1:
            pat3_alpha=min(pat3_alpha+17,255)
        else:
            pat3_alpha=max(pat3_alpha-17,0)

        if (count//15)%3==2:
            pat4_alpha=min(pat4_alpha+17,255)
        else:
            pat4_alpha=max(pat4_alpha-17,0)


        if count < 120:
            if (count//6)%20==0 or (count//6)%20==2:
                pat5_alpha=min(pat5_alpha+47,255)
            else:
                pat5_alpha=max(pat5_alpha-47,0)

            if (count//6)%20==4 or (count//6)%20==6:
                pat6_alpha=min(pat6_alpha+47,255)
            else:
                pat6_alpha=max(pat6_alpha-47,0)

            if (count//6)%20==8 or (count//6)%20==10:
                pat7_alpha=min(pat7_alpha+47,255)
            else:
                pat7_alpha=max(pat7_alpha-47,0)

            if (count//6)%20==12 or (count//6)%20==14:
                pat8_alpha=min(pat8_alpha+47,255)
            else:
                pat8_alpha=max(pat8_alpha-47,0)

            if (count//6)%20==16 or (count//6)%20==18:
                pat9_alpha=min(pat9_alpha+47,255)
            else:
                pat9_alpha=max(pat9_alpha-47,0)


        if(count//15)%7==0 and count < 120:
            pat10_alpha=min(pat10_alpha+17,255)
        else:
            pat10_alpha=max(pat10_alpha-17,0)

        if(count//15)%7==1 or count >= 120:
            pat11_alpha=min(pat11_alpha+17,255)
        else:
            pat11_alpha=max(pat11_alpha-17,0)

        if(count//15)%7==2 and count < 120:
            pat12_alpha=min(pat12_alpha+17,255)
        else:
            pat12_alpha=max(pat12_alpha-17,0)

        if(count//15)%7==3 and count < 120:
            pat13_alpha=min(pat13_alpha+17,255)
        else:
            pat13_alpha=max(pat13_alpha-17,0)

        if(count//15)%7==4 and count < 120:
            pat14_alpha=min(pat14_alpha+17,255)
        else:
            pat14_alpha=max(pat14_alpha-17,0)

        if(count//15)%7==5 and count < 120:
            pat15_alpha=min(pat15_alpha+17,255)
        else:
            pat15_alpha=max(pat15_alpha-17,0)

        if(count//15)%7==6 and count < 120:
            pat16_alpha=min(pat16_alpha+17,255)
        else:
            pat16_alpha=max(pat16_alpha-17,0)

        pat17_alpha = 255

        if (count//15)%2==0:
            pat18_alpha=min(pat18_alpha+17,255)
        else:
            pat18_alpha=max(pat18_alpha-17,0)

        if (count//15)%2==0:
            pat19_alpha=min(pat19_alpha+17,255)
        else:
            pat19_alpha=max(pat19_alpha-17,0)

        # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat20_img, pat20_img_x, pat20_img_y, pat20_img_width, pat20_img_height,pat20_alpha)
        # if (count//15)%5==0:
        #     pat20_alpha=min(pat20_alpha+17,255)
        # else:
        #     pat20_alpha=max(pat20_alpha-17,0)

        if count > 120 and count < 240:
            if (count//7)%4==0:
                pat21_alpha=min(pat21_alpha+36,255)
            else:
                pat21_alpha=max(pat21_alpha-36,50)

            if (count//7)%4==1:
                pat22_alpha=min(pat22_alpha+36,255)
            else:
                pat22_alpha=max(pat22_alpha-36,50)

            if (count//7)%4==2:
                pat23_alpha=min(pat23_alpha+36,255)
            else:
                pat23_alpha=max(pat23_alpha-36,50)

            if (count//7)%4==3:
                pat24_alpha=min(pat24_alpha+36,255)
            else:
                pat24_alpha=max(pat24_alpha-36,50)

        if count > 180 and count < 240:
            if (count//15)%2==0:
                pat25_alpha=min(pat25_alpha+17,255)
            else:
                pat25_alpha=max(pat25_alpha-17,0)

        if count > 240 and count < 280:
            if count > 240 and count < 250:
                pat26_alpha=255
            else:
                pat26_alpha=max(pat26_alpha-15,0)

            if count >= 250 and count < 260:
                pat27_alpha=255
            else:
                pat27_alpha=max(pat27_alpha-15,0)

            if count >= 260 and count < 270:
                pat28_alpha=255
            else:
                pat28_alpha=max(pat28_alpha-15,0)

            if count >= 270 and count < 280:
                pat29_alpha=255
            else:
                pat29_alpha=max(pat29_alpha-15,0)
        
        if count > 280 and count < 380:
            if count > 280 and count < 290:
                pat30_alpha=255
            else:
                pat30_alpha=max(pat30_alpha-30,0)

            if count > 290 and count < 300:
                pat31_alpha=255
            else:
                pat31_alpha=max(pat31_alpha-30,0)

            if count > 300 and count < 310:
                pat32_alpha=255
            else:
                pat32_alpha=max(pat32_alpha-30,0)

            if count > 310 and count < 320:
                pat33_alpha=255
            else:
                pat33_alpha=max(pat33_alpha-30,0)

            if count > 320 and count < 330:
                pat34_alpha=255
            else:
                pat34_alpha=max(pat34_alpha-30,0)

            if count > 330 and count < 340:
                pat35_alpha=255
            else:
                pat35_alpha=max(pat35_alpha-15,0)

            if count > 340 and count < 350:
                pat35_alpha=255
            else:
                pat35_alpha=max(pat35_alpha-15,0)

            if count > 350 and count < 360:
                pat36_alpha=255
            else:
                pat36_alpha=max(pat36_alpha-15,0)

            if count > 360 and count < 370:
                pat37_alpha=255
            else:
                pat37_alpha=max(pat37_alpha-15,0)

            if count > 370 and count < 380:
                pat38_alpha=255
            else:
                pat38_alpha=max(pat38_alpha-15,0)  



        if count < 120:
            pat39_alpha=255

            if count < 40:
                pat40_alpha=255

                if (count//15)%2==0:
                    pat41_alpha=min(pat41_alpha+17,255)
                else:
                    pat41_alpha=max(pat41_alpha-17,0)
            if count > 40 and count < 120:
                if (count//7)%4==0:
                    pat42_alpha=min(pat42_alpha+36,255)
                else:
                    pat42_alpha=max(pat42_alpha-36,0)

                if (count//7)%4==1:
                    pat43_alpha=min(pat43_alpha+36,255)
                else:
                    pat43_alpha=max(pat43_alpha-36,0)

                if (count//7)%4==2:
                    pat44_alpha=min(pat44_alpha+36,255)
                else:
                    pat44_alpha=max(pat44_alpha-36,0)

                if (count//7)%4==3:
                    pat45_alpha=min(pat45_alpha+36,255)
                else:
                    pat45_alpha=max(pat45_alpha-36,0)


        # print(count)

        # if (count//150)%2==0:
        #     jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, "60", test_txt_x,test_txt_y,test_txt_size,test_txt_R,test_txt_G,test_txt_B,test_txt_A)
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

        a3_number=100-(count//5)
        if a3_number >= 100:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number), test_txt_x+740,test_txt_y+40,80,0,255,255,255)
        else:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(a3_number)+'m', test_txt_x+758,test_txt_y+40,80,0,255,255,255)
    
        display.RenderOnce(bg_img, bg_img_width, bg_img_height,img_start_x,img_start_y)

        count=count+1
        
        # time.sleep(0.03)
        time.sleep(0.05)

