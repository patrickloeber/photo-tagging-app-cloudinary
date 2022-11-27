from dotenv import load_dotenv

load_dotenv()

# import os
# print(os.environ['CLOUDINARY_URL'])

import cloudinary
import cloudinary.uploader
import cloudinary.api
import pathlib
import os

# Set configuration parameter: return "https" URLs by setting secure=true
config = cloudinary.config(secure=True)

print(config.cloud_name)

suported_files = (".png", ".jpg", ".jpeg", ".heic")


def upload_image(filename, folder="my_photos"):
    stem = pathlib.Path(filename).stem

    # see https://cloudinary.com/documentation/image_upload_api_reference#asset_management
    # for all parameters

    res = cloudinary.uploader.upload(filename, public_id=stem, folder=folder)
    return res


def upload_and_tag_image(filename, folder="my_photos"):
    stem = pathlib.Path(filename).stem
    res = cloudinary.uploader.upload(
        filename,
        public_id=stem,
        folder=folder,
        detection="openimages",
        auto_tagging=0.25,
    )
    return res


def upload_folder():
    n = 0
    for file in sorted(os.listdir("photos")):
        if pathlib.Path(file).suffix.lower() in suported_files:
            try:
                upload_and_tag_image("photos/" + file)
                n += 1
            except Exception as e:
                print("failed for ", file)
                print(e)
    print(n, " photos uploaded")


def search_img():
    result = (
        cloudinary.Search()
        .expression("resource_type:image AND tags=Football")
        .sort_by("public_id", "desc")
        .execute()
    )
    # .max_results('30')
    # .with_field('tags')
    print(result["total_count"])
    for res in result["resources"]:
        print(res["url"])


def get_all_tags():
    all_tags = []
    tags = cloudinary.api.tags(max_results=100)
    all_tags.extend(tags["tags"])
    next_cursor = tags.get("next_cursor")

    while next_cursor:
        tags = cloudinary.api.tags(max_results=100, next_cursor=next_cursor)
        all_tags.extend(tags["tags"])
        next_cursor = tags.get("next_cursor")

    return all_tags


def get_all_images_with_tags():
    all_resources = []
    result = cloudinary.api.resources(
        type="upload",
        resource_type="image",
        prefix="my_photos",
        tags=True,
        max_results=100,
    )

    all_resources.extend(result["resources"])
    next_cursor = result.get("next_cursor")

    while next_cursor:
        result = cloudinary.api.resources(
            type="upload",
            resource_type="image",
            prefix="my_photos",
            max_results=100,
            tags=True,
            next_cursor=next_cursor,
        )
        all_resources.extend(result["resources"])
        next_cursor = result.get("next_cursor")

    return all_resources


if __name__ == "__main__":
    # upload_image("apple.jpg")
    # upload_and_tag_image("apple.jpg")
    # upload_folder()
    # search_img()
    # get_all_tags()
    # get_all_images_with_tags()
    pass
