from website import create_app


app = create_app()


if __name__ == '__main__':
    print('Starting the server...')
    print("mongoDB connected")
    app.run(debug=True)
