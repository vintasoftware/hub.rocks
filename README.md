# hub.rocks mvp

## How to run and deploy
1. Make sure you are in the mvp branch. This instructions are for it.
2. Create a new app in Heroku with `heroku create choose-a-good-name`
3. Add the necessary Heroku plugins: `heroku addons:add rediscloud` and `heroku addons:add pusher`
4. Get the `PUSHER_URL` and `REDISCLOUD_URL` with `heroku config`
5. Try locally with something like `PUSHER_URL=put-pusher-url-here REDISCLOUD_URL=put-rediscloud-url-here python server.py` (yes, we will try locally with production settings, this is a MVP!)
6. Deploy to Heroku with `git push heroku mvp:master`
7. Do `heroku ps:scale web=1`
8. Go to your Heroku app url and try it online! (don't use https, otherwise it will break)
