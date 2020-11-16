from tools.stats import (get_posts_stats,
                         get_info_stats)

import unittest

screen_name = 'api_test_group'
group_id = 199889983

class StatsTest(unittest.TestCase):
    def test_posts(self):
        stats = get_posts_stats([group_id], posts_per_day=True,
                                views_per_post=True,
                                likes_per_post=True,
                                n_posts=3,
                                n_days=1)
        self.assertEqual(stats[0]['posts_per_day'], 0.0)
        self.assertGreaterEqual(stats[0]['views_per_post'], 8)
        self.assertGreaterEqual(stats[0]['likes_per_post'], 1.0)

    def test_info(self):
        dayvinchik = 91050183
        stats = get_info_stats([dayvinchik], comments=False,
                               likes=True,
                               subscribed=True,
                               total_reach=True,
                               n_days=7)

        self.assertAlmostEqual(stats[0]['likes'], 1000000, delta=300000)
        self.assertAlmostEqual(stats[0]['subscribed'], 10000, delta=7000)
        self.assertAlmostEqual(stats[0]['total_reach'], 4000000, delta=500000)

if __name__ == '__main__':
    unittest.main()
