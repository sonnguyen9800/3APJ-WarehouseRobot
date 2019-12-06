import sys

import cv2
import numpy as np
from skimage.color import rgb2lab, deltaE_cie76

VIDEO_PORT = 2


frameWidth = 640
frameHeight = 480

comparison_flag = False


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
# fourcc = cv2.CV_FOURCC(*'DIVX')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

# out = cv2.VideoWriter('output.mp4',0x00000021, 15.0, (1280,480))
# out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frameWidth,frameHeight))
cap = cv2.VideoCapture(VIDEO_PORT)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",840,840)

cv2.createTrackbar("GaussianBlur:Size 1","Parameters",1, 100, empty)
cv2.createTrackbar("GaussianBlur:Size 2","Parameters",1, 100, empty)

cv2.createTrackbar("Dialate Iteration","Parameters",1,20,empty)

cv2.createTrackbar("Threshold1","Parameters",23,255,empty)
cv2.createTrackbar("Threshold2","Parameters",20,255,empty)

cv2.createTrackbar("Area","Parameters",5000,30000,empty)
cv2.createTrackbar("ContourApprox Precision","Parameters",1,100,empty)

cv2.createTrackbar("Yellow-R","Parameters",0,255,empty)
cv2.createTrackbar("Yellow-G","Parameters",0,255,empty)
cv2.createTrackbar("Yellow-B","Parameters",0,255,empty)

cv2.createTrackbar("Green-R","Parameters",0,255,empty)
cv2.createTrackbar("Green-G","Parameters",0,255,empty)
cv2.createTrackbar("Green-B","Parameters",0,255,empty)

cv2.createTrackbar("Blue-R","Parameters",0,255,empty)
cv2.createTrackbar("Blue-G","Parameters",0,255,empty)
cv2.createTrackbar("Blue-B","Parameters",0,255,empty)

def getRGBvalues(test_src_image):

    # load the image
    image = test_src_image

    chans = cv2.split(image)
    colors = ('b', 'g', 'r')
    features = []

    feature_data = []


    counter = 0
    for (chan, color) in zip(chans, colors):
        counter = counter + 1

        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.extend(hist)

        # find the peak pixel values for R, G, and B
        elem = np.argmax(hist)

        if counter == 1:
            blue = str(elem)
        elif counter == 2:
            green = str(elem)
        elif counter == 3:
            red = str(elem)
            feature_data.append(red)
            feature_data.append(green)
            feature_data.append(blue)

    return feature_data

COLORS = {
        'GREEN': [50,150,80],
        'BLUE': [10,74,205],
        'YELLOW': [180,200,100]
    }

COLORS_RANGE = {
    'GREEN': {
        'LOWER_BOUNDARY': [0,51,0],
        'UPPER_BOUNDARY': [100,255,100],
        'NAME' : "GREEN"
    },

    'BLUE': {
        'LOWER_BOUNDARY': [0, 153, 180],
        'UPPER_BOUNDARY': [30, 255, 255],
        'NAME': "BLUE"

    },

    'YELLOW': {
        'LOWER_BOUNDARY': [100, 100, 0],
        'UPPER_BOUNDARY': [180, 180, 100],
        'NAME': "YELLOW"

    }

}

def inRange(color:dict, upper_boundary:dict, lower_boundary:dict):
    if int(color[0]) < int(lower_boundary[0]):
        return False
    if int(color[1]) < int(lower_boundary[1]):
        return False
    if int(color[2]) < int(lower_boundary[2]):
        return False

    if int(color[0]) > int(upper_boundary[0]):
        return False
    if int(color[1]) > int(upper_boundary[1]):
        return False
    if int(color[2]) > int(upper_boundary[2]):
        return False
    return True


def comparison(colorsRGB, Colors: dict, ColorsRange:dict = COLORS_RANGE):
    selected_color = colorsRGB
    min = sys.maxsize
    color_picked = []

    color = ColorsRange




    if inRange(selected_color, color['GREEN']['UPPER_BOUNDARY'], color['GREEN']['LOWER_BOUNDARY']):
        comparison_flag = True
        return color['GREEN']['NAME']

    if inRange(selected_color, color['BLUE']['UPPER_BOUNDARY'], color['BLUE']['LOWER_BOUNDARY']):
        comparison_flag = True
        return color['BLUE']['NAME']

    if inRange(selected_color, color['YELLOW']['UPPER_BOUNDARY'], color['YELLOW']['LOWER_BOUNDARY']):
        comparison_flag = True
        return color['YELLOW']['NAME']


    # selected_color = rgb2lab(np.uint8(np.asarray([[colorsRGB]])))
    #
    # for color in Colors:
    #     curr_color = rgb2lab(np.uint8(np.asarray([[Colors[color]]])))
    #     diff = deltaE_cie76(selected_color, curr_color)
    #     if diff < min:
    #         min = diff
    #         color_picked = color

    comparison_flag =  False
    return "UNKNOWN"

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

prediction = None
color_extracted =  [0,0,0]
choosen_cnt = 0

