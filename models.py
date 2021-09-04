from datetime import datetime
from sqlalchemy import *
from init import db

class User(db.Model):
    id = Column(String(255), primary_key=True, nullable=False)
    email = Column(String(255), default="")
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(255))
    birthday = Column(DateTime, default=datetime.now())
    join_date = Column(DateTime, default=datetime.now())
    introduction = Column(Text, default="")
    address = Column(Text, default="")
    src_facebook = Column(Text, default="")
    src_youtube = Column(Text, default="")
    src_zalo = Column(Text, default="")
    phone_number = Column(String(20), default="")
    is_active = Column(Boolean, default=True)
    is_verify = Column(Boolean, default=False)
    is_indentity_verification = Column(Boolean, default=False)
    img_avatar = Column(Text, default="")
    img_indentity_card_front = Column(Text, default="")
    img_indentity_card_back = Column(Text, default="")
    banned = Column(Integer, default=0)
    banned_count = Column(Integer, default=0)
    role = Column(Integer, default=2)
    money_du = Column(BigInteger, default=0)
    money_da_dung = Column(BigInteger, default=0)
    money_hold = Column(BigInteger, default=0)


class Rating(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255))
    uid_assessor = Column(String(255))
    from_transaction = Column(String(255))
    content = Column(Text, default="")
    star_number = Column(Integer)
    submit_date = Column(DateTime, default=datetime.now())
    src_img = Column(Text)


class PaymentMethod(db.Model):
    __tablename__ = "payment_method"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255))
    type = Column(Integer)
    bank_number = Column(String(20))
    full_name = Column(String(255))
    bank_name = Column(String(255))


class HistoryBank(db.Model):
    __tablename__ = "history_bank"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid_sender = Column(String(255))
    uid_received = Column(String(255))
    type = Column(String(255))
    transaction_id = Column(String(255), default="")
    value = Column(BigInteger)
    value_received = Column(BigInteger)
    transaction_time = Column(DateTime)
    status = Column(Integer, default=0)


class BankRequest(db.Model):
    __tablename__ = "bank_request"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid_sender = Column(String(255))
    type = Column(String(255))
    transaction_id = Column(String(255))
    transaction_code = Column(String(255), default="")
    img_src = Column(Text, default="")
    time_sent = Column(DateTime, default=datetime.now())
    time_accept = Column(DateTime)
    status = Column(Integer, default=0)
    uid_admin = Column(String(255))


class Transaction(db.Model):
    id = Column(String(255), primary_key=True)
    uid_sender = Column(String(255))
    uid_received = Column(String(255))
    date_created = Column(DateTime, default=datetime.now())
    date_expired = Column(DateTime)
    value = Column(BigInteger)
    value_received = Column(BigInteger)
    title = Column(Text)
    description = Column(Text)
    is_accepted = Column(Boolean, default=False)
    status_sender = Column(Integer, default=0)
    starus_received = Column(Integer, default=0)
    is_done = Column(Integer, default=0)


class MessageHistory(db.Model):
    __tablename__ = "message_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_transaction = Column(String(255))
    uid_send = Column(String(255))
    content = Column(Text, default="")
    sent_date = Column(DateTime, default=datetime.now())


class VerifyMail(db.Model):
    __tablename__ = "verify_mail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_verify = Column(Boolean)
    time_accept = Column(DateTime)
    to_email = Column(String(255))
    verify_code = Column(Text)



class Notify(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    n_uid = Column(String(255))
    from_name = Column(Text)
    title = Column(Text)
    content = Column(Text)
    n_time = Column(DateTime, default=datetime.now())
    is_read = Column(Boolean, default=False)


class ReportHistory(db.Model):
    __tablename__ = "report_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String(255))
    title = Column(Text)
    content = Column(Text)
    is_done = Column(Integer, default=0)