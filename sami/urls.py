from django.conf.urls import patterns, include, url
from sami import views
from sami import user
from sami import devices
from sami import messages

urlpatterns = patterns('',

    url(r'^$', views.home, name='home'), #home url
    url(r'^users/login$', user.login, name='login'), #init oauth authentication url
    url(r'^users/authorized$', user.authorized, name='authorized'), #callback for oauth
    url(r'^users/logout$', user.logout, name='logout'), #logout
    url(r'^login_required$', user.loginRequired, name='loginRequired'), #redirect to this page when user is not logged in
    url(r'^messages/$', messages.showMessages, name='showMessages'),
    url(r'^devices/$', devices.showDevices, name='showDevices'),
    url(r'^devices/adddevice$', devices.addDevice, name='addDevice'),
)
