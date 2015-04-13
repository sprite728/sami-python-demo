import sys
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from UsersApi import UsersApi
from DevicesApi import DevicesApi
from samiio import ApiClient
from python import settings
from templateUtils import get_item
from django.contrib.auth.decorators import login_required
from user import getTokenAndId


@login_required
def showDevices(request):
    """shows the first ten devices for the logged in user

                Args:
                    request: django request object
                Returns: Render devices.html
                """
    context = RequestContext(request)

    #get token and user id from the django user
    token, userId = getTokenAndId(request.user)

    devicesEnvelope = getUserDevices(token, userId)

    #retrieve count and devices from the devices envelope
    count = devicesEnvelope.count
    devices = list(devicesEnvelope.data.devices)

    #get devices types pretty names to show on the html
    deviceTypes = getDeviceTypesForUser(token, userId)
    contextDict = {'active': 'devices', 'count': count, 'devices': devices, 'devicesTypes':deviceTypes}

    #TODO should disable "Register Device" button when navigating to the html page
    return render_to_response("devices.html", contextDict, context)

def getDeviceTypesForUser(token, userId):
    """get a list of device types so we can build a dictionary containing a device type id as key and a device name as value

                Args:
                    token: user access token
                    userId: samsung user id
                Returns: python dictionary with type device id as key and device type name as value
                """
    #build usersApi
    apiClient = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)
    usersApi = UsersApi(apiClient = apiClient)

    #get device types
    deviceTypesEnvelope = None
    try:
        deviceTypesEnvelope = usersApi.getUserDeviceTypes(userId, includeShared='true')
    except:
        print "Unexpected error:", sys.exc_info()[0]

    #retrieve the devices types from the device types envelope
    deviceTypes = []
    if not(deviceTypesEnvelope is None):
        deviceTypes = list(deviceTypesEnvelope.data.deviceTypes)

    #build dict
    deviceTypeDict = {}
    for dt in deviceTypes:
        deviceTypeDict[dt.id]= dt.name

    return deviceTypeDict



@login_required
def addDevice(request):
    """add a device for the logged in user

                Args:
                    request: django request object
                Returns: on POST redirects to /devices
                         on GET renders adddevice.html
                """
    context = RequestContext(request)

    #get token and user id from the django user
    token, userId = getTokenAndId(request.user)

    #build apiClient
    api_client = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)

    #get devices types dictionary
    deviceTypes = getDeviceTypesForUser(token, userId)

    if not deviceTypes:
        print "addDevice: got empty device type list. call showDevices() again  and early return"
        return showDevices(request)
    
    contextDict = {'active': 'devices', 'devicesTypes':deviceTypes}

    if (request.method == 'POST'):
        #user wants to add a device

        #retrieve device data from form
        deviceName = request.POST.get('deviceName', '')
        deviceType = request.POST.get('deviceType', '')
        optionManifest = request.POST.get('optionManifest', '')

        deviceApi = DevicesApi(api_client)
        #create a body for the post request of the api. Make sure not to send unicode strings.
        body = {'uid': userId.encode('ascii'),
                'dtid':deviceType.encode('ascii'),
                'name': deviceName.encode('ascii'),
                'manifestVersion': 2,
                'manifestVersionPolicy': optionManifest.encode('ascii')
        }

        #add the device
        deviceApi.addDevice(body)
        return HttpResponseRedirect('/devices')

    return render_to_response('adddevice.html', contextDict, context)

def getUserDevices(token, userId):
    """get devices for a samsung user

                Args:
                    token: user access token
                    userId: samsung user id
                Returns: devices envelope
                """
    #build usersApi object
    apiClient = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)
    usersApi = UsersApi(apiClient = apiClient)

    #get the first 10 devices
    devicesEnvelope = usersApi.getUserDevices(userId, count = 10)
    return devicesEnvelope

def getDevicesIds(devicesEnvelope):
    """get a list with users devices ids

                Args:
                    devicesEnvelope: devicesEnvelope containing the devices for the user
                Returns:  list with users devices ids
                """
    devices = []
    for device in devicesEnvelope.data.devices:
        devices.append(device.id)
    return devices

def getDeviceIdDict(devicesEnvelope):
    """get a dictionary with users devices ids as key and the device name as value

               Args:
                   devicesEnvelope: devicesEnvelope containing the devices for the user
               Returns:  dictionary with users devices ids as key and the device name as value
               """
    devices = {}
    for device in devicesEnvelope.data.devices:
        devices[device.id] = device.name
    return devices
