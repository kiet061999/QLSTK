from app import app, login, db
import hashlib
from flask_login import login_user
from flask_admin import Admin
from app.models import *


def validate_user(username, password):
    user = User.query.filter(User.username == username,
                             User.password == password).first()
    return user


def load(user_id):
    return User.query.get(user_id)


def load_type_book():
    return LoaiSo.query.all()


def load_customer_list():
    return KhachHang.query.all()


def find_customer(kw_cmnd=None, kw_makh=None):
    cus = KhachHang.query
    if kw_cmnd:
        cus = cus.filter(KhachHang.cmnd.contains(kw_cmnd))

    if kw_makh:
        cus = cus.filter(KhachHang.maKH.contains(kw_makh))
    return cus.all()


def get_customer(id=None):
    if id:
        cus = KhachHang.query.filter(KhachHang.maKH.contains(id)).first()
    return cus


def find_passbook_by_id(kw_maso=None):
    passb = SoTietKiem.query
    if kw_maso:
        passb = passb.filter(SoTietKiem.maSo.contains(kw_maso)).first()
    return passb


def add_customer(name, idcard, addr, birthday, gender, phonenum):
    try:
        # customer = KhachHang(tenKH=name, cmnd=idcard, diaChi=addr, ngaySinh=birthday, gioiTinh=gender, sDT=phonenum)
        customer = KhachHang()
        customer.tenKH = name
        customer.cmnd = idcard
        customer.diaChi = addr
        customer.ngaySinh = birthday
        customer.gioiTinh = gender
        customer.sDT = phonenum

        db.session.add(customer)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
        return False


def edit_customer(customer_id, name, id_card, address, birthday, gender, phone):
    customer = KhachHang.query.filter_by(maKH=customer_id).first()
    if customer:
        customer.tenKH = name
        customer.cmnd = id_card
        customer.diaChi = address
        customer.ngaySinh = birthday
        customer.gioiTinh = gender
        customer.sDT = phone

        # db.session.add(customer)
        db.session.commit()
        return customer
    else:
        return None


def load_passbook_list():
    pk = SoTietKiemKhongKyHan.query.all()
    pc = SoTietKiemCoKyHan.query.all()
    # return SoTietKiem.query.all()
    return pk+pc
