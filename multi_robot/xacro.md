### xacro学习记录

-----------

_language:中文_

1. **案例**

   ```xml
   <xacro:macro name="pr2_arm" params="suffix parent reflect">
       <pr2_upperarm suffix="${suffix}" reflect="${reflect}" parent="${parent}"/>
       <pr2_forearm suffix="${suffix}" reflect="${reflect}" parent="elbow_flex_${suffix}"/>
   </xacro:macro>
   
   <xacro:pr2_arm suffix="left" reflect="1" parent="torso"/>
   <xacro:pr2_arm suffix="right" reflect="-1" parent="torso"/>
   ```

   上面的片段扩展为下面的样子

   ```xml
   <pr2_upperarm suffix="left" reflect="1" parent="torso"/>
   <pr2_forearm suffix="left" reflect="1" parent="elbow_flex_left"/>
   <pr2_upperarm suffix="right" reflect="-1" parent="torso"/>
   <pr2_upperarm suffix="right" reflect="-1" parent="elbow_flex_right"/>
   ```

2. **属性与属性块**

   ```xml
   <xacro:property name="the_radius" value="2.1"/>
   <xacro:property name="the_lenght" value="4.5"/>
   
   <geometry type="cylinder" radius="${the_radius}" length="${the_length}"/>
   ```

   _使用转义字符：{}_

   使用属性块的示例

   ```xml
   <xacro:property name="front_left_origin">
   	<origin xyz="0 0 0" rpy="0 0 0"/>
   </xacro:property>
   
   <pr2_wheel name="front_left_wheel">
   	<xacro:insert_block name="front_left_origin"/>
   </pr2_wheel>
   ```

3. **数学表达式**

   支持基本算术和变量替换：

   ```xml
   <xacro:property name="pi" value="3.1415926535897931"/>
   <circle circumference="${2.5*pi}"/>
   ```

   **Jade后ROS中更新的地方**: 一些更复杂的例子

   ```xml
   <xacro:property name="R" value="2"/>
   <xacro:property name="alpha" value="${30/180*pi}"/>
   <circle circumference="${2*pi*R}" pos="${sin(alpha)} ${cos(alpha)}"/>
   ```

4. **条件块**

   ```xml
   <xacro:if value="<expression>">
   	<...some xml code here .../>
   </xacro:if>
   <xacro:unless value="<expression>">
   	<...some xml code here .../>
   </xacro:unless>
   ```

   **==ROS Launch中的if与unless==**

   **if=value (optional)**
    **如果value值为真，包含标签及其内容**
    **unless=value (optional)**

   **除非value为假，包含标签及其内容**

5. **使用Rospack命令**

   xacro允许使用rospack命令

   ```xml
   <foo value="$(find xacro)"/>
   <foo value="$(arg myvar)"/>
   ```

   xacro目前支持roslaunch使用替换args替换所有rospack命令。

   比如在命令行中指定: myvar := true .

   在Indigo中更新的地方

   自从ROS Indigo, 它也可以定义默认值如下:

   ```xml
   <xacro:arg name="myvar" default="false"/>
   ```

   对于上面的语句可以像下面这样来使用

   ```xml
   <param name="robot_description" command="$(find xacro)/xacro.py $(arg model) myvar:=true"/>
   ```

6. **宏命令**

   xacro的主要特性是它对宏的支持.使用宏标签定义宏，并指定宏名称和参数列表。参数列表应该以空格分隔。它们变成宏观本地属性

   ```xml
   <xacro:macro name="pr2_caster" params="suffix *origin **content **anothercontent">
     <joint name="caster_${suffix}_joint">
       <axis xyz="0 0 1" />
     </joint>
     <link name="caster_${suffix}">
       <xacro:insert_block name="origin" />
       <xacro:insert_block name="content" />
       <xacro:insert_block name="anothercontent" />
     </link>
   </xacro:macro>
   
   <xacro:pr2_caster suffix="front_left">
       <pose xyz="0 1 0" rpy="0 0 0"/>
       <container>
       	<color name="yellow"/>
           <mass>0.1</mass>
       </container>
       <another>
       	<inertial>
           	<origin xyz="0 0 0.5" rpy="0 0 0"/>
               <mass value="1"/>
               <inertia ixx="100" ixy="0" ixz="0" iyy="100" iyz="0" izz="100"/>
           </inertial>
       </another>
   </xacro:pr2_caster>
   ```

   这一示例声明了两个参数：suffix和origin；

   其中origin加一个星号表示origin是一个块参数，而不是一个简单的文本参数。这里origin指的是一个元素即“pose”块。双星号版本“content”和“anothercontent”允许插入在随后可用的元素(在上面的示例中分别是“container”，"another")中传递的任意数量的元素。

   ```xml
   <joint name="caster_front_left_joint">
   	<axis xyz = "0 0 1"/>
   </joint>
   <link name="caster_front_left">
   	<pose xyz="0 1 0" rpy="0 0 0"/>
       <color name="yellow"/>
       <mass>0.1</mass>
       <intertial>
           <origin xyz="0 0 0.5" rpy="0 0 0"/>
           <mass value="1"/>
           <inertia ixx="100" ixy="0" ixz="0" iyy="100" izz="100"/>
       </intertial>
   </link>
   ```

   **按指定的顺序处理多个块参数**

   ```xml
   <xacro:macro name="reorder" params="*frist *second">
   	<xacro:insert_block name="second"/>
       <xacro:insert_block name="first"/>
   </xacro:macro>
   <reorder>
       <first/>
       <second/>
   </reorder>
   ```

   **宏的包含问题**:外部宏先展开，任何内部宏展开

   ```xml
   <a>
   	<xacro:macro name="foo" params="x">
       	<in_foo the_x="${x}"/>
       </xacro:macro>
       
       <xacro:macro name="bar" params="y">
       	<in_bar>
           	<xacro:foo x="${y}"/>
           </in_bar>
       </xacro:macro>
       
       <xacro:bar y="12"/>
   </a>
   ```

   将会变成：

   ```xml
   <a>
   	<in_bar>
       	<in_foo the_x="12.0"/>
       </in_bar>
   </a>
   ```

   

7. 默认参数的使用

   ```xml
   <xacro:macro name="foo" params="x:=${x} y:=${2*y} z:=0"/>
   ```

   从外部传入参数的值改变宏的参数 _使用^_

   ```xml
   <xacro:macro name="foo" params="p1 p2:=expr_a p3:=^ p4:=^|expr_b"
   ```

   | 管道表示如果没有从外部给定值则使用给定的值

   Jade后的本地性质: 定义在宏中的性质与宏是local的,外部不可见。使用可选属性: scope="parent | global"，属性定义可以导出到父作用域或全局作用域

8. **包含其它xacro文件**

   使用xacro:include标记来包含其它xacro文件

   ```xml
   <xacro:include filename="${find package}/other_file.xacro"/>
   <xacro:include filename="other_file.xacro"/>
   <xacro:include filename="$(cwd)/other_file.xacro"/>
   ```

   文件"other_file.xacro"将被xacro包含和扩展。Jade中的新功能：相对文件名是被解释为相对于当前文件的。注意当宏中include文件时,不是宏定义时,而是宏调用文件应该是用include！。

   $(cwd)显式允许访问当前工作目录中的文件。

   **为了避免各种包含文件的属性和宏之间的名称冲突，可以为包含的文件指定命名空间。**

   ```xml
   <xacro:include filename="other_file.xacro" ns="namespace"/>
   ```

   访问命名空间宏和属性是通过预先命名空间来实现的，用点分隔

   ```xml
   ${namespace.property}
   ```

   

9. **YAML语言支持**

   ```xml
   <xacro:property name="props" value="${dict(a=1,b=2,c=3)}"/>
   <xacro:property name="numbers" value="${1,2,3,4}"/>
   ```

   或者从YAML文件中加载

   ```xml
   <xacro:property name="props" value="$(load_yaml('props.yaml'))"/>
   ```

