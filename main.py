import streamlit as st
import os
import random
from dotenv import load_dotenv
import base64
from openai import OpenAI

# Load environment variables
load_dotenv()
key = os.getenv('OPEN_AI_KEY')
MODEL = 'gpt-4o'
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Specify the folder containing images
IMAGE_FOLDER = "path/to/your/image/folder"  # Replace with your folder path

st.title('Listening to training images')

# Select a random image from the folder
if os.path.exists(IMAGE_FOLDER):
    image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]
    if image_files:
        random_image = random.choice(image_files)
        random_image_path = os.path.join(IMAGE_FOLDER, random_image)
        st.image(random_image_path, caption='Randomly Selected Image')

        # Encode the image
        base64_image = encode_image(random_image_path)

        # Make the API call
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in Markdown."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Could you describe the image and create a narrative to highlight important details and provide recommendations. Create a narrative with Observations, important details, and ideas for further analysis with bullet points."},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"}
                    }
                ]}
            ],
            temperature=0.0,
        )

        st.markdown(response.choices[0].message.content)
    else:
        st.error("No images found in the specified folder.")
else:
    st.error("The specified folder does not exist.")
