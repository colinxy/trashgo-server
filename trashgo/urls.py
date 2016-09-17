from django.conf.urls import url
# from rest_framework import routers
# from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# router = routers.DefaultRouter()
# router.register(r"hotspots", views.HotspotViewSet)

urlpatterns = [
    url(r"^hotspots/$", views.HotspotView.as_view()),
    url((r"^hotspots/"
         r"(?P<ne_lat>-?\d+\.?\d*)/"
         r"(?P<ne_lng>-?\d+\.?\d*)/"
         r"(?P<sw_lat>-?\d+\.?\d*)/"
         r"(?P<sw_lng>-?\d+\.?\d*)/$"),
        views.HotspotWithinView.as_view()),
    url((r"^bins/"
         r"(?P<ne_lat>-?\d+\.?\d*)/"
         r"(?P<ne_lng>-?\d+\.?\d*)/"
         r"(?P<sw_lat>-?\d+\.?\d*)/"
         r"(?P<sw_lng>-?\d+\.?\d*)/$"),
        views.BinWithinView.as_view()),
    url(r"^users/$", views.UserView.as_view()),
    url(r"^teams/$", views.TeamView.as_view()),
    url(r"^bins/$", views.BinView.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
