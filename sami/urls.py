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
    url(r'^login_required$', user.login_required, name='login_required'), #redirect to this page when user is not logged in
    url(r'^messages/$', messages.show_messages, name='show_messages'),
    url(r'^devices/$', devices.show_devices, name='show_devices'),
    url(r'^devices/adddevice$', devices.add_device, name='add_device'),
)
