from generator_app.website import create_app
import os

app = create_app()
app.secret_key = os.environ.get('SECRET_KEY', '123456789')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')