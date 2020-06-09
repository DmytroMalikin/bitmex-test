from rest_framework.routers import DefaultRouter
from api.views import OrderViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='orders')
urlpatterns = router.urls
