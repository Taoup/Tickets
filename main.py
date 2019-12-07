import damai
from utils import my_print

DEBUG = True

target_url = """
https://detail.damai.cn/item.htm?spm=a2oeg.home.card_0.ditem_3.b59c23e1Fiy2fm&id=608677793344
    """

if __name__ == '__main__':
    target_url = target_url.strip()
    retry = 100

    damai.login(nick_name = '麦子')

    for i in range(retry):
        try:
            damai.order(target = target_url,          #抢票页面的url
                    city = None,              #不用选择城市的场次，city传入None
                    date = '2020',        
                    price = '980', 
                    num_tickets = 2)
            damai.confirm_order(audiences = ['马宏涛', 'xxx'])
        except Exception as e:
            my_print(e)

        if damai.success:
            break
        my_print(f"重试第{i+1}次")