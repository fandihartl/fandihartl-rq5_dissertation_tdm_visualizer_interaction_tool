from index import app
import dash_auth
from dash_auth import BasicAuth
#from configuration import VALID_USERNAME_PASSWORD_PAIRS


server = app.server

auth = dash_auth.BasicAuth(
    app,
    (('abcde','1234',),)
)



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False, host="127.0.0.1", port=8050)