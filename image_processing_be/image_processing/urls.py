from django.urls import path
from .views import upload_csv, check_status, start_image_processing, webhook_update,get_products_by_request_id

urlpatterns = [
    # path('upload/', upload_csv, name='upload_csv'),
    path('upload/', upload_csv, name='upload_csv'),
    path('status/<uuid:request_id>/', check_status, name='check_status'),
    path('process/<uuid:request_id>/', start_image_processing, name='start_processing'),
    path('webhook/', webhook_update, name='webhook_update'),
    path('products/<uuid:request_id>/', get_products_by_request_id, name='get_products_by_request_id'),
]
