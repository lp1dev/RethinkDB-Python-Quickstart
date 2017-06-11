from sanic.response import json
from users.model import User
from thinktwice.exceptions import ThinkTwiceException
from thinktwice.decorators import MandatoryParams, requires_login


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
    @requires_login
    async def get_user(request, user, logged_user):
        if logged_user.username == user and User.get(logged_user.username) is not None:
            return json(User.get(user).export())
        return json({'error': 'You cannot access these information', 'code': 403}, status=403)
