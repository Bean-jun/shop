"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

    针对之前1.8中较为熟悉的namespace操作，这里需要注意下：
        - 目前在试探的内容：
            
            可以在子路由下写上app_name='子路由名'即可，当然想多在在这个主路由下写一写namespace='子路由名'也可
        
        - 目前已经确定的内容：

"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls', namespace='user')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('order/', include('apps.order.urls', namespace='order')),
    path('', include('apps.goods.urls', namespace='goods')),
]
