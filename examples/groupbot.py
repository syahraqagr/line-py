# -*- coding: utf-8 -*-
from linepy import *

#cl = LINE('EMAIL', 'PASSWORD')
cl = LINE('Et1fd26gCtgbLdd2jDgb.ggNCLqZ5irfKOvdzgQfq2W.EcY3RGwnjaFPDOgsRiTBxCjdpA9By/UR4Yq00WtS09M=')

cl.log("Auth Token : " + str(cl.authToken))
cl.log("Timeline Token : " + str(cl.tl.channelAccessToken))

# Initialize OEPoll with LINE instance
oepoll = OEPoll(cl)

# Receive messages from OEPoll
def RECEIVE_MESSAGE(op):
    '''
        This is sample for implement BOT in LINE group
        Invite your BOT to group, then BOT will auto accept your invitation
        Command availabe :
        > hi
        > /author
    '''
    msg = op.message
    
    text = msg.text
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from
    
    try:
        # Check content only text message
        if msg.contentType == 0:
            # Check only group chat
            if msg.toType == 2:
                # Chat checked request
                cl.sendChatChecked(receiver, msg_id)
                # Get sender contact
                contact = cl.getContact(sender)
                # Command list
                if text.lower() == 'hi':
                    cl.log('[%s] %s' % (contact.displayName, text))
                    cl.sendMessage(receiver, 'Hi too! How are you?')
                elif text.lower() == '/author':
                    cl.log('[%s] %s' % (contact.displayName, text))
                    cl.sendMessage(receiver, 'My author is linepy')
    except Exception as e:
        cl.log("[RECEIVE_MESSAGE] ERROR : " + str(e))
    
# Auto join if BOT invited to group
def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        group_id=op.param1
        # Accept group invitation
        cl.acceptGroupInvitation(group_id)
    except Exception as e:
        cl.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))

# Add function to OEPoll
oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP
})

while True:
    oepoll.trace()
