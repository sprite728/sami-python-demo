from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from python import settings
from samihub import ApiClient
from HistoricalApi import HistoricalApi
from devices import get_user_devices, get_devices_ids, get_device_types_for_user, get_device_id_dict
from user import get_token_and_id
from templateUtils import get_date, get_item

@login_required
def show_messages(request):
    """show messages for the devices of the logged in samsung user

                Args:
                    request: django request object
                Returns: render messages.html
                """
    context = RequestContext(request)

    #get user_id and token. Needed to retrieve the messages
    token, user_id = get_token_and_id(request.user)

    #build the historical api
    api_client = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)
    historical_api = HistoricalApi(api_client)

    #get devices associated to a user
    devices_envelope = get_user_devices(token, user_id)
    #build a string containing the devices ids separated by comma
    devices = ','.join (get_devices_ids(devices_envelope))

    #get devices types pretty names to show on the html
    device_types = get_device_types_for_user(token, user_id)

    #retrieve the last 20 messages for this devices
    message_envelope = historical_api.getNormalizedMessagesLast(devices, count = 20)

    #get the message count from the envelope and the messages
    count = message_envelope.count
    messages = message_envelope.data

    #get a dict containing the devices ids with an associated device name to show on the html
    devices = get_device_id_dict(devices_envelope)

    context_dict = {'active': 'messages', 'count': count, 'messages': messages, 'devices_types':device_types, 'devices':devices}
    return render_to_response("messages.html", context_dict, context)