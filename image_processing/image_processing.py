import threading
import uuid
import requests
from io import BytesIO
from PIL import Image
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from .models import Request, Product
import os




# def compress_image(image_url):
#     """Download, compress image by 50%, and save it locally."""
#     try:
#         print(f"Downloading image: {image_url}")

#         # ✅ Add headers to mimic a real browser
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
#                           "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         }
#         response = requests.get(image_url, headers=headers, stream=True)

#         if response.status_code != 200:
#             print(f"Failed to download image: {image_url}, Status Code: {response.status_code}")
#             return None

#         img = Image.open(BytesIO(response.content))
#         img = img.convert("RGB")  # Ensure it's in RGB mode

#         # Compress image
#         output_buffer = BytesIO()
#         img.save(output_buffer, format="JPEG", quality=50)  # 50% quality
#         output_buffer.seek(0)

#         # Generate unique filename
#         filename = f"compressed_{uuid.uuid4().hex}.jpg"
#         file_path = f"media/processed_images/{filename}"

#         # Ensure 'processed_images/' directory exists
#         if not os.path.exists("media/processed_images"):
#             os.makedirs("media/processed_images")

#         # Save compressed image
#         with open(file_path, 'wb') as output_file:
#             output_file.write(output_buffer.getvalue())

#         # ✅ Return URL for the compressed image
#         compressed_url = f"http://127.0.0.1:8000/{file_path}"
#         print(f"Compressed Image Saved: {compressed_url}")
#         return compressed_url

#     except Exception as e:
#         print(f"Error processing image {image_url}: {str(e)}")
#     return None

# def process_images(request_id):
#     """Background task to compress images and update database"""
#     request_obj = get_object_or_404(Request, id=request_id)
#     products = Product.objects.filter(request=request_obj)

#     for product in products:
#         output_urls = [compress_image(url) for url in product.input_image_urls if url]
#         product.output_image_urls = output_urls
#         product.save()

#     request_obj.status = "COMPLETED"
#     request_obj.save()




def compress_image(image_url):
    """Simulate image processing by appending '-output' to the input URL."""
    try:
        print(f"Processing image: {image_url}")
        
        # ✅ Simulated Output URL by appending "-output"
        output_url = f"{image_url}-output"

        print(f"Generated Output URL: {output_url}")
        return output_url

    except Exception as e:
        print(f"Error processing image {image_url}: {str(e)}")
        return None




def process_images(request_id):
    """Background task to update processed image URLs."""
    request_obj = get_object_or_404(Request, id=request_id)
    products = Product.objects.filter(request=request_obj)

    for product in products:
        print(f"Processing Product: {product.product_name}")
        print(f"Input URLs: {product.input_image_urls}")

        # ✅ Handle both string and list formats
        if isinstance(product.input_image_urls, str):
            input_urls = product.input_image_urls.split(", ")
        elif isinstance(product.input_image_urls, list):
            input_urls = product.input_image_urls
        else:
            print("Error: Invalid input_image_urls format!")
            continue

        output_urls = [compress_image(url.strip()) for url in input_urls]

        print(f"Generated Output URLs: {output_urls}")

        # ✅ Store as a list
        product.output_image_urls = output_urls  
        product.save()

    request_obj.status = "COMPLETED"
    request_obj.save()
