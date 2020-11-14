from multiprocessing.dummy import Pool as ThreadPool
import requests

left = 25000
right = 150000

def get_groups(offset):
    response = requests.get(
    'http://allsocial.ru/entity',
        params={
            'direction': 1,
            'is_closed': 1,
            'offset': offset,
            'order_by': 'quantity',
            'range': f'{left}:{right}',
        }
    )
    return [g['vk_id'] for g in response.json()['response']['entity']]

response = requests.get(
    'http://allsocial.ru/entity',
    params={
        'direction': 1,
        'is_closed': 1,
        'offset': 0,
        'order_by': 'quantity',
        'range': f'{left}:{right}',
    }
)
count = response.json()['response']['total_count']
pool = ThreadPool(4)
groups = [i for j in pool.map(get_groups, range(0, count, 25)) for i in j]

pool.close()
pool.join()