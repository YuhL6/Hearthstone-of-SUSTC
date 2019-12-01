# 				南方科技大学炉石传说开发手册（草稿六）

#### 概述

该软件分为三大块，分别为<u>客户端</u>、<u>游戏端</u>、<u>服务器端</u>，其中客户端和游戏端统称<u>前端</u>，五大系统，<u>登录系统</u>、<u>用户系统</u>、<u>好友系统</u>、<u>对战系统</u>、<u>抽卡系统</u>。

用户的信息分为两类：**隐私信息**、**基本信息**、和**用户扩展信息**。隐私信息包括<u>用户账号</u>、<u>用户密码</u>。<u>基本信息</u>包括<u>用户昵称</u>（不可重复）、<u>用户状态</u>、<u>用户Rank分</u>、<u>用户排名信息</u>。<u>扩展信息</u>包括<u>用户好友基本信息</u>、<u>用户对战信息</u>、<u>当前Rank榜前十名</u>。

当软件打开后先显示<u>登录系统</u>界面，主要功能是核对身份。

在登录成功之后进入<u>用户系统</u>界面，用户系统的主要功能是展示<u>用户基本信息</u>、<u>用户扩展信息</u>以及其它系统的入口。

用户在<u>用户系统</u>界面点开好友栏时将打开<u>好友系统</u>，<u>好友系统</u>将展示好友的<u>基本信息</u>，并且具有聊天功能。

#### 数据库

table: user_info

| Field          | Type         | Null | Key  | Default | Extra |
| -------------- | ------------ | ---- | ---- | ------- | ----- |
| user_id        | int(8)       | NO   | PRI  | NULL    |       |
| user_name      | varchar(10)  | NO   | UNI  | NULL    |       |
| password       | varchar(200) | NO   |      | NULL    |       |
| status         | int(11)      | NO   |      | 0       |       |
| total_game_num | int(11)      | NO   |      | 0       |       |
| win_rate       | float        | NO   |      | 0       |       |
| user_email     | varchar(30)  | YES  | UNI  | NULL    |       |
table: relation

| Field    | Type        | Null | Key  | Default | Extra      |
| -------- | ----------- | ---- | ---- | ------- | ---------- |
| cnt      | int(11)     | NO   | PRI  | NULL    | auto_extra |
| user_id1 | int(8)      | NO   |      | NULL    |            |
| name1    | varchar(10) | YES  |      | NULL    |            |
| user_id2 | int(8)      | NO   |      | NULL    |            |
| name2    | varchar(10) | YES  |      | NULL    |            |






#### 登录系统

<u>登录系统</u>包含有<u>注册</u>、<u>登录</u>、<u>修改密码</u>、<u>忘记密码</u>、<u>同步信息</u>等功能。

<u>登录系统</u>服务器端的端口为14290。

###### 注册

用户注册时需要填写如下信息：<u>邮箱地址</u>（用作账号）、<u>密码</u>（两次确认）、<u>昵称</u>（用户选择），**前端**应当核对<u>邮箱地址是否符合格式</u>、<u>两次密码是否一致</u>。确认无误后前端与服务器建立连接并发送**注册信息**以告知服务器。服务器将检索数据库判断<u>邮箱地址</u>是否已经注册、<u>用户昵称</u>是否已经占用，如有重复则返还**注册拒绝信息**，否则发送验证码到用户邮箱，前端要求用户填写验证码并且发送用户填写的验证码给服务器，如验证码不符合服务器返还<u>注册拒绝信息</u>，符合则返还**注册确认信息**。

注册之后服务器会关闭连接，登录需要重新连接。

> **注册信息**格式：
>
> "200 time_stamp\r\n"
>
> "User_id User_passport\r\n"
>
> "User_name\r\n"
>
> "\r\n"
>
> **注册拒绝信息**格式：
>
> "201 time_stamp\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **注册确认信息**格式：
>
> "202 time_stamp\r\n"
>
> "\r\n"

**Note**: information are split by space ' '



###### 登录

前端在登录时与服务器建立连接，应发送**登录信息**\*，服务器在接受到信息时，核对账号密码，如不符合则返还**登录拒绝信息**\*，前端应检测发送频率，如过于频繁则应当限制登录时间；如接受信息符合，则返还**登录许可信息**\*，并更新数据库中用户**状态**\*，前端在接收到许可信息后给予登录，而后服务器返还对应**用户信息块**\*，前端在接收到信息块之后默认更新信息块。

