## Geolocation Without GPS

![M5Stack](https://appelsiini.net/img/m5stack-map-1400.jpg)

Scans the nearby wifi networks and locates the board using [Google Maps Geolocation API](https://developers.google.com/maps/documentation/geolocation/intro). You must create a `settings.json` file which contains wifi credentials and a [Google Maps API key](https://developers.google.com/maps/documentation/geolocation/get-api-key). Use `settings.json.dist` as a template.

```
$ cp firmware/settings.json.dist settings/settings.json
$ nano -w settings/settings.json
```

When done upload the everything to the board and enter REPL. You might need to reset the board after entering REPL.

```
$ make sync
$ make repl
```
