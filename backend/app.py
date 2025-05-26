from stem_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # Make sure to use the correct port, especially if your frontend is expecting a specific port.
    # The default Flask port is 5000. If your React frontend (localhost:3000)
    # is making requests to a different port, you'll need to adjust this. 