"""
URL configuration for challenge project.

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

from core.client.views import ClientAccountBalance
from core.client.views import ClientCategoryAssignment
from core.client.views import ClientDetailUpdate
from core.client.views import ClientListCreate
from core.movements.views import MovementCreate
from core.movements.views import MovementDetailDelete

urlpatterns = [
    path('clients/', ClientListCreate.as_view()),
    path('clients/<int:pk>/', ClientDetailUpdate.as_view()),
    path('clients/<int:pk>/accounts/', ClientAccountBalance.as_view()),
    path('clients/categories/', ClientCategoryAssignment.as_view()),
    path('movements/', MovementCreate.as_view()),
    path('movements/<int:pk>/', MovementDetailDelete.as_view()),
    path('admin/', admin.site.urls),
]
