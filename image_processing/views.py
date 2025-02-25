import threading
import csv
import uuid
import os
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Request, Product
from .image_processing import process_images  # ✅ Import image processing functions


UPLOAD_DIR = os.path.join(os.getcwd(), 'uploads')  # Define absolute path for uploads

@api_view(['POST'])
def upload_csv(request):
    """Upload CSV and store product data."""
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']

        # ✅ Ensure the 'uploads/' directory exists
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        # Validate if the uploaded file is CSV
        if not uploaded_file.name.endswith('.csv'):
            return JsonResponse({'error': 'Invalid file type. Please upload a CSV file.'}, status=400)

        # ✅ Save file temporarily
        file_name = f"uploads/{uuid.uuid4().hex}_{uploaded_file.name}"
        file_path = default_storage.save(file_name, ContentFile(uploaded_file.read()))

        # ✅ Create a unique request ID
        request_id = str(uuid.uuid4())
        new_request = Request(id=request_id, status='PENDING')
        new_request.save()

        # ✅ Read CSV and store products
        products = []
        with default_storage.open(file_path, 'rb') as csv_file:  # ✅ Open in binary mode
            decoded_file = csv_file.read().decode('utf-8')  # ✅ Decode manually
            reader = csv.DictReader(decoded_file.splitlines())  # ✅ Read as lines
            for row in reader:
                product = Product(
                    request=new_request,
                    serial_number=int(row['S. No.']),
                    product_name=row['Product Name'],
                    input_image_urls=[url.strip() for url in row['Input Image Urls'].split(',')]
                )
                products.append(product)

        # ✅ Bulk insert products
        Product.objects.bulk_create(products)

        # ✅ Delete the uploaded file after processing
        default_storage.delete(file_path)

        return JsonResponse({'requestId': request_id}, status=202)

    return JsonResponse({'error': 'No file uploaded or invalid request method'}, status=400)

@api_view(['GET'])
def check_status(request, request_id):
    """Check request status"""
    request_obj = get_object_or_404(Request, id=request_id)
    return Response({"requestId": request_id, "status": request_obj.status})

@api_view(['POST'])
def start_image_processing(request, request_id):
    """Start image processing in a background thread"""
    request_obj = get_object_or_404(Request, id=request_id)
    request_obj.status = "PROCESSING"
    request_obj.save()

    # ✅ Start background processing
    thread = threading.Thread(target=process_images, args=(request_id,))
    thread.start()

    return Response({"message": "Processing started"}, status=202)

@api_view(['POST'])
def webhook_update(request):
    """Webhook endpoint to update request status"""
    data = request.data
    request_id = data.get('requestId')
    status_update = data.get('status')

    request_obj = get_object_or_404(Request, id=request_id)
    request_obj.status = status_update
    request_obj.save()

    return Response({"message": "Status updated"}, status=200)

@api_view(['GET'])
def get_products_by_request_id(request, request_id):
    """Retrieve all products related to a specific requestId."""
    products = Product.objects.filter(request_id=request_id).values(
        'serial_number', 'product_name', 'input_image_urls', 'output_image_urls'
    )

    if not products:
        return JsonResponse({'error': 'No products found for this requestId'}, status=404)

    return JsonResponse({'requestId': request_id, 'products': list(products)}, status=200)
