#coding:utf-8   #强制使用utf-8编码格式
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.image import  MIMEImage
from email.mime.multipart import MIMEMultipart

# 设置邮箱的域名，也可以是QQ 或者其他的
HOST = 'smtp.163.com'
SUBJECT = '这个星期搞搞比利搞大力'

# 这个写之前，必须确保自己邮箱的SMTP协议已经开启
# stmp: simple mail transfer protocol 简单邮件传输协议
FROM = 'luxianfeng0@163.com'
# 这个表示要发送的人，一次可以发送给多个人，用逗号隔开
TO = 'skyhill@foxmail.com, 另一个邮箱地址'
# related 表示使用内嵌资源的形式，将邮件发送给对方
message = MIMEMultipart('related')

# ------------------发送文本
message_html = MIMEText('大哥你家乡的电动车是白拿白拿的吗', 'plain', 'utf-8')
message.attach(message_html)

# 文本消息后面常用的有三个参数：
# 参数
#   1. 发送的内容， 内容必须是字符串
#   2. 内容的类型 文本类型默认为plain
#   3. 内容的编码方式， 使用utf-8 进行编码
# 也可以插入其他内容，如Html

# message_html = MIMEText('<h2 style="color:red;font-size:100px">我的烤面筋融化你的心</h2><img src="cid:small">', 'html', 'utf-8')
# message.attach(message_html)

message['From'] = FROM
message['To'] = TO
message['Subject'] = SUBJECT
#  获取简单邮件传输协议证书
email_client = smtplib.SMTP_SSL()
# 设置发件人邮箱的域名和端口 端口为465
email_client.connect(HOST, '465')
result = email_client.login(FROM, 'wfwsys12345')
print('登录结果', result)

message_xlsx = MIMEText(open('test.txt', 'rb').read(), 'base64', 'utf-8')
# 设置文件在附件当中的名字
message_xlsx['Content-Dispositon'] = 'attachment; filename="test.txt"'
message.attach(message_xlsx)

#  msg后面的结果必须是一个字符串  as_string 将整个对象转成字符串
email_client.sendmail(from_addr=FROM,to_addrs=TO.split(','),msg=message.as_string())
email_client.close()