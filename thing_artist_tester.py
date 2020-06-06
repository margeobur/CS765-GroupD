'''
This is the thing artist tester. It will extend the ArtistTester class.
'''

from artist_tester import ArtistTester
from thing_artist import ThingArtist
import random
import math
import turtle

class ThingArtistTester(ArtistTester):
    # Constructor
    def __init__(self):
        super().__init__()
        
    # Method for drawin the element.
    # In this case it is a few things in the environment
    def draw_element(self):
        artist1 = ThingArtist(1)
        artist2 = ThingArtist(1)
        artist3 = ThingArtist(1)
        artist4 = ThingArtist(1)
        artist5 = ThingArtist(1)
        artist6 = ThingArtist(1)
        artist7 = ThingArtist(1)
        artist8 = ThingArtist(1)
        artist9 = ThingArtist(1)
        smell_sig1 = [-0.9839331785325784, -0.5704448656826802, 0.19813476679260122, -0.48733626303552935, 0.3164121339906443]
        smell_sig2 = [-0.6087177587803845, -0.7086575054860784, -0.4292347100952876, -0.6775862006524294, 0.24007979529044876]
        smell_sig3 = [0.8219148952894033, 0.2832102912376675, 0.8423558565280047, -0.9507467210863441, -0.6497279333171668]

        artist1.x_position(150).y_position(150).colour("yellow").smell_signature(smell_sig1)
        artist2.x_position(250).y_position(150).colour("yellow").smell_signature(smell_sig2)
        artist3.x_position(350).y_position(150).colour("yellow").smell_signature(smell_sig3)
        artist4.x_position(150).y_position(250).colour("blue").smell_signature(smell_sig1)
        artist5.x_position(250).y_position(250).colour("blue").smell_signature(smell_sig2)
        artist6.x_position(350).y_position(250).colour("blue").smell_signature(smell_sig3)
        artist7.x_position(150).y_position(350).colour("red").smell_signature(smell_sig1)
        artist8.x_position(250).y_position(350).colour("red").smell_signature(smell_sig2)
        artist9.x_position(350).y_position(350).colour("red").smell_signature(smell_sig3)
        artist1.draw()
        artist2.draw()
        artist3.draw()
        artist4.draw()
        artist5.draw()
        artist6.draw()
        artist7.draw()
        artist8.draw()
        artist9.draw()

if __name__ == "__main__":
    ThingArtistTester()