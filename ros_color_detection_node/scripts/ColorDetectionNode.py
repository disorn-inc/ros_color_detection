#!/usr/bin/env python  
__author__ ='Jacques Saraydaryan'

import sys
import time
import rospy 
#import roslib
#roslib.load_manifest('ros_color_detection_node')
import actionlib
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2
from skimage import color
import numpy as np

from sensor_msgs.msg import Image
from ros_color_detection_msgs.msg import ColorD, ColorDList
from ros_color_detection_actions.msg import DetectColorFromImgAction, DetectColorFromImgResult
from ros_color_detection_srvs.srv import DetectColorFromImg

from process.KmeansColorDetection import KmeansColorDetection
from process.ColorRGBToName import ColorRGBToName

import matplotlib.pyplot as plt



class ColorDetectionNode():
    NB_KMEAN_CLUSTER=3
    SATURATION_BOOST=0.0
    VALUE_BOOST=0.1
    IS_PROCESS_DISPLAYED=False


    def __init__(self):
        rospy.init_node('color_detection_node', anonymous=False)
        self.configure()

        self._bridge = CvBridge()
        self._k_process=KmeansColorDetection(self.NB_KMEAN_CLUSTER,self.IS_PROCESS_DISPLAYED)
        self._color_to_name=ColorRGBToName()

        # Subscribe to the image 
        self.sub_rgb = rospy.Subscriber("/image", Image, self.rgb_callback, queue_size=1)
        self.pub_color = rospy.Publisher("/image_color", ColorDList, queue_size=1)

        #declare ros service 
        self.detectColorSrv = rospy.Service('detect_color_srv', DetectColorFromImg, self.detectColorSrvCallback)

         # create action server and start it
        self._actionServer = actionlib.SimpleActionServer('detect_color_action', DetectColorFromImgAction, self.executeColorDetectionActionServer, False)
        self._actionServer.start()

        #if self.IS_PROCESS_DISPLAYED :
            #plt.ion()
            #plt.show(block=False)
     
        # spin
        rospy.spin()


    def configure(self):
        #load face files form data directory
        self.NB_KMEAN_CLUSTER=rospy.get_param('kmean_cluster',3)
        rospy.loginfo("Param: kmean_cluster:"+str(self.NB_KMEAN_CLUSTER))
        self.IS_PROCESS_DISPLAYED=rospy.get_param('is_process_displayed',False)
        rospy.loginfo("Param: is_process_displayed:"+str(self.IS_PROCESS_DISPLAYED))

    def rgb_callback(self, data):
        main,colorDlist=self.processImg(data)
        self.pub_color.publish(colorDlist)
    
    def detectColorSrvCallback(self,req):
        main,colorDlist=self.processImg(req.img)
        return {'main_color':main,'main_colors':colorDlist}
        

    def processImg(self, img):
        frame = self._bridge.imgmsg_to_cv2(img, 'bgr8')
        clusters=self._k_process.process_image(frame)

        pixelSum=0
        max_label=0
        max_pixel=0
        i=0
        index_max=0
        for cluster in clusters.values():
            pixelSum=pixelSum+cluster.getNbPixel()
            if max_pixel<cluster.getNbPixel():
                max_pixel=cluster.getNbPixel()
                max_label=cluster.label
                index_max=i
            i=i+1

        colorList=[]
        for cluster in clusters.values():
            colorD=self.processClusterToAddName(cluster,pixelSum)
            colorList.append(colorD)

        cDList=ColorDList()
        cDList.colorList=colorList
        return colorList[max_label], cDList

        

    def processClusterToAddName(self,cluster,pixelSum):
        data = np.zeros(shape=(1, 1, 3), dtype=np.float64)
        data[0,0,:]=cluster.getValue()

        if data[0][0][1]+self.SATURATION_BOOST <1 :
            data[0][0][1]=data[0][0][1]+self.SATURATION_BOOST
        if data[0][0][2]+self.VALUE_BOOST <1:
            data[0][0][2]=data[0][0][2]+self.VALUE_BOOST
        
        R=(color.hsv2rgb(data)*255)[0][0][0]
        G=(color.hsv2rgb(data)*255)[0][0][1]
        B=(color.hsv2rgb(data)*255)[0][0][2]
        requested_color0=(R,G,B)
        #fix parameter for get best hue value
        #data[0][0][2]=cluster.max_V_value
        data[0][0][2]=1
        R=(color.hsv2rgb(data)*255)[0][0][0]
        G=(color.hsv2rgb(data)*255)[0][0][1]
        B=(color.hsv2rgb(data)*255)[0][0][2]
        requested_color=(R,G,B)
        actual_name, closest_name_original_value=self._color_to_name.get_color_name(requested_color0)
        
        actual_name, closest_name_max_value=self._color_to_name.get_color_name(requested_color)

        #FIXME currently not give expected result
        label_brightnes=self._color_to_name.black_white_gray_detector(None,cluster.getValue()[1]*100,cluster.getValue()[2]*100)
        rospy.loginfo("------------------V MAX: %s, V AVG: %s, S AVG: %s --------------------", str(cluster.max_V_value),str(cluster.getVAvg()),str(cluster.getSAvg()))
        rospy.loginfo( '------------------VALUE BLACK,GREY,WHITE: %s --------------------',str(label_brightnes))
        rospy.loginfo( '------------------NOT MODIFIED COLOR: %s --------------------',str(closest_name_original_value))
        simpleColorFromOriginal=self._color_to_name.simpleColor(closest_name_max_value.upper())
        color_name_result=''
        if None is not label_brightnes:
            if "DARK" is not label_brightnes:
                color_name_result=label_brightnes
            else:
                color_name_result=str(label_brightnes) + " " +str(simpleColorFromOriginal)
        else:
             color_name_result=simpleColorFromOriginal

        colorD=ColorD()
        colorD.color_name=str(color_name_result)
        colorD.color_web=str(closest_name_original_value)
        colorD.color_temp=str(simpleColorFromOriginal)
        colorD.color_brightness_name=str(label_brightnes)
        colorD.rgb=[R,G,B]
        colorD.hsv=[cluster.getValue()[0],cluster.getValue()[1],cluster.getValue()[2]]
        colorD.percentage_of_img=float(cluster.getNbPixel())/float(pixelSum)
        return colorD

    def executeColorDetectionActionServer(self, goal):
        isActionSucceed=False
        action_result = DetectColorFromImgResult()
        try:
            main,colorDlist =self.processImg(goal.img)
            action_result.main_color=main
            action_result.main_colors=colorDlist
            isActionSucceed=True
        except Exception as e:
            rospy.logwarn("unable to find or launch function corresponding to the action %s:, error:[%s]",str(action_result), str(e))
        if isActionSucceed:
            self._actionServer.set_succeeded(action_result)
        else:
            self._actionServer.set_aborted()

def main():
    #""" main function
    #"""
    node = ColorDetectionNode()

if __name__ == '__main__':
    main()