import requests
from pprint import pprint
import sqlite3

def create_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
              id TEXT PRIMARY KEY,
              title TEXT,
              score INTEGER,
              author TEXT,
              date REAL,
              url TEXT
        )
    ''')
    conn.commit()

def parse(subreddit, after = '', conn = None):
    url_template = 'https://old.reddit.com/r/{}/top.json?t=all{}'

    headers = {
        'User-Agent' : 'XDD'
    }
    params = f'&after={after}' if after else ''

    url = url_template.format(subreddit, params)
    response = requests.get(url, headers=headers)

    if response.ok:
        c = conn.cursor()
        data = response.json()['data']
        for post in data['children']:
            pdata = post['data']
            post_id = pdata['id']
            title = pdata['title']
            score = pdata['score']
            author = pdata['author']
            date = pdata['created_utc']
            url = pdata.get('url_overridden_by_dest')
            # print(f'Post ID: {post_id}')
            # print(f'Title: {title}')
            # print(f'Author: {author}')
            # print(f'Date: {date}')
            # print(f'(Image) URL: {url}')
            # print(f'Subreddit: {reddit}')
            # print('----')
            print(f'{post_id} ({score}) {title}')
            c.execute('INSERT OR IGNORE INTO posts VALUES (?,?,?,?,?,?)',
                      (post_id, title, score, author, date, url))
        conn.commit()
        return data['after']
    else:
        print(f'Error {response.status_code}')
        return None

def main():
    subreddit = 'programming'

    conn = sqlite3.connect('reddit-posts.db')
    create_table(conn)
    after = ''
    try:
        while True:
            after = parse(subreddit, after, conn)
            if not after:
                break
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        conn.close()
    
if __name__ == '__main__':
    main()

    
#V1
# import requests
# from pprint import pprint

# subreddit = 'programming'

# url = f'https://www.reddit.com/r/{subreddit}/top.json?t=all'

# headers = {
#     'User-Agent' : 'XDD'
# }

# response = requests.get(url, headers=headers)

# if response.ok:
#     data = response.json()['data']
#     for post in data['children']:
#         pdata = post['data']
#         author = pdata['author']
#         reddit = pdata['subreddit']
#         print(f'Author: {author}')
#         print(f'Subreddit: {reddit}')
#         print('----')
# else:
#     print(f'Error {response.status_code}')




#V2
# import requests
# from pprint import pprint

# def parse(subreddit, after = ''):
#     url_template = 'https://old.reddit.com/r/{}/top.json?t=all{}'

#     headers = {
#         'User-Agent' : 'XDD'
#     }
#     params = f'&after={after}' if after else ''

#     url = url_template.format(subreddit, params)
#     response = requests.get(url, headers=headers)

#     if response.ok:
#         data = response.json()['data']
#         for post in data['children']:
#             pdata = post['data']
#             author = pdata['author']
#             print(author)
#         return data['after']
#     else:
#         print(f'Error {response.status_code}')
#         return None

# def main():
#     subreddit = 'programming'
#     after = ''
#     while True:
#         after = parse(subreddit, after)
#         if not after:
#             break
    
# main()