'''
This is the environment artist tester. It will extend the ArtistTester class.
'''

from artist_tester import ArtistTester
from robot_artist import RobotArtist

class EnvironmentArtistTester(ArtistTester):
    # Constructor
    def __init__(self):
        super().__init__()
        
    # Method for drawin the element.
    # In this case it is a single robot
    def draw_element(self):
        artist = EnvironmentArtist(1)
        artist.draw_all()

if __name__ == "__main__":
    EnvironmentArtistTester()