def getContours(img, imgContour, flagExtractRectangle=False, choosen_cnt=choosen_cnt):
    # contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE)

    # mask = np.ones(img.shape[:2], dtype="uint8") * 255
    # for cnt in contours:
    #     area = cv2.contourArea(cnt)
    #     areaMin = cv2.getTrackbarPos("Area", "Parameters")
    #     if area >= areaMin and flagExtractRectangle == False:
    #         # cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
    #
    #         peri = cv2.arcLength(cnt, True)
    #         prec = cv2.getTrackbarPos("ContourApprox Precision","Parameters")
    #
    #         if prec == 0:
    #             prec = 1
    #         prec = prec/100
    #         approx = cv2.approxPolyDP(cnt, prec * peri, True)
    #
    #
    #         # print(len(approx))
    #         x , y , w, h = cv2.boundingRect(approx)
    #         # cv2.rectangle(imgContour, (x , y ), (x + w , y + h ), (0, 255, 0), 5)
    #
    #         extractedRec = imgContour[y:y + h, x:x + w]
    #
    #         # extractedRec = cv2.cvtColor(extractedRec, cv2.COLOR_RGB2BGR)
    #
    #         cv2.imshow("Extracted_Frame", extractedRec)
    #         color_extracted = getRGBvalues(extractedRec)
    #         prediction = comparison(color_extracted, COLORS)
    #
    #         cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
    #
    #         cv2.putText(imgContour, "Color:" + str(prediction), (0, 300 ), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),
    #                     2)
    #
    #         cv2.putText(imgContour, "Points: " + str(len(approx)), (0, 400), cv2.FONT_HERSHEY_COMPLEX, .7,
    #                     (0, 255, 0), 2)
    #         cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
    #                     (0, 255, 0), 2)

    if len(contours) != 0:
        # draw in blue the contours that were founded

        # find the biggest area
        c = max(contours, key=cv2.contourArea)
        cv2.drawContours(imgContour, c, -1, 255, 3)

        x, y, w, h = cv2.boundingRect(c)
        # draw the book contour (in green)
        cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)

        extractedRec = imgContour[y:y + h, x:x + w]
        cv2.imshow("Extracted_Frame", extractedRec)
        color_extracted = getRGBvalues(extractedRec)
        prediction = comparison(color_extracted, COLORS)
        cv2.putText(imgContour, "Color:" + str(prediction), (0, 300 ), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),2)

        cv2.putText(imgContour, "Mode Compare:" + str(comparison_flag), (0, 400 ), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),2)

        cv2.putText(imgContour, "RGB VALUE:" + str(color_extracted), (0,200 ), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0),2)





record_count = 0
while True:
    COLORS['YELLOW'] = [cv2.getTrackbarPos('Yellow-R', 'Parameters'),
                        cv2.getTrackbarPos('Yellow-G', 'Parameters'),
                        cv2.getTrackbarPos('Yellow-B', 'Parameters')]

    COLORS['GREEN'] = [cv2.getTrackbarPos('Green-R', 'Parameters'),
                       cv2.getTrackbarPos('Green-G', 'Parameters'),
                       cv2.getTrackbarPos('Green-B', 'Parameters')]

    COLORS['BLUE'] = [cv2.getTrackbarPos('Blue-R', 'Parameters'),
                       cv2.getTrackbarPos('Blue-G', 'Parameters'),
                       cv2.getTrackbarPos('Blue-B', 'Parameters')]


    # Record the data
    success, img = cap.read()

    # lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # # -----Splitting the LAB image to different channels-------------------------
    # l, a, b = cv2.split(lab)
    # # -----Applying CLAHE to L-channel-------------------------------------------
    # clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    # cl = clahe.apply(l)
    # # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    # limg = cv2.merge((cl, a, b))
    # # -----Converting image from LAB Color model to RGB model--------------------
    # img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)



    # Make a compy of the frame
    imgContour = img.copy()

    g1 = cv2.getTrackbarPos("GaussianBlur:Size 1", "Parameters")

    if g1 % 2 == 0:
        g1+=1
    g2 = cv2.getTrackbarPos("GaussianBlur:Size 1", "Parameters")
    if g2 % 2 == 0:
        g2+=1


    imgBlur = cv2.GaussianBlur(img, (g1, g2), 0, 0)

    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    #
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    #
    imgCanny = cv2.Canny(imgGray,threshold1,threshold2)

    # Image Dialation:
    iteration = cv2.getTrackbarPos("Dialate Iteration","Parameters")



    kernel = np.ones((5, 5))
    closing = cv2.morphologyEx(imgCanny, cv2.MORPH_CLOSE, kernel)

    imgDil = cv2.dilate(closing, kernel, iterations=iteration)
    getContours(imgDil,imgContour, flagExtractRectangle=False)

    # imgStack = stackImages(0.8,([img,imgContour],
    #                             [imgDil,imgContour]))
    # cv2.imshow("Image Blur", imgBlur)
    # cv2.imshow("Gray", imgGray)

    cv2.imshow("Closing", closing)
    cv2.imshow("Canny", imgCanny)
    cv2.imshow("Dilate", imgDil)

    cv2.putText(text="Press E to Record", color=(0,23,144), img=imgContour, fontScale=1.3, fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, org=(0,100))
    # cv2.putText(text="Color: " + str(prediction), color=(0,23,144), img=imgContour, fontScale=1.3, fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, org=(0,200))

    cv2.imshow("Contours", imgContour)

    # cv2.imshow("Result", img)

    if cv2.waitKey(1) & 0xFF == ord('e'):
        record_count+=1
        if record_count % 2 == 0:
            print("Stop Recording")
        else:
            print("Recording")


    if record_count % 2 == 0 and record_count !=0:
        out.release()
        break;
    else:
        out.write(imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()