> **登录信息**格式：
>
> "210 time_stamp\r\n"
>
> "User_id password\r\n"
>
> "\r\n"
>
> **登录拒绝信息**格式:
>
> "211 time_stamp\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **登录许可信息**格式:
>
> "212 time_stamp\r\n"
>
> "OTHER_MESSAGE\r\n"
>
> "\r\n"

**Note**: information are split by space ' ' and end with '/r/n'

​		  OTHER_MESSAGE包含用户信息，按顺序带有如下附件：<u>在线好友列表</u>、<u>用户战绩信息</u>、<u>排位信息</u>。其中在线好友列表格式为：<u>好友名</u>、<u>备注</u>（如存在），战绩信息格式为：<u>总场数</u>、<u>胜率</u>，排位信息格式为：<u>Rank分</u>、<u>用户昵称</u>、<u>用户胜率</u>。2



###### 修改密码

修改密码有两种方式：<u>通过现有密码进行修改</u>，<u>通过邮箱验证码进行修改</u>。

<u>通过现有密码进行修改</u>需要用户提供和<u>账号</u>和<u>当前密码</u>并填写<u>修改密码</u>，并且发送信息给服务器，若<u>当前密码</u>正确服务器则返回**修改成功信息**\*，<u>当前密码</u>错误则返回**修改失败信息**\*。

> **通过旧密码修改密码**格式：
>
> "220 time_stamp/r/n"
>
> "User_id old_password/r/n"
>
> "New_password/r/n"
>
> "/r/n"



###### 忘记密码

忘记密码同<u>通过邮箱验证码进行修改</u>。

> **通过邮件修改密码**格式：
>
> "230 time_stamp /r/n"
>
> "User_id /r/n"
>
> "/r/n"

**Note**: information are split by space ' '



> **Method Code**：							**Meaning:**
>
> 200												 注册信息
>
> 210                                                 登陆信息
>
> 220                                                 修改密码（通过旧密码）
>
> 230											     修改密码（通过邮件）



#### 用户系统

###### 购买卡包

> **购买卡包**格式：
>
> "300 time_stamp/r/n"
>
> "User_id/r/n"
>
> "/r/n"



###### 抽取卡牌

服务器将生成随机数来确定抽中的卡牌，并将之返还给客户端。服务器要注意抽中的卡牌不能与已有卡牌重叠。

> **抽取卡牌**格式：
>
> "305 time_stamp/r/n"
>
> "User_id/r/n"
>
> **错误信息**格式:
>
> "306 time_stamp/r/n"
>
> "REASON/r/n"
>
> **抽取成功**格式:
>
> "307 time_stamp/r/n"
>
> "Card_num/r/n"
>
> "/r/n"



###### 获取个人拥有卡牌

> **抽取卡牌**格式：
>
> "310 time_stamp/r/n"
>
> "User_id/r/n"
>
> "/r/n"
>
> **错误信息**格式:
>
> "311 time_stamp/r/n"
>
> "REASON/r/n"
>
> "/r/n"
>
> **抽取成功**格式:
>
> "312 time_stamp/r/n"
>
> "Card_num/r/n"
>
> "/r/n"



###### 获取卡组

> **获取卡组**格式：
>
> "315 time_stamp /r/n"
>
> "User_id list_name/r/n"
>
> **错误信息**格式:
>
> "316 time_stamp/r/n"
>
> "REASON/r/n"
>
> **获取成功**格式:
>
> "317 time_stamp/r/n"
>
> "list_names/r/n"



###### 新建卡组

> **新建卡组**格式：
>
> "320 time_stamp /r/n"
>
> "User_id list_name/r/n"
>



###### 获取卡组中卡牌

> **获取卡牌**格式：
>
> "325 time_stamp /r/n"
>
> "User_id list_name/r/n"
>
> **错误信息**格式:
>
> "326 time_stamp/r/n"
>
> "REASON/r/n"
>
> **获取成功**格式:
>
> "327 time_stamp/r/n"
>
> "card_numbers/r/n"



###### 删除卡组

