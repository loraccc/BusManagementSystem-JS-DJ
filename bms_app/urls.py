from django.urls import path, include

from . import views
from .views import UserViewSet, BusViewSet, SeatViewSet, BookingViewSet,ProfileView,CustomTokenObtainPairView,UserSignupView

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'buses', BusViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('index/', views.index, name='index'),
    #Bus
    path('', views.bus_list, name='bus_list'),
    path('book/<int:bus_id>/', views.book_bus, name='book_bus'),
    path('select_seat/<int:bus_id>/', views.select_seat, name='select_seat'),
    path('confirm_seat/', views.confirm_seat, name='confirm_seat'),
    path('reset_seats/', views.reset_seats, name='reset_seats'),
    path('book_seat/<int:bus_id>/<int:seat_id>/', views.book_seat, name='book_seat'),
    path('booking_confirmation/<int:bus_id>/<int:seat_id>/', views.booking_confirmation, name='booking_confirmation'),

    path('booking_history/<int:bus_id>/', views.booking_history, name='booking_history'),

    #User
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('serializer/', include(router.urls)),


    path('api/signup/', UserSignupView.as_view(), name='user_signup'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/', TokenVerifyView.as_view(), name='token_refresh'),

    path('api/profile/', ProfileView.as_view(), name='profile_view'),
    path('api/profile/<int:pk>/', ProfileView.as_view(), name='profile_view'),
]