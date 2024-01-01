#!/usr/bin/env python3
#emreybs
#Previous versions:https://github.com/emreYbs/Web-Scraper-Projects/edit/main/Downloaders/Photography/Unsplash
#Now this is the Streamlit version of the Unsplash Image Downloader


import streamlit as st
import requests
import string
import random
import os
import hashlib
from pathlib import Path
from urllib.parse import urlparse

def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc == "source.unsplash.com":
        return True
    else:
        return False

def download_image(search_term, resolution, amount):
    for x in range(amount): 
        url = f"https://source.unsplash.com/random/{resolution}/?{search_term}"
        validate_url(url)
        st.write("URL is valid")
        st.write(f"Downloading image {x + 1} of {amount} from {url}")
        st.write(f"Resolution: {resolution}")
        st.write(f"Topic: {search_term}")
        st.write(f"Amount: {amount}")
        response = requests.get(url, allow_redirects=True)
        filename = f"{search_term}_{generate_random_string(5)}_{x + 1}.png"
        save_path = os.path.join("photos", filename)
        os.makedirs("photos", exist_ok=True)
        st.write(f"Saving image to: {save_path}")
        with open(save_path, 'wb') as file:
            file.write(response.content)
        st.write(f"Saved image to: {save_path}")

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def calculate_hash_value(path, blocksize=65536):
    hasher = hashlib.md5()
    with open(path, 'rb') as file:
        buf = file.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(blocksize)
    return hasher.hexdigest()

def remove_duplicate_files(input_files):
    unique_files = {}
    duplicate_files = {}

    for file_path in input_files:
        if Path(file_path).exists():
            file_hash = calculate_hash_value(file_path)
            if file_hash in unique_files:
                st.write(f"Removing duplicate file: {file_path}")
                os.remove(file_path)
            else:
                st.write(f"Adding file: {file_path}")
                unique_files[file_hash] = file_path
        else:
            st.write(f"{file_path} is not a valid path, please verify")

def main():
    st.title("Unsplash Image Downloader")
    st.write("This program allows you to download random images from Unsplash based on a topic.")

    topic = st.text_input("Enter a topic")
    resolution = st.text_input("Enter a resolution")
    amount = st.number_input("Enter an amount", min_value=1, step=1, value=5)

    if st.button("Download Images"):
        if not topic or not resolution or not amount:
            st.error("Error: Please provide all the required arguments.")
        else:
            download_image(topic.lower(), resolution, int(amount))

            input_files_path = "photos"  # Directory
            input_files = [os.path.join(input_files_path, f) for f in os.listdir(input_files_path) if 
                           os.path.isfile(os.path.join(input_files_path, f))]
            remove_duplicate_files(input_files)
            st.success("Done")

if __name__ == "__main__":
    main()
