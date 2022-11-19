from pymongo import MongoClient
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import jwt
from bson import ObjectId
import certifi

app = Flask(__name__)

SECRET_KEY = 'firstpeungin'

ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.5zedkbw.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.firstpenguin


##############################
# path
##############################
@app.route('/', methods=['GET'])
def home_path():
    return render_template('index.html')


##user1
@app.route('/user1', methods=['GET'])
def user1_path():
    return render_template('user1.html')


##user2
@app.route('/user2', methods=['GET'])
def user2_path():
    return render_template('user2.html')


##user3
@app.route('/user3', methods=['GET'])
def user3_path():
    return render_template('user3.html')


##user4
@app.route('/user4', methods=['GET'])
def user4_path():
    return render_template('user4.html')


##user4
@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html')


##############################
# Post
##############################
# user1 읽기(Read)
@app.route('/user1/read', methods=['GET'])
def user1_read():
    reads = list(db.users.find({}, {'_id': False}))
    return jsonify({'all_reads': reads})


# user2 읽기(Read)
@app.route('/user2/read', methods=['GET'])
def user2_read():
    reads = list(db.users.find({}, {'_id': False}))
    return jsonify({'all_reads': reads})


# user3 읽기(Read)
@app.route('/user3/read', methods=['GET'])
def user3_read():
    reads = list(db.users.find({}, {'_id': False}))
    return jsonify({'all_reads': reads})


# user4 읽기(Read)
@app.route('/user4/read', methods=['GET'])
def user4_read():
    reads = list(db.users.find({}, {'_id': False}))
    return jsonify({'all_reads': reads})


##############################
# sa comment
##############################
## sa comment Post
@app.route('/sa', methods=['POST'])
def sa_comment_write():
    comment_receive = request.form['comment_give']
    name_receive = request.form['name_give']

    doc = {
        'comment': comment_receive,
        'name': name_receive
    }
    db.sacomment.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '댓글 작성되었습니다.'})


## sa comment Get
@app.route('/sa', methods=['GET'])
def sa_comment_read():
    comment = list(db.sacomment.find({}, {'_id': False}))
    return jsonify({'all_comment': comment})


##############################
# park comment
##############################
## park comment Post
@app.route('/park', methods=['POST'])
def park_comment_write():
    comment_receive = request.form['comment_give']
    name_receive = request.form['name_give']
    doc = {
        'comment': comment_receive,
        'name': name_receive
    }
    db.parkcomment.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '댓글 작성되었습니다.'})


## park comment Get
@app.route('/park', methods=['GET'])
def park_comment_read():
    comment = list(db.parkcomment.find({}, {'_id': False}))
    return jsonify({'all_comment': comment})


##############################
# su comment
##############################
## su comment Post
@app.route('/su', methods=['POST'])
def su_comment_write():
    comment_receive = request.form['comment_give']
    name_receive = request.form['name_give']

    doc = {
        'comment': comment_receive,
        'name': name_receive
    }
    db.sucomment.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '댓글 작성되었습니다.'})


## su comment Get
@app.route('/su', methods=['GET'])
def su_comment_read():
    comment = list(db.sucomment.find({}, {'_id': False}))
    return jsonify({'all_comment': comment})


##############################
# go comment
##############################
## go comment Post
@app.route('/go', methods=['POST'])
def go_comment_write():
    comment_receive = request.form['comment_give']
    name_receive = request.form['name_give']

    doc = {
        'comment': comment_receive,
        'name': name_receive
    }
    db.gocomment.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '댓글 작성되었습니다.'})


## go comment Get
@app.route('/go', methods=['GET'])
def go_comment_read():
    comment = list(db.gocomment.find({}, {'_id': False}))
    return jsonify({'all_comment': comment})


##############################
# edit page
##############################

# edit 읽기 요청(Edit)
@app.route('/form_edit', methods=['GET'])
def form_edit():
    try:
        token_receive = request.cookies.get('mytoken')
        jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        return jsonify({'result': 'success'})
    except:
        return jsonify({'result': 'fail', 'msg': '로그인이 필요합니다.'})


# edit 경로 설정
@app.route('/form_edit_read', methods=['GET'])
def form_edit_path():
    return render_template('form_edit.html')


@app.route('/form_edit_read/write', methods=['GET'])
def form_edit_wirte():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload['id']}, {'_id': False})

    return jsonify({'all_user_info': user_info})


@app.route('/form_edit_read/modify', methods=['POST'])
def form_edit_modify():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    introduction_receive = request.form['introduction_give']
    mbti_receive = request.form['mbti_give']
    blog_receive = request.form['blog_give']

    db.users.update_one({'id': id_receive}, {
        '$set': {'name': name_receive, 'introduction': introduction_receive, 'mbti': mbti_receive,
                 'blog': blog_receive}})
    return jsonify({'result': 'success', 'msg': '수정이 완료되었습니다.'})


##############################
# user
##############################
# user 회원가입, 로그인
@app.route('/user', methods=['GET'])
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


# user 회원가입 생성
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
    doc = {
        "id": id_receive,  # 아이디
        "pw": pw_hash,  # 비밀번호
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# user회원가입 시 아이디 중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"id": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})


# user 로그인
@app.route('/sign_in', methods=['POST'])
def sign_in():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': username_receive, 'pw': pw_hash}, {'_id': False})

    if result is not None:
        payload = {
            'id': username_receive,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# # user 사용자 정보 확인 api
# @app.route('/user/info', methods=['POST'])
# def user_valid():
#     token_receive = request.cookies.get('mytoken')
#     try:
#         payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
#         user_info = db.users.find_one({"id": payload["id"]})
#         print(user_info)
#         return jsonify({
#             'result' : {
#                 'success': 'true',
#                 'message': '사용자 정보 성공',
#                 'row_count': 1,
#                 'row': [
#                     {
#                         'user_id': payload["id"],
#                     },
#                 ]
#             }
#         })
#     except jwt.ExpiredSignatureError:
#         return jsonify({
#             'result' : {
#                 'success': 'false',
#                 'message': '사용자 정보 실패 (ExpiredSignatureError)'
#             },
#             'row_count': 0,
#             'row': [{},]
#         })
#     except jwt.exceptions.DecodeError:
#         return jsonify({
#             'result' : {
#                 'success': 'false',
#                 'message': '사용자 정보 실패 (DecodeError)'
#             },
#             'row_count': 0,
#             'row': [{},]
#         })


# # user 사용자 로그인 여부 확인 api
# @app.route('/user/islogin', methods=['POST'])
# def checkcookie():
#     token_receive = request.cookies.get('mytoken')
#     if token_receive is not None:
#         return jsonify({
#             'result' : {
#                     'success': 'true',
#                     'message': '사용자 로그인 되어 있음',
#                     'row_count': 0,
#                     'row': [ {}, ]
#                 }
#             })
#     else :
#         return jsonify({
#             'result' : {
#                     'success': 'false',
#                     'message': '사용자 로그인 되어 있지 않음',
#                     'row_count': 0,
#                     'row': [ {}, ]
#                 }
#             }
#         )


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)