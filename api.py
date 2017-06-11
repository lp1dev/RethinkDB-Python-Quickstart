#!./env/bin/python
import rethinkdb as r
from sanic import Sanic
from sanic.response import json
from users.model import User
from thinktwice.exceptions import ThinkTwiceException
import config
import users.routes

app = Sanic()


@app.route("/")
async def api(request):
    return json({'name': config.project_name, 'version': config.version})


def init_routes():
    users.routes.init(app)


def init_db():
    conn = r.connect(config.db_host, config.db_port)
    conn.repl()
    return conn


def build_db(conn):
    r.db_create(config.db_name).run(conn)
    r.table_create('users').run()
    r.table('users').index_create('username').run()
    r.table('users').index_wait('username').run()


def main():
    conn = init_db()
    try:
        conn.use(config.db_name)
        User(username='admin', password='admin', group=0)
    except r.errors.ReqlOpFailedError:
        build_db(conn)
        User(username='admin', password='admin', group=0)
    except ThinkTwiceException:
        pass
    init_routes()
    app.run(host=config.webapi_host, port=config.webapi_port)
    return 0


if __name__ == "__main__":
    exit(main())
