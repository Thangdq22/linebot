
import os
import json
# from dotenv import load_dotenv
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, FlexSendMessage, MessageEvent, TextMessage
# load_dotenv('.env')
# print(os.getenv("CHANNEL_ACCESS_TOKEN"))
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
# working_status = os.geten


app = Flask(__name__)


@app.route('/')
def home():
    return "Hello world!"


@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info('Request body: ' + body)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.type != 'text':
        return
    
    if event.message.text == 'test':
        reply_message = test()
        line_bot_api.reply_message(
            event.reply_token,
            reply_message
        )
        return
    
    if event.message.text == 'test flex':
        reply_message = test_flex()
        line_bot_api.reply_message(
            event.reply_token,
            reply_message
        )
        return


def test():
    message = TextSendMessage(text='hello world!')
    return message
    
    

def test_flex():
    with open('flex.json', 'r') as f:
        flex_content = json.load(f)
    flex_bubbles = []
    flex_bubbles.append(flex_content)
    carousel = {}
    carousel['type'] = "carousel"
    carousel['contents'] = flex_bubbles
    
    message = FlexSendMessage(alt_text='flex', contents=carousel)
    return message
if __name__ == "__main__":
    app.run()

