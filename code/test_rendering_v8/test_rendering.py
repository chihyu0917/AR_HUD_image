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
    display = jetson.utils.glDisplay(1920,1080,width,height,if_no_title,if_transparent_window)
    img_start_x=0
    img_start_y=0

    bg_img,bg_img_width,bg_img_height=jetson.utils.loadImageRGBA("background.png")
    pat1_img,pat1_img_width,pat1_img_height=jetson.utils.loadImageRGBA("logo.png")
    pat2_img,pat2_img_width,pat2_img_height=jetson.utils.loadImageRGBA("black_transparent_pic.png")

    pat1_alpha=0
    pat1_img_x=133
    pat1_img_y=0
    pat1_img_width=268
    pat1_img_height=268
    
    test_txt_x=330
    test_txt_y=480
    test_txt_size=150
    test_txt_R,test_txt_G,test_txt_B,test_txt_A=(255,0,0,255)

    count=0
    while display.IsOpen():
        jetson.utils.Overlay_all(bg_img, bg_img_width, bg_img_height, 0,0,0,255)
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat1_img, pat1_img_x, pat1_img_y, pat1_img_width, pat1_img_height,pat1_alpha)
        if (count//15)%2==0:
            pat1_alpha=min(pat1_alpha+17,255)
        else:
            pat1_alpha=max(pat1_alpha-17,0)

        if (count//150)%2==0:
            jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, "60", test_txt_x,test_txt_y,test_txt_size,test_txt_R,test_txt_G,test_txt_B,test_txt_A)
        test_number=80-(count//30)
        jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(test_number), test_txt_x+200,test_txt_y,250,0,255,255,255)
        
        jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat1_img, 500, pat1_img_y, pat1_img_width, pat1_img_height,255)
        jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, pat2_img, 500, pat1_img_y, pat2_img_width, pat2_img_height)
        
        display.RenderOnce(bg_img, bg_img_width, bg_img_height,img_start_x,img_start_y)

        count=count+1
        
        time.sleep(0.03)

