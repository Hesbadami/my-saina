"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from store import views as store_views
from CoachContracts import views as cc_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registerlogin/', store_views.registerlogin, name='registerlogin'),
    path('logout/', store_views.logoutUser, name='logout'),
    path('profile/', store_views.userProfile, name='profile'),
    path('', store_views.landing, name='landing'),
    path('CoachContracts/Consulation', cc_views.consulation, name='cc_consulation'),
    path('CoachContracts/Contracts/Register', cc_views.register, name='coach_register'),
    path(
        "create-checkout-session/<int:pk>/",
        store_views.StripeCheckoutSession.as_view(),
        name="create-checkout-session",
    ),
    path("success/", store_views.SuccessView.as_view(), name="success"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
