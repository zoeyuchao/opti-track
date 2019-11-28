# opti-track

运行Ros_env.launch文件，转换字符串格式的节点名称为vrpn_pose.py，订阅car_pose_server这个topic即可。

## optitrack使用教程

### 基础设施准备

插上黑色的网线，插上usb形状的key，打开桌面上的motive（桌面上的Motive_2.0.2_Final_x64是安装包！）

### 校准

首先**edit->application settings**，然后**layout->calibrate**，在右侧的**camera calibration**工具栏选择**mask visible**屏蔽已经存在的噪点（在这一步时，可以将界面正中的的  perspective view上面的toolbar的第一个选项点一下改为multi camera 2d view，切换成  camera preview这时可以看到每个摄像机，上面都有一些白色噪点（现在没铺地面，所以有很多的反光，界面左侧有一个devices工具栏，该工具栏上有一个按钮可以使相机画面在只有光点的画面和能成像的画面之间切换），点完**mask visible**就会发现噪点变红，表示噪点  被屏蔽了），我们也可以点旁边的**clear mask**重置这一过程。

### 标定

**点击start wanding**（这一栏下面的optiwand对应我们的丁字杆，如果丁字杆的三个反光点都在b则选择cw-250，若是都在a则选择cw-500，我们这个场地用cw-250），然后手持丁字杆在场地中晃悠，直到calibration中所有摄像机的采样点都超过3000，然后点击calculate，如果计算结果中的wanderror小于0.2结果就合格（实际上我们的场地很一般，现在用的精度只有0.5）。

### 建立坐标系，完成

此时我们应该会进入camera calibration工具栏的第二栏ground plane，我们将直角杆放入场地中，然后点击**set ground plane**即可保存校准结果。该文件为cal文件。

### 开始记录

首先打开刚刚创建的cal文件，将小车放入场地中，将小车上的几个点框起来，右键选择**Rigid Body->Create Rigid Body**，然后按空格开始记录小车的移动（今天没有开始使用同步器，使用同步器之后再更新这里），记录完后仍按空格停止记录。

### 保存

**file->save current take**将刚刚记录的结果保存，文件为tak文件。

### 数据导出

打开刚刚的tak文件，**file->export tracking data**，结果会存为一个csv文件，我们就能用excel查看结果了（关于excel中数据的排列方式需要日后进一步补充）
