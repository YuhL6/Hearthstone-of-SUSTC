# 				南方科技大学炉石传说开发手册（草稿七）

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
| user_id1 | int(8)      | NO   | fr1  | NULL    |            |
| name1    | varchar(10) | YES  |      | NULL    |            |
| user_id2 | int(8)      | NO   | fr2  | NULL    |            |
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
> "User_id password\r\n"
>
> "User_name\r\n"
>
> "Email\r\n"
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
> #User_information
>
> "User_name Total_game_number Win_rate\r\n"
>
> #FRIENDS_LIST
>
> "Friends_number\r\n"
>
> "Friend_name Memo(select)\r\n"
>
> #REPEAT
>
> #RELATION_REQUEST
>
> "Name\r\n"
>
> #REPEAT
>
> "\r\n"

**Note**: information are split by space ' ' and end with '/r/n'



###### 修改密码

修改密码有两种方式：<u>通过现有密码进行修改</u>，<u>通过邮箱验证码进行修改</u>。

<u>通过现有密码进行修改</u>需要用户提供和<u>账号</u>和<u>当前密码</u>并填写<u>修改密码</u>，并且发送信息给服务器，若<u>当前密码</u>正确服务器则返回**修改成功信息**\*，<u>当前密码</u>错误则返回**修改失败信息**\*。

> **通过旧密码修改密码**格式：
>
> "220 Time_stamp\r\n"
>
> "User_id old_password\r\n"
>
> "New_password\r\n"
>
> "\r\n"
>
> **修改密码**成功：
>
> "221 Time_stamp\r\n"
>
> "\r\n"
>
> **修改密码**失败：
>
> "222 Time_stamp\r\n"
>
> "REASON\r\n"
>
> "\r\n"



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



**Note**: 除了登录系统使用User_id，其他所有的user_id都使用user_name。



#### 用户系统

###### 购买卡包

> **购买卡包**格式：
>
> "300 time_stamp/r/n"
>
> "User_name/r/n"
>
> "/r/n"



###### 抽取卡牌

服务器将生成随机数来确定抽中的卡牌，并将之返还给客户端。服务器要注意抽中的卡牌不能与已有卡牌重叠。

> **抽取卡牌**格式：
>
> "305 time_stamp/r/n"
>
> "User_name/r/n"
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
> "User_name/r/n"
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
> "User_name list_name/r/n"
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
> "User_name list_name/r/n"
>



###### 获取卡组中卡牌

> **获取卡牌**格式：
>
> "325 time_stamp /r/n"
>
> "User_name list_name/r/n"
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
> "User_name list_number/r/n"
>



###### 卡组加牌

> **卡组加牌**格式：
>
> "340 time_stamp/r/n"
>
> "User_id list_name/r/n"
>
> "card_number/r/n"



#### 好友系统

###### 请求好友

添加好友支持通过**用户账号**及**用户昵称**添加，发送请求前客户端需要判断是否已经添加为好友，发送后服务器将再进行一次判断。如已经添加、用户不存在或是对方拒绝，则返还**添加失败**，没有返还失败信息则表示**请求成功**，服务器将发送**请求好友**给接收方。

可以添加离线用户，当用户上线时会受到添加请求。

> **请求好友**格式（客户端）：
>
> "400 Time_stamp\r\n"
>
> "User_id Receiver_name(or id)/r/n"
>
> "\r\n"
>
> **请求好友**（服务器端）：
>
> "400 Time-stamp\r\n"
>
> "Sender_name(or id)\r\n"
>
> "\r\n"
>
> **添加失败**格式：
>
> "401 Time_stamp\r\n"
>
> "Name(or id)\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **添加成功**格式：
>
> "402 Time_stamp\r\n"
>
> "Name(or id)\r\n"
>
> "\r\n"



###### 接受好友请求

当用户接受好友请求时，服务器将判断该请求是否存在，如存在则返还**添加成功**，失败则返还原因

> **接受好友申请**格式：
>
> "410 Time_stamp\r\n"
>
> "User_id Sender_name(or id)\r\n"
>
> "\r\n"
>
> **接受好友请求失败**格式：
>
> "411 Time_stamp\r\n"
>
> "Name(or id)\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **接受好友请求成功**格式：
>
> "412 Time_stamp\r\n"
>
> "Name(or id)\r\n"
>
> "\r\n"

###### 拒绝好友请求

如果拒绝好友失败（例如没有请求或用户不存在），则返还**拒绝好友请求失败**信息，如没有返还则为成功。

> **拒绝好友申请**格式：
>
> "415 Time_stamp\r\n"
>
> "User_id Sender_name(or id)\r\n"
>
> "\r\n"
>
> **拒绝好友请求失败**格式：
>
> "416 Time_stamp\r\n"
>
> "Name(or id)\r\n"
>
> "REASON\r\n"
>
> "\r\n"



###### 发送消息

只能给在线好友发送信息，离线好友不可

