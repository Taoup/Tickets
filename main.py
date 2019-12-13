from damai import GoDamai
from utils import my_print

target_url = """
https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_1.591b23e1MH53GB&id=608715045715    """

if __name__ == '__main__':
    target_url = target_url.strip()
    retry = 100

    go = GoDamai(debug=True)
    go.login(nick_name = '麦子')

    for i in range(retry):
        try:
            go.order(target = target_url,          #抢票页面的url
                    city = None,              #不用选择城市的场次，city传入None
                    date = '2020',        
                    price = '888', 
                    num_tickets = 2)
            go.confirm_order(audiences = ['马宏涛', 'xxx'])
        except Exception as e:
            my_print(e)

        if go.success:
            break
        my_print(f"重试第{i+1}次")