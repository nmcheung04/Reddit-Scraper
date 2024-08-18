import requests
from pprint import pprint
import sqlite3

visited = set()

def create_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS subreddits (
              id_date TEXT PRIMARY KEY,
              author TEXT,
              subreddit TEXT
        )
    ''')
    conn.commit()

def parse_user(user, after='', conn=None):
    url_template = 'https://old.reddit.com/user/{}/.json?t=all{}'

    headers = {
        'User-Agent': 'XDD'
    }
    params = f'&after={after}' if after else ''

    url = url_template.format(user, params)
    response = requests.get(url, headers=headers)

    if response.ok:
        c = conn.cursor()
        data = response.json()['data']
        for post in data['children']:
            pdata = post['data']
            date = pdata['created_utc']
            post_id = pdata['id']
            id_date = post_id + str(date)
            author = pdata['author']
            reddit = pdata['subreddit']
            print(f'{id_date} ({author}) {reddit}')
            c.execute('INSERT OR IGNORE INTO subreddits VALUES (?,?,?)',
                      (id_date, author, reddit))
        conn.commit()
        return data['after']
    else:
        print(f'Error {response.status_code}')
        return None

def parse_subreddit(subreddit, after='', conn=None):
    # url_template = 'https://old.reddit.com/r/{}/.json{}'
    url_template = 'https://old.reddit.com/r/{}/top.json?t=all{}'     #TOP OF ALL TIME

    headers = {
        'User-Agent': 'XDD'
    }
    params = f'&after={after}' if after else ''

    url = url_template.format(subreddit, params)
    response = requests.get(url, headers=headers)

    if response.ok:
        data = response.json()['data']
        for post in data['children']:
            pdata = post['data']
            author = pdata['author']
            if author in visited:
                continue
            visited.add(author)
            parse_user(author, after='', conn=conn)
        return data['after']
    else:
        print(f'Error {response.status_code}')
        return None

def main():
    subreddit = 'politics'
    conn = sqlite3.connect('test.db')
    create_table(conn)
    after = ''
    try:
        while True:
            after = parse_subreddit(subreddit, after, conn)
            if not after:
                break
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        conn.close()

if __name__ == '__main__':
    main()