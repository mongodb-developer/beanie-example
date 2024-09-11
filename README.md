# Building a Cocktail API with Beanie!

This is a sample cocktail API built with [MongoDB](https://www.mongodb.com/company/what-is-mongodb),
[Beanie](https://beanie-odm.dev/),
and [FastAPI](https://fastapi.tiangolo.com/).

This code was written to try out Beanie and was used to write a [blog post](https://developer.mongodb.com/article/beanie-odm-fastapi-cocktails/),
which may be more interesting than this code.

## Install It

Run the following to install the project (and dev dependencies) into your active virtualenv:

```bash
python -m pip install -e .[dev]
```

## Initialize Your Database

The previous step installs a script, `init-db`, that will generate some random
cocktails for you, if you want:

```bash
# This will create 100 dummy cocktails in your database
# (or run without --dummy-data to just initialize indexes.):
export MONGODB_URL="mongodb+srv://<user>:<pass>@host/database"
init-db --dummy-data
```

> **Don't consume any of the cocktails this script generates, they're randomly generated!


## Run It

If you have an Atlas database you can run the server with:

```bash
export MONGODB_URL="mongodb+srv://<user>:<pass>@host/database"
uvicorn beaniecocktails:app --reload
```

You should then be able to view your API docs at http://127.0.0.1:8000/docs/

> **Note:** This app will only work on MongoDB Atlas clusters, because it makes use of [Atlas Search](https://docs.atlas.mongodb.com/atlas-search/).

## Feedback

I'd love to know whether you found this useful, or if you had any problems.
Please leave feedback on the [MongoDB Community Forums](https://developer.mongodb.com/community/forums/) and tag me `@Mark_Smith`.