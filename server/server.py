from services import FlaskService, AuthenticationService
from controllers import trails_controller, admin_controller
from flask_cors import CORS

FlaskService.setup_app()
app = FlaskService.app
CORS(app)

app.register_blueprint(trails_controller, url_prefix="/trails")
app.register_blueprint(admin_controller, url_prefix="/admin")


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    # Sanity check
    x = AuthenticationService.generate_token(0)
    y = AuthenticationService.verify_token(x)

    if y != x:
        return {}, 500

    return {}, 200


FlaskService.run_app()
