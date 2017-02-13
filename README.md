# squawk

I made this one late night for my sister to help her study for an ornithology test. Pulls MP3s from www.allaboutbirds.org to create a randomized, interactive quiz. 

##Usage
1. `pip install -r requirements.txt`
2. Populate [birdlist.yaml](https://github.com/MortimerMcMire315/squawk/blob/master/birdlist.yaml) as demonstrated with a list of birds separated into categories 
3. Run [birdquiz.py](https://github.com/MortimerMcMire315/squawk/blob/master/birdquiz.py) with Python 3. 

##Dependencies
* PyYAML >=3.12
* Beautiful Soup >=4.5.3
* Certifi >=2017.1.23
* DryScrape == 1.0
    * requires `qt5-default` and `libqt5webkit5-dev`

DryScrape [can be a pain to install](https://github.com/niklasb/dryscrape#a-word-about-qt-56) if you have Qt >= 5.6 installed. I'm hoping to lose it as a dependency soon, but I have to do some snooping through allaboutbirds.org's JavaScript to see if I can find a quick POST request to make instead of having to curl a page and literally run all of the JS in a headless WebKit instance for every quiz question.
