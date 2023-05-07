# Fast Image API


Image API written using Python with FastAPI and SQLAlchemy

Features:
* authentication based on JWT
* ability to upload an image

* images are private (UUID filename, XSendFile)

* standard users can download original images
* pro users can download transformed image(colors, crop, resize, mirror)

* edited images are cached for 24h(changeable?), then deleted


```
get original image:
/images/<user_uuid>/<image_uuid>

edit image:
/images/<user_uuid>/<image_uuid>/edit


returns url to:
/images/edited/<task_uuid>
```