from base.utils import create_app
from configs.config import settings

app = create_app()
app.config['SECRET_KEY'] = settings.get('secret_key')


@app.route('/')
def ping():
    return 'ping!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
