from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime
from .models import *


line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


# Create your views here.
def index(request):
    x = "current date : " + str(datetime.now())
    userid = "skyxrna"
    nickname = "rainburn"
    register(userid, nickname)
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

    # command guide 
    # create event : /create [event_name] [where/site/game] [time-userdefined]
    # join event : /join [event-name]-[event-id]
    # register : /register [nickname]
    # rename : /rename [nickname]
    # leave event : /leave [event_name]-[event-id]

    # original message
    msg_from_user = event.message.text

    # check whether it's a command or chat
    if (msg_from_user[0] != "/"): # not command
        return

    parameters = msg_from_user[1:len(msg_from_user)].split(" ")

    command = parameters[0]

    if (command == "register"):
        user_id = event.source.user_id

        if (is_user_registered(user_id)):
            show_error_msg(event.reply_token, "Cannot register twice !")
            return

        if (len(parameters) == 1): # no nickname was given
            try:
                profile = line_bot_api.get_profile(user_id)
                line_username = profile.display_name
                register(user_id, line_username)
                return
            
            except:
                show_error_msg(event.reply_token, "Cannot register. Please add the bot as your friend or include your nickname after 'register' command")
                return


        nickname = " ".join(parameters[1:len(parameters)])
        
        user_id = str(user_id)
        nickname = str(nickname)

        user_id_on_db = register(user_id, nickname)

    elif (command == "rename"):
        user_id = event.source.user_id

        if (len(parameters) == 1): # no new nickname was given
            show_error_msg(event.reply_token, "Failed to rename. New nickname cannot be empty")
            return

        if not (is_user_registered(user_id)):
            show_error_msg(event.reply_token, "Only registered users can use 'rename' command")
            return

        nickname = " ".join(parameters[1:len(parameters)])
        rename(user_id, nickname)

    elif (command == "create"):

        # TODO: Add try-except later

        event_name = parameters[1]
        event_site = parameters[2]
        event_time = parameters[3:len(parameters)]
        event_id = add_event(event_name, event_site, event_time)

        # Event creator auto join the event
        user_id = event.source.user_id
        join_event(event_id, user_id)

        # show event details
        show_event_details(event.reply_token, event_id)

    elif (command == "join"):

        # TODO: Add try-except later

        event_details  = parameters[1].split("-")
        event_id = event_details[1]
        user_id = event.source.user_id
        join_event(event_id, user_id)
    
        # show event details
        show_event_details(event.reply_token, event_id)

    elif (command == "leave"):

        # TODO: Add try-except later

        event_details  = parameters[1].split("-")
        event_id = event_details[1]
        user_id = event.source.user_id
        leave_event(event_id, user_id)

            # show event details
        show_event_details(event.reply_token, event_id)

    else : # Command not found
        warn_text = "Command '" + command + "' not found !"
        message = TextSendMessage(text=warn_text)
        line_bot_api.reply_message(event.reply_token, message)
    

def show_msg(reply_token, msg):
    message = TextSendMessage(text=msg)
    line_bot_api.reply_message(reply_token, message)

def show_error_msg(reply_token, msg=""):
    error_msg = "Invalid command parameters !" if msg == "" else msg
    message = TextSendMessage(text=error_msg)
    line_bot_api.reply_message(reply_token, message)

def register(user_id, nickname):
    new_user = User(userid=user_id, nickname=nickname)
    new_user.save()
    return new_user.userid

def rename(user_id, nickname):
    user = User.objects.get(userid=user_id)
    user.nickname = nickname
    user.save()

def add_event(name, site, when):
    new_event = Event(name=name, site=site, when=when)
    new_event.save()
    return new_event.id

def join_event(eventid, userid):

    # eventid needed to be int
    eventid = int(eventid)

    # check whether user has already join the event
    event = Event.objects.get(id=eventid)
    user = User.objects.get(userid=userid)

    result = list(EventParticipant.objects.filter(event=event, user=user))
    if result:
        return

    new_member = EventParticipant(event=event, user=user)
    new_member.save()

def leave_event(eventid, userid):
    # eventid needed to be int
    eventid = int(eventid)

    event = Event.objects.get(id=eventid)
    user = User.objects.get(userid=userid)

    instance = EventParticipant.objects.get(event=event, user=user)
    instance.delete()
    return

def is_user_registered(userid):
    user = list(User.objects.filter(userid=userid))
    if user:
        return True
    else:
        return False

def force_register_user(replytoken, userid):
    result = list(User.objects.filter(userid=userid))
    if not result: # User not registered
        
        # get user line profile
        try:
            profile = line_bot_api.get_profile(userid)
            line_username = profile.display_name
            register(userid, line_username)

        except:
            error_msg = TextSendMessage(text="Something's wrong. Adding Lucere BOT may fix the issue.")
            line_bot_api.reply_message(replytoken, error_msg)
            return

    return

def show_event_details(reply_token, eventid):
    # Structure
    # Event ID : [event_name]-[event_id]
    # [event_name]
    # [event_site]
    # [event_when]
    # [list of members]

    # eventid needed to be int
    eventid = int(eventid)

    result = ""
    
    try :
        event = Event.objects.get(id=eventid)
        event_name_id = "Event ID: " + event.name + "-" + str(event.id) + '\n'
        event_name = event.name
        event_site = event.site + '\n'
        event_when = event.when + '\n\n'

        result = event_name_id + event_name + event_site + event_when

        event = Event.objects.get(id=eventid)

        members = list(EventParticipant.objects.filter(event=event))
        for i in range(len(members)):
            user = members[i].user
            nickname = user.nickname
            
            currMember = f'{i+1}. {nickname}\n'
            result = result + currMember


        show_msg(reply_token, result)

    except Event.DoesNotExist:
        show_error_msg(reply_token, eventid)
        return
