#! /usr/bin/env python
__author__ ='Jacques Saraydaryan'
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
from ros_color_detection_srvs.srv import DetectColorFromImg

def LoadImgAndUseSrv():
    rospy.init_node('color_detection_node_test', anonymous=False)
    _bridge = CvBridge()
    test_folder=rospy.get_param('/color_detection/imgtest_folder','/data')

    #Load Image
    #img_loaded1 = cv2.imread(test_folder+'/blue-short.jpg')
    img_loaded1 = cv2.imread(test_folder+'/top-purple.jpg')
    msg_im1 = _bridge.cv2_to_imgmsg(img_loaded1, encoding="bgr8")

    img_loaded2 = cv2.imread(test_folder+'/top-gray-2.jpg')
    #img_loaded2 = cv2.imread(test_folder+'/top-white.jpg')
    #img_loaded2 = cv2.imread(test_folder+'/top-white-2.jpeg')
    #img_loaded2 = cv2.imread(test_folder+'/trousers-black-2.jpg')
    #img_loaded2 = cv2.imread(test_folder+'/trousers-black.png')
    
    msg_im2 = _bridge.cv2_to_imgmsg(img_loaded2, encoding="bgr8")

    
    
    
    #call service to detect color
    rospy.wait_for_service('detect_color_srv')
    try:
        detect_from_img_srv = rospy.ServiceProxy('detect_color_srv', DetectColorFromImg)
        content1 = detect_from_img_srv(msg_im1)
        resp1 =content1.main_color
        rospy.loginfo("color:%s, color_web:%s, color_temp:%s, color_brightness_name:%s, RGB:[%s,%s,%s], percentage:%s",str(resp1.color_name),str(resp1.color_web),str(resp1.color_temp),str(resp1.color_brightness_name),str(resp1.rgb[0]),str(resp1.rgb[1]),str(resp1.rgb[2]),str(resp1.percentage_of_img))
    except rospy.ServiceException, e:
        rospy.logwarn("Service call failed: %s",e)


    #try:
    #    content2 = detect_from_img_srv(msg_im2)
    #    resp2=content2.main_color
    #    rospy.loginfo("color:%s, color_web:%s, color_temp:%s, color_brightness_name:%s, RGB:[%s,%s,%s], percentage:%s",str(resp2.color_name),str(resp2.color_web),str(resp2.color_temp),str(resp2.color_brightness_name),str(resp2.rgb[0]),str(resp2.rgb[1]),str(resp2.rgb[2]),str(resp2.percentage_of_img))
    #except rospy.ServiceException, e:
    #    rospy.logwarn("Service call failed: %s",e)

    # spin
    rospy.spin()

if __name__ == '__main__':
    try:
        LoadImgAndUseSrv()
    except rospy.ROSInterruptException:
        pass