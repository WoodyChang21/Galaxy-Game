# Galaxy-Game
This is a full python game created with python kivy and mongo database. The main two python libraries used in this project are **kivy** and **pymongo**

## Feature
This Galaxy game can be played in Android, IOS, Linux, Windows. It is integrated with mongo database to record the top 5 record in all time.

## User interaction
The user interaction is coded in the **user_actions.py**, which specifies the corresponding response when the screen is pressed or when key left, right is pressed.

<img width="438" alt="image" src="https://user-images.githubusercontent.com/99929453/208507091-c6430387-f470-438a-8c02-68f50eaf0cd6.png">


## Game Logic
The main game logic is shown in the **main.py** file

The player gets to move left or right to control the ship to stay on the path.

It constantly checks if the ships collided or not. This checking process is specified in **def update(self,dt)** which runs every 1/60 second.

## Game Display
### Game Interface
The game interface consist two major parts. (The path and the ship)

The path is generated randomly every 1/60 second in **def update(self,dt)**. 

The ship coordinates are updated in **def update(self,dt)** with the corresponding user response.

<img width="677" alt="image" src="https://user-images.githubusercontent.com/99929453/208507818-bdd8078b-27a6-4540-8775-53ef64de3e65.png">



###  Menu Interface
The menu interface is coded in **menu.py** and **menu.kv**. These two files compile the the menu interface.

<img width="673" alt="image" src="https://user-images.githubusercontent.com/99929453/208505120-ad8fff7b-c239-460e-8720-2cae0044540b.png">

### Rank interface
**rank.py** and **rank.kv** together compile the rank interface which shows the top 5 record of all time.
**bestscore_db** collects the data from **mongodb** which is modified and imported through the python library (pymongo)

<img width="674" alt="image" src="https://user-images.githubusercontent.com/99929453/208505722-79ef5b1c-8e7e-44a2-bd6c-c3406c840fcc.png">

## Audio
This game also comes with sound while playing. It has corresponding sounds when launching the game, playing the game and when gameover. These files can be found in the audio files located above.

