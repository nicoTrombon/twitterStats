from flask import Flask,render_template
import get_stats

app = Flask(__name__)

##codigo
@app.route('/', methods = ['GET'])
@app.route('/<handle>', methods = ['GET'])
def index(handle='nicoteiz'):
    stats, tags = get_stats.main(handle)
    return render_template('layout.html', handle = stats['screen_name'], name = stats['name'], desc = stats['description'], pic = stats['pic'], frds = stats['friends_count'], fols = stats['followers_count'], tags = tags)


if __name__ == '__main__':
    app.run()