> **发送消息**（客户端）格式：
>
> "420 Time_stamp\r\n"
>
> "User_id receiver_name\r\n"
>
> "messages\r\n"
>
> "\r\n"
>
> **发送消息**（服务器端）格式：
>
> "420 Time_stamp\r\n"
>
> "Name\r\n"
>
> "messages\r\n"
>
> "\r\n"N
>
> **发送失败**格式：
>
> "421 Time-stamp\r\n"
>
> "Name\r\n"
>
> "REASON\r\n"
>
> "\r\n"



###### 删除好友

> **删除好友**格式：
>
> "430 Time_stamp\r\n"
>
> "User_id be_deleted_name\r\n"
>
> "\r\n"
>
> **删除失败**格式:
>
> "431 Time_stamp\r\n"
>
> "Name\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **删除成功**格式：
>
> "432 Time_stamp\r\n"
>
> "Name\r\n"
>
> "\r\n"
>
> **被删除**格式：
>
> "433 Time_stamp\r\n"
>
> "Name\r\n"
>
> "\r\n"



#### 对战系统

###### 列出房间

> **列出房间 list_room**格式：
>
> "500 Time_stamp\r\n"
>
> "User_id\r\n"
>
> "\r\n"
>
> **房间**格式:
>
> "502 Time_stamp\r\n"
>
> "ROOM_NUMBER\r\n"
>
> "Room_id Room_status Room_owner/r/n"
>
> "\r\n"

###### 创建房间

> **创建房间 create_room**格式：
>
> "510 Time_stamp\r\n"
>
> "User_id\r\n"
>
> "\r\n"
>
> **创建房间失败 create_room_fail**格式：
>
> "511 Time_stamp\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **创建房间成功 create_room_suc**格式：
>
> "512 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"



###### 加入房间

> **加入房间 add_into_room**格式：
>
> "520 Time_stamp\r\n"
>
> "User_id room_number\r\n"
>
> "\r\n"
>
> **加入失败 add_room_fail**格式：
>
> "521 Time_stamp\r\n"
>
> "Room_id REASON\r\n"
>
> "\r\n"
>
> **加入成功 add_room_suc**格式：
>
> "522 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"



###### 准备游戏

> **准备游戏 get_ready**格式：
>
> "530 Time_stamp\r\n"
>
> "User_id Room_number\r\n"
>
> "\r\n"
>
> **准备游戏失败 ready_fail**格式：
>
> "531 Time_stamp\r\n"
>
> "Room_number\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **准备游戏成功 ready_suc**格式：
>
> "532 Time_stamp\r\n"
>
> "Room_number\r\n"
>
> "\r\n"

###### 取消准备

> **取消准备 cancel_ready**格式：
>
> "535 Time_stamp\r\n"
>
> "User_id Room_number\r\n"
>
> "\r\n"
>
> **取消准备失败 ready_fail**格式：
>
> "536 Time_stamp\r\n"
>
> "Room_number\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **取消准备游戏成功 ready_suc**格式：
>
> "537 Time_stamp\r\n"
>
> "Room_number\r\n"
>
> "\r\n"

###### 开始游戏

> **开始游戏**格式：
>
> "540 time_stamp\r\n"
>
> "User_id room_id\r\n"
>
> "\r\n"
>
> **开始失败**格式：
>
> "541 time_stamp\r\n"
>
> "Room_id\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **开始成功**格式：
>
> "542 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"



###### 退出房间

> **退出房间 leave_room**格式：
>
> "545 Time_stamp\r\n"
>
> "User_id room_id\r\n"
>
> '\r\n'
>
> **退出房间失败 leave_room_fail**格式：
>
> "546 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "REASON\r\n"
>
> '\r\n'
>
> **退出房间成功 leave_room_suc**格式：
>
> "547 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> '\r\n'
>
> 

###### 开始游戏

> **开始游戏 start_game**格式：
>
> "550 Time_stamp\r\n"
>
> "User_id Room_id\r\n"
>
> "\r\n"
>
> **开始失败 start_game_fail**格式：
>
> "551 Time_stamp\r\n"
>
> "room_id\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **开始成功 start_game_suc**格式：
>
> "552 Time_stamp\r\n"
>
> "room_id Priority\r\n"
>
> "Picture_id\r\n"
>
> //0: 4, 1: 3
>
> "Card_id\r\n"
>
> "\r\n"

###### 获取卡牌

> **获取卡牌 get_card**格式：
>
> "570 Time_stamp\r\n"
>
> "User_id room_id\r\n"
>
> "r\n"
>
> **获取卡牌失败 get_card_fail**格式：
>
> "571 Time_stamp\r\n"
>
> "room_id\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **获取卡牌成功 get_card_suc**格式：
>
> "572 Time_stamp\r\n"
>
> "room_id\r\n"
>
> "card_num\r\n"
>
> "\r\n"

###### 出牌

> **出牌 put_card**格式：
>
> "580 Time_stamp\r\n"
>
> "User_id room_id\r\n"
>
> "card_num\r\n"
>
> "\r\n"
>
> **出牌失败 put_card_fail**格式：
>
> "581 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **出牌（服务器转发） put_card**格式：
>
> "582 Time_stamp\r\n"
>
> "Card_id\r\n"
>
> "\r\n"

###### 攻击

