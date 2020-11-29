from rest_framework import routers
from metallics_api import views_api as api_view

router = routers.DefaultRouter()
router.register(r'chemical_element', api_view.ChemicalViewSet)
router.register(r'commodity', api_view.CommodityViewSet)
router.register(r'chemical_concentration', api_view.CompositionViewSet)
