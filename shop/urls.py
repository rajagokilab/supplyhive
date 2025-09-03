from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('files/', views.files, name='files'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('paper/', views.paper, name='paper'),
    path('pens/', views.pens, name='pens'),
     path('school/', views.school, name='school'),
      path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/update/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
      path("api/register/", views.register_user, name="register"),
    path("api/login/", views.login_user, name="login"),
    path("api/logout/", views.logout_user, name="logout"),
    path('auth/', views.auth_view, name='auth'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('api/check-login/',views.check_login_status,name="check_login"),
    path('my-orders/', views.my_orders, name='my_orders'),
     path('track-order/<int:order_id>/', views.track_order, name='track_order'),
     path('product/<int:product_id>/', views.product_detail, name='product_detail'),
# path("search/", views.search_products, name="search_products"),
path("search/", views.search_redirect, name="search_redirect"),
]
