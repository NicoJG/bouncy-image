from PIL import Image
import numpy as np
from constants import image_path,image_height,crop_image, filter_white_pixels

def load_image():
    img = Image.open(image_path)
    img = img.convert("RGBA")
    # filter the outer background for cropping
    if filter_white_pixels and crop_image: img = cut_background(img,100,5)
    if crop_image: img = img.crop(box=img.getbbox())
    aspect_ratio = img.width/img.height
    img = img.resize( (int(image_height*aspect_ratio), image_height) , resample=Image.BICUBIC)
    # filter all pixels that are almost white (invisible)
    if filter_white_pixels: img = cut_background(img,255,10)
    return img, aspect_ratio

def cut_background(img,threshold,dist):
    pix = np.array(img)
    r = pix[:,:,0]
    g = pix[:,:,1]
    b = pix[:,:,2]
    a = pix[:,:,3]
    mask = ((r>threshold)
      & (g>threshold)
      & (b>threshold)
      & (np.abs(r-g)<dist)
      & (np.abs(r-b)<dist)
      & (np.abs(g-b)<dist)
      )
    pix[mask,3] = 0
    pix[a<50,3] = 0
    return Image.fromarray(pix)