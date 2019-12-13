import PySimpleGUI as sg

from damai import GoDamai
from utils import my_print

sg.change_look_and_feel('BluePurple')

layout = [[sg.Text('你登录后显示的昵称：'), sg.Input(key='nick_name')],
          [sg.Text('抢票页面网址：'), sg.Input(key='target_url')],
          [sg.Text('城市（没有不填）：'), sg.Input(key='city')],
          [sg.Text('场次：'), sg.Input(key='date')],
          [sg.Text('票档：'), sg.Input(key='price')],
          [sg.Text('数量：'), sg.Input(key='num_tickets')],
          [sg.Text('观众：（逗号分隔，中文的）'), sg.Input(key='audiences')],
          [sg.Button('开抢！'), sg.Button('Exit')]]

window = sg.Window('开冲', layout)

go = None
while True:  # Event Loop
    event, values = window.read()
    if event in  (None, 'Exit'):
        if go:
            go.driver.quit()
        break
    if event == '开抢！':
        go = GoDamai(debug=True)
        target_url = values['target_url']
        retry = 100
        go.login(nick_name = values['nick_name'])
        for i in range(retry):
            try:
                go.order(target = target_url, 
                        city = values['city'],            
                        date = values['date'],        
                        price = values['price'], 
                        num_tickets = values['num_tickets'])
                audiences = values['audiences'].split('，')
                go.confirm_order(audiences = audiences)
            except Exception as e:
                my_print(e)

            if go.success:
                break
            my_print(f"重试第{i+1}次")
window.close()