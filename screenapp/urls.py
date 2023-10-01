from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views
from django.views.decorators.csrf import csrf_exempt


router = SimpleRouter()
router.register('api', views.ScreenVideoViewSet)

urlpatterns=[
    #home page
    #path('', views.index, name='index'),
    #path('api',views.PersonListView.as_view(),name='Person-list'),
    path('api/upload',views.ScreenVideoUploadView.as_view(),name='create-video'),
   # path('api/<str:name>', views.PersonRetrieveByName.as_view(),name="Retrieve-Person-by-name")
   
]