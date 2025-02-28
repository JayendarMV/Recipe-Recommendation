from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
import time
from google.api_core.exceptions import ResourceExhausted


app = Flask(__name__)

# Configure API key
API_KEY = os.getenv("")

genai.configure(api_key=API_KEY)

# Create the model with optimized config
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,  # Reduced to avoid quota errors
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(model_name="gemini-2.0-flash", generation_config=generation_config)

@app.route('/')
def index():
    return render_template('chatbot1.html')

@app.route("/get", methods=["POST"])
def chat():
    try:
        user_message = request.form["msg"]
        
        chat_session = model.start_chat(
            system_instruction="""
            Recommend food recipes based on given ingredients without adding any extra ingredients. 
            Use only the provided ingredients to create the recipe. Present recipe options in English, Tamil, and Hindi.
            Wait for the user's response. Once a recipe is chosen, ask the user to select a language (English/Tamil/Hindi) 
            and provide a step-by-step guide in the selected language in a simple manner.
            """
        )

        response = chat_session.send_message(user_message)
        return jsonify({"response": response.text})

    except ResourceExhausted:
        time.sleep(5)
        return jsonify({"response": "I'm experiencing heavy traffic, please try again later."})
    
    except Exception as e:
        print(f"Error: {e}")  # Debugging output
        return jsonify({"response": f"Sorry, an error occurred: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
