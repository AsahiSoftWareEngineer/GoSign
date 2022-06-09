from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("check/<str:agreement_id>/",views.Check.as_view(), name="check"),
    path("confirm/", views.Confirm.as_view(), name="confirm"),
    path("certificate/<str:agreement_id>/", views.Certificate.as_view(), name="certificate"),
    path("manage/create/", views.CreateView.as_view(), name="create"),
    path("manage/list/", views.ListView.as_view(), name="list"),
    path("manage/agreement/<str:agreement_id>/", views.PreView.as_view(), name="agreement"),
    path("complete/", views.CompleteView.as_view(), name="complete")
]