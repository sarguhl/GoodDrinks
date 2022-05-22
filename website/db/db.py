import imp
from os.path import isfile
import pymysql.cursors
import time

from apscheduler.triggers.cron import CronTrigger

DB_PATH = "./data/db/database.db"
BUILD_PATH = "./data/db/build.sql"

time.sleep(500)

db = pymysql.connect(
    host="172.17.0.1",
    user="sarguhl_user710953",
    password="TioTio$a!1234",
    database="sarguhl_bereich"
)
cur = db.cursor()


def with_commit(func):
	def inner(*args, **kwargs):
		func(*args, **kwargs)
		commit()

	return inner


@with_commit
def build():
	if isfile(BUILD_PATH):
		scriptexec(BUILD_PATH)



def commit():
    db.commit()


def close():
    db.close()


def field(command, *values):
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchone()


def records(command, *values):
    cur.execute(command, tuple(values))

    return cur.fetchall()


def column(command, *values):
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    cur.execute(command, tuple(values))


def multiexec(command, valueset):
    cur.executemany(command, valueset)


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())