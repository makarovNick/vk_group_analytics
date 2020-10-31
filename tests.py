from utils import  *
import unittest

screen_name = 'api_test_group'

class SmallGroupTest(unittest.TestCase):
    def test_group_id(self):
        self.assertEqual(get_group_id(screen_name), 199889983)
    
    def test_group_posts(self):
        posts = get_group_posts(199889983, count = 2)
        self.assertEqual(len)
