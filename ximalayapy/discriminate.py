""" 
原识别腾讯滑块验证 https://github.com/wkunzhi/Python3-Spider/blob/master/%E6%BB%91%E5%8A%A8%E9%AA%8C%E8%AF%81%E7%A0%81/%E3%80%90%E8%85%BE%E8%AE%AF%E3%80%91%E6%BB%91%E5%9D%97%E9%AA%8C%E8%AF%81/discriminate.py
改写后识别喜马拉雅滑块验证的准确率在60-70%
"""
 



"""
pip3 install opencv-python
"""

import cv2 as cv


def get_pos(image):
    """ 获取距离 """
    blurred = cv.GaussianBlur(image, (5, 5), 0)
    canny = cv.Canny(blurred, 200, 400)
    contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    target_contour = None
    target_contourArea = 0
    for i, contour in enumerate(contours):
        m = cv.moments(contour)
        if m['m00'] == 0:
            cx = cy = 0
        else:
            cx, cy = m['m10'] / m['m00'], m['m01'] / m['m00']
        testcontourArea = cv.contourArea(contour)
        testarcLength = cv.arcLength(contour, True)
        # print(testcontourArea,testarcLength)
        # 初步筛选
        if 15 <= cv.contourArea(contour) and 250 < cv.arcLength(contour, True)<1200:
            # if cx < 150:
            #     continue
            testcontourArea = cv.contourArea(contour)
            testarcLength = cv.arcLength(contour, True)
            if testcontourArea > target_contourArea and cx >150:
                target_contour = contour
                target_contourArea = testcontourArea
    if not target_contourArea ==0:
        x, y, w, h = cv.boundingRect(target_contour)  # 外接矩形
        # cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # cv.imshow('image', image)
        return x
    return 0


            
    

if __name__ == '__main__':
    img0 = cv.imread('19bg.jpg')
    result = get_pos(img0)
    print(result)
    cv.waitKey(0)
    cv.destroyAllWindows()
