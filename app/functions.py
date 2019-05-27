import os


def upload_images(file, old_img=None):
    if old_img:
        try:
            os.remove('app' + old_img)
        except OSError:
            return False, None

    path = "/static/upload_images/" + file.filename
    file.save('app' + path)
    return True, path
