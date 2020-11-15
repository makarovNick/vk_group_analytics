from tools.utils import (get_group_members, 
                         get_group_posts,
                         get_group_info,
                         get_group_stats,
                         date_n_days_ago)

from parser.parser import (parse_info,
                           parse_post,
                           parse_stats,
                           parse_user)

import unittest

screen_name = 'api_test_group'
group_id = 199889983

class ParserTest(unittest.TestCase):
    def test_user(self):
        fields = ['sex', 'bdate', 'city', 'country', 'online', 'education', 'last_seen']
        user = parse_user(get_group_members(group_id, count=1, fields=fields)[0])
        self.assertEqual(user['first_name'], 'Иван')
        self.assertEqual(user['last_name'], 'Иванов')
        self.assertEqual(user['sex'], 2)
        self.assertEqual(user['bdate'], '1.1.1991')
    
    def test_posts(self):
        posts = list(map(parse_post, get_group_posts(group_id, count = 3)))
        self.assertEqual(posts[2]['date'], 1604089060)
        self.assertEqual(posts[1]['text'], 'cat')
        self.assertEqual(posts[1]['comments_count'], 2)
        self.assertEqual(posts[2]['attachments'][0], 'photo')
    
    def test_info(self):
        fields = ['status', 'start_date', 'members_count', 'description', 'counters', 'country', 'activity']
        info = parse_info(get_group_info(group_id, fields=fields))
        self.assertEqual(info['name'], 'VK_API_TEST_GROUP')
        self.assertEqual(info['description'], 'description')
        self.assertEqual(info['photos_count'], 1)
        self.assertEqual(info['albums_count'], 1)
    
    # def test_stats(self):         strange unittest bug...
    #     dayvinchik = 91050183
    #     stats = parse_stats(get_group_stats(dayvinchik, timestamp_from=10))
    #     self.assertGreater(stats[-1]['RU_reach'], 3000000)
    #     self.assertGreater(stats[-1]['18-21_visitors'], stats[-1]['45-100_visitors'])
    #     self.assertEqual(len(stats), 10)


if __name__ == '__main__':
    unittest.main()