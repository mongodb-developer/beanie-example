# beanie-cocktails

A cocktail API built with MongoDB and Beanie.

This code was written to try out Beanie and was used to write a [blog post](https://developer.mongodb.com/learn/) which may well be more interesting than this code.

## Developing

Run the following to install the project (and dev dependencies) into your active virtualenv:

```bash
pip install -e .[dev]
```

## Run It

If you have an Atlas database you can run the server with:

```bash
export MONGODB_URL="mongodb+srv://<user>:<pass>@host/database"
uvicorn beaniecocktails:app --reload --debug
```

This app will only work on MongoDB Atlas clusters, because it makes use of [Atlas Search](https://docs.atlas.mongodb.com/atlas-search/).

## Feedback

I'd love to know whether you found this useful, or if you had any problems.
Please leave feedback on the [MongoDB Community Forums](https://developer.mongodb.com/community/forums/) and tag me `@Mark_Smith`.