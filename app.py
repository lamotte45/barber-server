import os
import replicate
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('')
def home()
    return Barber Shop AI is Running!

@app.route('process_haircut', methods=['POST'])
def process_haircut()
    try
        # 1. Check if image exists
        if 'image' not in request.files
            return jsonify({error No image uploaded}), 400
            
        file = request.files['image']
        
        # 2. Send to Replicate (Stable Diffusion Inpainting)
        # We use a specific model version known for good quality
        model_version = stability-aistable-diffusion-inpainting82845061acdbc19163b0a72714a9eef5467443547f8725ee19688587d5b1287c
        
        output = replicate.run(
            model_version,
            input={
                image file,
                prompt bald man, clean shaven scalp, realistic skin texture, pore detail, cinematic lighting,
                negative_prompt hair, stubble, wig, plastic, blur, cartoon,
                strength 0.95, # High strength = replace hair completely
                guidance_scale 7.5
            }
        )
        
        # 3. Get the Result URL
        # Replicate returns a list of URLs. We take the first one.
        if output and len(output)  0
            return jsonify({result_image output[0]})
        else
            return jsonify({error AI failed to generate image}), 500

    except Exception as e
        return jsonify({error str(e)}), 500

if __name__ == '__main__'
    app.run(host='0.0.0.0', port=5000)