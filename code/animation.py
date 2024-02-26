import cv2
from PIL import Image

# gif = []
# img1, img2, img3 = Image.open('../UI_image/a2_l.png'), Image.open('../UI_image/a2_b.png'), Image.open('../UI_image/a2_r.png')
# gif.append(img1)
# gif.append(img2)
# gif.append(img3)

# gif[0].save("../UI_image/a2.gif", save_all=True, append_images=gif[1:], duration=400, loop=0, disposal=0)

def transparent(image_path, out_img_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if image.shape[2] < 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        frames = []
        for alpha in range(0, 256, 25):
            tmp = image.copy()   
            tmp[:, :, 3] = alpha        
            # 使用Pillow轉換格式        
            pil_img = Image.fromarray(cv2.cvtColor(tmp, cv2.COLOR_BGRA2RGBA))        
            frames.append(pil_img)
        frames[0].save(out_img_path, save_all=True, append_images=frames[1:], optimize=False, duration=100, loop=0)
    
transparent('../UI_image/a2_l.png', '../UI_image/a2.gif')