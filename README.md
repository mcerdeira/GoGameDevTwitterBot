A bot for helping me (and you?) with gamedev advertising on Twitter

Uses python-twitter https://github.com/bear/python-twitter 

## Usage

```
python gamedevbot.py
```
Starts the server. 
The first time you run it, Gamedevbot will ask for some configuration and store it in a .cfg file:

 - Your twitter API tokens (see https://dev.twitter.com/oauth/overview/application-owner-access-tokens)
 - A media path where the app will be searching for new media. Here you drop pngs, jpegs, gifs.
 - A number of seconds representing the monitor frequency
 - A template path for your tweets. Here your configure tweet texts in .txt files (or any plain text format)
 
The gamedevbot will monitor your media path every N seconds and tweet that media chosing a random template from your template path.
Then it will move the media to a subfolder in your media path at \hist\

You can have as many gamedevbots servers running as you want but they cannot share the same media folder and executable folder.
For example, if you may want to have 2 twitter accounts tweeting the same media, you must have 2 media folders (one for each) and the two instances of gamedevbot must be in different folders too.

Knowing that when the bot finds a media file it moves to a \hist\ subfolder, you can be as creative as you want, for example, the hist subfolder from one instance could be the media folder of another, 'chaining' 2 or more bots making them share the sames files.
