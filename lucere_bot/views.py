from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


# Create your views here.
def index(request):
    x = "current date : " + str(datetime.now())
    return HttpResponse(x)

@csrf_exempt
def callback(request):
    if (request.method == 'POST'):
        # get X-Line-Signature header value
        signature = request.META['HTTP_X_LINE_SIGNATURE']

        global domain
        domain = request.META['HTTP_HOST']

        # get request
        body = request.body.decode('utf-8')
        
        logger.debug("Response body : ", body)

        # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()
        
        return HttpResponse()
    
    else :
        return HttpResponseBadRequest()


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg_from_user = event.message.text
    if (msg_from_user == "Hello"):
        message = TextSendMessage(str(event))
        line_bot_api.reply_message(event.reply_token, message)
    else :
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)