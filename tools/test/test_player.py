import unittest

from player_scaling import *

class TestPlayer(unittest.TestCase):

    def test_suitable_target(self):
        scaler = PlayerScaling()
        player = scaler.get_suitable_player(target=20000)
        self.assertEqual("raz0r", player.name)

    def test_suitable_out_of_bounds(self):
        scaler = PlayerScaling()
        player = scaler.get_suitable_player(target=10**20)
        self.assertEqual("Protean", player.name)
