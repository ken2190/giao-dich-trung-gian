from datetime import datetime, timedelta
from flask import request, jsonify, make_response
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from init import app, db
from extended_function import *



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')

        if not token:
            return jsonify(response_base(401, "Không tìm thấy token!", {})), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter(User.id == data['id']).first()
        except:
            return jsonify(response_base(401, "Token lỗi!", {})), 401

        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/user/<username>', methods=['GET'])
def get_one_user(username):
    user_query = User.query.filter(User.username == username).first()

    if not user_query:
        return jsonify(response_base(0, "Không tìm thấy tài khoản %s!!!" % username, {})), 0
    else:
        data = {
            "email": user_query.email,
            "username":user_query.username,
            "id": user_query.id,
            "full_name":user_query.full_name,
            "birthday":user_query.birthday.strftime("%m/%d/%Y"),
            "join_date":user_query.join_date.strftime("%m/%d/%Y"),
            "introduction":user_query.introduction,
            "address":user_query.address,
            "src_facebook":user_query.src_facebook,
            "src_youtube":user_query.src_youtube,
            "zalo_number":user_query.src_zalo,
            "phone_number":user_query.phone_number,
            "is_verify_card":user_query.is_indentity_verification,
            "img_avatar":user_query.img_avatar,
            "role":user_query.role
        }
        rates = Rating.query.filter(Rating.uid == user_query.id)
        data_rates = []
        star_number = 0
        for rate in rates:
            data_rate = {
                "transition":rate.from_transaction,
                "by_user_id":rate.uid_assessor,
                "content":rate.content,
                "submit_time":rate.submit_date.strftime("%m/%d/%Y"),
                "star_number":rate.star_number,
                "src_img":rate.src_img
            }
            star_number += rate.star_number
            data_rates.append(data_rate)
        if len(data_rates) != 0:
            star_number = star_number/len(data_rates)

        response_data = {
            "users":data,
            "star_number":star_number,
            "rating":data_rates
        }
        return jsonify(response_base(200, "Lấy dữ liệu thành công!", response_data)), 200


@app.route('/user', methods=['POST'])
def create_user():
    data = get_request(request.get_json())

    data['username'] = remove_accents(data['username'])

    user = User.query.filter(User.username==data['username'] or User.email == data['email']).first()
    if user:
        return jsonify(response_base(0, "Username hoặc email đã được sử dụng, vui lòng thử lại!", {})), 0

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User()
    new_user.id = random_str(20)
    new_user.username = data['username']
    new_user.password = hashed_password
    new_user.email = data['email']
    new_user.full_name = data['full_name']
    new_user.is_verify = False
    new_user.is_active = True

    # otp = random_str(size=80)
    # v = VerifyMail()
    # v.is_verify = False
    # v.verify_code = otp
    # v.to_email = data['email']

    # if send_mail_to_verify(data['email'], data['full_name'], otp, request.host.title().lower()) == True:
    #     db.session.add(new_user)
    #     db.session.add(v)
    #     db.session.commit()
    #     return jsonify(response_base(200, "Vui lòng xác minh email trước khi đăng nhập!", {})), 200
    # else:
    #     return jsonify(response_base(0, "Lỗi hệ thống, không thể gửi email xác minh. Vui lòng thử lại!", {})), 0

    new_user.is_verify = True
    db.session.add(new_user)
    db.session.commit()
    return jsonify(response_base(200, "Đăng ký tài khoản thành công!", {}))


@app.route('/user/me', methods=['GET'])
@token_required
def get_my_profile(current_user):
    data = {
        "email": current_user.email,
        "username":current_user.username,
        "id": current_user.id,
        "full_name":current_user.full_name,
        "birthday":current_user.birthday.strftime("%m/%d/%Y"),
        "join_date":current_user.join_date.strftime("%m/%d/%Y"),
        "introduction":current_user.introduction,
        "address":current_user.address,
        "src_facebook":current_user.src_facebook,
        "src_youtube":current_user.src_youtube,
        "zalo_number":current_user.src_zalo,
        "phone_number":current_user.phone_number,
        "is_verify_card":current_user.is_indentity_verification,
        "img_avatar":current_user.img_avatar,
        "role":current_user.role
    }
    return jsonify(response_base(200, "Lấy dữ liệu thành Công!", {"users": data})), 200


