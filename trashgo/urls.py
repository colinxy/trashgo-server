from django.conf.urls import url
# from rest_framework import routers

from . import views

# router = routers.DefaultRouter()
# router.register(r"hotspots", views.HotspotViewSet)

urlpatterns = [
    url(r"^hotspots", views.HotspotView.as_view()),
]
