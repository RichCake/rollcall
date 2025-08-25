from django.test import TestCase

from games.models import Game


class CategoryModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Game.objects.create(name='Test Game')

    def test_game_creation(self):
        game = Game.objects.create(name='Another Game')
        self.assertIsInstance(game, Game)
        self.assertEqual(game.name, 'Another Game')