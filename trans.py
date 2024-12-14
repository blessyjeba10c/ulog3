import base64
import os
import requests

# Simulated transmission functions
def transmit_data(data):
    """
    Simulate transmitting data. In real-world this could be sent over a network or saved to a shared medium.
    Here we are simply returning the data.
    """
    print("Data is being transmitted...")
    return data

def receive_data(transmitted_data):
    """
    Simulate receiving data. This is where the transmitted data would be processed.
    """
    print("Data is being received...")
    return transmitted_data

# Encode the image to Base64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode('utf-8')
    print("Image encoded into Base64 successfully.")
    return base64_encoded

# Decode the Base64 data back into an image
def decode_base64_to_image(base64_data, output_path):
    image_data = base64.b64decode(base64_data)
    with open(output_path, "wb") as image_file:
        image_file.write(image_data)
    print(f"Image successfully decoded and saved to {output_path}.")

# Download image from GitHub repository
def download_image_from_github(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Image downloaded successfully from GitHub to: {save_path}")
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")

# Simulate Transmission of the Image
github_image_url = "https://raw.githubusercontent.com/blessyjeba10c/ulog3/main/WhatsApp%20Image%202024-12-14%20at%2013.39.23_7287c42f.jpg"  # Replace with your GitHub URL
image_path = "/mnt/data/downloaded_image.jpg"
output_image_path = "/mnt/data/received_transmitted_image.jpg"

try:
    # Step 1: Download the image from GitHub
    download_image_from_github(github_image_url, image_path)

    # Step 2: Sender encodes the image
    encoded_data = encode_image_to_base64(image_path)

    # Step 3: Simulate virtual transmission
    transmitted_data = transmit_data(encoded_data)

    # Step 4: Receiver decodes the received data
    received_data = receive_data(transmitted_data)
    decode_base64_to_image(received_data, output_image_path)

    print(f"Simulation complete. Image received and saved at: {output_image_path}")

except FileNotFoundError:
    print("Error: Image file not found. Please check the GitHub URL.")
except Exception as e:
    print(f"An error occurred: {e}")
