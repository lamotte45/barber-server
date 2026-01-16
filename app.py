import os
import replicate
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Barber Shop AI is Running!"

@app.route('/process_haircut', methods=['POST'])
def process_haircut():
    try:
        print("--- Received Image, Starting Processing ---")
        if 'image' not in request.files:
            print("ERROR: No image file found in request")
            return jsonify({"error": "No image uploaded"}), 400
            
        file = request.files['image']
        
        # Using a reliable model
        model_version = "stability-ai/stable-diffusion-inpainting:82845061acdbc19163b0a72714a9eef5467443547f8725ee19688587d5b1287c"
        
        print("--- Sending to Replicate ---")
        output = replicate.run(
            model_version,
            input={
                "image": file,
                "prompt": "bald man, clean shaven scalp, realistic skin texture, pore detail, cinematic lighting",
                "negative_prompt": "hair, stubble, wig, plastic, blur, cartoon",
                "strength": 0.95, 
                "guidance_scale": 7.5
            }
        )
        print(f"--- Replicate Success: {output} ---")
        
        if output and len(output) > 0:
            return jsonify({"result_image": output[0]})
        else:
            return jsonify({"error": "AI failed to generate image"}), 500

    except Exception as e:
        # 🔴 THIS IS THE IMPORTANT PART: PRINT THE ERROR
        print(f"!!!!! AI ERROR: {str(e)} !!!!!")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
