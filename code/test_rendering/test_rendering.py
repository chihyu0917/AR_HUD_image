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

    # image position

    # pat1_alpha=0
    # pat1_img_x=133
    # pat1_img_y=0
    # pat1_img_width=268
    # pat1_img_height=268

    pat1_alpha=0
    pat1_img_x=80
    pat1_img_y=387
    pat1_img_width=150
    pat1_img_height=150

    pat2_alpha=0
    pat2_img_x=265
    pat2_img_y=387
    pat2_img_width=240
    pat2_img_height=145

    pat3_alpha=0
    pat3_img_x=265
    pat3_img_y=387
    pat3_img_width=240
    pat3_img_height=145

    pat4_alpha=0
    pat4_img_x=265
    pat4_img_y=387
    pat4_img_width=240
    pat4_img_height=145
    
    test_txt_x=330
    test_txt_y=480
    test_txt_size=150
    test_txt_R,test_txt_G,test_txt_B,test_txt_A=(255,0,0,255)

    pat5_alpha=0
    pat5_img_x=571
    pat5_img_y=422
    pat5_img_width=160
    pat5_img_height=90

    pat6_alpha=0
    pat6_img_x=571
    pat6_img_y=407
    pat6_img_width=160
    pat6_img_height=118

    pat7_alpha=0
    pat7_img_x=571
    pat7_img_y=407
    pat7_img_width=160
    pat7_img_height=123

    pat8_alpha=0
    pat8_img_x=571
    pat8_img_y=422
    pat8_img_width=160
    pat8_img_height=80

    pat9_alpha=0
    pat9_img_x=571
    pat9_img_y=407
    pat9_img_width=160
    pat9_img_height=128

    pat10_alpha=0
    pat10_img_x=785
    pat10_img_y=407
    pat10_img_width=219
    pat10_img_height=120

    pat11_alpha=0
    pat11_img_x=780
    pat11_img_y=407
    pat11_img_width=231
    pat11_img_height=120

    pat12_alpha=0
    pat12_img_x=780
    pat12_img_y=407
    pat12_img_width=230
    pat12_img_height=120

    pat13_alpha=0
    pat13_img_x=787
    pat13_img_y=409
    pat13_img_width=215
    pat13_img_height=115

    pat14_alpha=0
    pat14_img_x=787
    pat14_img_y=409
    pat14_img_width=215
    pat14_img_height=115

    pat15_alpha=0
    pat15_img_x=780
    pat15_img_y=419
    pat15_img_width=230
    pat15_img_height=95

    pat16_alpha=0
    pat16_img_x=785
    pat16_img_y=419
    pat16_img_width=221
    pat16_img_height=96

    pat17_alpha=0
    pat17_img_x=1045
    pat17_img_y=407
    pat17_img_width=160
    pat17_img_height=122

    pat18_alpha=0
    pat18_img_x=70
    pat18_img_y=155
    pat18_img_width=82
    pat18_img_height=164

    pat19_alpha=0
    pat19_img_x=1128
    pat19_img_y=155
    pat19_img_width=82
    pat19_img_height=164

    pat20_alpha=0
    pat20_img_x=585
    pat20_img_y=175
    pat20_img_width=110
    pat20_img_height=285

    pat21_alpha=0
    pat21_img_x=585
    pat21_img_y=175
    pat21_img_width=110
    pat21_img_height=285

    pat22_alpha=0
    pat22_img_x=585
    pat22_img_y=175
    pat22_img_width=110
    pat22_img_height=285

    pat23_alpha=0
    pat23_img_x=585
    pat23_img_y=175
    pat23_img_width=110
    pat23_img_height=285

    pat24_alpha=0
    pat24_img_x=585
    pat24_img_y=175
    pat24_img_width=110
    pat24_img_height=285

    count=0
    while display.IsOpen():
        jetson.utils.Overlay_all(bg_img, bg_img_width, bg_img_height, 0,0,0,255)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat1_img, pat1_img_x, pat1_img_y, pat1_img_width, pat1_img_height,pat1_alpha)
        # if (count//15)%2==0:
        #     pat1_alpha=min(pat1_alpha+17,255)
        # else:
        #     pat1_alpha=max(pat1_alpha-17,0)
        pat1_alpha = 255

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat2_img, pat2_img_x, pat2_img_y, pat2_img_width, pat2_img_height,pat2_alpha)
        if (count//15)%3==0:
            pat2_alpha=min(pat2_alpha+17,255)
        else:
            pat2_alpha=max(pat2_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat3_img, pat3_img_x, pat3_img_y, pat3_img_width, pat3_img_height,pat3_alpha)
        if (count//15)%3==1:
            pat3_alpha=min(pat3_alpha+17,255)
        else:
            pat3_alpha=max(pat3_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat4_img, pat4_img_x, pat4_img_y, pat4_img_width, pat4_img_height,pat4_alpha)
        if (count//15)%3==2:
            pat4_alpha=min(pat4_alpha+17,255)
        else:
            pat4_alpha=max(pat4_alpha-17,0)


        if count < 120:
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat5_img, pat5_img_x, pat5_img_y, pat5_img_width, pat5_img_height,pat5_alpha)
            if (count//6)%20==0 or (count//6)%20==2:
                pat5_alpha=min(pat5_alpha+47,255)
            else:
                pat5_alpha=max(pat5_alpha-47,0)

            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat6_img, pat6_img_x, pat6_img_y, pat6_img_width, pat6_img_height,pat6_alpha)
            if (count//6)%20==4 or (count//6)%20==6:
                pat6_alpha=min(pat6_alpha+47,255)
            else:
                pat6_alpha=max(pat6_alpha-47,0)

            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat7_img, pat7_img_x, pat7_img_y, pat7_img_width, pat7_img_height,pat7_alpha)
            if (count//6)%20==8 or (count//6)%20==10:
                pat7_alpha=min(pat7_alpha+47,255)
            else:
                pat7_alpha=max(pat7_alpha-47,0)

            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat8_img, pat8_img_x, pat8_img_y, pat8_img_width, pat8_img_height,pat8_alpha)
            if (count//6)%20==12 or (count//6)%20==14:
                pat8_alpha=min(pat8_alpha+47,255)
            else:
                pat8_alpha=max(pat8_alpha-47,0)

            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat9_img, pat9_img_x, pat9_img_y, pat9_img_width, pat9_img_height,pat9_alpha)
            if (count//6)%20==16 or (count//6)%20==18:
                pat9_alpha=min(pat9_alpha+47,255)
            else:
                pat9_alpha=max(pat9_alpha-47,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat10_img, pat10_img_x, pat10_img_y, pat10_img_width, pat10_img_height,pat10_alpha)
        if(count//15)%7==0:
            pat10_alpha=min(pat10_alpha+17,255)
        else:
            pat10_alpha=max(pat10_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat11_img, pat11_img_x, pat11_img_y, pat11_img_width, pat11_img_height,pat11_alpha)
        if(count//15)%7==1:
            pat11_alpha=min(pat11_alpha+17,255)
        else:
            pat11_alpha=max(pat11_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat12_img, pat12_img_x, pat12_img_y, pat12_img_width, pat12_img_height,pat12_alpha)
        if(count//15)%7==2:
            pat12_alpha=min(pat12_alpha+17,255)
        else:
            pat12_alpha=max(pat12_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat13_img, pat13_img_x, pat13_img_y, pat13_img_width, pat13_img_height,pat13_alpha)
        if(count//15)%7==3:
            pat13_alpha=min(pat13_alpha+17,255)
        else:
            pat13_alpha=max(pat13_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat14_img, pat14_img_x, pat14_img_y, pat14_img_width, pat14_img_height,pat14_alpha)
        if(count//15)%7==4:
            pat14_alpha=min(pat14_alpha+17,255)
        else:
            pat14_alpha=max(pat14_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat15_img, pat15_img_x, pat15_img_y, pat15_img_width, pat15_img_height,pat15_alpha)
        if(count//15)%7==5:
            pat15_alpha=min(pat15_alpha+17,255)
        else:
            pat15_alpha=max(pat15_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat16_img, pat16_img_x, pat16_img_y, pat16_img_width, pat16_img_height,pat16_alpha)
        if(count//15)%7==6:
            pat16_alpha=min(pat16_alpha+17,255)
        else:
            pat16_alpha=max(pat16_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat17_img, pat17_img_x, pat17_img_y, pat17_img_width, pat17_img_height,pat17_alpha)
        pat17_alpha = 255

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat18_img, pat18_img_x, pat18_img_y, pat18_img_width, pat18_img_height,pat18_alpha)
        if (count//15)%2==0:
            pat18_alpha=min(pat18_alpha+17,255)
        else:
            pat18_alpha=max(pat18_alpha-17,0)

        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat19_img, pat19_img_x, pat19_img_y, pat19_img_width, pat19_img_height,pat19_alpha)
        if (count//15)%2==0:
            pat19_alpha=min(pat19_alpha+17,255)
        else:
            pat19_alpha=max(pat19_alpha-17,0)

        # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat20_img, pat20_img_x, pat20_img_y, pat20_img_width, pat20_img_height,pat20_alpha)
        # if (count//15)%5==0:
        #     pat20_alpha=min(pat20_alpha+17,255)
        # else:
        #     pat20_alpha=max(pat20_alpha-17,0)

        if count > 120:
            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat21_img, pat21_img_x, pat21_img_y, pat21_img_width, pat21_img_height,pat21_alpha)
            if (count//7)%4==0:
                pat21_alpha=min(pat21_alpha+36,255)
            else:
                pat21_alpha=max(pat21_alpha-36,50)

            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat22_img, pat22_img_x, pat22_img_y, pat22_img_width, pat22_img_height,pat22_alpha)
            if (count//7)%4==1:
                pat22_alpha=min(pat22_alpha+36,255)
            else:
                pat22_alpha=max(pat22_alpha-36,50)

            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat23_img, pat23_img_x, pat23_img_y, pat23_img_width, pat23_img_height,pat23_alpha)
            if (count//7)%4==2:
                pat23_alpha=min(pat23_alpha+36,255)
            else:
                pat23_alpha=max(pat23_alpha-36,50)

            jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat24_img, pat24_img_x, pat24_img_y, pat24_img_width, pat24_img_height,pat24_alpha)
            if (count//7)%4==3:
                pat24_alpha=min(pat24_alpha+36,255)
            else:
                pat24_alpha=max(pat24_alpha-36,50)

        # print(count)


        # if (count//150)%2==0:
        #     jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, "60", test_txt_x,test_txt_y,test_txt_size,test_txt_R,test_txt_G,test_txt_B,test_txt_A)
        # test_number=80-(count//30)
        # jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(test_number), test_txt_x+200,test_txt_y,250,0,255,255,255)
        display.RenderOnce(bg_img, bg_img_width, bg_img_height,img_start_x,img_start_y)

        count=count+1
        
        # time.sleep(0.03)
        time.sleep(0.05)

