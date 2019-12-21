import numpy as np
import cv2

VIDEO_PORT = 0

cap = cv2.VideoCapture(VIDEO_PORT)


def setupCV():
    cv2.namedWindow("Parameters")
    cv2.resizeWindow("Parameters", 840, 840)
    cv2.createTrackbar("GaussianBlur:Size 1", "Parameters", 17, 100, empty)
    cv2.createTrackbar("GaussianBlur:Size 2", "Parameters", 1, 100, empty)
    cv2.createTrackbar("Dialate Iteration", "Parameters", 1, 20, empty)
    cv2.createTrackbar("Threshold1", "Parameters", 23, 255, empty)
    cv2.createTrackbar("Threshold2", "Parameters", 20, 255, empty)
    cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)
    cv2.createTrackbar("Area Threshold", "Parameters", 50000, 80000, empty)
    cv2.createTrackbar("ContourApprox Precision", "Parameters", 1, 100, empty)


def empty(a):
    pass


setupCV()


def getShape(approx):
    # if the shape is a triangle, it will have 3 vertices
    if len(approx) == 3:
        shape = "triangle"

    # if the shape has 4 vertices, it is either a square or
    # a rectangle
    elif len(approx) == 4:
        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        shape = "rectangle"

    # if the shape is a pentagon, it will have 5 vertices
    elif len(approx) == 5:
        shape = "pentagon"

    # otherwise, we assume the shape is a circle
    else:
        shape = "circle"

    # return the name of the shape
    return shape

STOP_FLAG = True


def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        min_area = cv2.getTrackbarPos("Area", "Parameters")
        maximum_threshold = cv2.getTrackbarPos("Area Threshold", "Parameters")

        if area >= min_area:
            peri = cv2.arcLength(cnt, True)
            prec = 0.04
            approx = cv2.approxPolyDP(cnt, prec * peri, True)

            if area >= maximum_threshold and getShape(approx) == 'rectangle':
                cv2.putText(imgContour, "Found the Target", (20, 40), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 2)
                x, y, w, h = cv2.boundingRect(approx)
                extractedRec = imgContour[y:y + h, x:x + w]
                cv2.imwrite("image.jpg", extractedRec)
                return True
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)

            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + int(w / 2), y + int(h / 2)),
                        cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Shape: " + str(getShape(approx)), (x + int(w / 2), y + int(h / 2) + 20),
                        cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)
    return False


while (STOP_FLAG):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Make copy from the frame
    imgContour = frame.copy()

    g1 = cv2.getTrackbarPos("GaussianBlur:Size 1", "Parameters")
    if g1 % 2 == 0:
        g1 += 1
    g2 = cv2.getTrackbarPos("GaussianBlur:Size 1", "Parameters")
    if g2 % 2 == 0:
        g2 += 1
    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    iteration = cv2.getTrackbarPos("Dialate Iteration", "Parameters")
    kernel = np.ones((5, 5))

    imgBlur = cv2.GaussianBlur(frame, (g1, g2), 0, 0)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    closing = cv2.morphologyEx(imgCanny, cv2.MORPH_CLOSE, kernel)

    cv2.imshow("Canny: ", imgCanny)
    imgDil = cv2.dilate(closing, kernel, iterations=iteration)
    status = getContours(imgDil, imgContour)
    cv2.imshow("Contours", imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q') :
        break
    if status == True:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
