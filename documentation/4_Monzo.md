Step Four: Get Monzo & SetUp
===

1. Register an account on [Monzo](https://monzo.com/)
2. Head to the [API Playground](https://developers.monzo.com/)
3. Note down your **Account ID** (note if you are using the Monzo current account Vs. Prepaid account you will need to Get /accounts?account_type=uk_retail to obtain your CA ID)

![API Playgrounds](https://raw.githubusercontent.com/d-Rickyy-b/Monzo-Meter/master/documentation/images/api_playgrounds.png)

Do a POST request in the console - replace the **account_id**, the **url** and the [**password**]((https://github.com/d-Rickyy-b/Monzo-Meter/blob/master/heroku/web.py#L37)) with yours each:

`$ /webhooks account_id=<your_account_id> \ url=https://your_app_name.herokuapp.com/catch?key=password`

Alternatively you can go ahead and use [Postman](https://www.getpostman.com/) or cURL:

```bash
$ curl -X POST \
       -H "Authentication: <MonzoAccessToken>" \
       -H "Content-Type: application/x-www-form-urlencoded" \
       -d "account_id= <your_account_id>" \
       -d "url=https://your_app_name.herokuapp.com/catch?key=password" \
       https://api.monzo.com/webhooks
```
When you have done this (and don't forget about the [**password**](https://github.com/d-Rickyy-b/Monzo-Meter/blob/master/heroku/web.py#L37)), the webhook should be set up. You'll now get all transactions as a POST to the python app on Heroku.
___
Last Step: [Customize](https://github.com/d-Rickyy-b/Monzo-Meter/tree/master/documentation/5_Customize.md)
