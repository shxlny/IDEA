from django.urls import path
from crowdapp import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_signup, name='register'),
    path('news/', views.news_page, name='news'),
    path('about/', views.about_page, name='about'),
    path('faq/', views.faq_page, name='faq'),
    path('account/', views.update_profile, name='account'),
    path('update-photo/', views.update_photo, name='update_photo'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('add_idea/', views.add_idea, name='add_idea'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
