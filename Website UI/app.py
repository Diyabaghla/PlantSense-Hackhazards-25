# from flask import Flask, render_template, request, jsonify
# import tensorflow as tf
# import numpy as np
# import os
# import cv2
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
#
# # Load trained CNN model with error handling
# MODEL_PATH = os.path.abspath("my_model.keras")
#
# if not os.path.exists(MODEL_PATH):
#     print(f"❌ Model file not found: {MODEL_PATH}")
#     model = None
# else:
#     try:
#         model = tf.keras.models.load_model(MODEL_PATH)
#         print("✅ Model loaded successfully!")
#     except Exception as e:
#         print(f"❌ Error loading model: {e}")
#         model = None
#
# # Define class labels
# CLASS_NAMES = ["Healthy", "Early Blight", "Late Blight"]
#
# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
#
#
# def allowed_file(filename):
#     """Check if file extension is allowed."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# # Home route
# @app.route('/')
# def home():
#     return render_template("final.html")
#
#
# # Image preprocessing function
# def preprocess_image(img_path):
#     """Load, convert, resize, and normalize an image."""
#     img = cv2.imread(img_path)
#     if img is None:
#         raise ValueError(f"❌ Error loading image: {img_path}")
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = cv2.resize(img, (255, 255))
#     img = img.astype('float32') / 255.0
#     img = np.expand_dims(img, axis=0)
#     return img
#
#
# @app.route("/predict", methods=["POST"])
# def predict():
#     # Check if the request contains a file
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
#
#     file = request.files["file"]
#
#     # Ensure a file is actually selected
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#
#     # Validate file type
#     if not allowed_file(file.filename):
#         return jsonify({"error": "Invalid file format. Use .jpg, .jpeg, or .png"}), 400
#
#     # Save and process the file
#     filename = secure_filename(file.filename)
#     file_path = os.path.join("static/uploads", filename)
#     os.makedirs("static/uploads", exist_ok=True)  # Ensure the directory exists
#     file.save(file_path)
#
#     # Check if the model is available
#     if model is None:
#         return jsonify({"error": "Model not available"}), 500
#
#     try:
#         # Preprocess and predict
#         img_array = preprocess_image(file_path)
#         predictions = model.predict(img_array)
#         confidence = float(np.max(predictions)) * 100  # Confidence percentage
#         predicted_class = CLASS_NAMES[np.argmax(predictions)]
#
#         # Cleanup uploaded file (optional)
#         os.remove(file_path)
#
#         return jsonify({
#             "predicted_value": predicted_class,
#             "confidence": f"{confidence:.2f}%"
#         })
#     except Exception as e:
#         return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
#
#
# # Routes for other pages
# @app.route('/analyzer')
# def analyzer():
#     return render_template('analyzer.html')
#
#
# @app.route('/forum')
# def forum():
#     return render_template('forum.html')
#
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
#
# @app.route('/library')
# def library():
#     return render_template('library.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
# from flask import Flask, render_template, request, jsonify
# import tensorflow as tf
# import numpy as np
# import os
# import cv2
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
#
# # Load trained CNN model with error handling
# MODEL_PATH = os.path.abspath("my_model.keras")
#
# if not os.path.exists(MODEL_PATH):
#     print(f"❌ Model file not found: {MODEL_PATH}")
#     model = None
# else:
#     try:
#         model = tf.keras.models.load_model(MODEL_PATH)
#         print("✅ Model loaded successfully!")
#     except Exception as e:
#         print(f"❌ Error loading model: {e}")
#         model = None
#
# # Define class labels
# CLASS_NAMES = ["Healthy", "Early Blight", "Late Blight"]
#
# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
#
#
# def allowed_file(filename):
#     """Check if file extension is allowed."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# # Home route by default page
# @app.route('/')
# def home():
#     return render_template("plant.html")
#
#
# # Image preprocessing function
# def preprocess_image(img_path):
#     """Load, convert, resize, and normalize an image."""
#     img = cv2.imread(img_path)
#     if img is None:
#         raise ValueError(f"❌ Error loading image: {img_path}")
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = cv2.resize(img, (255, 255))
#     img = img.astype('float32') / 255.0
#     img = np.expand_dims(img, axis=0)
#     return img
#
#
# @app.route("/predict", methods=["POST"])
# def predict():
#     # Check if the request contains a file
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
#
#     file = request.files["file"]
#
#     # Ensure a file is actually selected
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#
#     # Validate file type
#     if not allowed_file(file.filename):
#         return jsonify({"error": "Invalid file format. Use .jpg, .jpeg, or .png"}), 400
#
#     # Save and process the file
#     filename = secure_filename(file.filename)
#     file_path = os.path.join("static/uploads", filename)
#     os.makedirs("static/uploads", exist_ok=True)  # Ensure the directory exists
#     file.save(file_path)
#
#     # Check if the model is available
#     if model is None:
#         return jsonify({"error": "Model not available"}), 500
#
#     try:
#         # Preprocess and predict
#         img_array = preprocess_image(file_path)
#         predictions = model.predict(img_array)
#         confidence = float(np.max(predictions)) * 100  # Confidence percentage
#         predicted_class = CLASS_NAMES[np.argmax(predictions)]
#
#         # Cleanup uploaded file (optional)
#         os.remove(file_path)
#
#         return jsonify({
#             "predicted_value": predicted_class,
#             "confidence": f"{confidence:.2f}%"
#         })
#     except Exception as e:
#         return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
#
#
# # Routes for other pages
# @app.route('/analyzer')
# def analyzer():
#     return render_template('analyzer.html')
#
#
# @app.route('/forum')
# def forum():
#     return render_template('forum.html')
#
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
#
# @app.route('/library')
# def library():
#     return render_template('library.html')
#
#
# if __name__ == '__main__':
    #app.run(debug=True)
