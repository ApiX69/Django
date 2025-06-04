from django.urls import path
from .views import signup_view, login_view, logout_view, home_view, custom_change_roles_view, about_view, deals_view, reservation_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', home_view, name='home'),
    path('change_roles/', custom_change_roles_view, name='change_roles'),
    path('about/', about_view, name='about'),
    path('deals/', deals_view, name='deals'),
    path('reservation/', reservation_view, name='reservation'),
]
