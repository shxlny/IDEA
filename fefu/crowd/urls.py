from django.urls import path
from crowdapp import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_signup, name='register'),
    path('news/', views.news_page, name='news'),
    path('about/', views.about_page, name='about'),
    path('faq/', views.faq_page, name='faq'),
    path('account/', views.account_view, name='account'),  # Теперь использует account_view
    path('update-photo/', views.update_photo, name='update_photo'),
    path('add-idea/', views.add_idea, name='add_idea'),
    path('like/<int:idea_id>/', views.like_idea, name='like_idea'),
    path('dislike/<int:idea_id>/', views.dislike_idea, name='dislike_idea'),
    path('idea/<int:idea_id>/comments/', views.idea_comments, name='idea_comments'),
    path('idea/<int:idea_id>/add_comment/', views.add_comment, name='add_comment'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
