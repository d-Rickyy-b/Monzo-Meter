Step Five: Customize
===

There are several parameters you can and should customize.

1. Setting the [particle_token](https://github.com/d-Rickyy-b/Monzo-Meter/blob/master/heroku/web.py#L23) and the [device_id](https://github.com/d-Rickyy-b/Monzo-Meter/blob/master/heroku/web.py#L24)
2. Changing the preset [password](https://github.com/d-Rickyy-b/Monzo-Meter/blob/master/heroku/web.py#L37), so that only requests from Monzo can change values
3. You can set the mode in which the app is working.
  - **FIXED_MAX**: The maximum angle equivalents to a preset amount of money.
  - **VARIABLE_MAX** : The maximum angle equivalents to the latest amount of load.
4. If you chose the FIXED_MAX mode, you should set the [maximum balance](https://github.com/d-Rickyy-b/Monzo-Meter/blob/master/heroku/web.py#L27)

If there is still anything unclear, don't hesitate to [contact me on Telegram](https://t.me/d_Rickyy_b) or via GitHub issues.
