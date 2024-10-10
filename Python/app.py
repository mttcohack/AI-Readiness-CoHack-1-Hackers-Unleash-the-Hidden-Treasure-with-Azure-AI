from flask import Flask, request, jsonify, render_template
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from dotenv import load_dotenv, dotenv_values
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speechsdk
import logging
import json
import base64
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

app = Flask(__name__)

load_dotenv()

# Load environment variables
keyVaultUri = os.environ.get('AKV_URL')
tenant_id = os.environ.get('SP_TENANT_ID')
client_id = os.environ.get('SP_CLIENT_ID')
client_secret = os.environ.get('SP_CLIENT_SECRET')
storage_url = os.environ.get('STORAGE_URL')
container = os.environ.get('STORAGE_CONTAINER')
oai_endpoint=os.environ.get('AOAI_URL')
oai_deployment=os.environ.get('AOAI_DEPLOYMENT')
cognitive_endpoint = os.environ.get('COGNITIVE_URL')
region = os.environ.get('COGNITIVE_REGION')

# Secret names in Key Vault
SECRET_AOAI_KEY = "AOAI-KEY"
SECRET_COGNITIVE_KEY = "COGNITIVE-KEY"

# Initialize Azure credentials
credential = ClientSecretCredential(tenant_id=tenant_id, client_id=client_id, client_secret=client_secret)
blob_service_client = BlobServiceClient(account_url=storage_url, credential=credential)
container_client = blob_service_client.get_container_client(container)

# Hackathon step 1: Change the default hunter name to your name
title=' Hunter X'

# Hackathon step 2: Retrieve AOAI and Cognitive API keys from Key Vault

# Hackathon step 3a: Aunthticate the Vision client
def authenticate_vision_client():

    return vision_client

# Hackathon step 4
def openai(text):

    return response_from_aoai

# Hackathon step 5
def text_to_speech(text):

    return "Speech synthesis completed"

@app.route('/', methods=['GET', 'POST'])
def aivision():
        images =[]
        analysis_results = ""
        if request.method == 'GET':
            
            
            blob_list = container_client.list_blobs()
            for blob in blob_list:
                print(blob.name)
                blob_client = container_client.get_blob_client(blob.name)
                download_stream = blob_client.download_blob()
                image_data = download_stream.readall()
                # Encode image data to base64
                encoded_image = base64.b64encode(image_data).decode('utf-8')
                images.append(encoded_image)
        
                print(f"Images count: {len(images)}")

            return render_template('index.html', images=images, analysis_results=None, title=title)
            
        if request.method == 'POST':
             analysis_results = None 

             selected_image_base64 = request.form.get('selected_image')
             print("Selected image received")
             print(selected_image_base64[:100])  # Print the first 100 characters for verification

             if selected_image_base64:
                client = authenticate_vision_client()

                image_data = base64.b64decode(selected_image_base64)

                # Hackathon step 3b: Extract text from the selected image
                result = client.x(image_data, visual_features=[VisualFeatures.])

                # Extract text from the result
                combined_text = ""
                if result.read is not None:
                    words = []
                    for line in result.read.blocks[0].lines:
                        print(f"   Line: '{line.text}', Bounding box {line.bounding_polygon}")
                        for word in line.words:
                            print(f"     Word: '{word.text}")
                            words.append(word.text)
                    combined_text = " ".join(words) 
                    
                    read_results = combined_text  

                    # Hackathon step 4: Analyze the text and find the hidden info
                    # complete the function def openai(text)
                    final_result=openai(combined_text)

                    #assign the final_result to the analysis_result variable
                    analysis_results = final_result

                    # Hackathon step 5: Convert the result to speech
                    # Use the same cognitive service for speech
                    # complete the function def text_to_speech(text)

                    text_to_speech(analysis_results)
                            
                return render_template('index.html', analysis_results=analysis_results, images=selected_image_base64)
            

if __name__ == '__main__':
    app.run(debug=True)
