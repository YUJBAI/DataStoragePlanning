from website import create_app
from flask_swagger_ui import get_swaggerui_blueprint

app = create_app()




if __name__ == '__main__':
    app.run(debug=True)

# SWAGGER_URL = '/swagger'
# API_URL = "../website/static/swagger.json"
# SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': "Seans-Python-Flask-REST-Boilerplate"
#     }
# )
# app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