10. **使用CMakeList.txt进行构建**

    ```cmake
    # Generate .world files from .world.xacro files
    find_package(xacro REQUIRED)
    # You can also add xacro to the list of catkin packages:
    #   find_package(catkin REQUIRED COMPONENTS ... xacro)
    
    # Xacro files
    file(GLOB xacro_files ${CMAKE_CURRENT_SOURCE_DIR}/worlds/*.world.xacro)
    
    foreach(it ${xacro_files})
      # remove .xacro extension
      string(REGEX MATCH "(.*)[.]xacro$" unused ${it})
      set(output_filename ${CMAKE_MATCH_1})
    
      # create a rule to generate ${output_filename} from {it}
      xacro_add_xacro_file(${it} ${output_filename})
    
      list(APPEND world_files ${output_filename})
    endforeach(it)
    
    # add an abstract target to actually trigger the builds
    add_custom_target(media_files ALL DEPENDS ${world_files})
    ```

    更为简单的版本

    ```cmake
    file(GLOB xacro_files worlds/*.world.xacro)
    xacro_add_files(${xacro_files} TARGET media_files)
    ```

    如果你希望产生的文件具有.urdf后缀,那么请将将输入文件改为.urdf.xacro, .xacro后缀将会被CMake function移除。最后将会返回带有.urdf后缀的文件。

11. 元素与属性

    为了使用动态定义的元素与属性，你可以使用特殊的xacro tags

    ```xml
    <xacro:element xacro:name="${element_name}" [other attributes]>
    	[content]
    </xacro:element>
    <xacro:attribute name="${attribute_name}" value="${attribute_value}"/>
    ```

    \<xacro:attribute\>的使用例子

    ```xml
    <xacro:property name="foo" value="my_attribute_name"/>
    <tag>
    	<xacro:attribute name="${foo}" value="my_attribute_value"/>
    </tag>
    ```

    将会得到

    ```xml
    <tag my_attribute_name="my_attribute_value"/>
    ```

    

12. 处理顺序

    典型地，xacro首先载入所有的includes,然后处理所有property和macro定义，并最后实例化macros和判断表达式。所以，最新的属性或者macro定义将会覆盖原来的那个。此外，条件tags\<if\>与\<unless\>,对于macro或者属性定义以及包含的其它文件没有影响。

    Jade后的更新：

    自从ROS Jade后，xacro提供一个命令行选项--inorder,这将允许按顺序去处理整个文件夹。因此将会用到最新的属性和宏的最新定义。这将具有如下优点：

    * 如果标签分别至于宏内或者置于一个条件tags内，则可以推迟或者完全禁止包含文件
    * 可以属性或者宏参数指定包含的文件名
    * 通过改变全局范围的属性，如果在宏中使用这些属性，则宏的实例化可以产生不同的结果。
    * 属性的定义可以是有条件的
    * 宏可以在本地范围内定义属性，而不会影响外部

    因为--inorder处理是如此的有用，在Jade后的未来版本中，这一新的处理方式将会变为默认。

     you should check the compatibility of your xacro files. Usually, both  processing styles should give identical results. You can easily check  this like so: 

    ```bash
    rosrun xacro xacro file.xacro > /tmp/old.xml
    rosrun xacro xacro --inorder file.xacro > /tmp/new.xml
    diff /tmp/old.xml /tmp/new.xml
    ```

    If there are any differences shown, you should check and adapt your  xacro file. A common reason will be the late loading of calibration data (as properties). In this case, simply move them up front, i.e. before  usage. To facilitate search for wrongly placed property definitions, you can run xacro with option `--check-order`. If there are any problematic properties, they will be listed on stderr: 

    ```bash
    Document is incompatible to --inorder processing.
    The following properties were redefined after usage:
    foo redefined in issues.xacro
    ```

    Using the command-line option `-vv` or `-vvv` one can increase verbosity level to log all defintions of properties. 

13. 

