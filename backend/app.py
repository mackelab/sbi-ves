import os

from api import app

if __name__ == '__main__':
    if not os.path.exists('./uploads'):
        os.mkdir('./api/uploads')
        os.mkdir('./api/uploads/files')
        os.mkdir('./api/uploads/temp')

    app.run(debug=True)
