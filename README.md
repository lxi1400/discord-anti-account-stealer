# Discord Anti Account Stealer
Simple script to try to prevent bad actors from logging in 

# How it works 

Discord has a new endpoint called sessions, where you can see all the current devices logged into your discord acount. This script will check the sessions endpoint every 5 seconds, and if a device from a new location that you haven't whitelisted appears, it will attempt to change your password thus logging them out. 


# How to setup 
Firstly, you're going to want to grab your token and your 'X-Super-Properties' (google how to get these if you do not know how)
Second, in the `config.json` file, update it with your info (If you have 2FA enabled, make sure to set 2FA to `true` and put a backup code in there so that the program can change your password)
Third, you want to go to the main.py file, and add all whitelisted locations. This is important as if your location isn't whitelisted, it'll change your password as soon as you login. An example location looks like `whitelisted = ["New York, New York, United States"]`
Lastly, just run the file and boom! The script should be up and running 


# Disclaimer 
This is for education purposes only. Discord may choose to terminate your account for using this script. I am not responsible for anything that may happen. 
