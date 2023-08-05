## TimeTrack

Time is tracked by logging the active, focused window of the user every second.
The consolidate script is mean to be run on a 5 minute interval on the seconds, and consolidates the raw time log.

You then upload your consolidated time log to <https://timetrack.slgotting.com>, and you can inspect your time usage with a graphical UI

## Compatibility

Right now this script is only usable on Linux. Tested working on Ubuntu 18. It should work on any linux distro if the following commands are available:

* xdotool
* wmctrl
* xprintidle

I may add support for Windows in the future but I wanted to get it out as it is right now.

## Getting Started

### Install package with

`pip install timetrack-slg`


## Install the easy way

`sudo install-timetrack-slg`

## Install the hard way

This is the hard way, make sure to look over any commands and see that they contain proper variable values

### 1. Set up systemd to automatically run script (on boot and always restart on fail)

 :warning: | Make sure to change username to your username
 :---: | :---
 :warning: | Also your python file install might be at a location other than `/home/username/.local/bin/timetrack-slg`. To find location, run `whereis timetrack-slg`. Update ExecStart as necessary
 :information_source: | The -s switch is set to .9766 because this is the interval I found gives me close to or exactly 1 run per second. See ["Calculate your sleep time"](#calculate-your-sleep-time) for information on how to calculate what value you should use.
 :information_source: | Get your DISPLAY variable with `env \| grep DISPLAY`
 :information_source: | Output file `-o /home/username/timetrack-slg/time-log.json` must be a json file
 :information_source: | Run timetrack-slg -h to see all options

:warning: Before running this command make sure you change the necessary variables using the above as guidance to doing so.

In your terminal, run:

```
echo '[Unit]
Description=Time tracker
After=multi-user.target

[Service]
User=username
Type=simple
Restart=always
Environment="DISPLAY=:0"
ExecStart=/home/username/.local/bin/timetrack-slg \
            --output_filepath /home/username/timetrack-slg/time-log.json \
            --sleep_time 0.9766 \
            --time_til_idle 30 \
            --config_filepath /home/username/.config/slg/time-log.yml

[Install]
WantedBy=multi-user.target' | sudo tee /etc/systemd/system/timetrack-slg.service >/dev/null
```

Restart systemctl daemon:

`sudo systemctl daemon-reload`

Then tell systemd to start this up at boot with:

`sudo systemctl enable timetrack-slg.service`

And start er up with:

`sudo systemctl start timetrack-slg.service`


### 2. Set up cron job to automatically consolidate log

Add this line to your crontab (changing username and paths where necessary):

`*/5 * * * * /home/username/.local/bin/timetrack-consolidate-slg --input_filepath /home/username/timetrack-slg/time-log.json --config_filepath /home/username/.config/slg/time-log.yml --run_interval 5`

This line consolidates the time-log.json file every 5 minutes so that our timelog filesize doesnt grow too big.


### 3. Success

If you've done everything correctly, you should have a time-log-consolidated.json generated in the input_filepath location (if at least 5 minutes have passed).



## More Info

### Calculate your sleep time

> 1. Make sure timetrack-consolidate-slg is running in crontab every 5 minutes.
> 2. Run the script without any -s flag set for a while. 10 minutes to be safe. Shouldn't need to do this more than once so find something else to do while waiting.
> 3. Inspect your consolidate file and add up the times of a 5 minute block. The value should be relatively close to 300 (~ 290 - 299). Mine was 293
> 4. Divide number by 300. So in my case I had 293 so ( 293 / 300 ) is .9766, hence the value you see above.

> Note: Since we will simply overwrite any times that already exist, we can use a number lower than this and run the script more frequently (0.96 or even lower) to guarantee we have 300 data points every 5 minutes.
