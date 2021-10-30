<!DOCTYPE html>

<html lang="en" data-color-mode="auto" data-light-theme="dark" data-dark-theme="dark" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />

</head>
<body style="word-wrap: break-word; color: white; background-color: black;">
    <h1>MQTT Alsa Volume remote control</h1>
    <p>Remote Control for Alsa on Raspberry Pi for control by <a href="https://www.home-assistant.io/" rel="nofollow">Home Assistant</a></p>
    </br></br></p>
    <h1>Installation</h1>
    <p>
        1)  On the Raspberry Pi or other devices using Alsa, copy the MqttVol.py and RpiMqtt.conf files to a convenient folder.
        The folder used in testing was /var/www/html. </br></br>
        2)  The python app must be run by the instance of user pi's current desktop or it may not see the Alsa outputs.</br>
        It is most convenient to start the app at the Pi desktop start as this will insure the proper Alsa output is available.</br>
        To enable startup at boot and manual restart of the app, copy mqttvolD to the /etc/init.d folder.
        </br></br>
        3)  Copy MqttVolStart to the /home/pi/.config/autostart folder and insure it has execute rights.
        </br>Do not add it to rc.d as that will break the link to Alsa outputs.</br></br>
        4)  For the start and restart to work properly python3 needs to be linked to pyvol.</br>Enter the command "sudo ln /usr/bin/python3 /usr/bin/pyvol" </br>
        This allows the program to be stopped and started without affecting other python3 programs.
        "
    </p>
    <h1>Homeassistant</h1>
    <p>
        The volume control will look like a light to Homeassistant</br>
        It can be added to the lights.yaml file with the entry in lights.yaml.</br>
        It can also be added to configuration.yaml as a light
    </p>
    <h1>Notes:</h1>
    <p>Suggestions branches or anything to improve this is welcome.</p>
</body>
</html>