@app.route('/user/me', methods=['POST'])
@token_required
def promote_user(current_user):
    data = get_request(request.get_json())
    type = request.args.get('change')
    if type == "avatar":
        files = data['files']

        if len(files) == 0:
            return jsonify(response_base(0, "Data trống!", {})), 0

        url_image = upload_image(files)
        if len(url_image) > 0:
            current_user.img_avatar = url_image
            db.session.commit()
            return jsonify(response_base(200, "Upload avatar thành công!", {"img_src": url_image})), 200
        else:
            return jsonify(response_base(0, "Không thể upload, vui lòng thử lại!", {})), 0
    elif type == "password":
        password_old = data['password_old']
        password_new = data['password_new']
        if len(password_old) == 0 or len(password_new) == 0:
            return jsonify(0, "Data trống!", {}), 0
        if check_password_hash(current_user.password, password_old):
            current_user.password = generate_password_hash(password_new)
            db.session.commit()
            return jsonify(response_base(200, "Đổi mật khẩu thành công!", {})), 200
        else:
            return jsonify(response_base(0, "Mật khẩu không chính xác!", {})), 0

    elif type == "information":
        try:
            full_name = data['full_name']
            birthday = data['birthday']
            phone = data['phone']
            address = data['address']
            introduce = data['introduce']

            current_user.full_name = full_name
            current_user.birthday = datetime.strptime(birthday, "%d/%m/%Y")
            current_user.phone_number = phone
            current_user.address = address
            current_user.introduction = introduce

            db.session.commit()
            return jsonify(response_base(200, "Update thành công!", {})), 200
        except:
            return jsonify(response_base(0, "Không thành công, vui lòng thử lại!", {})), 0



@app.route('/verify', methods=['GET'])
def verify_mail():
    code = request.args.get('code')
    k = VerifyMail.query.filter(VerifyMail.verify_code == code).first()
    if k:
        if k.is_verify == True:
            return jsonify(response_base(0, "Tài khoản đã được xác minh!", {})), 0
        else:
            u = User.query.filter(User.email == k.to_email).first()
            if u:
                u.is_verify = True
                k.is_verify = True
                db.session.commit()
                return jsonify(response_base(200, "Xác minh email thành công!", {})), 200
    else:
        return jsonify(response_base(0, "Mã xác minh sai, vui lòng thử lại!", {})), 0


@app.route('/login', methods=["POST"])
def login():
    data = get_request(request.get_json())
    username = data['username']
    password = data['password']
    user = User.query.filter(User.username == username).first()
    if not user:
        user = User.query.filter(User.email == username).first()

    # print(user)
    if user:
        if check_password_hash(user.password, password):
            if user.is_verify:
                token = jwt.encode({"id":user.id, "exp":datetime.utcnow() + timedelta(hours=24)}, app.config['SECRET_KEY'])
                # print(token)
                return jsonify(response_base(200, "Đăng nhập thành công!", {"token": token.decode('UTF-8')})), 200
            else:
                return jsonify(response_base(0, "Vui lòng xác minh email trước khi đăng nhập!", {})), 0

    return jsonify(response_base(0, "Tài khoản hoặc mật khẩu không chính xác!", {})), 0


@app.route('/search', methods=['GET'])
@token_required
def search_user(current_user):
    try:
        if "query" in request.args:
            content = request.args.get('query', '')
            user_list_username = User.query.filter(User.username.contains(content)).all()
            user_list_fullname = User.query.filter(User.full_name.contains(content)).all()

            data_username = []
            data_fullname = []

            for user in user_list_username:
                data = {
                    "email": user.email,
                    "id": user.id,
                    "username":user.username,
                    "full_name":user.full_name,
                    "birthday":user.birthday.strftime("%m/%d/%Y"),
                    "join_date":user.join_date.strftime("%m/%d/%Y"),
                    "introduction":user.introduction,
                    "address":user.address,
                    "src_facebook":user.src_facebook,
                    "src_youtube":user.src_youtube,
                    "zalo_number":user.src_zalo,
                    "phone_number":user.phone_number,
                    "is_verify_card":user.is_indentity_verification,
                    "img_avatar":user.img_avatar,
                    "role":user.role
                }
                data_username.append(data)

            for user in user_list_fullname:
                data = {
                    "email": user.email,
                    "id":user.id,
                    "username": user.username,
                    "full_name": user.full_name,
                    "birthday": user.birthday.strftime("%m/%d/%Y"),
                    "join_date": user.join_date.strftime("%m/%d/%Y"),
                    "introduction": user.introduction,
                    "address": user.address,
                    "src_facebook": user.src_facebook,
                    "src_youtube": user.src_youtube,
                    "zalo_number": user.src_zalo,
                    "phone_number": user.phone_number,
                    "is_verify_card": user.is_indentity_verification,
                    "img_avatar": user.img_avatar,
                    "role": user.role
                }
                data_fullname.append(data)

            return jsonify(response_base(200, "Lấy dữ liệu thành công!", {"username": data_username, "full_name": data_fullname}))
        else:
            return jsonify(response_base(0, "Không thể lấy dữ liệu!", {}))
    except:
        return jsonify(response_base(0, "Không thể lấy dữ liệu!", {}))