# from flask import Flask, render_template, request, jsonify
# import tensorflow as tf
# import numpy as np
# import os
# import cv2
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__)
#
# # Load trained CNN model with error handling
# MODEL_PATH = os.path.abspath("my_model.keras")
#
# if not os.path.exists(MODEL_PATH):
#     print(f"❌ Model file not found: {MODEL_PATH}")
#     model = None
# else:
#     try:
#         model = tf.keras.models.load_model(MODEL_PATH)
#         print("✅ Model loaded successfully!")
#     except Exception as e:
#         print(f"❌ Error loading model: {e}")
#         model = None
#
# # Define class labels
# CLASS_NAMES = ["Healthy", "Early Blight", "Late Blight"]
#
# # Allowed file extensions
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
#
#
# def allowed_file(filename):
#     """Check if file extension is allowed."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# # Home route
# @app.route('/')
# def home():
#     return render_template("plant.html")
#
#
# # Image preprocessing function
# def preprocess_image(img_path):
#     """Load, convert, resize, and normalize an image."""
#     img = cv2.imread(img_path)
#     if img is None:
#         raise ValueError(f"❌ Error loading image: {img_path}")
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = cv2.resize(img, (255, 255))
#     img = img.astype('float32') / 255.0
#     img = np.expand_dims(img, axis=0)
#     return img
#
#
# @app.route("/predict", methods=["POST"])
# def predict():
#     # Check if the request contains a file
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded"}), 400
#
#     file = request.files["file"]
#
#     # Ensure a file is actually selected
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
#
#     # Validate file type
#     if not allowed_file(file.filename):
#         return jsonify({"error": "Invalid file format. Use .jpg, .jpeg, or .png"}), 400
#
#     # Save and process the file
#     filename = secure_filename(file.filename)
#     file_path = os.path.join("static/uploads", filename)
#     os.makedirs("static/uploads", exist_ok=True)  # Ensure the directory exists
#     file.save(file_path)
#
#     # Check if the model is available
#     if model is None:
#         return jsonify({"error": "Model not available"}), 500
#
#     try:
#         # Preprocess and predict
#         img_array = preprocess_image(file_path)
#         predictions = model.predict(img_array)
#         confidence = float(np.max(predictions)) * 100  # Confidence percentage
#         predicted_class = CLASS_NAMES[np.argmax(predictions)]
#
#         # Cleanup uploaded file (optional)
#         os.remove(file_path)
#
#         return jsonify({
#             "predicted_value": predicted_class,
#             "confidence": f"{confidence:.2f}%"
#         })
#     except Exception as e:
#         return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
#
#
# # Routes for other pages
# @app.route('/analyzer')
# def analyzer():
#     return render_template('analyzer.html')
#
#
# @app.route('/forum')
# def forum():
#     return render_template('forum.html')
#
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
#
# @app.route('/library')
# def library():
#     return render_template('library.html')
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

