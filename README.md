# arx_ii-13
Agent developed to compete in the AI Sports Challange 2020 hosted by Coder One.

## Description

This agent uses the A* Algorithm for path finding and a very crude method for determining the optimal bombing location. The bombing location is determined by scoring all possible bombing location and picking the one which would score the most points with a singular bomb. Additionally a basic configuarable bomb avoidance logic has coded in, so it shouldn't die too easily.

## Running the Agent

1. Head over to the [Dungeon and Data Structures Repo](https://github.com/gocoderone/dungeons-and-data-structures) to download and install a copy of the latest game.
2. Clone this repo.
3. Run `coderone-dungeon --interactive arx_ii-13`, where arx_ii-13 is the directory of this repo.

## Notes

The code base has been refactored since the challenge to tidy-up the huge mess when coding against a tight deadline (still messy though). However the logic still remains the same.