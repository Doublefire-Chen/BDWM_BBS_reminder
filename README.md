# BDWM_BBS_reminder  
未名BBS微信消息推送爬虫  
## 前言  
作者这学期选了一个Python爬虫选修课，又特别喜欢水BBS。经常点开BBS客户端，生怕自己错过消息。于是，作者利用所学知识，写了该脚本。  
## 功能介绍  
1. 爬取十大内容（可选）  
2. 爬取未读站内信  
3. 爬取未读消息  
4. 将上述内容进行微信推送  
5. 定时运行  
## 食用指南  
仓库里一共有2个函数，都能实现该功能。  
1.```BBS_reminder_by_requests.py```为requests实现，无需额外的驱动（推荐使用）  
2.```BBS_reminder_by_chrome.py```为无头Chrome浏览器实现，需要下载Chrome驱动（方法请自行百度）（不推荐使用）  
以下以```BBS_reminder_by_requests.py```为例（装包的事儿应该不用我多说了吧，缺啥包就装啥包）  
打开```BBS_reminder_by_requests.py```文件，将配置区的内容补全，根据需要在函数末尾修改定时运行函数，然后运行即可。  
### 关于配置区参数的获取  
1. ```skey```和```uid```。谷歌浏览器（有开发者工具的浏览器都行）进入BBS https://bbs.pku.edu.cn/v2/mobile/home.php 并登陆，打开开发者工具（快捷键：F12），点击Network如图：  
![Image load fail](https://bbs.pku.edu.cn/attach/.thumbnail/eb/90/eb902c4ef5e6a5d5.jpg)  
然后刷新网页，点击home.php，如图：  
![Image load fail](https://bbs.pku.edu.cn/attach/.thumbnail/8f/8b/8f8b5c0c57d7c4ed.jpg)  
然后右边的headers一栏下面就是出现cookie和相应的值。  
2.```corpid,userid,agentid,corpsecret```，请自行前往 https://blog.csdn.net/qq_29300341/article/details/115560813 学习（不是我懒，是人家写的真好，23333），我也是在这里学的（之前用的server酱，免费版一天只能推送5条消息，多的要w，这篇博文教你如何搭建一个免费的server酱，体验上简直一模一样。也不麻烦，由于我之前用server酱的时候就用的企业微信推送，我发现二者的配置操作起来简直一模一样）  
## 鸣谢  
感谢三位好兄弟的辅助测试（BBS_id:ddvdv,dysyyds,kangkangcmr）  
