from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from UsersApi import UsersApi
from DevicesApi import DevicesApi
from samihub import ApiClient
from python import settings
from templateUtils import get_item
from django.contrib.auth.decorators import login_required
from user import get_token_and_id

@login_required
def show_devices(request):
    """shows the first ten devices for the logged in user

                Args:
                    request: django request object
                Returns: Render devices.html
                """
    context = RequestContext(request)

    #get token and user id from the django user
    token, user_id = get_token_and_id(request.user)

    devices_envelope = get_user_devices(token, user_id)

    #retrieve count and devices from the devices envelope
    count = devices_envelope.count
    devices = list(devices_envelope.data.devices)

    #get devices types pretty names to show on the html
    device_types = get_device_types_for_user(token, user_id)
    context_dict = {'active': 'devices', 'count': count, 'devices': devices, 'devices_types':device_types}
    return render_to_response("devices.html", context_dict, context)

def get_device_types_for_user(token, user_id):
    """get a list of device types so we can build a dictionary containing a device type id as key and a device name as value

                Args:
                    token: user access token
                    user_id: samsung user id
                Returns: python dictionary with type device id as key and device type name as value
                """
    #build usersApi
    api_client = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)
    users_api = UsersApi(apiClient = api_client)

    #get device types
    device_types_envelope = users_api.getUserDeviceTypes(user_id, includeShared='true')

    #retrieve the devices types from the device types envelope
    device_types = list(device_types_envelope.data.deviceTypes)

    #build dict
    device_type_dict = {}
    for dt in device_types:
        device_type_dict[dt.id]= dt.name

    return device_type_dict



@login_required
def add_device(request):
    """add a device for the logged in user

                Args:
                    request: django request object
                Returns: on POST redirects to /devices
                         on GET renders adddevice.html
                """
    context = RequestContext(request)

    #get token and user id from the django user
    token, user_id = get_token_and_id(request.user)

    #build apiClient
    api_client = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)

    #get devices types dictionary
    device_types = get_device_types_for_user(token, user_id)
    context_dict = {'active': 'devices', 'devices_types':device_types}


    if (request.method == 'POST'):
        #user wants to add a device

        #retrieve device data from form
        device_name = request.POST.get('deviceName', '')
        device_type = request.POST.get('deviceType', '')
        option_manifest = request.POST.get('optionManifest', '')

        device_api = DevicesApi(api_client)
        #create a body for the post request of the api. Make sure not to send unicode strings.
        body = {'uid': user_id.encode('ascii'),
                'dtid':device_type.encode('ascii'),
                'name': device_name.encode('ascii'),
                'manifestVersion': 2,
                'manifestVersionPolicy': option_manifest.encode('ascii')
        }

        #add the device
        device_api.addDevice(body)
        return HttpResponseRedirect('/devices')


    return render_to_response('adddevice.html', context_dict, context)

def get_user_devices(token, user_id):
    """get devices for a samsung user

                Args:
                    token: user access token
                    user_id: samsung user id
                Returns: devices envelope
                """
    #build usersApi object
    api_client = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)
    users_api = UsersApi(apiClient = api_client)

    #get the first 10 devices
    devices_envelope = users_api.getUserDevices(user_id, count = 10)
    return devices_envelope

def get_devices_ids(devices_envelope):
    """get a list with users devices ids

                Args:
                    devices_envelope: devicesEnvelope containing the devices for the user
                Returns:  list with users devices ids
                """
    devices = []
    for device in devices_envelope.data.devices:
        devices.append(device.id)
    return devices

def get_device_id_dict(devices_envelope):
    """get a dictionary with users devices ids as key and the device name as value

               Args:
                   devices_envelope: devicesEnvelope containing the devices for the user
               Returns:  dictionary with users devices ids as key and the device name as value
               """
    devices = {}
    for device in devices_envelope.data.devices:
        devices[device.id] = device.name
    return devices
