from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('tes.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    # Check if the request has a file part
    if 'image' not in request.files:
        return 'No file uploaded.', 400

    file = request.files['image']

    # If user does not select a file, the browser also submits an empty part
    if file.filename == '':
        return 'No selected file.', 400

    if file:
        # Save the uploaded image to the uploads folder
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(image_path)

        # Open the image using PIL
        image = Image.open(image_path)

        # Use pytesseract to extract text
        extracted_text = pytesseract.image_to_string(image)

        # Remove the image after processing (optional)
        os.remove(image_path)

        # Return the extracted text to be displayed on the HTML page
        return {
            'extracted_text': extracted_text
        }

if __name__ == '__main__':
    app.run(debug=True)
