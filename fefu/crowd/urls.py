from django.urls import path
from crowdapp import views
from django.contrib.auth import views as auth_views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="IDEA",
        default_version="v0.1",
        description="Описание работы API IDEA",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="styxykk@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    # Статические страницы
    path('', views.main_page, name='main'),
    path('news/', views.news_page, name='news'),
    path('about/', views.about_page, name='about'),
    path('faq/', views.faq_page, name='faq'),

    # Авторизация
    path('login/', views.user_login, name='login'),
    path('register/', views.user_signup, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Профиль
    path('account/', views.account_view, name='account'),
    path('update-photo/', views.update_photo, name='update_photo'),

    # Идеи
    path('add-idea/', views.add_idea, name='add_idea'),
    path('like/<int:idea_id>/', views.like_idea, name='like_idea'),
    path('dislike/<int:idea_id>/', views.dislike_idea, name='dislike_idea'),

    # Комментарии
    path('idea/<int:idea_id>/comments/', views.idea_comments, name='idea_comments'),
    path('idea/<int:idea_id>/add_comment/', views.add_comment, name='add_comment'),

    # API
    path('api/signup/', views.UserSignupAPIView.as_view(), name='user_signup'),
    path('api/login/', views.UserLoginAPIView.as_view(), name='user_login'),
    path('api/add-idea/', views.AddIdeaAPIView.as_view(), name='add_idea'),
    path('api/ideas/<int:idea_id>/like/', views.LikeIdeaAPIView.as_view(), name='like_idea'),
    path('api/ideas/<int:idea_id>/add_comment/', views.AddCommentAPIView.as_view(), name='add_comment'),

    # Документация
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)