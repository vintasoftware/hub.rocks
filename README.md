# hub.rocks

## Dependencies
* Python 3.5

## Deployment (Heroku)
- before deploying to Heroku, do this:

`heroku config:set BUILDPACK_URL=https://github.com/vintasoftware/heroku-buildpack-multi.git`

`heroku run python manage.py createcachetable django_db_cache_collectfast`

## Local
`pip install -r requirements.txt`

`python manage.py syncdb`

`python manage.py migrate`

`python manage.py bower install`

## Help
If you have any questions or need help, please send an email to: contact@vinta.com.br
