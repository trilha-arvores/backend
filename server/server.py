from services import FlaskService
from controllers import trails_controller

FlaskService.setup_app()
app = FlaskService.app

app.register_blueprint(trails_controller, url_prefix="/trails")


@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return {}, 200


FlaskService.run_app()
