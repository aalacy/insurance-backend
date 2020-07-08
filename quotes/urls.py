from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter

from quotes.views import (
	QuoteShellViewSet,
	QuoteViewSet,
	DriverViewSet,
	VehicleViewSet,
	AddressViewSet
)

# Create a router and register our viewsets with it.
# router = DefaultRouter()
# router.register(r'', views.QuoteShellViewSet)
# router.register(r'quotes', views.QuoteViewSet)
# router.register(r'drivers', views.DriverViewSet)
# router.register(r'vehicles', views.VehicleViewSet)

# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
# 	pass

# router = NestedDefaultRouter()

router = ExtendedSimpleRouter()
quote_router = router.register(r'api/quoteshell', QuoteShellViewSet, basename='shell')
quote_router.register(
				r'quotes',
				QuoteViewSet,
				basename='quotes',
				parents_query_lookups=['quote_shell']
			)

"""
	Drivers

	Create URL
		api/quoteshell/<quote_shell_id>/quotes/<quote_id>/drivers/

	Update URL
		api/quoteshell/<quote_shell_id>/quotes/<quote_id>/drivers/<driver_id>/
"""
quote_router.register(
				r'quotes',
				QuoteViewSet,
				basename='quotes',
				parents_query_lookups=['quote_shell']
			).register(
				r'drivers',
				DriverViewSet,
				basename='quotes-drivers',
				parents_query_lookups=['quote__quote_shell', 'quote']
			)

"""
	Vehicles

	Create URL
		api/quoteshell/<quote_shell_id>/quotes/<quote_id>/vehicles/

	Update URL
		api/quoteshell/<quote_shell_id>/quotes/<quote_id>/vehicles/<vehicle_id>/
"""
quote_router.register(
				r'quotes',
				QuoteViewSet,
				basename='quotes',
				parents_query_lookups=['quote_shell']
			).register(
				r'vehicles',
				VehicleViewSet,
				basename='quotes-vehicles',
				parents_query_lookups=['quote__quote_shell', 'quote']
			)

"""
	Address

	Create URL
		api/quoteshell/<quote_shell_id>/quotes/<quote_id>/vehicles/

	Update URL
		api/quoteshell/<quote_shell_id>/quotes/<quote_id>/vehicles/<vehicle_id>/
"""
quote_router.register(
				r'quotes',
				QuoteViewSet,
				basename='quotes',
				parents_query_lookups=['quote_shell']
			).register(
				r'addresses',
				AddressViewSet,
				basename='quotes-addresses',
				parents_query_lookups=['quote__quote_shell', 'quote']
			)
			
# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls))
]