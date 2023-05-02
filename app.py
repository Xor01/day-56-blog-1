from flask import Flask, render_template
from markupsafe import escape
from requests import get
from post import Post

app = Flask(__name__)
post_objs = []


def request_api():
    posts = get(url="https://api.npoint.io/c790b4d5cab58020d391").json()
    for post in posts:
        post_obj = Post(post['id'], post['title'], post['subtitle'], post['body'])
        post_objs.append(post_obj)


@app.errorhandler(404)
def file_not_find():
    return render_template('404.html')


@app.route('/')
def get_blog():
    post_objs.clear()
    request_api()
    return render_template('index.html', posts=post_objs)


@app.route('/post/<int:post_id>')
def get_post_by_id(post_id):
    wanted_post = None
    for post in post_objs:
        if post.post_id == int(escape(post_id)):
            wanted_post = post
            break
    return render_template('post.html', my_post=wanted_post)


if __name__ == '__main__':
    app.run(debug=True)
