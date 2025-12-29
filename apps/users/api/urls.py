from django.urls import path, include

urlpatterns = [
    # Djoser's default endpoints (Register, Me, Password Reset, etc.)
    path('', include('djoser.urls')),

    # JWT endpoints (Login, Refresh)
    path('', include('djoser.urls.jwt')),
]