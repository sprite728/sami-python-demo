from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from python import settings
from samiio import ApiClient
from MessagesApi import MessagesApi
from devices import getUserDevices, getDevicesIds, getDeviceTypesForUser, getDeviceIdDict
from user import getTokenAndId
from templateUtils import get_date, get_item

@login_required
def showMessages(request):
    """show messages for the devices of the logged in samsung user

                Args:
                    request: django request object
                Returns: render messages.html
                """
    context = RequestContext(request)

    #get user_id and token. Needed to retrieve the messages
    token, userId = getTokenAndId(request.user)

    #build the message api
    apiClient = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)
    messagesApi = MessagesApi(apiClient)

    #get devices associated to a user
    devicesEnvelope = getUserDevices(token, userId)
    #build a string containing the devices ids separated by comma
    devices = ','.join (getDevicesIds(devicesEnvelope))

    #get devices types pretty names to show on the html
    devicesTypes = getDeviceTypesForUser(token, userId)

    #retrieve the last 20 messages for this devices
    messageEnvelope = messagesApi.getNormalizedMessagesLast(devices, count = 20)

    #get the message count from the envelope and the messages
    count = messageEnvelope.count
    messages = messageEnvelope.data

    #get a dict containing the devices ids with an associated device name to show on the html
    devices = getDeviceIdDict(devicesEnvelope)

    contextDict = {'active': 'messages', 'count': count, 'messages': messages, 'devicesTypes':devicesTypes, 'devices':devices}
    return render_to_response("messages.html", contextDict, context)