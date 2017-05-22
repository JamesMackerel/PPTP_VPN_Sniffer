from datetime import datetime
from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    login_logs = Set('LoginLog')


class LoginLog(db.Entity):
    id = PrimaryKey(int, auto=True)
    timestamp = Required(datetime)
    user = Required(User)


class HttpAccess(db.Entity):
    id = PrimaryKey(int, auto=True)
    host = Required(str)
    timestamp = Required(datetime)
    method = Required(str)
    sniff_session = Required('SniffSession')


class FtpAccess(db.Entity):
    id = PrimaryKey(int, auto=True)
    host = Required(str)
    action = Required(int)
    content = Required(str)
    timestamp = Required(datetime)
    sniff_session = Required('SniffSession')


class EmailWarning(db.Entity):
    id = PrimaryKey(int, auto=True)
    host = Required(str)


class SniffSession(db.Entity):
    id = PrimaryKey(int, auto=True)
    timestamp = Required(datetime)
    ftp_accesses = Set(FtpAccess)
    http_accesses = Set(HttpAccess)
    current_session = Required(bool)


db.bind("sqlite", "db.sqlite", create_db=True)
db.generate_mapping(create_tables=True)