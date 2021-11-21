### TF学习日记

----------

_language:中文_

[TF2官网教程](http://wiki.ros.org/tf2/Tutorials)

[旋量的介绍](https://zhuanlan.zhihu.com/p/172092658)

[TF_Python_version](https://www.cnblogs.com/xialuobo/p/6097806.html#:~:text=ROS%20%E4%B8%ADTF%E5%AD%A6%E4%B9%A0%201.%E4%BB%80%E4%B9%88%E6%98%AFTF%20TF%E6%98%AF%E5%A4%84%E7%90%86%E6%9C%BA%E5%99%A8%E4%BA%BA%E4%B8%8D%E5%90%8C%E4%BD%8D%E7%BD%AE%E5%9D%90%E6%A0%87%E7%B3%BB%E7%9A%84%E4%B8%80%E4%B8%AA%E5%8C%85%EF%BC%8C%E6%9C%BA%E5%99%A8%E4%BA%BA%E4%B8%8D%E5%90%8C%E9%83%A8%E4%BD%8D%E5%92%8C%E4%B8%96%E7%95%8C%E7%9A%84%E5%9D%90%E6%A0%87%E7%B3%BB%E4%BB%A5,tree%20structure%20%E7%9A%84%E5%BD%A2%E5%BC%8F%E5%AD%98%E5%82%A8%E8%B5%B7%E6%9D%A5%EF%BC%8CTF%E5%8F%AF%E4%BB%A5%E4%BD%BF%E4%BB%BB%E4%BD%95%E4%B8%A4%E4%B8%AA%E5%9D%90%E6%A0%87%E7%B3%BB%E4%B9%8B%E9%97%B4%E7%9A%84%E7%82%B9%20%E5%90%91%E9%87%8F%E7%9B%B8%E4%BA%92%E8%BD%AC%E5%8C%96%E3%80%82)

1. **TF经典工具安装**

   ```bash
   $ sudo apt-get install ros-$ROS_DISTRO-turtle-tf2 ros-$ROS_DISTRO-tf2-tools ros-$ROS_DISTRO-tf
   ```

2. 范例

   ```bash
   $roslaunch turtle_tf2 turtle-tf2_demo.launch
   ```

   此命令行会召唤出两只乌龟

   ```bash
   $rosrun turtlesim turtle_teleop_key
   ```

   通过箭头来移动一只乌龟，可以看到另一只乌龟一直追

3. 实现原理: tf2库创建三个坐标系:==世界坐标系==，==turtle1坐标系==和==turtle2坐标系==。tf2广播器发布turtle坐标系，并使用tf2侦听器计算turtle坐标系中的差异并移动一只乌龟跟随另一只乌龟。

4. **tf2工具**

   4.1 view_frames 创建tf2通过ROS广播的所有坐标系的示意图，他们的相互关系

   ```bash
   $rosrun tf2_tools view_frames.py
   ```

   tf2侦听器正在侦听通过ROS广播的坐标系，并绘制坐标系连接方式的树。要查看树：

   ```bash
   $evince frames.pdf
   ```

   

   4.2 tf_echo报告 通过ROS广播的任何两个坐标系之间的转换关系

   ```bash
   $rosrun tf tf_echo [reference_frame] [target_frame]
   ```

   看一下turtle2坐标系相对于turtle1坐标系的变换

   ```bash
   $rosrun tf tf_echo turtle1 turtle2
   ```

   

   4.3 rviz

   rviz,可视化工具,用于检查tf2坐标系。使用turtle_tf2配置文件，使用rviz的-d选项启动rviz

   ```bash
   $ rosrun rviz rviz  -d 'rospack find turtle_tf2'/rviz/turtle_rviz.rviz
   ```

   _In Here, 还可学习到如何使用rviz调用别的包中的rviz文件_

5. **代码部分**

   将静态坐标系广播到tf2

   ```bash
   $ catkin_create_pkg learning_tf2 tf2 tf2_ros roscpp turtlesim
   ```

   **How to broadcast transforms**

   ```c++
   #include <ros/ros.h>
   #include <tf2_ros/static_transform_broadcaster.h>
   #include <geometry_msgs/TransformStamped.h>
   #include <tf2/LinearMath/Quaternion.h>
   
   std::string static_turtle_name;
   int main(int argc,char** argv)
   {
       ros::init(argc,argv,"my_static_tf2_broadcaster");//初始化ros节点
       if(argc !=8)
       {
           ROS_ERROR("Invalid number of parameters\nusage: static_turtle_tf2_broadcaster child_frame_name x y z roll pitch yaw");
           return -1;
       }
   	if(strcmp(argv[1],"world")==0)
     	{
       ROS_ERROR("Your static turtle name cannot be 'world'");
       return -1;
     	}
       static_turtle_name=argv[1];
       
       static tf2_ros::StaticTransformBroadcaster static_broadcaster;
       geometry_msgs::TransformStamped static_transformStamped;
       
       static_transformStamped.header.stamp = ros::Time::now();
       static_transformStamped.header.frame_id = "world";
       static_transformStamped.child_frame_id = static_turtle_name;
       static_transformStamped.transform.translation.x = atof(argv[2]);
       static_transformStamped.transform.translation.y = atof(argv[3]);
   	static_transformStamped.transform.translation.z = atof(argv[4]);
       tf2::Quaternion quat;
       quat.setRPY(atof(argv[5]),atof(argv[6]),atof(argv[7]));
       static_transformStamped.transform.rotation.x = quat.x();
       static_transformStamped.transform.rotation.y = quat.y();
       static_transformStamped.transform.rotation.z = quat.z();
       static_transformStamped.transform.rotation.w = quat.w();
       static_broadcaster.sendTransform(static_transformStamped);
       ROS_INFO("Spinning until killed publishing %s to world",static_turtle_name.c_str());
       ros::spin();
       return 0;
   };
   ```

   main函数中没有while循环，只执行一次。

   相当于设定一个静态(不变)的坐标系和世界坐标系的转换(TF)

   编译运行，在CMakeLists.txt中添加

   ```cmake
   add_executable(static_turtle_tf2_broadcaster src/static_turtle_tf2_broadcaster.cpp)
   target_link_libraries(static_turtle_tf2_broadcaster  ${catkin_LIBRARIES} )
   
   ```

   

   编译、运行三板斧

   ```bash
   $ catkin_make
   $ source devel/setup.bash
   $ roscore rosrun learning_tf2 static_turtle_tf2_broadcaster mystaticturtle 0 0 1 0 0 0
   ```

   **因为是静态坐标(父坐标系默认为"world")**

   ```bash
   $ rostopic echo /tf_static
   ```

   **/tf_static这一topic可能会存放所有通过StaticTransformBroadcaster静态坐标转换**

6. **tf2_ros**

   tf2_ros除了提供相应的头文件外还有名为static_transform_publisher的可执行文件

   ```markdown
   static_transform_publisher x y z yaw pitch roll frame_id child_frame_id
    
   Publish a static coordinate transform to tf2 using an x/y/z offset in meters and quaternion. 
   ```

7. **tf2动态坐标变换**

   静态: 两坐标变换关系不变

   动态: 两坐标变换关系改变

   ```bash
   $ catkin_create_pkg learning_tf2 tf2 tf2_ros roscpp rospy turtlesim
   ```

   代码

   ```c++
   #include <ros/ros.h>
   #include <tf2/LinearMath/Quaternion.h>
   #include <tf2_ros/transform_broadcaster.h>
   #include <geometry_msgs/TransformStamped.h>
   #include <turtlesim/Pose.h>
   
   std::string turtle_name;
   
   void poseCallback(const turtlesim::PoseConstPtr& msg){
       static tf2_ros::TransformBroadcaster br;
       geometry_msgs::TransformStamped transformStamped;
       
       transformStamped.header.stamp =ros::Time::now();
       transformStamped.header.frame_id = "world";
       transformStamped.child_frame_id = turtle_name;
       transformStamped.transform.translation.x = msg->x;
       transformStamped.transform.translation.y = msg->y;
       transformStamped.transform.translation.z = 0.0;
       tf2::Quaternion q;
       q.setRPY(0,0,msg->theta);
       transformStamped.transform.rotation.x =q.x();
       transformStamped.transform.rotation.y =q.y();
       transformStamped.transform.rotation.z =q.z();
       transformStamped.transform.rotation.w =q.w();
       
       br.sendTransform(transformStamped);
   }
   
   int main(int arg,char** argv){
       ros::init(argc,argv,"my_tf2_broadcaster");
       ros::NodeHandle private_node("~");
       if(! private_node.hasParam("turtle"))
       {
           if(argc!=2){ROS_ERROR("need turtle name as argument")；
               return -1；}；
           turtle_name=argv[1];
       }
       else{
           private_node.getParam("turtle",turtle_name);
       }
       ros::NodeHandle node;
       ros::Subscriber sub=node.subscribe(turtle_name+"/pose",10,$poseCallback);
       ros::spin();
       return 0;
   }
   ```

   编译运行三板斧

   ```cmake
   ### CMakeLists.txt中加入
   add_executable(turtle_tf2_broadcaster src/turtle_tf2_broadcaster.cpp)
   target_link_libraries(turtle_tf2_broadcaster
    ${catkin_LIBRARIES}
   )
   ```

   ```bash
   $ catkin_make
   ```

   ```xml
     <launch>
        <!-- Turtlesim Node-->
       <node pkg="turtlesim" type="turtlesim_node" name="sim"/>
   
       <node pkg="turtlesim" type="turtle_teleop_key" name="teleop" output="screen"/>
       <!-- Axes -->
       <param name="scale_linear" value="2" type="double"/>
       <param name="scale_angular" value="2" type="double"/>
   
       <node pkg="learning_tf2" type="turtle_tf2_broadcaster"
             args="/turtle1" name="turtle1_tf2_broadcaster" />
       <node pkg="learning_tf2" type="turtle_tf2_broadcaster"
             args="/turtle2" name="turtle2_tf2_broadcaster" />
     </launch>
   ```

   

   

   ```bash
   roslaunch learning_tf2 start_demo.launch
   ```

   显示效果

   ```bash
   $ rosrun tf tf_echo /world /turtle1
   ```

8. 编写一个TF监听器

   ```c++
   #include <ros/ros.h>
   #include <tf2_ros/transform_listener.h>
   #include <geometry_msgs/TransformStamped.h>
   #include <geometry_msgs/Twist.h>
   #include <turtlesim/Spawn.h>
   
   int main(int argc,char** argv){
       ros::init(argc,argv,"my_tf2_listener");
       
       ros::NodeHandle node;
       
       // 新添加一个turtle
       ros::service::waitForService("spawn");
       ros::ServiceClient spawner=node.serviceClient<turtlesim::Spawn>("spawn");
       turtlesim::Spawn turtle;
       turtle.request.x = 4;
       turtle.request.y = 2;
       turtle.request.theta = 0;
       turtle.request.name="turtle2";
       spawner.call(turtle);
       
       ros::Publisher turtle_vel = node.advertise<geometry_msgs::Twist>("turtle2/cmd_vel",10);
       
       tf2_ros::Buffer tfBuffer;
       tf2_ros::TransformListener tfListener(tfBuffer);
       //此构造函数会需要传入一个Buffer，同时会启动多线程
       
       ros::Rate rate(10.0);
       while(node.ok()){
           geometry_msgs::TransformStamped transformStamped;
           try{
               transformStamped = tfBuffer.lookupTransform("turtle2","turtle1",ros::Time(0));
           }
           catch(tf2::TransformException &ex){
               ROS_WARN("%s",ex.what());
               ros::Duration(1.0).sleep();
               continue;
           }
           
           geometry_msgs::Twist vel_msg;
           
           vel_msg.angular.z = 4.0*atan2(transformStamped.transform.translation.y,transformStamped.transform.translation.x);
           vel_msg.linear.x = 0.5*sqrt(pow(transformStamped.transform.translation.x,2)+pow(transformStramped.transform.translation.y,2));
           turtle_vel.pusblish(vel_msg);
           
           rate.sleep();
       }
       return 0;
   };
   ```

   编译运行几板斧

   ```cmake
   add_executable(turtle_tf2_listener src/turtle_tf2_listener.cpp)
   target_link_libraries(turtle_tf2_listener
    ${catkin_LIBRARIES}
   )
   ```

   同时添加到launch文件中

   ```c++
    <launch>
      ...
      <node pkg="learning_tf2" type="turtle_tf2_listener"
            name="listener" />
    </launch>
   ```

   运行

   ```bash
   $ roslaunch learning_tf2 start_demo.launch
   ```

9. **添加额外的固定坐标系**

   **where_to_add_frames?**
   
   tf2 builds up a tree structure of frames; it does not allow a closed loop in the frame structure. This means that a frame only has one single parent, but it can have multiple children. Currently our tf2 tree contains three frames: world, turtle1 and turtle2. The two turtles are children of world. If we want to add a new frame to tf2, one of the three existing frames needs to be the parent frame, and the new frame will become a child frame.
   
   **How to add a frame?**
   
   ```c++
   #include <ros/ros.h>
   #include <tf2_ros/transform_broadcaster.h>
   #include <tf2/LinearMath/Quaternion.h>
   
   int main(int argc,char** argv){
       ros::init(argc,argv,"my_tf2_broadcaster");
       ros::NodeHanle node;
       
       tf2_ros::TransformBroadcaster tfb;
       geometry_msgs::TransformStamped transformStamped;
       
       transformStamped.header.frame_id = "turtle1";
       transformStamped.child_frame_id = "carrot1";
       transformStamped.transform.translation.x = 0.0;
       transformStamped.transform.translation.y = 2.0;
       transformStamped.transform.translation.z = 0.0;
       tf2::Quaternion q;
       q.serRPY(0,0,0);
       transformStamped.transform.rotation.x= q.x();
       transformStamped.transform.rotation.y = q.y();
       transformStamped.transform.rotation.z = q.z();
       transformStamped.transform.rotation.w = q.w();
       
       ros::Rate rate(10.0);
       while(node.ok()){
           transformStamped.header.stamp = ros::Time::now();
           tfb.sendTransform(transformStamped);
           rate.sleep();
           printf("sending\n");
       }
   };
   ```
   
   编译运行几板斧
   
   ```cmake
   add_executable(frame_tf2_broadcaster src/frame_tf2_broadcaster.cpp)
   target_link_libraries(frame_tf2_broadcaster
    ${catkin_LIBRARIES}
   )
   ```
   
   ```xml
     <launch>
       ...
       <node pkg="learning_tf2" type="frame_tf2_broadcaster"
             name="broadcaster_frame" />
     </launch>
   ```
   
   如何检查效果？打开turtle_tf2_listener.cpp作如下修改
   
   ```c++
   transformStamped = listener.lookupTransform("/turtle2", "/carrot1",
                               ros::Time(0));
   ```
   
   如果想Broadcasting一个移动的坐标系，请将下面的代码拷贝至while循环内
   
   ```c++
   transformStamped.transform.translation.x = 2.0*sin(ros::Time::now().toSec());
      2   transformStamped.transform.translation.y = 2.0*cos(ros::Time::now().toSec());
   ```
   
   
   
10. 指定获取transform的时间

    原来的代码

    ```c++
     try{
        transformStamped = listener.lookupTransform("/turtle2", "/carrot1", ros::Time(0));
      } catch (tf2::TransformException &ex) {
        ROS_WARN("Could NOT transform turtle2 to turtle1: %s", ex.what());
      }
    ```

    修改后的代码

    ```c++
      try{
        transformStamped = tfBuffer.lookupTransform("turtle2", "turtle1", ros::Time(0));
      } catch (tf2::TransformException &ex) {
        ROS_WARN("Could NOT transform turtle2 to turtle1: %s", ex.what());
      }
    ```

    You can also see we specified a time equal to 0. For tf2, time 0 means  "the latest available" transform in the buffer. Now, change this line to get the transform at the current time, "`now()`": 

    ```c++
    try{
        transformStamped = tfBuffer.lookupTransform("turtle2", "turtle1", ros::Time::now());
      } catch (tf2::TransformException &ex) {
        ROS_WARN("Could NOT transform turtle2 to turtle1: %s", ex.what());
      }
    ```

    再次运行会出现报错

    ```c++
    [ERROR] 1253918454.307455000: Extrapolation Too Far in the future: target_time is 1253918454.307, but the closest tf2  data is at 1253918454.300 which is 0.007 seconds away.Extrapolation Too Far in the future: target_time is 1253918454.307, but the closest tf2 data is at 1253918454.301 which is 0.006 seconds away. See http://pr.willowgarage.com/pr-docs/ros-packages/tf2/html/faq.html for more info. When trying to transform between /turtle1 and /turtle2. See http://www.ros.org/wiki/tf2#Frequently_Asked_Questions
    ....
    ```

    **报错原因：** 每一个listener有一个buffer用于存储不同的tf2广播发来的坐标系变换。当一个广播发出一个变换时，它需要一些时间来使得变换存进buffer中。(往往是需要几milliseconds).所以当你要求“now”坐标变换时，你应该等待几milliseconds.

    _**等待变换：**_向lookupTransform()中加入Duration参数

    ```c++
    try{
        transformStamped = tfBuffer.lookupTransform("turtle2", "turtle1", ros::Time::now(), 
                                                    ros::Duration(3.0));
      } catch (tf2::TransformException &ex) {
        ROS_WARN("Could NOT transform turtle2 to turtle1: %s", ex.what());
      }
    ```

    The `lookupTransform()` can take four arguments. The 4th is an optional timeout. It will block for up to that duration waiting for it to timeout.   (`ros::Duration` time values are given in seconds or seconds and nanoseconds. 

    So `lookupTransform``()` will actually **block** until the transform between the two turtles becomes available (this  will usually take a few milliseconds), OR --if the transform does not  become available-- until the timeout has been reached. 

    当再次出现如下报错

    ```bash
    [ERROR] 1253918454.307455000: Extrapolation Too Far in the future: target_time is 1253918454.307, but the closest tf2  data is at 1253918454.300 which is 0.007 seconds away.Extrapolation Too Far in the future: target_time is 1253918454.307, but the closest tf2  data is at 1253918454.301 which is 0.006 seconds away. See http://pr.willowgarage.com/pr-docs/ros-packages/tf2/html/faq.html for more info. When trying to transform between /turtle1 and /turtle2. See http://www.ros.org/wiki/tf2#Frequently_Asked_Questions
    ```

    This happens because `turtle2` takes a non-zero time to spawn and start publishing tf2 frames. So the first time that you ask for now the `/turtle2` frame may not have existed, when the transform is requested the  transform may not exist yet and fails the first time. After the first  transform all the transforms exist and the turtle behaves as expected. 

11. **Time travel**

    原来的代码

    ```c++
     try{
        ros::Time now = ros::Time::now();
        transformStamped= tfBuffer.lookupTransform("turtle2", "turtle1",
                                 now);
    ```

    Now, instead of making the second turtle go to where the first turtle is **now**, make the second turtle go to where the first turtle was **5 seconds ago**: 

    修改后的代码

    ```c++
    try{
        ros::Time past = ros::Time::now() - ros::Duration(5.0);
        transformStamped = tfBuffer.lookupTransform("turtle2", "turtle1",
                                   past, ros::Duration(1.0));
    ```

    So now, if you would run this, what would you expect  to see? Definitely during the first 5 seconds the second turtle would  not know where to go, because we do not yet have a 5 second history of  the first turtle. But what after these 5 seconds? Let's just give it a  try: 

    所以现在，如果你运行这一代码，你期待会发生什么？肯定是在头5秒内第二只乌龟不知道去哪里，因为我们没有5秒前的历史。如果是五秒之后呢？可以试一试

    ```bash
    $ catkin_make
    $ roslaunch learning_tf2 start_demo.launch
    ```

    ![random.png](http://wiki.ros.org/tf2/Tutorials/Time%20travel%20with%20tf2%20%28C%2B%2B%29?action=AttachFile&do=get&target=random.png)

    乌龟将会到处乱转像截屏一样。所以发生了什么呢？

    * 我们询问tf2"*What was the pose of `/turtle1` 5 seconds ago, relative to `/turtle2` 5 seconds ago?*",This means we are controlling the second turtle based on where it was 5  seconds ago as well as where the first turtle was 5 seconds ago.
    * 我们真正想问的是:  *"What was the pose of `/turtle1` 5 seconds ago, relative to the current position of the `/turtle2`?"*.   

    **实现正确问法的代码**

    ```c++
    try{
        ros::Time now = ros::Time::now();
        ros::Time past = now - ros::Duration(5.0);
        transformStamped = tfBuffer.lookupTransform("turtle2", now,
                                 "turtle1", past,
                                 "world", ros::Duration(1.0));
    ```

    在过去的那个时刻将会计算从第一个乌龟到世界坐标系的变化，当时间变到现在，tf2计算从世界坐标系到第二只乌龟。

    六个参数的意味是：

    1. Give the transform from this frame,
    2. at this time...
    3. ...to this frame,
    4. at this time.
    5. Specify the frame that does not change over time, in this case the "/world" frame, and 
    6. the time-out.
