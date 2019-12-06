import damai
from utils import my_print

DEBUG = True

target_url = """
https://detail.damai.cn/item.htm?spm=a2oeg.search_category.0.0.359a47487igv4I&id=608107319952&clicktitle=2019%20JonyJ%E5%8D%97%E4%BA%AC%E5%A5%A5%E4%BD%93%E6%BC%94%E5%94%B1%E4%BC%9A    
    """

if __name__ == '__main__':
    target_url = target_url.strip()
    retry = 10

    damai.login(nick_name = '麦子')
    damai.double_check_login(nick_name = '麦子')

    for i in range(retry):
        try:
            damai.order(target = target_url,          #抢票页面的url
                    city = None,              #不用选择城市的场次，city传入None
                    date = '2019-12-21',        
                    price = '180元', 
                    num_tickets = 2)

            damai.confirm_order(audiences = ['xxx', 'xxx'])
        except Exception as e:
            print(e)
        if damai.success:
            break
        my_print(f"重试第{i+1}次")