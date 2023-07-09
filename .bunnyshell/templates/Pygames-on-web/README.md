> Let's say you've just started building a game using Pygame or just thinking about it and you're looking for a readily available template that you can use to code, test, and deploy - then this repo is for you

## Table of Contents

- [What is does?](#what-is-does)
- [Gameplay](#gameplay)
- [Purpose of each component?](#purpose-of-each-component)
  - [dev](#1-dev-component)
  - [stg](#2-stg-component)
  - [prod](#3-prod-component)
- [How to Add New Games?](#how-to-add-new-games)
- [Build With](#build-with)
- [Setup Environment for local](#setup-environment-for-local-development-and-testing)
- [FAQs](#faqs)

## What is does?

`Deploy any of your pygames code to web with a single push with Bunnyshell Environment as a Service (EaaS) platform`

### [Click here to try out the games!](https://prod-pygame-sandyinspires.bunnyenv.com/)

## Gameplay

![PC Gameplay](https://github.com/Santhoshkumard11/bunnyshell-deploy-pygame/blob/main/images/gameplay.gif?raw=true)

### UI Snapshot
![UI](https://github.com/Santhoshkumard11/bunnyshell-deploy-pygame/blob/main/images/ui.png?raw=true)


## Purpose of each component?

We've a total of three components in our environment `dev, stg, and prod`

### 1. dev component

- This is a safe place to try out new things, push as much code as possible
- Making a push to the `dev` branch will redeploy the code

### 2. stg component

- This is a place to test all the functions and share it across the team to start the verification/testing
- Merge your dev branch with `stg` branch to trigger a deployment

### 3. prod component

- This is a place to share it with wider audience and the live application is here
- Push to `main` only if all the test cases and checks are cleared
- Merge your stg branch with `main` branch to trigger a deployment

## How to Add New Games?

It's an extremely easy process (having a lot of steps), follow the steps below:

- Add your entire game to `/pygames` folder in the repo
- Make sure to build the game locally as instructed [here](#setup-environment-for-local-development-and-testing)
- You've to edit the Dockerfile inside `/pygames` folder, add a path in mkdir command of the game you're trying to add
- Add a line in copying the game folder inside the container (it can be optimized to just one copy - working on it)
- Add a line to build the new game you've just added with Pygbag
- Add the path of the new game you've added inside the nginx image
- Copy the new game build from the `pygame_build` stage to `prod`

## Build With

- Python - General Programming
- Pygame - Writing Game Logic
- Pygbag - Python WebAssembly for everyone ( packager + test server )
- Docker - Build and deploy the game

## Setup Environment for local development and testing

### Create a virtual environment

`python3 -m venv venv`

`source venv/bin/activate`

### Install all Python libraries

`pip install -r requirements.txt`

### Run the game

`python3 pygames/classic_hunt/main.py`

### Run on Web - runs on port localhost:8000

`python3 -m pygbag pygames/classic_hunt/`

## FAQs

1. My game is not loading up at localhost:8000?

   - Please use [this](#run-the-game) step to verify it works on just Python before trying to build with Pygbag, running this way will given you a hint of any exception you might not have handled in the game logic

2. My game assets are not getting build properly in docker?

   - Please make sure you're copying the game assets to the right folders in the Dockerfile, I know there are many moving parts in the Dockerfile, you can copy any example line and just edit the path

3. Game audio files are not working?
   - Pygbag wants your audio files to be in `.ogg` format so please convert all your audio files to `.ogg` format if not already

## Reference/Credits:
- [Python](https://www.python.org/)
- [Pygbag](https://pygame-web.github.io/)
- [Pygame](https://www.pygame.org/news)

Space Invaders - [leerob](https://github.com/leerob), Classic Hunt - [sumosp](https://github.com/sumosp), Flappy Bird - [cprakash64](https://github.com/cprakash64), and Street Fighter [OyeMad](https://github.com/OyeMad)

[Go to top](#bunnyshell-deploy-pygames)
