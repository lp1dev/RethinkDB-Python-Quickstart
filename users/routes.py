from sanic.response import json
from users.model import User
from thinktwice.exceptions import ThinkTwiceException
from thinktwice.decorators import MandatoryParams


def init(app):
    @app.route("/user/login", methods=['POST'])
    @MandatoryParams(['username', 'password'])
    async def login_user(request):
        return json(User.login(request.json['username'], request.json['password']))

    @app.route("/user/", methods=["PUT"])
    @MandatoryParams(['username', 'password'])
    def put_user(request):
        try:
            User(request.json['username'], request.json['password']).export()
            return json({})
        except ThinkTwiceException as e:
            return json({"error": e.message, "code": e.code}, status=e.code)

    @app.route("/user/<user>", methods=['GET'])
    async def get_user(request, user):
        return json(User.get(user).export())
