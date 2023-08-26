from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from users.views import ResetPasswordView

app_name = 'core'

urlpatterns = [

    path('', views.main_dashboard, name='main_dashboard'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('forgot_password/', views.forget_password, name='forgot_password'),
    path('login/', views.login_base, name='login'),
    path('change_password/<str:token>/', views.change_password, name='change_password')
    # url(r'^finance_account/$', views.finance_accounts, name='finance_account'),
    # url(r'^branch1/$',views.branch1,name='branch1'),
    # url(r'^get_data/$', views.get_dashboard_data, name='get_data'),
    # url(r'^get_data_finance/$',views.get_finance_account_data, name='finance_data'),
    # url(r'^filter_data/$',views.filter_data,name='filter_data'),
    # url(r'^finance_filter/$',views.finance_filter,name='finance_filter')
]