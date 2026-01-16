import os
import replicate
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allows your phone to talk to the server

@app.route('/')
def home():
    return "Barber Shop AI is Running!"

@app.route('/process_haircut', methods=['POST'])
def process_haircut():
    try:
        print("--- 1. Received Image from App ---")
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400
            
        file = request.files['image']
        
        # ✅ FIX: Save the web upload to a real temporary file
        # The AI library needs a real file on the disk, not a web stream.
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        file.save(temp.name)
        temp_path = temp.name
        print(f"--- 2. Saved to temp file: {temp_path} ---")

        # ✅ PREPARE AI: Use the file we just saved
        model_version = "stability-ai/stable-diffusion-inpainting:82845061acdbc19163b0a72714a9eef5467443547f8725ee19688587d5b1287c"
        
        print("--- 3. Sending to Replicate AI ---")
        output = replicate.run(
            model_version,
            input={
                "image": open(temp_path, "rb"), # Open the temp file we created
                "prompt": "bald man, clean shaven scalp, realistic skin texture, pore detail, cinematic lighting",
                "negative_prompt": "hair, stubble, wig, plastic, blur, cartoon",
                "strength": 0.95, 
                "guidance_scale": 7.5
            }
        )
        print(f"--- 4. Success! Result URL: {output} ---")
        
        # Clean up (Optional, but keeps the server clean)
        try:
            os.remove(temp_path)
        except:
            pass
        
        # Return the result to the phone
        if output and len(output) > 0:
            return jsonify({"result_image": output[0]})
        else:
            return jsonify({"error": "AI failed to generate image"}), 500

    except Exception as e:
        print(f"!!!!! AI ERROR: {str(e)} !!!!!")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
