from datetime import datetime
from pony.orm import *


db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str)
    login_logs = Set('LoginLog')
    http_accesses = Set('HttpAccess')
    ftp_accesses = Set('FtpAccess')


class LoginLog(db.Entity):
    id = PrimaryKey(int, auto=True)
    timestamp = Required(datetime)
    user = Required(User)
    sniff_session = Required('SniffSession')
    ip = Required(str)


class HttpAccess(db.Entity):
    id = PrimaryKey(int, auto=True)
    host = Required(str)
    timestamp = Required(datetime)
    method = Required(str)
    user = Required(User)
    sniff_session = Required('SniffSession')
    uri = Optional(str)


class FtpAccess(db.Entity):
    id = PrimaryKey(int, auto=True)
    host = Required(str)
    action = Required(int)
    content = Optional(str)
    timestamp = Required(datetime)
    user = Required(User)
    sniff_session = Required('SniffSession')


class EmailWarning(db.Entity):
    id = PrimaryKey(int, auto=True)
    host = Required(unicode)
    method = Optional(str, nullable=True)


class SniffSession(db.Entity):
    id = PrimaryKey(int, auto=True)
    timestamp = Required(datetime)
    login_logs = Set(LoginLog)
    http_accesses = Set(HttpAccess)
    ftp_accesses = Set(FtpAccess, cascade_delete=True)
    current_session = Required(bool)


db.bind("sqlite", "db.sqlite", create_db=True)
db.generate_mapping(create_tables=True)