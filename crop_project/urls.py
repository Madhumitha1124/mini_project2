from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('prediction.urls')),
    path('accounts/', include('accounts.urls')),
    path('login/', RedirectView.as_view(url='/accounts/login/', permanent=False)),
    path('register/', RedirectView.as_view(url='/accounts/register/', permanent=False)),
    path('logout/', RedirectView.as_view(url='/accounts/logout/', permanent=False)),
    path('profile/', RedirectView.as_view(url='/accounts/profile/', permanent=False)),
]
