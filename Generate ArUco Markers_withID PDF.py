import cv2
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image

def generate_aruco_marker(id, size=5):
    """Generate an ArUco marker image."""
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, id, 200)
    return marker_image

def create_aruco_pdf(output_file, marker_size_mm=12, page_size=(210, 297)):
    """Create a PDF with ArUco markers and their IDs."""
    c = canvas.Canvas(output_file, pagesize=(page_size[0]*mm, page_size[1]*mm))
    
    marker_size_points = marker_size_mm * 72 / 25.4  # Convert mm to points
    
    # Calculate how many markers can fit on the page
    markers_per_row = int(page_size[0] / (marker_size_mm + 5))  # 5mm gap
    markers_per_column = int(page_size[1] / (marker_size_mm + 10))  # 10mm gap for ID text
    
    for i in range(markers_per_row * markers_per_column):
        marker = generate_aruco_marker(i)
        
        # Convert OpenCV image to PIL Image
        pil_image = Image.fromarray(marker)
        
        # Save PIL image to a BytesIO object
        bio = BytesIO()
        pil_image.save(bio, format='PNG')
        
        # Get the position for this marker
        row = i // markers_per_row
        col = i % markers_per_row
        x = col * (marker_size_mm + 5) * mm
        y = page_size[1]*mm - (row + 1) * (marker_size_mm + 10) * mm
        
        # Draw the marker on the PDF
        c.drawImage(ImageReader(bio), x, y, width=marker_size_points, height=marker_size_points)
        
        # Add the marker ID below the marker
        c.setFont('Helvetica', 8)  # Set font to Helvetica, size 8
        c.drawString(x + (marker_size_mm / 2) * mm - 10, y - 3 * mm, f"ID: {i}")
    
    c.save()

# Generate the PDF
create_aruco_pdf('aruco_markers_with_ids.pdf')
print("ArUco markers PDF with IDs has been generated.")