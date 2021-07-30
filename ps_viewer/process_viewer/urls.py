from django.urls import path
from . import views

urlpatterns = [
    path('monitor', views.values_list),
    path('monitor/<int:pk>', views.values_detail),
    path('show_table', views.DataList.as_view(), name='data_table')
]
