from flaskr import create_app
from flaskr.models import create_db


if __name__ == '__main__':
    app = create_app()
    create_db(app.config['DATABASE'])
    app.run(host='localhost', port=8000)
