import requests
from pprint import pprint
import sqlite3

def create_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS subreddits (
              id TEXT PRIMARY KEY,
              author TEXT,
              subreddit TEXT
        )
    ''')
    conn.commit()

def parse(user, after = '', conn = None):
    url_template = 'https://old.reddit.com/user/{}/.json?t=all{}'

    headers = {
        'User-Agent' : 'XDD'
    }
    params = f'&after={after}' if after else ''

    url = url_template.format(user, params)
    response = requests.get(url, headers=headers)

    if response.ok:
        c = conn.cursor()
        data = response.json()['data']
        for post in data['children']:
            pdata = post['data']
            post_id = pdata['id']
            author = pdata['author']
            reddit = pdata['subreddit']
            print(f'{post_id} ({author}) {reddit}')
            c.execute('INSERT INTO subreddits VALUES (?,?,?)',
                      (post_id, author, reddit))
        conn.commit()
        return data['after']
    else:
        print(f'Error {response.status_code}')
        return None

def main():
    user = 'the_phet'

    conn = sqlite3.connect('reddit4.db')
    create_table(conn)
    after = ''
    try:
        while True:
            after = parse(user, after, conn)
            if not after:
                break
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        conn.close()
    
if __name__ == '__main__':
    main()


# user = 'grepnork'

# url = f'https://old.reddit.com/user/{user}/.json?t=all'

# headers = {
#     'User-Agent' : 'XDD'
# }

# response = requests.get(url, headers=headers)

# all_reddits = {}

# if response.ok:
#     data = response.json()['data']
#     for post in data['children']:
#         pdata = post['data']
#         reddit = pdata['subreddit']
#         if reddit in all_reddits:
#             all_reddits[reddit] += 1
#         else:
#             all_reddits[reddit] = 1
#         # print(f'Subreddit: {reddit}')
#         # print('----')
# else:
#     print(f'Error {response.status_code}')

# print(all_reddits)

# def parse(user, after = ''):
#     url_template = 'https://old.reddit.com/user/{}/.json?t=all{}'

#     headers = {
#         'User-Agent' : 'XDD'
#     }
#     params = f'&after={after}' if after else ''

#     url = url_template.format(user, params)
#     response = requests.get(url, headers=headers)

#     if response.ok:
#         data = response.json()['data']
#         for post in data['children']:
#             pdata = post['data']
#             reddit = pdata['subreddit']
#             # if reddit in all_reddits:
#             #     all_reddits[reddit] += 1
#             # else:
#             #     all_reddits[reddit] = 1
#             print(f'Subreddit: {reddit}')
#         return data['after']
#     else:
#         print(f'Error {response.status_code}')
#         return None

# def main():
#     user = 'the_phet'
#     after = ''
#     while True:
#         after = parse(user, after)
#         if not after:
#             break
    
# main()