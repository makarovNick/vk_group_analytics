from tools.utils import *

import asyncio

asyncio.coroutines._DEBUG = False

async def write_users(group_id):
    members = await async_get_members(group_id, count=-1)
    with open(f'groups/group_{str(group_id)}', 'w+') as f:
        for m in members:
            f.write("%d\n" % m)


async def main():
    count = 0
    with open('groups/groups.csv', 'r') as f:
        groups = [int(line) for line in f.readlines()]

    for g in groups:
        # print("AT ", j, i)
        try:
            await write_users(g)
        except VKGroupError:
            await asyncio.sleep(1)

        count+=1

if __name__ == '__main__':
    asyncio.run(main)
