from django.urls import path,include
from django.conf.urls import url
from . import views
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns=[
    path('',views.home,name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/login/', RedirectView.as_view(url='/accounts/login/?next=/admin/', permanent=True),name='staff_login'),
    path('admin/', admin.site.urls),
    path('logout/',views.userlogout,name="logout"),
    path('signup/',views.signup,name='signup'),
    path('user_login/',views.user_login,name="user_login"),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('cancel/<int:id>/',views.cancel,name='cancel'),
    path('search_hotel',views.search_hotel,name='search_hotel'),
    path('hotel_info/<int:hotel_id>/',views.hotel_info,name='hotel_info'),
    path('book_room/<int:hotel_id>/(<checkin>\d{4}-\d{2}-\d{2})/(<checkout>\d{4}-\d{2}-\d{2})/',views.book_room,name='book_room'),
    path('reservation_room/<int:room_id>/(<checkin>\d{4}-\d{2}-\d{2})/(<checkout>\d{4}-\d{2}-\d{2})/',views.reservation_room,name='reservation_room'),
    path('process_booking/<int:room_id>/(<checkin>\d{4}-\d{2}-\d{2})/(<checkout>\d{4}-\d{2}-\d{2})/',views.process_booking,name='process_booking'),
]