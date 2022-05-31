from api.views import CommentViewSet, ReviewViewSet
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r"titles/(?P<title_id>[^/.]+)/reviews", ReviewViewSet, basename='review'
)
router.register(
    r"titles/(?P<title_id>[^/.]+)/reviews/(?P<review_id>[^/.]+)/comments",
    CommentViewSet,
    basename='comment'
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('', include(router.urls))
]
