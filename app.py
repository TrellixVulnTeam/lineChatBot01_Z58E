import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
###แก้ *
from linebot.models import * 

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = '52614572cd6990774cdc45cb2e78fa7f'
channel_access_token = 'fqUkl9Htr7LzDAExz0wjLy+b1vW04kQ9Jz82hIFyeB8h0NgeJcTOPezD5rPiwMY527NTkvuRnwnL+5XxW3nJ9hrFkXT9RV7vKuEUZMKif48HHKlDDOhIKju3UTRmEb5OPfIY2b1jar327csK8tHsBAdB04t89/1O/w1cDnyilFU='
# if channel_secret is None:
#     print('Specify LINE_CHANNEL_SECRET as environment variable.')
#     sys.exit(1)
# if channel_access_token is None:
#     print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
#     sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

###แก้ route
@app.route("/webhook", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    reply_token =  event.reply_token
    text_frofmuser = event.message.text
    text = TextSendMessage(text=text_frofmuser)
   
   
    # text2 = TextSendMessage(text="test")
    # image_message_1 = ImageSendMessage(
    #     original_content_url='https://image.freepik.com/free-photo/green-blue-transparent-leaves_23-2148239758.jpg',
    #     preview_image_url='https://image.freepik.com/free-photo/green-blue-transparent-leaves_23-2148239758.jpg'
    # )
    # line_bot_api.reply_message(
    #     reply_token,
    #     messages=[text,text2,image_message_1]
    # )
    # line_bot_api.push_message(
    #     to=str(event.source),
    #     messages=text
    # )
    # # line_bot_api.multicast(["U65c8c03c10487a69855fd591bd830ac1","U4dd62d9af204ed4fa2f0a3f58c47db19"],text)
    # line_bot_api.push_message("U65c8c03c10487a69855fd591bd830ac1",TextSendMessage(text='Hello World!'))
    if 'เช็คราคา' in text_frofmuser:
        from Resource.bxAPI import GetBxPrice
        from random import randint
        from flexMsg import setCarousel,setbubble
        num = randint(1,10)
        data = GetBxPrice(num)

        flex_data = setCarousel(data) 
        print(flex_data)
        from Resource.reply import SetMenuMessage_Object,send_flex
        flex= SetMenuMessage_Object(flex_data)
        send_flex(reply_token,flex,channel_access_token)
    else:
        text_list = [
            'วัยรุ่นไม่เข้าใจเลย','ฉันไม่เข้าใจที่คุณพูดค่ะ กรุณาลองใหม่อีกครั้งค่ะ','กรุณาลองพิมพ์ใหม่ได้ไหม'
        ]
        from random import choice
        text_data = choice(text_list)
        text = TextSendMessage(text=text_data)
        line_bot_api.reply_message(reply_token,text)
    
@handler.add(FollowEvent)
def RegisRichmenu(event):
    user_id = event.source.user_id
    disname = line_bot_api.get_profile(user_id=user_id).display_name

    button_1 = QuickReplyButton(action=MessageAction(label='เช็คราคา',text='เช็คราคา'))
    button_2 = QuickReplyButton(action=MessageAction(label='เช็คข่าวสาร',text='เช็คข่าวสาร'))
    qbtn = QuickReply(items=[button_1,button_2])

    text = TextSendMessage(text='สวัสดีคุณ {} ยินดีต้อนรับสู่บริการแชทบอก'.format(disname))
    text2 = TextSendMessage(text='กรุณาเลือกเมนูที่ท่านต้องการ',quick_reply = qbtn)

    line_bot_api.link_rich_menu_to_user(user_id,'richmenu-5f423e3fd478bb501fc6029e49452b59')
    
    line_bot_api.reply_message(event.reply_token,messages=[text,text2])

if __name__ == "__main__":
    app.run(port=200)