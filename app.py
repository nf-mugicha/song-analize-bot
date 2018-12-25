#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

import settings
import code_analize

app = Flask(__name__)
# httpsでアクセスできるようにする
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# context.load_cert_chain('cert.crt', 'server_secret.key')


line_bot_api = LineBotApi(settings.YOUR_CHANNERL_ACCESS_TOKEN)
handler = WebhookHandler(settings.YOUR_CHANNERL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

# 音声ファイルを受け取る関数
@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: '+str(body))
    print('Request body: ' + str(body))

    # hadle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # eventがRequest Body
    """
    Request body: {
        "events":
                [
                    {
                    "type":"message",
                    "replyToken":"7ba6d25051584a7ca74ac658a5bdc758",
                    "source":{
                        "userId":"Ufc78ba9ae7596cda855bc9f7e4f00498",
                        "type":"user"
                        },
                    "timestamp":1545766534620,
                    "message":{
                        "type":"text",
                        "id":"9070678793256",
                        "text":"はやか"
                        }
                    }
                ],
        "destination":"Ue5d4eb302368f469540f3742b5f6d2dc"
        }
    """
    # 入ってきたものがaudio以外だったら、とりあえずおうむ返し処理にする
    if event.massage.type is not 'audio':
        if event.message.type is 'text':
            app.logger.info('Sending Message: ' + str(event.message.text))
            print('Sending Message: ' + str(event.message.text))
            # LINE BOTが返す内容を決める
            line_bot_api.reply_message(
                event.reply_token,  # トークンとテキストで紐づけてる
                TextSendMessage(text=event.message.text)
            )
        return '音声ファイルを送信してね'

    # tmpフォルダにダウンロードする
    code_analize.set_param_to_api(event.message.replyToken)

if __name__ == '__main__':
    port = os.environ.get('PORT', 3333)
    # app.run(
    #     host = 'localhost',port=3333, ssl_context=context, threaded=True, debug=True
    # )
    app.run(
        host = 'localhost',port=3333
    )