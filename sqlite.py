import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('users.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS 'profiles' ('users_id' PRIMARY KEY, 'name' TEXT);")

    db.commit()


async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profiles WHERE 'users_id' == '{key}'".format(key=user_id))
    if not user:
        cur.execute("INSERT INTO profiles VALUES (?, ?)", (user_id, 'name'))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute("UPDATE profiles SET name = '{}' WHERE users_id == '{}'".format(data['name'], user_id))
        db.commit()