import cloudinary.uploader

def upload_to_cloudinary(file, folder):
    result = cloudinary.uploader.upload(
        file,
        resource_type="image",
        folder=folder
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }
