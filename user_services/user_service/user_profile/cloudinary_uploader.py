import cloudinary.uploader


def upload_avatar(file, user_id: str):
    """
    Uploads avatar image to Cloudinary.
    This function is PURE. No Django models here.
    """
    result = cloudinary.uploader.upload(
        file,
        resource_type="image",
        folder=f"avatars/{user_id}",
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }
