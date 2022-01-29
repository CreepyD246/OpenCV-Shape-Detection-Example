import cv2 # OpenCV Library

# Image to detect shapes on below
image = cv2.imread("INSERT PATH TO IMAGE FILE HERE")

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # Converting to gray image

# Setting threshold value to get new image (In simpler terms: this function checks every pixel, and depending on how
# dark the pixel is, the threshold value will convert the pixel to either black or white (0 or 1)).
_, thresh_image = cv2.threshold(gray_image, 220, 255, cv2.THRESH_BINARY)

# Retrieving outer-edge coordinates in the new threshold image
contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Iterating through each contour to retrieve coordinates of each shape
for i, contour in enumerate(contours):
    if i == 0:
        continue

    # The 2 lines below this comment will approximate the shape we want. The reason being that in certain cases the
    # shape we want might have flaws or might be imperfect, and so, for example, if we have a rectangle with a
    # small piece missing, the program will still count it as a rectangle. The epsilon value will specify the
    # precision in which we approximate our shape.
    epsilon = 0.01*cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # Drawing the outer-edges onto the image
    cv2.drawContours(image, contour, 0, (0, 0, 0), 4)

    # Retrieving coordinates of the contour so that we can put text over the shape.
    x, y, w, h= cv2.boundingRect(approx)
    x_mid = int(x + (w/3)) # This is an estimation of where the middle of the shape is in terms of the x-axis.
    y_mid = int(y + (h/1.5)) # This is an estimation of where the middle of the shape is in terms of the y-axis.

    # Setting some variables which will be used to display text on the final image
    coords = (x_mid, y_mid)
    colour = (0, 0, 0)
    font = cv2.FONT_HERSHEY_DUPLEX

    # This is the part where we actually guess which shape we have detected. The program will look at the amount of edges
    # the contour/shape has, and then based on that result the program will guess the shape (for example, if it has 3 edges
    # then the chances that the shape is a triangle are very good.)
    #
    # You can add more shapes if you want by checking more lenghts, but for the simplicity of this tutorial program I
    # have decided to only detect 5 shapes.
    if len(approx) == 3:
        cv2.putText(image, "Triangle", coords, font, 1, colour, 1) # Text on the image
    elif len(approx) == 4:
        cv2.putText(image, "Quadrilateral", coords, font, 1, colour, 1)
    elif len(approx) == 5:
        cv2.putText(image, "Pentagon", coords, font, 1, colour, 1)
    elif len(approx) == 6:
        cv2.putText(image, "Hexagon", coords, font, 1, colour, 1)
    else:
        # If the length is not any of the above, we will guess the shape/contour to be a circle.
        cv2.putText(image, "Circle", coords, font, 1, colour, 1)
    
# Displaying the image with the detected shapes onto the screen
cv2.imshow("shapes_detected", image)
cv2.waitKey(0)
