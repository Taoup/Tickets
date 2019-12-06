# Autoticket
大麦网自动抢票工具

注：**目前仅在win10，chrome环境测试过。**


## 环境安装
- python 3.6及以上环境
- 下载一个[浏览器驱动](https://github.com/Entromorgan/Autoticket/releases/download/v0.6/chromedriver.exe)放到bang.py同目录。
- pip install -r requirement.txt。


## 使用详解

**抢票前，确保DEBUG的值为False，最好首先在非目标票种那先测试下，毕竟它网页在不断变化，有些定位方式可能需要调整**

抢票主要包括3个步骤，我使用了4个函数来完成。
1. 登录：login和double_check_login， 这一步需要用到的参数有：大麦网的url & 登录后显示的nick name(用于脚本确认已经登录)
```python 
login(url = home_page, nick_name = '麦子')
double_check_login(url = home_page, nick_name = '麦子')
```
2. 下单:order(...),场次信息、票档（票价）信息，需要从下单的页面copy过来，如下图框中的部分。这个函数还有一个默认参数：refresh_interval，即刷新频率，目前设置为0.5s，看需要自己设置。有时候刷新太快会：
> 抱歉！系统繁忙，暂时无法处理您的请求……

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
