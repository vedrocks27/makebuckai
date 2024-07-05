# from flask import Flask, request, send_file, jsonify, render_template
# from diffusers import StableDiffusionPipeline
# from transformers import pipeline
# import torch

# app = Flask(__name__)

# # Load the Stable Diffusion model
# model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4", 
#                                                 revision="fp16", 
#                                                 torch_dtype=torch.float16, 
#                                                 use_auth_token=True)


# model = StableDiffusionPipeline.from_pretrained(
#     "CompVis/stable-diffusion-v1-4",
#     variant="fp16",  # Changed from revision to variant
#     torch_dtype=torch.float16,
#     use_auth_token=True
# )

# model = model.to("cpu")

# def generate_image_from_text(text):
#     image = model(text).images[0]
#     image.save("generated_image.png")
#     return "generated_image.png"

# @app.route('/', methods=['GET'])
# def home():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     text = request.json['text']
#     image_path = generate_image_from_text(text)
#     return send_file(image_path, mimetype='image/png')

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, request, send_file, jsonify, render_template, copy_current_request_context
# from diffusers import StableDiffusionPipeline
# import torch
# from threading import Thread

# app = Flask(__name__)

# # Load the Stable Diffusion model
# model = StableDiffusionPipeline.from_pretrained(
#     "CompVis/stable-diffusion-v1-4",
#     variant="fp16",
#     torch_dtype=torch.float16,
#     use_auth_token=True
# )
# model = model.to("cpu")

# def generate_image_from_text(text, callback):
#     image = model(text).images[0]
#     image.save("generated_image.png")
#     callback("generated_image.png")

# @app.route('/', methods=['GET'])
# def home():
#     return render_template('index.html')

# @app.route('/generate', methods=['POST'])
# def generate():
#     text = request.json['text']

#     @copy_current_request_context
#     def send_image(path):
#         return send_file(path, mimetype='image/png')

#     thread = Thread(target=generate_image_from_text, args=(text, send_image))
#     thread.start()
#     return "Image is being processed", 202

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, send_file, jsonify, render_template
from diffusers import StableDiffusionPipeline
import torch
import os

app = Flask(__name__)

# Load the Stable Diffusion model
auth_token = os.getenv('HUGGINGFACE_AUTH_TOKEN')  # Ensure you set this environment variable
model = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    variant="fp16",  # Using fp16 variant but loading as fp32 on CPU
    torch_dtype=torch.float32,
    use_auth_token=auth_token
)
model = model.to("cpu")

def generate_image_from_text(text):
    try:
        image = model(text).images[0]
        image_path = "generated_image.png"
        image.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error during image generation: {e}")
        return None

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.json['text']
    image_path = generate_image_from_text(text)
    if image_path:
        return send_file(image_path, mimetype='image/png')
    else:
        return jsonify({"error": "Failed to generate image"}), 500



if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
