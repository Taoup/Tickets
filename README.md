# Tickets!!
简单易用的图形大麦抢票脚本。
欢迎大家使用，提issue、PR。

注：**目前仅在win10，chrome环境测试过。**

## 新增功能
- 使用图形界面进行简单包装,大概长这样：
![image.png](http://butnotover.live/static/media/gui.PNG)


## 特色：
- 页面元素选取和抢票代码逻辑解耦，虽然目前只有chrome支持，想要扩展其他浏览器变得非常简单
- 页面元素的选取统一采用css selector。
- 利用了senelium的implicit wait，使得页面元素超时等待逻辑非常简单。
- 还有简单的图形界面wrapper...

## 环境安装
- python 3.6及以上环境
- 下载一个[浏览器驱动](https://github.com/Entromorgan/Autoticket/releases/download/v0.6/chromedriver.exe)放到bang.py同目录。
- pip install -r requirement.txt。


## 使用详解


运行方法：
- 根据下列步骤设置好main.py里的参数
- ```python main.py```
- or ```python gui.py```(图形界面，把参数填好就ok，第一步就可以略过了)

**抢票前，最好首先在非目标票种那先测试下，毕竟它网页在不断变化，有些定位方式可能需要调整**

抢票主要包括3个步骤，我使用了3个函数来完成。
1. 登录：login， 这一步需要用到的参数有：**登录后显示的昵称**(用于脚本确认已经登录)
```python 
login(nick_name = '麦子')
```
2. 下单:order(...),场次信息、票档（票价）信息，需要从下单的页面copy过来，如下图框中的部分：
[![image.png](https://i.postimg.cc/Pr7KMZPs/image.png)](https://postimg.cc/0bppkzYc)


```python
order(target = target_url,          #抢票页面的url
        city = None,              #不用选择城市的场次，city传入None
        date = '2019-12-22 周日 19:30',        
        price = '1080元（内场）', 
        num_tickets = 2)
```
3. 确认订单：confirm_order(), 这里的参数为观众，买几张票就列几个人（虽然根据抢的票的不同也不一定用得上），**注：列在这里的观众必须在你的常用购票人里，没有的话先去添加好**，列在第一个的最好是下单的人。
```python
confirm_order(audiences = ['xxx', 'xxx'])
```

## Ref
本代码修改自[Entromorgan](https://github.com/Entromorgan/Autoticket)
