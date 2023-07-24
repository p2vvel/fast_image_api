# Fast Image API

### Image API written in FastAPI.

My main goal was to rewrite my old Django project ([image_api](https://github.com/p2vvel/image_api)) into FastAPI for learning purposes, but during development I decided to make some changes to the project. Old projects functionality was limited to storing images and downloading thumbnails. This project is more like a photo editor, where you can upload an image and then edit it (you can change resolution, scale, orientation, rotation and change colors).

### Functionality:
* user registration, login
* ability to upload an image
* ability to download original image
* ability to edit image and download edited version
* images privacy provided by self-implemented XsendFile (and of course configured in nginx) - other users can't see your private pictures

<br/>

## Used stack:
* FastAPI as main framework
* SQLAlchemy for DB operations (SQLite used during development, Postgres at 'production')
* Celery with Redis as broker/backend for running editing tasks
* PIL for image editing
* Pytest for testing
* PyJWT with passlib for providing JWT auth
* Github Actions to automatically run flake8 and tests, after successful run, pushed commit is merged into "stable" branch (I was looking for a reason to try Github Actions, so I decided to use it here 😊)
* Docker with Docker Compose for easier deployment


<br/>


## Running project:

Just use docker-compose to run the project, it will automatically build images and run containers:
```
docker-compose up
```


API will be accessible at http://localhost, open http://localhost/docs or http://localhost/redoc to see API docs.


<br/>
<br/>
<br/>

### TODO (things that could be improved):
* Alembic migrations (probably the most important thing left to do here)
* writing more tests would be a good idea, coverage could be better 😅
* add more editing options