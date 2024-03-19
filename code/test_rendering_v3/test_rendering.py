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
            'A1': './png/W_A1_SL.png', # A1
            'A2_B': './png/W_A2_R_B.png', 'A2_L': './png/W_A2_R_L.png', 'A2_R': './png/W_A2_R_R.png', # A2
            'A3_SF': './png/W_A3_SF.png', 'A3_BL': './png/W_A3_BL.png', 'A3_MH': './png/W_A3_MH.png', 'A3_MS': './png/W_A3_MS.png', 'A3_BF': './png/W_A3_BF.png', # A3
            'A4_S': './png/N_A4_S.png', 'A4_TR': './png/N_A4_TR.png', 'A4_TL': './png/N_A4_TL.png', 'A4_KR': './png/N_A4_KR.png', 
            'A4_KL': './png/N_A4_KL.png', 'A4_TA': './png/N_A4_TA.png', 'A4_D': './png/N_A4_D.png', # A4
            'A5': './png/W_A5_A.png', # A5
            'B5': './png/A_B5_LBIN.png', 'B6': './png/A_B6_RBIN.png', # B5, B6
            'B1_S': './png/N_B1_S.png', 'B1_S_1': './png/N_B1_S_1.png', 'B1_S_2': './png/N_B1_S_2.png', 'B1_S_3': './png/N_B1_S_3.png', 'B1_S_4': './png/N_B1_S_4.png', # B1
            'B1_FTR': './png/N_B1_FTR.png', 'B1_NTR_2': './png/N_B1_NTR_2.png', 'B1_NTR_4': './png/N_B1_NTR_4.png', 'B1_NTR_3': './png/N_B1_NTR_3.png', 'B1_NTR_1': './png/N_B1_NTR_1.png',
            'B2_TRI_1': './png/N_B2_TRI_1.png', 'B2_TRI_2_d': './png/N_B2_TRI_2_d.png', 'B2_TRI_2_a': './png/N_B2_TRI_2_a.png', 'B2_TRI_2_e': './png/N_B2_TRI_2_e.png', # B2
            'B2_TRI_2_b': './png/N_B2_TRI_2_b.png', 'B2_TRI_2_f': './png/N_B2_TRI_2_f.png', 'B2_TRI_2_c': './png/N_B2_TRI_2_c.png', 'B2_TRI_2_g': './png/N_B2_TRI_2_g.png', 'B2_TRI_2': './png/N_B2_TRI_2.png', 
            'B2_TRI_3_a': './png/N_B2_TRI_3_a.png', 'B2_TRI_3_b': './png/N_B2_TRI_3_b.png', 'B2_TRI_3_c': './png/N_B2_TRI_3_c.png', 'B2_TRI_3_d': './png/N_B2_TRI_3_d.png',
            'B3_FCW_B': './png/A_B3_FCW_B.png', 'B3_FCW_BA': './png/A_B3_FCW_BA.png', 'B3_FCW_R': './png/A_B3_FCW_R.png', 'B3_PDW_1': './png/A_B3_PDW_1.png', # B3
            'B3_PDW_2': './png/A_B3_PDW_2.png', 'B3_PDW_3': './png/A_B3_PDW_3.png', 'B3_PDW_4': './png/A_B3_PDW_4.png',
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
    
    B1_NTR_2 = attributes(images['B1_NTR_2'][0], images['B1_NTR_2'][1], images['B1_NTR_2'][2], 0, 550, 415)
    B1_NTR_4 = attributes(images['B1_NTR_4'][0], images['B1_NTR_4'][1], images['B1_NTR_4'][2], 0, 580, 315)
    B1_NTR_3 = attributes(images['B1_NTR_3'][0], images['B1_NTR_3'][1], images['B1_NTR_3'][2], 0, 610, 235)
    B1_NTR_1 = attributes(images['B1_NTR_1'][0], images['B1_NTR_1'][1], images['B1_NTR_1'][2], 0, 640, 175)
    
    B2_TRI_1 = attributes(images['B2_TRI_1'][0], images['B2_TRI_1'][1], images['B2_TRI_1'][2], 0, 560, 232)
    B2_TRI_2_d = attributes(images['B2_TRI_2_d'][0], images['B2_TRI_2_d'][1], images['B2_TRI_2_d'][2], 0, 540, 226)
    B2_TRI_2_a = attributes(images['B2_TRI_2_a'][0], images['B2_TRI_2_a'][1], images['B2_TRI_2_a'][2], 0, 520, 220)
    B2_TRI_2_e = attributes(images['B2_TRI_2_e'][0], images['B2_TRI_2_e'][1], images['B2_TRI_2_e'][2], 0, 500, 214)
    B2_TRI_2_b = attributes(images['B2_TRI_2_b'][0], images['B2_TRI_2_b'][1], images['B2_TRI_2_b'][2], 0, 480, 207)
    B2_TRI_2_f = attributes(images['B2_TRI_2_f'][0], images['B2_TRI_2_f'][1], images['B2_TRI_2_f'][2], 0, 460, 201)
    B2_TRI_2_c = attributes(images['B2_TRI_2_c'][0], images['B2_TRI_2_c'][1], images['B2_TRI_2_c'][2], 0, 440, 195)
    B2_TRI_2_g = attributes(images['B2_TRI_2_g'][0], images['B2_TRI_2_g'][1], images['B2_TRI_2_g'][2], 0, 420, 189)
    
    B2_TRI_2 = attributes(images['B2_TRI_2'][0], images['B2_TRI_2'][1], images['B2_TRI_2'][2], 0, 400, 182)
    B2_TRI_3_a = attributes(images['B2_TRI_3_a'][0], images['B2_TRI_3_a'][1], images['B2_TRI_3_a'][2], 0, 400, 182)
    B2_TRI_3_b = attributes(images['B2_TRI_3_b'][0], images['B2_TRI_3_b'][1], images['B2_TRI_3_b'][2], 0, 400, 182)
    B2_TRI_3_c = attributes(images['B2_TRI_3_c'][0], images['B2_TRI_3_c'][1], images['B2_TRI_3_c'][2], 0, 400, 182)
    B2_TRI_3_d = attributes(images['B2_TRI_3_d'][0], images['B2_TRI_3_d'][1], images['B2_TRI_3_d'][2], 0, 400, 182)
    
    B3_FCW_B = attributes(images['B3_FCW_B'][0], images['B3_FCW_B'][1], images['B3_FCW_B'][2], 0, 310, 175)
    B3_FCW_BA = attributes(images['B3_FCW_BA'][0], images['B3_FCW_BA'][1], images['B3_FCW_BA'][2], 0, 310, 175)
    B3_FCW_R = attributes(images['B3_FCW_R'][0], images['B3_FCW_R'][1], images['B3_FCW_R'][2], 0, 310, 175)
    B3_PDW_1 = attributes(images['B3_PDW_1'][0], images['B3_PDW_1'][1], images['B3_PDW_1'][2], 0, 310, 175)
    B3_PDW_2 = attributes(images['B3_PDW_2'][0], images['B3_PDW_2'][1], images['B3_PDW_2'][2], 0, 310, 175)
    B3_PDW_3 = attributes(images['B3_PDW_3'][0], images['B3_PDW_3'][1], images['B3_PDW_3'][2], 0, 310, 175)
    B3_PDW_4 = attributes(images['B3_PDW_4'][0], images['B3_PDW_4'][1], images['B3_PDW_4'][2], 0, 310, 175)
    
    B4_R_B = attributes(images['B4_R_B'][0], images['B4_R_B'][1], images['B4_R_B'][2], 0, 311, 161)
    B4_R_R = attributes(images['B4_R_R'][0], images['B4_R_R'][1], images['B4_R_R'][2], 0, 311, 161)
    B4_BL = attributes(images['B4_BL'][0], images['B4_BL'][1], images['B4_BL'][2], 0, 650, 161)
    B4_L_B = attributes(images['B4_L_B'][0], images['B4_L_B'][1], images['B4_L_B'][2], 0, 311, 161)
    B4_L_R = attributes(images['B4_L_R'][0], images['B4_L_R'][1], images['B4_L_R'][2], 0, 311, 161)

    bg_img,bg_img_width,bg_img_height=jetson.utils.loadImageRGBA("background.png")
    # pat1_img,pat1_img_width,pat1_img_height=jetson.utils.loadImageRGBA("logo.png")
    # pat2_img,pat2_img_width,pat2_img_height=jetson.utils.loadImageRGBA("black_transparent_pic.png")

    # pat1_alpha=0
    # pat1_img_x=133
    # pat1_img_y=0
    # pat1_img_width=268
    # pat1_img_height=268
    
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
            A1.alpha = renderPattern(A1.img, A1.img_x, A1.img_y, A1.img_width, A1.img_height, A1.alpha, 255, 255, 1, 255, 1, 0, count)
        # if (count//15)%2==0:
        #     pat1_alpha=min(pat1_alpha+17,255)
        # else:
        #     pat1_alpha=max(pat1_alpha-17,0)

        # A2
        if count < 120:
            A2_B.alpha = renderPattern(A2_B.img, A2_B.img_x, A2_B.img_y, A2_B.img_width, A2_B.img_height, A2_B.alpha, 0, 255, 10, 25, 2, 0, count) # 1 Hz
        if count > 120 and count < 240:
            A2_L.alpha = renderPattern(A2_L.img, A2_L.img_x, A2_L.img_y, A2_L.img_width, A2_L.img_height, A2_L.alpha, 0, 255, 10, 25, 2, 0, count)
        if count > 240 and count < 360:
            A2_R.alpha = renderPattern(A2_R.img, A2_R.img_x, A2_R.img_y, A2_R.img_width, A2_R.img_height, A2_R.alpha, 0, 255, 10, 25, 2, 0, count)

        # A3
        if count < 120:
            if count < 24:
                A3_SF.alpha = renderPattern(A3_SF.img, A3_SF.img_x, A3_SF.img_y, A3_SF.img_width, A3_SF.img_height, A3_SF.alpha, 0, 255, 10, 25, 2, 0, count)
            if count > 24 and count < 48:
                A3_BL.alpha = renderPattern(A3_BL.img, A3_BL.img_x, A3_BL.img_y, A3_BL.img_width, A3_BL.img_height, A3_BL.alpha, 0, 255, 10, 25, 2, 0, count)
            if count > 48 and count < 72:
                A3_MH.alpha = renderPattern(A3_MH.img, A3_MH.img_x, A3_MH.img_y, A3_MH.img_width, A3_MH.img_height, A3_MH.alpha, 0, 255, 10, 25, 2, 0, count)
            if count > 72 and count < 96:
                A3_MS.alpha = renderPattern(A3_MS.img, A3_MS.img_x, A3_MS.img_y, A3_MS.img_width, A3_MS.img_height, A3_MS.alpha, 0, 255, 10, 25, 2, 0, count)
            if count > 96 and count < 120:
                A3_BF.alpha = renderPattern(A3_BF.img, A3_BF.img_x, A3_BF.img_y, A3_BF.img_width, A3_BF.img_height, A3_BF.alpha, 0, 255, 10, 25, 2, 0, count)

        # A4
        if count < 120:
            if count < 20:
                A4_S.alpha = renderPattern(A4_S.img, A4_S.img_x, A4_S.img_y, A4_S.img_width, A4_S.img_height, A4_S.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 20 and count < 40:
                A4_TL.alpha = renderPattern(A4_TL.img, A4_TL.img_x, A4_TL.img_y, A4_TL.img_width, A4_TL.img_height, A4_TL.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 40 and count < 60:
                A4_KR.alpha = renderPattern(A4_KR.img, A4_KR.img_x, A4_KR.img_y, A4_KR.img_width, A4_KR.img_height, A4_KR.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 60 and count < 80:
                A4_KL.alpha = renderPattern(A4_KL.img, A4_KL.img_x, A4_KL.img_y, A4_KL.img_width, A4_KL.img_height, A4_KL.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 80 and count < 100:
                A4_TA.alpha = renderPattern(A4_TA.img, A4_TA.img_x, A4_TA.img_y, A4_TA.img_width, A4_TA.img_height, A4_TA.alpha, 255, 255, 1, 255, 1, 0, count)
            if count > 100 and count < 120:
                A4_D.alpha = renderPattern(A4_D.img, A4_D.img_x, A4_D.img_y, A4_D.img_width, A4_D.img_height, A4_D.alpha, 255, 255, 1, 255, 1, 0, count)

        if count > 120 and count < 460:
            A4_TR.alpha = renderPattern(A4_TR.img, A4_TR.img_x, A4_TR.img_y, A4_TR.img_width, A4_TR.img_height, A4_TR.alpha, 255, 255, 1, 255, 1, 0, count)

        # A5
        if count < 460:
            A5.alpha = renderPattern(A5.img, A5.img_x, A5.img_y, A5.img_width, A5.img_height, A5.alpha, 255, 255, 1, 255, 1, 0, count)

        # B5
        if count < 120:
            B5.alpha = renderPattern(B5.img, B5.img_x, B5.img_y, B5.img_width, B5.img_height,B5.alpha, 0, 255, 15, 17, 2, 0, count)

        # B6
        if count > 120:
            B6.alpha = renderPattern(B6.img, B6.img_x, B6.img_y, B6.img_width, B6.img_height,B6.alpha, 0, 255, 15, 17, 2, 0, count)

        # B1
        if count > 120 and count < 240:
            B1_S_1.alpha = renderPattern(B1_S_1.img, B1_S_1.img_x, B1_S_1.img_y, B1_S_1.img_width, B1_S_1.img_height,B1_S_1.alpha, 50, 255, 7, 36, 4, 0, count) 
            B1_S_2.alpha = renderPattern(B1_S_2.img, B1_S_2.img_x, B1_S_2.img_y, B1_S_2.img_width, B1_S_2.img_height,B1_S_2.alpha, 50, 255, 7, 36, 4, 1, count)
            B1_S_3.alpha = renderPattern(B1_S_3.img, B1_S_3.img_x, B1_S_3.img_y, B1_S_3.img_width, B1_S_3.img_height,B1_S_3.alpha, 50, 255, 7, 36, 4, 2, count)
            B1_S_4.alpha = renderPattern(B1_S_4.img, B1_S_4.img_x, B1_S_4.img_y, B1_S_4.img_width, B1_S_4.img_height,B1_S_4.alpha, 50, 255, 7, 36, 4, 3, count)

        if count > 180 and count < 240:
            B1_FTR.alpha = renderPattern(B1_FTR.img, B1_FTR.img_x, B1_FTR.img_y, B1_FTR.img_width, B1_FTR.img_height,B1_FTR.alpha, 0, 255, 7, 36, 4, 3, count)

        
        if count > 240 and count < 280:
            if count > 240 and count < 250:
                B1_NTR_2.alpha = renderPattern(B1_NTR_2.img, B1_NTR_2.img_x, B1_NTR_2.img_y, B1_NTR_2.img_width, B1_NTR_2.img_height, B1_NTR_2.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 250 and count < 260:
                B1_NTR_2.alpha = renderPattern(B1_NTR_2.img, B1_NTR_2.img_x, B1_NTR_2.img_y, B1_NTR_2.img_width, B1_NTR_2.img_height, B1_NTR_2.alpha, 0, 255, 15, 17, 2, 50, count)
                B1_NTR_4.alpha = renderPattern(B1_NTR_4.img, B1_NTR_4.img_x, B1_NTR_4.img_y, B1_NTR_4.img_width, B1_NTR_4.img_height, B1_NTR_4.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 260 and count < 270:
                B1_NTR_2.alpha = renderPattern(B1_NTR_2.img, B1_NTR_2.img_x, B1_NTR_2.img_y, B1_NTR_2.img_width, B1_NTR_2.img_height, B1_NTR_2.alpha, 0, 255, 15, 17, 2, 50, count)
                B1_NTR_4.alpha = renderPattern(B1_NTR_4.img, B1_NTR_4.img_x, B1_NTR_4.img_y, B1_NTR_4.img_width, B1_NTR_4.img_height, B1_NTR_4.alpha, 0, 255, 15, 17, 2, 50, count)
                B1_NTR_3.alpha = renderPattern(B1_NTR_3.img, B1_NTR_3.img_x, B1_NTR_3.img_y, B1_NTR_3.img_width, B1_NTR_3.img_height, B1_NTR_3.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 270 and count < 275:
                B1_NTR_4.alpha = renderPattern(B1_NTR_4.img, B1_NTR_4.img_x, B1_NTR_4.img_y, B1_NTR_4.img_width, B1_NTR_4.img_height, B1_NTR_4.alpha, 0, 255, 15, 17, 2, 50, count)
                B1_NTR_3.alpha = renderPattern(B1_NTR_3.img, B1_NTR_3.img_x, B1_NTR_3.img_y, B1_NTR_3.img_width, B1_NTR_3.img_height, B1_NTR_3.alpha, 0, 255, 15, 17, 2, 50, count)
                B1_NTR_1.alpha = renderPattern(B1_NTR_1.img, B1_NTR_1.img_x, B1_NTR_1.img_y, B1_NTR_1.img_width, B1_NTR_1.img_height, B1_NTR_1.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 275 and count < 280:
                B1_NTR_1.alpha = renderPattern(B1_NTR_1.img, B1_NTR_1.img_x, B1_NTR_1.img_y, B1_NTR_1.img_width, B1_NTR_1.img_height, B1_NTR_1.alpha, 0, 255, 15, 17, 2, 50, count)
        
        # B2    
        if count > 280 and count < 380:
            if count > 280 and count < 285:
                B2_TRI_1.alpha = renderPattern(B2_TRI_1.img, B2_TRI_1.img_x, B2_TRI_1.img_y, B2_TRI_1.img_width, B2_TRI_1.img_height, B2_TRI_1.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 285 and count < 280:
                B2_TRI_2_d.alpha = renderPattern(B2_TRI_2_d.img, B2_TRI_2_d.img_x, B2_TRI_2_d.img_y, B2_TRI_2_d.img_width, B2_TRI_2_d.img_height, B2_TRI_2_d.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 290 and count < 295:
                B2_TRI_2_a.alpha = renderPattern(B2_TRI_2_a.img, B2_TRI_2_a.img_x, B2_TRI_2_a.img_y, B2_TRI_2_a.img_width, B2_TRI_2_a.img_height, B2_TRI_2_a.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 295 and count < 300:
                B2_TRI_2_e.alpha = renderPattern(B2_TRI_2_e.img, B2_TRI_2_e.img_x, B2_TRI_2_e.img_y, B2_TRI_2_e.img_width, B2_TRI_2_e.img_height, B2_TRI_2_e.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 300 and count < 305:
                B2_TRI_2_b.alpha = renderPattern(B2_TRI_2_b.img, B2_TRI_2_b.img_x, B2_TRI_2_b.img_y, B2_TRI_2_b.img_width, B2_TRI_2_b.img_height, B2_TRI_2_b.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 305 and count < 310:
                B2_TRI_2_f.alpha = renderPattern(B2_TRI_2_f.img, B2_TRI_2_f.img_x, B2_TRI_2_f.img_y, B2_TRI_2_f.img_width, B2_TRI_2_f.img_height, B2_TRI_2_f.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 310 and count < 315:
                B2_TRI_2_c.alpha = renderPattern(B2_TRI_2_c.img, B2_TRI_2_c.img_x, B2_TRI_2_c.img_y, B2_TRI_2_c.img_width, B2_TRI_2_c.img_height, B2_TRI_2_c.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 315 and count < 320:
                B2_TRI_2_g.alpha = renderPattern(B2_TRI_2_g.img, B2_TRI_2_g.img_x, B2_TRI_2_g.img_y, B2_TRI_2_g.img_width, B2_TRI_2_g.img_height, B2_TRI_2_g.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 320 and count < 330:
                B2_TRI_2.alpha = renderPattern(B2_TRI_2.img, B2_TRI_2.img_x, B2_TRI_2.img_y, B2_TRI_2.img_width, B2_TRI_2.img_height, B2_TRI_2.alpha, 255, 255, 1, 255, 1, 0, count)
            

            if count > 330 and count < 350:
                B2_TRI_3_a.alpha = renderPattern(B2_TRI_3_a.img, B2_TRI_3_a.img_x, B2_TRI_3_a.img_y, B2_TRI_3_a.img_width, B2_TRI_3_a.img_height, B2_TRI_3_a.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 350 and count < 360:
                B2_TRI_3_a.alpha = renderPattern(B2_TRI_3_a.img, B2_TRI_3_a.img_x, B2_TRI_3_a.img_y, B2_TRI_3_a.img_width, B2_TRI_3_a.img_height, B2_TRI_3_a.alpha, 0, 255, 15, 17, 2, 50, count)
                B2_TRI_3_b.alpha = renderPattern(B2_TRI_3_b.img, B2_TRI_3_b.img_x, B2_TRI_3_b.img_y, B2_TRI_3_b.img_width, B2_TRI_3_b.img_height, B2_TRI_3_b.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 360 and count < 370:
                B2_TRI_3_a.alpha = renderPattern(B2_TRI_3_a.img, B2_TRI_3_a.img_x, B2_TRI_3_a.img_y, B2_TRI_3_a.img_width, B2_TRI_3_a.img_height, B2_TRI_3_a.alpha, 0, 255, 15, 17, 2, 50, count)
                B2_TRI_3_b.alpha = renderPattern(B2_TRI_3_b.img, B2_TRI_3_b.img_x, B2_TRI_3_b.img_y, B2_TRI_3_b.img_width, B2_TRI_3_b.img_height, B2_TRI_3_b.alpha, 0, 255, 15, 17, 2, 50, count)
                B2_TRI_3_c.alpha = renderPattern(B2_TRI_3_c.img, B2_TRI_3_c.img_x, B2_TRI_3_c.img_y, B2_TRI_3_c.img_width, B2_TRI_3_c.img_height, B2_TRI_3_c.alpha, 255, 255, 1, 255, 1, 0, count)
            if count >= 370 and count < 380:
                B2_TRI_3_b.alpha = renderPattern(B2_TRI_3_b.img, B2_TRI_3_b.img_x, B2_TRI_3_b.img_y, B2_TRI_3_b.img_width, B2_TRI_3_b.img_height, B2_TRI_3_b.alpha, 0, 255, 15, 17, 2, 50, count)
                B2_TRI_3_c.alpha = renderPattern(B2_TRI_3_c.img, B2_TRI_3_c.img_x, B2_TRI_3_c.img_y, B2_TRI_3_c.img_width, B2_TRI_3_c.img_height, B2_TRI_3_c.alpha, 0, 255, 15, 17, 2, 50, count)
                B2_TRI_3_d.alpha = renderPattern(B2_TRI_3_d.img, B2_TRI_3_d.img_x, B2_TRI_3_d.img_y, B2_TRI_3_d.img_width, B2_TRI_3_d.img_height, B2_TRI_3_d.alpha, 255, 255, 1, 255, 1, 0, count)


        # B3
        if count < 120:
            B3_FCW_B.alpha = renderPattern(B3_FCW_B.img, B3_FCW_B.img_x, B3_FCW_B.img_y, B3_FCW_B.img_width, B3_FCW_B.img_height, B3_FCW_B.alpha, 255, 255, 1, 255, 1, 0, count)
            if count < 40:
                B3_FCW_BA.alpha = renderPattern(B3_FCW_BA.img, B3_FCW_BA.img_x, B3_FCW_BA.img_y, B3_FCW_BA.img_width, B3_FCW_BA.img_height, B3_FCW_BA.alpha, 255, 255, 1, 255, 1, 0, count)
                B3_FCW_R.alpha = renderPattern(B3_FCW_R.img, B3_FCW_R.img_x, B3_FCW_R.img_y, B3_FCW_R.img_width, B3_FCW_R.img_height, B3_FCW_R.alpha, 0, 255, 15, 17, 2, 0, count)
            if count > 40 and count < 60:
                B3_PDW_1.alpha = renderPattern(B3_PDW_1.img, B3_PDW_1.img_x, B3_PDW_1.img_y, B3_PDW_1.img_width, B3_PDW_1.img_height, B3_PDW_1.alpha, 0, 255, 5, 51, 2, 0, count) # 0.5 Hz
            if count > 60 and count < 80:
                B3_PDW_2.alpha = renderPattern(B3_PDW_2.img, B3_PDW_2.img_x, B3_PDW_2.img_y, B3_PDW_2.img_width, B3_PDW_2.img_height, B3_PDW_2.alpha, 0, 255, 5, 51, 2, 0, count)
            if count > 80 and count < 100:
                B3_PDW_3.alpha = renderPattern(B3_PDW_3.img, B3_PDW_3.img_x, B3_PDW_3.img_y, B3_PDW_3.img_width, B3_PDW_3.img_height, B3_PDW_3.alpha, 0, 255, 5, 51, 2, 0, count)
            if count > 100 and count < 120:
                B3_PDW_4.alpha = renderPattern(B3_PDW_4.img, B3_PDW_4.img_x, B3_PDW_4.img_y, B3_PDW_4.img_width, B3_PDW_4.img_height, B3_PDW_4.alpha, 0, 255, 5, 51, 2, 0, count)

        # B4
        if count > 380:
            if count > 380 and count < 460:
                B4_R_B.alpha = renderPattern(B4_R_B.img, B4_R_B.img_x, B4_R_B.img_y, B4_R_B.img_width, B4_R_B.img_height, B4_R_B.alpha, 255, 255, 1, 255, 1, 0, count)
                B4_R_R.alpha = renderPattern(B4_R_R.img, B4_R_R.img_x, B4_R_R.img_y, B4_R_R.img_width, B4_R_R.img_height, B4_R_R.alpha, 255, 255, 1, 255, 1, 0, count)
                for i in range(0, 8):
                    if (count//2)%8==i:
                        # B4_R_BL.alpha = renderPattern(B4_R_BL.img, B4_R_BL.img_x+i*20, B4_R_BL.img_y, B4_R_BL.img_width, B4_R_BL.img_height, B4_R_BL.alpha, 200, 200, 1, 255, 1, 0, count)
                        jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B4_BL.img, B4_BL.img_x+i*20, B4_BL.img_y, B4_BL.img_width, B4_BL.img_height)
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
                B4_L_B.alpha = renderPattern(B4_L_B.img, B4_L_B.img_x, B4_L_B.img_y, B4_L_B.img_width, B4_L_B.img_height, B4_L_B.alpha, 255, 255, 1, 255, 1, 0, count)
                B4_L_R.alpha = renderPattern(B4_L_R.img, B4_L_R.img_x, B4_L_R.img_y, B4_L_R.img_width, B4_L_R.img_height, B4_L_R.alpha, 255, 255, 1, 255, 1, 0, count)
                for i in range(0, 8):
                    if (count//2)%8==i:
                        # pat48_alpha = renderPattern(pat48_img, pat48_img_x-314-i*20, pat48_img_y, pat48_img_width, pat48_img_height, pat48_alpha, 200, 200, 1, 255, 1, 0, count)
                        # B4_R_BL.alpha = renderPattern(B4_R_BL.img, B4_R_BL.img_x-314-i*20, B4_R_BL.img_y, B4_R_BL.img_width, B4_R_BL.img_height, B4_R_BL.alpha, 200, 200, 1, 255, 1, 0, count) 
                        jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, B4_BL.img, B4_BL.img_x-300-i*20, B4_BL.img_y, B4_BL.img_width, B4_BL.img_height)


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
    

        # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat1_img, pat1_img_x, pat1_img_y, pat1_img_width, pat1_img_height,pat1_alpha)
        # if (count//15)%2==0:
        #     pat1_alpha=min(pat1_alpha+17,255)
        # else:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
        #     pat1_alpha=max(pat1_alpha-17,0)

        # if (count//150)%2==0:
        #     jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, "60", test_txt_x,test_txt_y,test_txt_size,test_txt_R,test_txt_G,test_txt_B,test_txt_A)
        # test_number=80-(count//30)
        # jetson.utils.Overlay_word(bg_img, bg_img_width, bg_img_height, str(test_number), test_txt_x+200,test_txt_y,250,0,255,255,255)
        
        # jetson.utils.Overlay_pat(bg_img, bg_img_width, bg_img_height, pat1_img, 500, pat1_img_y, pat1_img_width, pat1_img_height,255)
        # if count > 460:
        #     jetson.utils.Overlay_pat_selfalpha(bg_img, bg_img_width, bg_img_height, pat2_img, 500, pat1_img_y, pat2_img_width, pat2_img_height)
        
        display.RenderOnce(bg_img, bg_img_width, bg_img_height,img_start_x,img_start_y)

        count=count+1
        
        time.sleep(0.03)