> **删除卡组**格式：
>
> "330 time_stamp/r/n"
>
> "User_id list_number/r/n"
>



###### 卡组加牌

> **卡组加牌**格式：
>
> "340 time_stamp/r/n"
>
> "User_id list_name/r/n"
>
> "card_number/r/n"



###### 列出房间

> **列出房间**格式：
>
> "350 time_stamp/r/n"
>
> "User_id/r/n"
>
> **没有房间**格式:
>
> "351 time_stamp/r/n"
>
> "User_id REASON/r/n"
>
> **有房间**格式:
>
> "352 time_stamp/r/n"
>
> "User_id rooms_information/r/n"



###### 创建房间

> **创建房间**格式：
>
> "360 time_stamp /r/n"
>
> "User_id /r/n"
>



###### 加入房间

> **加入房间**格式：
>
> "370 time_stamp/r/n"
>
> "User_id room_number/r/n"
>
> **加入失败**格式：
>
> "371 time_stamp/r/n"
>
> "User_id reason/r/n"
>
> **加入成功**格式：
>
> "372 time_stamp/r/n"
>
> "User_id/r/n"



###### 准备游戏

> **准备游戏**格式：
>
> "380 time_stamp/r/n"
>
> "User_id/r/n"
>



###### 开始游戏

> **开始游戏**格式：
>
> "390 time_stamp/r/n"
>
> "User_id/r/n"
>
> **开始失败**格式：
>
> "391 time_stamp/r/n"
>
> "User_id reason/r/n"
>
> **开始成功**格式：
>
> "392 time_stamp/r/n"
>
> "User_id/r/n"



###### 退出房间

> **退出房间**格式：
>
> "395 time_stamp/r/n"
>
> "User_id /r/n"
>



#### 好友系统

###### 请求好友

添加好友支持通过**用户账号**及**用户昵称**添加，由客户端判断Receiver是账号(int, 400)还是昵称(String, 405)，发送请求前客户端需要判断是否已经添加为好友，发送后服务器将再进行一次判断。

> **请求好友**格式：
>
> "400 time_stamp /r/n"
>
> "User_id Receiver_name/r/n"
>



###### 接受好友请求

> **接受好友申请**格式：
>
> "410 time_stamp /r/n"
>
> "User_id Sender_name/r/n"
>



###### 发送消息

只能给在线好友发送信息，离线好友不可

> **发送消息**格式：
>
> "420 time_stamp/r/n"
>
> "sender_id receiver_name/r/n"
>
> "messages/r/n"
>



###### 删除好友

> **删除好友**格式：
>
> "430 time_stamp /r/n"
>
> "operator_id be_deleted_name /r/n"
>



**Method Code**：							**Meaning:**

**400**												   **请求好友**

410													接受好友

420                                                   发送信息

430                                                   删除好友

#### 对战系统



###### 传输操作

**传输操作**格式：

"Method_code time_stamp\r\n"

"actor_id room_id\r\n"



###### 游戏交流

**游戏交流**格式：

"550 time_stamp\r\n"

"sender_id room_id\r\n"

"messages\r\n"



**Method Code**：							**Meaning:**

**500**												   **替换卡牌**

510													抽取卡牌

520                                                   游戏投降

530                                                   增加战绩

540													增加金币



#### 协议

**登录信息**应当按照如下顺序发送：<u>账号</u>、<u>密码</u>。

**登录拒绝信息**包含两种代码，<u>211代表账号不存在</u>，<u>213代表用户密码错误</u>。

**登录许可信息**代码为212，并按顺序带有如下附件：<u>在线好友列表</u>、<u>用户战绩信息</u>、<u>排位信息</u>。其中在线好友列表格式为：<u>账号</u>、<u>好友名</u>、<u>备注</u>（如存在），战绩信息格式为：<u>总场数</u>、<u>胜率</u>，排位信息格式为：<u>Rank分</u>、<u>用户昵称</u>、<u>用户胜率</u>。

**状态**分为三种：<u>离线</u>，<u>在线</u>，<u>游戏中</u>。当某用户状态变化时，服务器将发送信息给其所有在线好友，通知他们更新好友信息。

**用户信息块**包括用户的基本信息：<u>头像</u>、<u>用户名</u>、<u>个人简介</u>、<u>好友信息</u>、<u>战绩信息</u>。