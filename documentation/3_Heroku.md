Step Three: Getting Heroku
===

1. You'll first need to create an account on [Heroku](https://www.heroku.com/).
2. When this is done go ahead and [Download the CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
3. Login with the Heroku CLI (enter your credentials):

   `$ heroku login`

4. Create and open a folder where your project directory will be saved to.
   Into this folder clone the github repo

   `$ git clone https://github.com/d-Rickyy-b/Monzo-Meter.git`

5. Create your app on Heroku with the CLI

   `$ heroku create your_app_name`

6. Activate the redis add-on (might require credit card details)

   `$ heroku addons:create heroku-redis:hobby-dev -a your_app_name`

   ![heroku-addons](https://raw.githubusercontent.com/d-Rickyy-b/Monzo-Meter/master/documentation/images/heroku_addons.png)

7. Modify the code (see [Customize](https://github.com/d-Rickyy-b/Monzo-Meter/tree/master/documentation/5_Customize.md)) and push it to Heroku

   After inserting your tokens into the code and changing the [password](https://github.com/d-Rickyy-b/Monzo-Meter/blob/master/heroku/web.py#L37), push it to Heroku with the following command:

   ```bash
   $ git add .
   $ git commit -m "Initial commit"
   $ git push heroku master
   ```

That's basically everything you need to do on the heroku part.
___
Next Step: [Get Monzo & SetUp](https://github.com/d-Rickyy-b/Monzo-Meter/tree/master/documentation/4_Monzo.md)
