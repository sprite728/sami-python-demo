from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from UsersApi import UsersApi
from samiio import ApiClient
from python import settings
from urllib import urlencode
from models import Profile
import requests
from django.contrib.auth.decorators import login_required
import ast


def getSelf(token):
    """Get current user from api

            Args:
                token (required): access token for oauth2
            Returns: User
            """
    #create and build the UsersApi
    apiClient = ApiClient(apiKey=token, apiServer = settings.SAMI_SERVER_URL)
    usersApi = UsersApi(apiClient = apiClient)

    #get current user
    userEnvelope = usersApi.self()

    #return content of the user_envelope, that is, the current user
    return userEnvelope.data

def login(request):
    """Login user to samsung account service

                Args:
                    request: django request object
                Returns: Redirect to https://accounts.samihub.com/authorize?
                """
    #build oauth2 authorize url. This step is needed to get the code for the second oauth2 step
    url = settings.SAMI_ACCOUNT_SERVER_URL + "/authorize?"

    param = {'client_id':settings.CLIENT_ID, #(required) your app client_id
             'response_type':'code', #(required) we tell the account server we need a code as return value
             'redirect_uri':settings.SAMI_RETURN_URI, #(optional but recommended) Url callback. Oauth2 server will call our server on this url with
                                                        #the code parameter. Be sure to have registered this url on http://portal.samihub.com
             'scope':'read,write'  #(Optional) The type of permissions the application is requesting over the user's data, as a comma separated list. For example: read or read,write. If omitted its default value is read,write.
             }
    query = urlencode(param)
    url += query

    return HttpResponseRedirect(url)

def authorized(request):
    """Callback for the oauth2 authorize call

                Args:
                    request: django request object
                Returns: Redirect to home page on success
                """
    context = RequestContext(request)

    if (request.method == 'GET'):
        #retrieve code from url
        code = request.GET.get('code', '')

        #build the url needed for the second step of the oauth2 flow. With this we should get the access token
        url = settings.SAMI_ACCOUNT_ACCESS_TOKEN

        param = {'code':code, #(required) code we just retrieved
             'redirect_uri':settings.SAMI_RETURN_URI, #(optional) a redirect url in case something goes wrong
             'client_id': settings.CLIENT_ID, #(required) app client id
             'client_secret': settings.CLIENT_SECRET, #(required) app client secret
             'grant_type': "authorization_code" #(required) type of access to be granted
            }

        #do a post request for the second step of the oauth2 flow
        result = requests.post(url, data = param)
        if (result.status_code != 200):
            print("Error: Could not get access token from oauth server")

        data = ast.literal_eval(result.text)
        token = (data["access_token"])

        #get current user
        samiUser = getSelf(token=token)

        contextDict = {'active':"home"}
        response = HttpResponseRedirect('/', contextDict, context)

        #We will use django built in login funcionality to log in and log out users to the demo site. We shall associate
        #a profile model containing the access_token for the user so we can retrieve each time the user does a request
        try:
            #we use the sami user id as user name so it is unique
            user = User.objects.get(username=samiUser.id)
        except User.DoesNotExist:

            #if no user found we create one
            user = User.objects.create_user(username=samiUser.id, password=samiUser.id)

            #we create a profile, stash the access token and link it to the user
            profile = Profile()
            profile.user = user
            profile.oauth_token = token
            profile.save()

        #django login
        user = authenticate(username=samiUser.id, password=samiUser.id)
        django_login(request, user)

    return response

@login_required
def logout(request):
    """Logout a user and redirect to home page

                Args:
                    request: django request object
                Returns: Redirect to home page
                """
    context = RequestContext(request)

    contextDict = {'active':"home"}
    django_logout(request)

    return HttpResponseRedirect('/', contextDict, context)

def getTokenAndId(user):
    """Retrieve a user id and token for a logged in user

                Args:
                    user: django user model
                Returns: token: access token string
                         userId: samsung user id
                """
    #retrieve profile based on the django user id (not the samsung id)
    profile = Profile.objects.get(user=user.id)
    token = profile.oauth_token
    userId = user.username
    return token, userId

def loginRequired(request):
    """The server redirects to this view when a user tries to do an action that requieres login

                Args:
                    request: django request object
                Returns: Redirect to login.html
                """

    context = RequestContext(request)

    contextDict = {'active':"home"}

    return render_to_response("login.html", contextDict, context)