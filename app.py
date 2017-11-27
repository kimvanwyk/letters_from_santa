from flask import Flask, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField, PasswordField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.secret_key = '76e2653e-d2c4-11e7-bfa8-80fa5b4a283c'
# csrf = CsrfProtect(app)

import glob
import os, os.path

BG_IMAGES = [os.path.basename(bg) for bg in glob.glob('static/bg_*.png')]
BG_IMAGES.sort()

WORDINGS = ['''Dear %(name)s<p>Did you know that all my elves have been talking about you? They are all very impressed that you %(accomplishment)s this year. Mrs. Claus and I are proud of you too!<p>The elves and I have been busy building toys and getting my sleigh ready for the big trip. Mrs. Claus is hard at work making me a new outfit. It seems that I've outgrown my suit from last year! The reindeer are training each day, so they'll be ready for the big Christmas Eve journey! So, you can see we're keeping busy, but we're looking forward to visiting %(town)s and stopping at your house. I understand that you have asked for %(present)s from Santa this year.<p>The elves and I are searching the Toy Workshop to see if we might be able to find it for you!<p>Please be in bed early on Christmas Eve and don't forget to hang your stocking out with care!<p>Merry Christmas and Warmest Wishes!<p>Santa Claus''',
            '''Dear %(name)s<p>Merry Christmas greetings!<p>Rudolph just whispered in my ear that the sleigh is nearly packed. He can hardly wait to lead the reindeer with my sleigh full of toys on our long trip to visit the homes of good boys and girls. The elves are busy putting bows and ribbons on the last of the presents.<p>I just had to take a minute to write to you and tell you that I am very pleased with the good reports I have received about you. I see that you %(accomplishment)s this year!<p>The reindeer and I are planning to arrive in %(town)s just after midnight to deliver your gifts. Please be sure to hang your stocking and be in bed early as Christmas will be such a busy day!<p>Well, Mrs. Claus is calling me for dinner, so I have to get going. Keep on being good and Merry Christmas to you and your family!<p>Merry Christmas and Warmest Wishes!<p>Santa Claus''',
            '''Hi %(name)s<p>The weather has turned very cold up here at the North Pole and we are getting ready for another wonderful Christmas Season! Coming to visit you in %(town)s is something the reindeer and I are especially excited about, since %(province)s is one of our very favourite places to visit!<p>Have you ever noticed the old black boots I always wear with my red suit? I've had them for a long time and I really love them lots. This year Mrs Claus decided they needed a good shining, so she took them down to her sewing room to polish them up for me. Unfortunately, she didn't tell me she was taking them, so I spent all morning searching for them so I could go down to breakfast. I was really hungry and didn't think I could wait much longer, so I went down to the hall in just my socks! When I sat down to eat my porridge I noticed I had a hole in my left sock, right at the big toe! Boy was I embarrassed! Luckily Mrs Claus returned my boots right after breakfast and the elves didn't even notice. I'd better ask Mrs Claus to fix up my socks, too.<p>I'm so glad I get to share another Christmas with you, %(name)s. I'll bring you some wonderful presents on Christmas Eve.<p>See you soon!<p>Love Santa Claus''']

DEFAULT_VALS = {'name':'George',
                'surname':'Washington',
                'accomplishment':'scored 3 goals',
                'town':'Pietermaritzburg',
                'province':'KwaZulu Natal',
                'present':'a bicycle'}

SELECT_PREFIX = 'select_'

def get_selection(form_keys, choices, session_key):
    for sel in form_keys:
        if SELECT_PREFIX in sel:
            i = int(sel[len(SELECT_PREFIX):])
            print i, choices[i]
            session[session_key] = i

@app.route('/select_bg', methods=['POST', 'GET'])
def select_bg():
    if request.method == 'POST':
        get_selection(request.form.keys(), BG_IMAGES, 'bg')
        print session
    choices = ['<img src="static/%s" width="100%%">' % bg for bg in BG_IMAGES]
    message = 'Please select the background of the letter. '
    return render_template('select.html', name="Select Background Image",
                           choices=choices, target=request.url, width=100/len(choices))

@app.route('/select_wording', methods=['POST', 'GET'])
def select_wording():
    if request.method == 'POST':
        get_selection(request.form.keys(), WORDINGS, 'wording')
        print session
    choices = [w % DEFAULT_VALS for w in WORDINGS]
    message = 'Please select the wording of the letter. You will be asked to customise the letter for the receiving child on the next page.'
    return render_template('select.html', name="Select Wording",
                           choices=choices, target=request.url, width=100/len(choices))

if __name__ == '__main__':
    app.run(debug=True)
