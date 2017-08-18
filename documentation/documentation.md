Documentation
===

This instruction was made for building a custom "Monzo-Meter" - a small device for showing your current balance of your Monzo account. This idea comes from Simon Vans-Colina - he thought about a problem everyone seems to know:
>One particular piece of information that's important to just about everyone, is *“how much of my pay is still in my bank account”*.

This documentation provides you with all the code. All you need is the hardware. It is divided into six major parts.

Credits are going to [Simon Vans-Colina](https://medium.com/@simonvc) and his amazing instructions in [his article](https://medium.com/@simonvc/the-internet-of-things-that-connect-to-your-bank-account-ab8a6a2a44d7) which gave me the idea for this project.

Disclaimer: Monzo is currently only available in the UK.
___
Step Zero: Buying the Hardware
===
Here's a list of things you'll need:
- [Photon µC](https://store.particle.io/) (19$)
- 9g digital micro server (anologue wont work)

Step One: Wiring up the Hardware
===



Step Two: Power up Particle.io
===

1. Get yourself a [Particle.io](https://www.particle.io/) account
2. Open their [Console](https://console.particle.io/devices) and register your Photon µC - **note down the Device ID**
3. Open their [IDE](https://build.particle.io/build) and paste in the code you can find in [particle_code.ino](https://github.com/d-Rickyy-b/Monzo-Meter/blob/master/particle.io/device_code.ino)
4. Save your code and **note the Access Token**. In the python code it's called *particle_token*

   ![particle-code](https://raw.githubusercontent.com/d-Rickyy-b/Monzo-Meter/master/documentation/images/particle.io_token.png)

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

7. Modify the code and push it to Heroku

   After inserting your tokens into the code, push it to Heroku with the following command:

   ```bash
   $ git add .
   $ git commit -m "Initial commit"
   $ git push heroku master
   ```

That's basically everything you need to do on the heroku part.

Step Four: Get Monzo & SetUp
===
1. Register an account on [Monzo](https://monzo.com/)
2. Head to the [API Playground](https://developers.monzo.com/)
3. Note down your **Account ID**

![API Playgrounds](https://raw.githubusercontent.com/d-Rickyy-b/Monzo-Meter/master/documentation/images/api_playgrounds.png)

Do a POST request in the console - replace the **account_id** and the **url** with yours each:

`$ /webhooks account_id=<your_account_id> \ url=https://your_app_name.herokuapp.com/catch`

Alternatively you can go ahead and use [Postman](https://www.getpostman.com/) or cURL.

```bash
$ curl -X POST \
       -H "Authentication: <MonzoAccessToken>" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       -d "account_id= <your_account_id>" \
       -d "url=https://your_app_name.herokuapp.com/catch" \
       https://api.monzo.com/webhooks
```
When you have done this, the webhook should be set up. You'll now get all transactions as a POST to the python app on Heroku.

Step Five: Customize
===
You can set a custom "max"
