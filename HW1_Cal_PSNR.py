import cv2
import math

def calculateMSE(oriImg, modifiedImg):
    #shape : [height, width, channel]
    imgWidth = oriImg.shape[1]
    imgHeight = oriImg.shape[0]
    sum = 0

    i = 0 # y軸
    while i < imgHeight :
        j = 0  # x軸
        while j < imgWidth :
            diff = int(oriImg[i][j]) - int(modifiedImg[i][j])  # original - modified
            sum += (diff ** 2)
            j += 1   # next pixel
        i += 1   # next line

    MSE = sum / (imgWidth * imgHeight)
    return MSE

def calculatePSNR():
    # load color images as greyscale
    original_img = cv2.imread('image/original.jpg', 0)
    contrast_img = cv2.imread('image/original_contrast.jpg', 0)
    brightness_img = cv2.imread('image/original_brightness.jpg', 0)


    MSE1 = calculateMSE(original_img, contrast_img)
    print(MSE1)
    psnr1 = (10*math.log10((255*255) / MSE1))
    print (psnr1)

    MSE2 = calculateMSE(original_img, brightness_img)
    print(MSE2)
    psnr2 = (10 * math.log10((255 * 255) / MSE2))
    print(psnr2)

    # save the two modified images
    cv2.imwrite("image/result/greyscale_contrast.jpg", contrast_img)
    cv2.imwrite("image/result/greyscale_brightness.jpg", brightness_img)




if __name__ == '__main__':
    calculatePSNR()


