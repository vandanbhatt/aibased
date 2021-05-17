from base import app

if __name__ == '__main__':
    app.run(host="localhost", debug=True, threaded=True, port=5429)
