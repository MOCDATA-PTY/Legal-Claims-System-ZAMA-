from django.urls import path
from . import views

urlpatterns = [
    # Existing URL patterns
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('add/', views.add_shipment, name='add_shipment'),
    path('shipments/', views.shipment_list, name='shipment_list'),
    path('shipment/<int:pk>/edit/', views.edit_shipment, name='edit_shipment'),
    path('export/excel/', views.export_shipments_excel, name='export_shipments_excel'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('666/', views.register, name='register'),
    path('get-client-names/', views.get_client_names, name='get_client_names'),
    path('import/excel/', views.import_shipments, name='import_shipments'),
    path('delete_shipment/<int:pk>/', views.delete_shipment, name='delete_shipment'),
    # New URL for clearing the database
    path('clear-database/', views.clear_database, name='clear_database'),
    path('client-autocomplete/', views.client_autocomplete, name='client_autocomplete'),
]
