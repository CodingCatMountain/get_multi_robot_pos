### 多机器人关节笛卡尔空间位置获取小任务
--------------------
_language:中文_

#### Dependence
---------
1. universal_robot 功能包
2. iiwa_stack 功能包
3. Baxter 功能包(似乎存在版本问题)

#### Usage
------
```Bash
roslaunch ur_description view_ur5.launch
rosrun multi_robot single_ur_pos.py
rostopic echo single_ur5_pos
```

#### Log
------
目前仅完成单个ur5的这项工作，后续将从过去的多机器人项目中学习如何往单一rviz界面中导入多个机器人并完成相应的关节位置输出
