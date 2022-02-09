from django.urls import path
from .views import list_moves, main_view, validate_moves, test_json_view


urlpatterns = [
    path('', main_view),
    path('jsonresp/', test_json_view),
    path('api/v1/<str:figure>/<str:field>/', list_moves),
    path('api/v1/<str:figure>/<str:field1>/<str:field2>/', validate_moves)
]