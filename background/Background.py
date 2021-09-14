import cv2
import numpy as np


def run_grabcut(img_orig, rect_final):
    mask = np.zeros(img_orig.shape[:2],np.uint8)
    x,y,w,h = rect_final
    mask[y:y+h, x:x+w] = 1

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)

    cv2.grabCut(img_orig,mask,rect_final,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img_orig = img_orig*mask2[:,:,np.newaxis]
    return img_orig