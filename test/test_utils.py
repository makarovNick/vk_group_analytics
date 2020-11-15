from tools.utils import (get_group_id, 
                         get_group_posts, 
                         get_group_info, 
                         get_group_stats,
                         get_group_members)
import unittest

screen_name = 'api_test_group'
group_id = 199889983

class SmallGroupTest(unittest.TestCase):
    def test_id(self):
        self.assertEqual(get_group_id(screen_name), group_id)
    
    def test_posts(self):
        posts = get_group_posts(group_id)
        self.assertEqual(len(posts), 3)
        self.assertEqual(posts[0]['text'][:100], 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore ')
        self.assertEqual(posts[1]['attachments'][0]['type'], 'video')
        self.assertEqual(posts[2]['attachments'][0]['type'], 'photo')

    def test_info(self):
        fields = ['status', 'start_date', 'members_count', 'description', 'counters', 'country', 'activity']
        info = get_group_info(group_id, fields)
        self.assertEqual(info['description'], 'description')
        self.assertEqual(info['country']['title'], 'Россия')

    def test_stats(self):
        stats = get_group_stats(get_group_id('memes'), int((datetime.datetime.now() - datetime.timedelta(days=2)).timestamp()))
        self.assertEqual(len(stats), 2)
        self.assertGreater(stats[0]['reach']['reach'], stats[0]['reach']['mobile_reach'])

    def test_members(self):
        members = get_group_members(group_id)
        self.assertIn(604972063, members)


if __name__ == '__main__':
    unittest.main()