# 1. ros_color_detection

## 2. Description
the project provides a ros node for getting the dominant colors of a given image. The following steps are done:
  The RGB color image is transformed into HSV Color image
  The Kmean clustering approach is used on the H of the HSV color image values.
  The given clusters are named fixing S and V with the average S and V values of the cluster and selecting the webcolor closest to the given value
  Another simple color name is given fixing V value to 1 and testing Gray, black an white value through fixed threshold


1 launch file is available getting the configuration from the common_color.yaml file:
```python
  #number of dominant color to extract
  kmean_cluster: 3
  #Test image color location
  imgtest_folder: "/home/jsaraydaryan/ros_robotcupathome_ws/src/people_management/ros_color_detection/ros_color_detection_node/data"
  #Displayed resulted clustering currently not working
  is_process_displayed: True
```

## 3. Node

 ### 3.1  Subscribed Topics

  #### 4.1.1 topic /image ([sensor_msgs/Image](http://docs.ros.org/api/sensor_msgs/html/msg/Image.html))
   Incoming images for color detection
        
 ### 3.2 Published Topics
  #### 4.2.1 topic /image_color ([ros_color_detection/ColorDList](https://github.com/jacques-saraydaryan/ros_color_detection/blob/master/ros_color_detection_msgs/msg/ColorD.msg))
   List of dominant colors and associated names

            
 ### 3.3 Services
  #### 4.3.1 detect_color_srv ([ros_color_detection/ros_color_detection_srvs](https://github.com/jacques-saraydaryan/ros_color_detection/blob/master/ros_color_detection_srvs/srv/DetectColorFromImg.srv))
   Get main colors of the given image
  
 ### 3.4 Action
 #### 4.3.1 detect_color_action ([ros_face_recognition/LearnFace](https://github.com/jacques-saraydaryan/ros_face_recognition/blob/master/srv/LearnFace.srv))
 Get main colors of the given image

### 4.4  Params
 #### 4.4.1 kmean_cluster (int,default: 3)
  face_folder contains the initial labeled faces, these images are loaded at the node start
 
 #### 4.4.2 imgtest_folder (string)
 
 #### 4.4.3 is_process_displayed (bool, default: false) 
