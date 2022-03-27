#Author:Doublefire.Chen
#time:2022年03月27日11:17:50
#location:HSC of PKU or BJMU(dawu,23333)
# coding:utf-8
import requests
from bs4 import BeautifulSoup
import json
import time
import schedule
global skey,uid,agentid,corpid,corpsecret
#无头浏览器登陆  参考：https://blog.csdn.net/qq_43055565/article/details/99345542
############配置区##############
skey="" #填入你的cookie中的skey值
uid="" #填入你的cookie中的uid值
corpid = '' #填入你的企业id
agentid =  #填入你的企业应用id（这个不要加引号）
corpsecret = '' #填入你的企业应用secret
Big_ten_flag="0" #是否爬十大，是填0，否填1
#定时运行 参考：https://blog.csdn.net/hxxjxw/article/details/121065659
#定时运行时间可根据需要自行修改
schedule.every().day.at("07:00").do(main) # 每天7点执行
schedule.every().day.at("12:00").do(main) # 每天12点执行
schedule.every().day.at("17:00").do(main) # 每天17点执行
schedule.every().day.at("21:00").do(main) # 每天21点执行
###############################
Cookie='skey='+skey+';'+'uid='+uid
header = {
'Accept':'*/*',
'Accept-Encoding':'gzip',
'Accept-Language':'en-US,en;q=0.9',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
'Cookie': Cookie,
'Host': 'bbs.pku.edu.cn',
'Pragma': 'no-cache',
'Referer': 'https://bbs.pku.edu.cn/v2/home.php',
'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': "macOS",
'Sec-Fetch-Dest': 'script',
'Sec-Fetch-Mode': 'no-cors',
'Sec-Fetch-Site': 'same-origin',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36'
}
def main():
	print("尝试连接BBS主页") #提示性输出
	r=requests.get('https://bbs.pku.edu.cn/v2/mobile/home.php',headers=header)
	print("连接成功") #提示性输出
	soup=BeautifulSoup(r.text,"html.parser") #解析
	if Big_ten_flag=="0":
		Big_ten='************全站十大************\n' #初始赋值
		card_big_ten=soup.find('div',class_='card big-ten') #找到大框
		for ul in card_big_ten.find_all('ul'): #遍历爬十大
			for li in ul.find_all('li'):
				rank_digit=li.find('span',class_='rank-digit').get_text() #爬排名
				post_title=li.find('a',class_='post-title').get_text() #爬标题
				post_info=li.find('a',class_='post-info').get_text().replace('','') #爬回帖数，删除乱码字（本来是一个图图，变成文本就乱码了）
				print("已爬十大第"+rank_digit) #提示性输出
				Big_ten=Big_ten+'['+rank_digit+']'+post_title+"\n"+post_info+'re'+'\n' #组合内容
		Big_ten=Big_ten+'\n' #空一行排版好看
	else:
		Big_ten='未开启爬取全站十大功能'+'\n'
	mail_num=soup.find('a',href='mail.php').find('span',class_="num") #获取新站内信数量
	message_num=soup.find('a',href='message.php').find('span',class_="num") #获取新消息数量
	if mail_num!=None:  #爬站内信
		print("开始爬站内信") #提示性输出
		mail_num=mail_num.get_text()
		r=requests.get('https://bbs.pku.edu.cn/v2/mobile/mail.php',headers=header)
		soup=BeautifulSoup(r.text,"html.parser") #解析	
		mail='************新站内信************'+'\n' #初始赋值
		for mail_item_unread in soup.find_all('div',class_='mail-item unread'): #定位未读站内信
			for author_text_limit in mail_item_unread.find_all('div',class_='author text-limit'): #爬发信人信息
				id=author_text_limit.find('span',class_="id").get_text()
				name=author_text_limit.find('span',class_="name").get_text()
			time_r=mail_item_unread.find('span',class_="time r").get_text() #爬发信时间
			title=mail_item_unread.find('div',class_="title").get_text() #爬信件标题
			content=mail_item_unread.find('div',class_="content").get_text() #爬信件内容
			print("正在进行爬站内信") #提示性输出
			mail=mail+time_r+'\n'+id+'('+name+')'+'\n'+'标题：'+title+'\n'+'内容：'+content+'\n'+'\n' #组合内容
	else:
		mail='没有新的站内信'+'\n'
	print("站内信爬取结束") #提示性输出

	if message_num!=None:  #爬消息
		print("开始爬消息") #提示性输出
		message_num=message_num.get_text()
		r=requests.get('https://bbs.pku.edu.cn/v2/mobile/message.php',headers=header)
		soup=BeautifulSoup(r.text,"html.parser") #解析			
		message="************新消息************"+'\n' #初始赋值
		i=0 #一个控制循环的变量，因为无法直接定位未读的消息
		list=soup.find('div',class_='list') #爬到list
		for chat in list.find_all('a',href=True): #逐个消息框判断
			count=chat.find('span',class_='count') #爬该消息框共有多少消息未读
			if count==None: #none表示消息都读过，继续判断下一个消息框
				continue
			else:
				i=i+int(count.get_text()) #计数
			if i<=int(message_num): #当爬到的未读消息等于总的未读消息数时结束
				for info in chat.find_all('div',class_='info'):	#爬info框
					id=info.find('p').contents[0] #爬最新消息内容（可惜网页只显示最新的消息内容，所以只能爬最新的，除非加代码，我懒得写了）
					nickname=info.find('p').find('span',class_='nickname').get_text() #爬发消息者昵称
					content=info.find_all('p')[1].get_text() #爬消息内容
					time=chat.find('span',class_='time').get_text() #爬发送消息的时间
					print("正在爬消息") #提示性输出
					message=message+time+'\n'+id+'('+nickname+')'+'\n'+'未读消息数量：'+count.get_text()+'\n'+'对方发送的最新消息内容：'+content+'\n'+'\n' #组合内容
	else:
		message='没有新的消息'+'\n'
	print("消息爬取结束") #提示性输出

	#微信推送 参考：https://blog.csdn.net/qq_29300341/article/details/115560813
	def send_message_QiYeVX(_message, useridlist = []): # 默认发送给自己
	    print("准备发送微信推送") #提示性输出
	    useridstr = "|".join(useridlist)
	    response = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}")
	    data = json.loads(response.text)
	    access_token = data['access_token']
	    json_dict = {
	       "touser" : useridstr,
	       "msgtype" : "text",
	       "agentid" : agentid,
	       "text" : {
	           "content" : _message
	       },
	       "safe": 0,
	       "enable_id_trans": 0,
	       "enable_duplicate_check": 0,
	       "duplicate_check_interval": 1800
	    }
	    json_str = json.dumps(json_dict)
	    response_send = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}", data=json_str)
	    print("微信消息推送成功") #提示性输出
	    return json.loads(response_send.text)['errmsg'] == 'ok'
	wechat_message=Big_ten+mail+message
	send_message_QiYeVX(wechat_message, useridlist = [''])

while True:
    schedule.run_pending() # 运行所有可运行的任务