# from flask import Flask, request, jsonify, render_template
# import os
# import numpy as np
# import cv2
# import tensorflow as tf
# from werkzeug.utils import secure_filename
#
# app = Flask(__name__, template_folder='templates')
#
# # Load the model
# MODEL_PATH = os.path.abspath("my_model.keras")
# if os.path.exists(MODEL_PATH):
#     try:
#         model = tf.keras.models.load_model(MODEL_PATH)
#         print("✅ Model loaded successfully!")
#     except Exception as e:
#         print(f"❌ Error loading model: {e}")
#         model = None
# else:
#     print(f"❌ Model file not found: {MODEL_PATH}")
#     model = None
#
# # Allowed extensions
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
#
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# # Image Preprocessing
# def preprocess_image(img_path):
#     """Load, convert, resize, and normalize an image."""
#     img = cv2.imread(img_path)
#     if img is None:
#         raise ValueError("Error loading image.")
#
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     img = cv2.resize(img, (255, 255))
#     img = img.astype('float32') / 255.0
#     img = np.expand_dims(img, axis=0)
#     return img
#
#
# @app.route("/predict", methods=["POST"])
# def predict():
#     if "file" not in request.files:
#         return jsonify({"error": "No file uploaded. Ensure you select an image before clicking Analyze."}), 400
#
#     file = request.files["file"]
#
#     if file.filename == '':
#         return jsonify({"error": "No selected file. Please choose an image file."}), 400
#
#     if not allowed_file(file.filename):
#         return jsonify({"error": "Invalid file format. Use .jpg, .jpeg, or .png"}), 400
#
#     # Save file
#     filename = secure_filename(file.filename)
#     file_path = os.path.join("static/uploads", filename)
#     os.makedirs("static/uploads", exist_ok=True)
#     file.save(file_path)
#
#     # Check if model is loaded
#     if model is None:
#         return jsonify({"error": "Model not available"}), 500
#
#     try:
#         img_array = preprocess_image(file_path)
#         predictions = model.predict(img_array)
#         confidence = float(np.max(predictions)) * 100  # Confidence percentage
#         predicted_class = CLASS_NAMES[np.argmax(predictions)]
#
#         os.remove(file_path)  # Cleanup file after processing
#
#         return jsonify({
#             "predicted_value": predicted_class,
#             "confidence": f"{confidence:.2f}%"
#         })
#
#     except Exception as e:
#         return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
#
#
# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
import os
import cv2
import re
from werkzeug.utils import secure_filename
import long_responses as long  # Import your long responses

app = Flask(__name__)

# Load trained CNN model with error handling
MODEL_PATH = os.path.abspath("my_model.keras")

if not os.path.exists(MODEL_PATH):
    print(f"❌ Model file not found: {MODEL_PATH}")
    model = None
else:
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = None

# Define class labels
CLASS_NAMES = ["Healthy", "Early Blight", "Late Blight"]

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home route
@app.route('/')
def home():
    return render_template("plant.html")


# Image preprocessing function
def preprocess_image(img_path):
    """Load, convert, resize, and normalize an image."""
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError(f"❌ Error loading image: {img_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (255, 255))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file format. Use .jpg, .jpeg, or .png"}), 400

    # Save and process file
    filename = secure_filename(file.filename)
    file_path = os.path.join("static/uploads", filename)

    os.makedirs("static/uploads", exist_ok=True)  # Ensure directory exists
    file.save(file_path)

    # Check if model is loaded
    if model is None:
        return jsonify({"error": "Model not available"}), 500

    try:
        # Preprocess the image
        img_array = preprocess_image(file_path)

        # Get predictions
        predictions = model.predict(img_array)
        confidence = float(np.max(predictions)) * 100  # Confidence percentage
        predicted_class = CLASS_NAMES[np.argmax(predictions)]

        # Response JSON
        result = {
            "actual_value": predicted_class,
            "predicted_value": predicted_class,
            "confidence": f"{confidence:.2f}%"
        }

        # Cleanup uploaded file (Uncomment if debugging)
        os.remove(file_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


# Chatbot page route
@app.route('/chatbot')
def chatbot():
    return render_template("chatbot.html")


# Message probability function (for basic response logic)
def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words)) if recognised_words else 0

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    return int(percentage * 100) if has_required_words or single_response else 0


# Handle incoming user message
def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Add your responses here like:
    response('Hello! I am your Plant Health Assistant. Upload a plant image or ask me about plant diseases.',
             ['hello', 'hi', 'hey', 'greetings'], single_response=True)
    response('Goodbye! Feel free to return if you need help with plant disease diagnosis.',
             ['bye', 'goodbye', 'see', 'you'], single_response=True)

    # Add other specific plant-related responses (similar to above)

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match


def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    return check_all_messages(split_message)


# API route to handle chatbot responses
@app.route('/chatbot/get_response', methods=['POST'])
def chatbot_response():
    user_message = request.json.get("message", "")

    # Get the chatbot's response based on the user message
    response_text = get_response(user_message)

    return jsonify({"response": response_text})


# Routes for other pages (like forum, about, etc.)
@app.route('/analyzer')
def analyzer():
    return render_template('analyzer.html')


@app.route('/forum')
def forum():
    return render_template('forum.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/guides')
def guides():
    return render_template('guides.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/careers')
def careers():
    return render_template('careers.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/library')
def library():
    return render_template('library.html')


if __name__ == '__main__':
    app.run(debug=True)

