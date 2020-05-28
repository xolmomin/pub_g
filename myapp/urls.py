from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .bot import UpdateBot
from .views import index, signup, login_user, logout_user, activate, add_tournament

urlpatterns = [
    path('', csrf_exempt(index), name='index'),
    path('signup/', csrf_exempt(signup), name='signup'),
    path('login/', csrf_exempt(login_user), name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('secret', csrf_exempt(UpdateBot.as_view())),
    path('add/<int:id>', csrf_exempt(add_tournament), name='add_tournament'),
]