@app.route('/home', methods=['GET'])
@token_required
def home_page(current_user):
    # get last ip login
    last_ip_login = request.remote_addr

    # get Transction
    data_tranactions = Transaction.query.filter(Transaction.uid_sender == current_user.id or Transaction.uid_received == current_user.id).all()
    number_transaction = len(data_tranactions)
    sucess_number = 0
    failed_number = 0
    for transaction in data_tranactions:
        if transaction.is_done == 2:
            sucess_number += 1
        elif transaction.is_done == 3:
            failed_number += 1

    trans_data_response = {
        "number_transaction":number_transaction,
        "success":sucess_number,
        "failed":failed_number,
        "pending":number_transaction - sucess_number - failed_number
    }

    # get Notify
    data_notices = Notify.query.filter(Notify.n_uid == current_user.id).all()
    noti_data_response = []
    for noti in data_notices:
        noti_data_response.append({
            "id":noti.id,
            "from":noti.from_name,
            "title":noti.title,
            "content":noti.content,
            "time":noti.n_time.strftime("%m/%d/%Y"),
            "mark_read":noti.is_read
        })

    # get Top 10
    # data_trans_week = Transaction.query.filter(Transaction.date_confirm <= datetime.utcnow() and Transaction.date_confirm >= datetime.utcnow() - timedelta(days=7)).all()
    # user_trans_in_week = []
    # for tran in data_trans_week:
    #     user_trans_in_week.append(tran.uid_sender)
    #     user_trans_in_week.append(tran.uid_received)
    # user_trans_in_week = list(set(user_trans_in_week))
    # for user in user_trans_in_week:
    #     data = {
    #         "user_id":user,
    #         "full_name":
    #         "coin":0
    #     }
    top_10_week_response = []


    return jsonify(response_base(200, "Lấy dữ liệu thành công!", {"last_ip_login":last_ip_login, "notify":noti_data_response, "transation_data":trans_data_response, "top10":top_10_week_response}))


@app.route('/transaction/all', methods=["GET"])
@token_required
def list_transation(current_user):
    if current_user.role == 0:
        all_transaction = Transaction.query.filter().all()
    else:
        all_transaction = Transaction.query.filter(Transaction.uid_sender == current_user.id or Transaction.uid_received == current_user.id).all()
    transation_response = []
    for tran in all_transaction:
        data = {
            "title":tran.title,
            "time_created":tran.date_created,
            "time_expired":tran.date_expired,
            "status":tran.is_done
        }
        transation_response.append(data)

    return jsonify(response_base(200, "Lấy dữ liệu thành công!", transation_response))



@app.route("/transaction/gerenal", methods=["GET"])
@token_required
def transaction_gerenal(current_user):
    # get params id noti để set noti read = true
    pass


@app.route('/transaction/create', methods=["POST"])
@token_required
def transaction_create(current_user):
    data = get_request(request.get_json())
    trans_created = Transaction()
    trans_created.id = random_str(12)
    data['title'] = remove_accents(data['title'])
    data['description'] = remove_accents(data['description'])
    if current_user.id == data['uid_sender']:
        if current_user.money_du < data['value']:
            return jsonify(response_base(0, "Số dư không đủ!", {}))
        user_received = User.query.filter(User.id == data['uid_received'])

        trans_created.uid_sender = data['uid_sender']
        trans_created.uid_received = data['uid_received']
        trans_created.date_created = datetime.utcnow()
        trans_created.date_expired = datetime.strptime(data['time_experied'], "%d/%m/%Y")
        trans_created.value = data['value']
        trans_created.value_received = data['value'] * 1
        trans_created.title = data['title']
        trans_created.description = data['description']

        noti = Notify()
        noti.n_uid = data['uid_received']
        noti.from_name = current_user.full_name
        noti.title = data['title']
        noti.content = "Ban co 1 giao dich moi voi tai khoan %s dang cho xac nhan" % current_user.full_name
        noti.n_time = datetime.utcnow()

        db.session.add(noti)
        db.session.add(trans_created)
        db.session.commit()
        return jsonify(response_base(200, "Gửi yêu cầu giao dịch thành công!", {}))
    else:
        user_sender = User.query.filter(User.id == data['uid_sender']).first()
        if user_sender.money_du < data['value']:
            return jsonify(response_base(0, "Số dư không đủ!", {}))

        trans_created.uid_sender = data['uid_sender']
        trans_created.uid_received = data['uid_received']
        trans_created.date_created = datetime.utcnow()
        trans_created.date_expired = datetime.strptime(data['time_experied'], "%d/%m/%Y")
        trans_created.value = data['value']
        trans_created.value_received = data['value'] * 1
        trans_created.title = data['title']
        trans_created.description = data['description']

        noti = Notify()
        noti.n_uid = user_sender.full_name
        noti.from_name = current_user.full_name
        noti.title = data['title']
        noti.content = "Ban co 1 giao dich moi voi tai khoan %s dang cho xac nhan" % current_user.full_name
        noti.n_time = datetime.utcnow()

        db.session.add(noti)
        db.session.add(trans_created)
        db.session.commit()
        return jsonify(response_base(200, "Gửi yêu cầu giao dịch thành công!", {}))


@app.route('/transaction/accept', methods=["POST"])
@token_required
def transaction_accept(current_user):
    data = get_request(request.get_json())

    return ''


if __name__ == "__main__":
    app.run(debug=True)