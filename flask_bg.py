import os
import joblib
import tensorflow
from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input # type: ignore
from tensorflow.keras.preprocessing.image import img_to_array # type: ignore
# from flask_cors import CORS # For Mobile App

app = Flask(__name__)
# CORS(app) # For Mobile App

mobilenet = MobileNetV2(weights='imagenet', include_top=False, pooling='avg') # Comment In if does not run

# Call SVM Model
model_path = os.path.join(os.getcwd(), 'svm_model.pkl')
model = joblib.load(model_path)

# Preprocessing Uploaded image so that it gets coverted into MobileNetV2 accepted format(224, 224, 3)
def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224)) 
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    features = mobilenet.predict(img_array) #type: ignore
    return features


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image_path = os.path.join('uploads', image.filename)
    os.makedirs('uploads', exist_ok=True)
    image.save(image_path)

    try:
        processed_image = preprocess_image(image_path)

        prediction = model.predict(processed_image)

        os.remove(image_path)

        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
