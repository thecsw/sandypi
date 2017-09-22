# PiSandy Bot

- Hello fellas! 
- THis is a folder with a script for pisandy bot.
- This bot measures temperature from 5 Dallas (DS18B20) sensors via 1 wire.
- It can be easily modified to collect data from any w1 device.
- The code is heavily commented, so it's easy to read.
- Also this bot uses sensehat to collect data from humidity and pressure sensors.
- All this is sent via telegram to multiple users.
- To test it add the bot to your telegram --> telegram.me/pisandy_bot
##### Sometimes it can be offline, no worries, most of the time it's working 24/7.
- This bot has been heavily modified as RGB bulb has been added.
- This LGB bulb is showing green when the T < 26, yellow when 26 < T < 30 and red when T > 30.
- Use it as an easy-to-unserstand script so you can build your own.
- If you can and want to, pull requests.
- I tried to optimize the code, functions are kinda ugly
- Bot can handle up to 20 people simultaneosly, but the telepot API function.
- MessageLoop won't handle more than that, so you will need to use another telepot API
- function called WebHook. 
- It's harder to configure, but it's worth it.
## Good luck and have a nace day!
### From time to time it will be somehow improved, can't make it 100% sure.
