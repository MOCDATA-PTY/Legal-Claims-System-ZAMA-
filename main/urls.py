from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root redirects to login if not authenticated
    path('home/', views.home, name='home'),  # Home page (protected)
    path('add/', views.add_shipment, name='add_shipment'),  # Form page for adding shipments
    path('shipments/', views.shipment_list, name='shipment_list'),  # View all shipments
    path('shipment/<int:pk>/edit/', views.edit_shipment, name='edit_shipment'),  # Edit a shipment
    path('export/excel/', views.export_shipments_excel, name='export_shipments_excel'),  # Export shipments to Excel
    path('login/', views.user_login, name='login'),  # User login
    path('logout/', views.user_logout, name='logout'),  # User logout
    # path('666/', views.register, name='register'),  # User registration
    path('get-client-names/', views.get_client_names, name='get_client_names'),  # Client names API
    path('import/excel/', views.import_shipments, name='import_shipments'),  # Import shipments from Excel
]
