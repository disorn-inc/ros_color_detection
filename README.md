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

### 3.1  Messages
### 3.1.1 ColorD Message

Message holding color information, color names, rgb color, hsv color

string color_name
# color name without correction (black, white, gray)
string color_temp
# closest web color name
string color_web
# custom black, white, gray, dark brightness name
string color_brightness_name
# rgb[0]=R, rgb[1]=G, rgb[2]=B
float32[] rgb
# hsv[0]=H, hsv[1]=S, hsv[2]=V
float32[] hsv
# percentage of the current color into the image (after kmean clusterisation)
float32 percentage_of_img

### 3.1.2 ColorDList Message
Message holding main colors information

ros_color_detection_msgs/ColorD[] colorList

 ### 3.1  Subscribed Topics

 self.sub_rgb = rospy.Subscriber("/image", Image, self.rgb_callback, queue_size=1)
        self.pub_color = rospy.Publisher("/image_color", ColorDList, queue_size=1)

  #### 4.1.1 topic /image ([sensor_msgs/Image](http://docs.ros.org/api/sensor_msgs/html/msg/Image.html))
   Incoming images for color detection
        
 ### 3.2 Published Topics
  #### 4.2.1 topic /image_color ([ros_color_detection/ColorDList])
   List of dominant colors and associated names

            
 ### 3.3 Services
  #### 4.3.1 detect_color_srv ([ros_face_recognition/LearnFace](https://github.com/jacques-saraydaryan/ros_face_recognition/blob/master/srv/LearnFace.srv))
   Get main colors of the given image
  
 ### 3.4 Action
 #### 4.3.1 detect_color_action ([ros_face_recognition/LearnFace](https://github.com/jacques-saraydaryan/ros_face_recognition/blob/master/srv/LearnFace.srv))
 Get main colors of the given image

### 4.4  Params
 #### 4.4.1 kmean_cluster (int,default: 3)
  face_folder contains the initial labeled faces, these images are loaded at the node start
 
 #### 4.4.2 imgtest_folder (string)
 
 #### 4.4.3 is_process_displayed (bool, default: false) 
