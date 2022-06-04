from pony.orm import Database, Required, Optional, db_session

try:
    from loadconfig import __db_config__
except ImportError:
    exit('set DATABASE_CFG')

db = Database()
db.bind(**__db_config__)


class UserState(db.Entity):
    user_id = Required(int, unique=True)
    username = Required(str, sql_default="''")
    user_state = Optional(str, sql_default="''")


class File(db.Entity):
    user_id = Required(int)
    username = Required(str)
    file_path = Required(str)
    del_file = Optional(bool)


async def create_user(user_id, username, user_state):
    user_id = int(user_id)
    with db_session:
        if not UserState.get(user_id=user_id):
            UserState(user_id=user_id, username=username, user_state=user_state)
        else:
            UserState.get(user_id=user_id).delete()
            UserState(user_id=user_id, username=username, user_state=user_state)


async def update_user(user_id, user_state):
    with db_session:
        user = UserState.get(user_id=int(user_id))
        if not user:
            UserState(user_id=int(user_id), user_state=user_state)
            user = UserState.get(user_id=int(user_id))
        user.user_state = user_state


async def delete_user(user_id):
    with db_session:
        if UserState.get(user_id=int(user_id)):
            UserState.get(user_id=int(user_id)).delete()


# async def register_user(data):
#     with db_session:
#         user_id, username, file_path, del_file = data
#         file = File(
#             user_id=user_id,
#             username=username,
#             file_path=file_path,
#             del_file=del_file
#         )


db.generate_mapping(create_tables=True)
