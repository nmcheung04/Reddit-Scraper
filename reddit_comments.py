import requests
import sqlite3
import csv

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    sql_create_table = """CREATE TABLE IF NOT EXISTS Comments (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                author TEXT NOT NULL,
                                upvotes INTEGER,
                                subreddit TEXT,
                                permalink TEXT,
                                comment TEXT UNIQUE
                            );"""
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except sqlite3.Error as e:
        print(e)

def insert_comment(conn, comment):
    sql_insert_comment = """INSERT OR IGNORE INTO Comments (author, upvotes, subreddit, permalink, comment)
                            VALUES (?, ?, ?, ?, ?);"""
    try:
        c = conn.cursor()
        c.execute(sql_insert_comment, comment)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def fetch_comments(url, headers, depth=1):
    url += f'?depth={depth}'
    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()[1]['data']
        comments = []
        for post in data['children']:
            pdata = post['data']
            if pdata.get('body'):
                comment = pdata['body'].replace('\n', '')  # Remove newline characters
                if (comment != '[removed]' and comment != '[deleted]'):
                    author = pdata['author']
                    upvotes = pdata['ups']
                    subreddit = pdata['subreddit']
                    permalink = pdata['permalink']
                    comments.append((author, upvotes, subreddit, permalink, comment))
        return comments
    else:
        print(f'Error {response.status_code}')
        return []

def save_to_csv(comments, csv_file):
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Author', 'Upvotes', 'Subreddit', 'Permalink', 'Comment'])
        writer.writerows(comments)

def main():
    db_file = 'post6.db'
    conn = create_connection(db_file)
    if conn is not None:
        create_table(conn)
    else:
        print("Error! Cannot create the database connection.")

    url = 'https://www.reddit.com/r/QAnonCasualties/comments/xbiy5s/tw_my_qdad_snapped_and_killed_my_family_this/.json'
    headers = {'User-Agent': 'test'}
    depth = 2  

    all_comments = fetch_comments(url, headers, depth)
    for comment in all_comments:
        insert_comment(conn, comment)

    conn.close()

    # Save comments to CSV
    csv_file = 'testxtzzzz.csv'
    save_to_csv(all_comments, csv_file)

if __name__ == '__main__':
    main()