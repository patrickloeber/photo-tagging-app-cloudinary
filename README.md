# Media Library and Content Analysis Dashboard built with Cloudinary

This app can upload, store, and automatically tag images & videos using the Cloudinary API.

The app is built with Streamlit where it displays an image gallery that can be filtered by tag, and also shows a Dashboard that analyzes all tags.

## Installation

```bash
pip install cloudinary python-dotenv streamlit

pip install streamlit pandas plotly
```
## Configuration

Follow the quick start guide to create a .env file with the CLOUDINARY_URL

https://cloudinary.com/documentation/python_quickstart

```bash
CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
```

## Implement the Cloudinary Service

The file `cloudinary_service.py` contains helper functions to upload, tag, and search images.

Prepare a folder with all the photos you want to upload, and then call the `upload_folder()`function inside the `cloudinary_service.py` to upload and tag all images.

## Run the app

Start the app with

```
streamlit run app.py
```
