from django.urls import path
from .views import CookieStandList, ThingDetail

urlpatterns = [
    path("", CookieStandList.as_view(), name="thing_list"),
    path("<int:pk>/", ThingDetail.as_view(), name="thing_detail"),
]
