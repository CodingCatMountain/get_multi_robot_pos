### 多机器人关节笛卡尔空间位置获取小任务
--------------------
_language:中文_

#### Dependence
---------
1. universal_robot 功能包
2. iiwa_stack 功能包
3. Baxter 功能包(似乎存在版本问题)

#### Usage

---------------

分别在两个终端窗口中输入

```Bash
roslaunch multi_robot ur5_iiwa_baxter_display.launch
```

```bash
roslaunch multi_robot joint_pos_echo.launch
```



#### Log

------
目前已经完成多个机器人关节空间的输出任务

节点图如下：

![节点图](./rosgraph.png)
