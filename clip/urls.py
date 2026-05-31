from django.urls import path


from .views import (
    process_video_api,
    history_api,
    register_api,
    login_api,
)

urlpatterns = [
    path(
        "process/",
        process_video_api
    ),

    path(
        "history/",
        history_api
    ),
    path(
        "register/",
        register_api
    ),

    path(
        "login/",
        login_api
    ),
]