# kbdcycle
System76 keyboard color phaser 

## KBD Cycle for System76
Sometimes you get bored and want to mess with sine functions in Python. This simple script phases the color of the left, center, and right keyboard panes on System76 laptops equipped with a backlit keyboard. 

## Make it a Service
1. Copy the kbd-cycle.py script to /usr/bin or wherever you would like. I personally selected /etc/init.d.
2. Create a Unit File in /lib/systemd/system/kbd-cycle.service to define the service.
```
[Unit]
Description=Keyboard Rainbow

[Service]
Type=simple
ExecStart=/usr/bin/python3 /etc/init.d/kbd-cycle.py
StandardInput=tty-force

[Install]
WantedBy=multi-user.target
```
3. Reload the systemctl daemon:
```
$ sudo systemctl daemon-reload
```
4. Enable the new service:
```
$ sudo systemctl enable kbd-cycle.service
```
5. Start the new servie

```
sudo systemctl start kbd-cycle.service
```
6. Enjoy rainbow phased keyboard!
7. Stop the new service (because this is a crazy thing to have all the time)
```
$ sudo systemctl stop kbd-cycle.service
```