> **攻击 attack**格式：
>
> "590 Time_stamp\r\n"
>
> "User_id Room_id\r\n"
>
> "attacker_card injured_card\r\n"
>
> "\r\n"
>
> **攻击失败 attack_fail**格式：
>
> "591 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **攻击（服务器转发） attack**格式：
>
> "592 Time_stamp\r\n"
>
> "attacker_card injured_card\r\n"
>
> "\r\n"

###### 结束回合

> **结束回合（用户发送） round_end**格式：
>
> "600 Time_stamp\r\n"
>
> "User_id Room_id\r\n"
>
> "Side"			// 0 stands for first hand, 1 stands for last hand
>
> "\r\n"
>
> **结束失败 round_end_fail**格式：
>
> "601 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "REASON\r\n"
>
> "\r\n"
>
> **结束回合（服务器发送) round_end**格式：
>
> "602 Time_stamp\r\n"
>
> "Side"			// 0 stands for first hand, 1 stands for last hand
>
> "\r\n"

###### 结束游戏

> **游戏结束（服务器发送） game over**格式：
>
> "610 Time_stamp\r\n"
>
> "Side\r\n"
>
> "\r\n"

###### 投降

> **投降（用户发送） yield**格式：
>
> "710 Time_stamp\r\n"
>
> "User_id Room_id\r\n"
>
> "\r\n"
>
> **投降（服务器发送） yield**格式：
>
> "710 Time_stamp\r\n"
>
> "Side\r\n"
>
> "\r\n"

620

chat

###### 游戏交流

**游戏交流**格式：

"550 time_stamp\r\n"

"sender_id room_id\r\n"

"messages\r\n"



**Method Code**：							**Meaning:**

**560**												   **替换卡牌**

570													抽取卡牌

520                                                   游戏投降

530                                                   增加战绩

540													增加金币



#### 消息推送

服务器主动向用户发送消息推送

###### 好友登录/退出推送

> **好友上线 friend_online**提示格式：
>
> "100 Time_stamp\r\n"
>
> "Friend_name\r\n"
>
> "\r\n"
>
> **好友下线 friend_outline** 提示格式：
>
> "101 Time_stamp\r\n"
>
> "Friend_name\r\n"
>
> "\r\n"

###### 好友状态改变推送（好友视角）

> **好友进入房间 friend_in_room**提示格式：
>
> "102 Time_stamp\r\n"
>
> "Friend_name\r\n"
>
> "\r\n"
>
> **好友退出房间 friend_out_room**提示格式：
>
> "103 Time_stamp\r\n"
>
> "Friend_name\r\n"
>
> "\r\n"
>
> **好友进入游戏 friend_in_game**提示格式：
>
> "104 Time_stamp\r\n"
>
> "Friend_name\r\n"
>
> "\r\n"
>
> **好友退出游戏 friend_out_game**提示格式：
>
> "105 Time_stamp\r\n"
>
> "Friend_name\r\n"
>
> "\r\n"

###### 房间状态改变（外部视角）

> **新增房间 new_room**格式：
>
> "106 Time_stamp\r\n"
>
> "Room_id  Room_owner\r\n"
>
> "\r\n"
>
> **删除房间 delete_room**格式：
>
> "107 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"
>
> **玩家加入房间 room_full**格式：
>
> "108 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"
>
> **玩家退出房间 room_empty**格式：
>
> "109 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"
>
> **房间开始游戏 room_start_game**格式：
>
> "110 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"
>
> **房间结束游戏 room_end_game**格式：
>
> "111 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"
>
> **房主改变 owner_change**格式：
>
> "112 Time_stamp\r\n"
>
> "Room_id Name\r\n"
>
> "\r\n"

###### 房间状态改变（房主视角）

> **玩家加入房间 player_in**格式：
>
> "113 Time_stamp\r\n"
>
> "Room_id Name\r\n"
>
> "\r\n"
>
> **玩家退出房间 player_out**格式：
>
> "114 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"
>
> **玩家准备 player_ready**格式：
>
> "115 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"
>
> **玩家取消准备 player_not_ready**格式
>
> "116 Time_stamp\r\n"
>
> "Room_id\r\n"
>
> "\r\n"

#### 协议

**登录信息**应当按照如下顺序发送：<u>账号</u>、<u>密码</u>。

**登录拒绝信息**包含两种代码，<u>211代表账号不存在</u>，<u>213代表用户密码错误</u>。

**登录许可信息**代码为212，并按顺序带有如下附件：<u>在线好友列表</u>、<u>用户战绩信息</u>、<u>排位信息</u>。其中在线好友列表格式为：<u>账号</u>、<u>好友名</u>、<u>备注</u>（如存在），战绩信息格式为：<u>总场数</u>、<u>胜率</u>，排位信息格式为：<u>Rank分</u>、<u>用户昵称</u>、<u>用户胜率</u>。

**状态**分为三种：<u>离线</u>，<u>在线</u>，<u>游戏中</u>。当某用户状态变化时，服务器将发送信息给其所有在线好友，通知他们更新好友信息。

**用户信息块**包括用户的基本信息：<u>头像</u>、<u>用户名</u>、<u>个人简介</u>、<u>好友信息</u>、<u>战绩信息</u>。