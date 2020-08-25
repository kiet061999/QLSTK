from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from app import db, admin
from flask_login import UserMixin, current_user, logout_user
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask import redirect


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class LoaiKyHan(db.Model):
    __tablename__ = "loaikyhan"

    maLoai = Column(Integer, primary_key=True, autoincrement=True)
    tenLoai = Column(String(50), nullable=False)

    soCoKyHans = relationship('STKCoKyHan', backref='loaikyhan', lazy=True)

    def __str__(self):
        return self.tenLoai


class KhachHang(db.Model):
    __tablename__ = "khachhang"

    maKH = Column(Integer, primary_key=True, autoincrement=True)
    tenKH = Column(String(50), nullable=False)
    cmnd = Column(Integer, nullable=False)
    diaChi = Column(String(50), nullable=True)
    ngaySinh = Column(DateTime, nullable=False)
    gioiTinh = Column(Boolean, nullable=False)
    sDT = Column(Integer, nullable=False)

    soTietKiems = relationship('SoTietKiem', backref='khachhang', lazy=True)

    def __str__(self):
        return self.tenKH


class LoaiSo(db.Model):
    __tablename__ = "loaiso"

    maLoaiSo = Column(String(50), primary_key=True, nullable=False)
    tenLoaiSo = Column(String(50), nullable=False)

    soTietKiems = relationship('SoTietKiem', backref='loaiso', lazy=True)

    def __str__(self):
        return self.tenLoaiSo


class SoTietKiem(db.Model):
    __tablename__ = "sotietkiem"

    maSo = Column(Integer, primary_key=True, autoincrement=True)
    soDu = Column(Float(50), nullable= False)
    ngayLapSo = Column(DateTime, nullable=False)
    chuThich = Column(String(200), nullable=True)
    maKH = Column(Integer, ForeignKey(KhachHang.maKH), nullable=False)
    maLoaiSo = Column(String(50), ForeignKey(LoaiSo.maLoaiSo), nullable=False)

    def __str__(self):
        return str(self.maSo)


class STKCoKyHan(db.Model):
    __tablename__ = "stkcokyhan"

    ma = Column(Integer,  ForeignKey(SoTietKiem.maSo), primary_key=True)
    ngayDaoHan = Column(DateTime, nullable=False)
    lKyHan = Column(Integer, ForeignKey(LoaiKyHan.maLoai), nullable=False)

    def __str__(self):
        return str(self.ma)


class STKKhongKyHan(db.Model):
    __tablename__ = "stkkhongkyhan"

    ma = Column(Integer, ForeignKey(SoTietKiem.maSo), primary_key=True)

    def __str__(self):
        return str(self.ma)


class LoaiKyHanModelView(AuthenticatedView):
    column_display_pk = True


class KhachHangModelView(AuthenticatedView):
    column_display_pk = True
    column_hide_backref = True
    can_export = True
    form_columns = ('tenKH', 'cmnd', 'diaChi', 'ngaySinh', 'gioiTinh', 'sDT')


class SoTietKiemModelView(AuthenticatedView):
    column_hide_backrefs = False
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True


class LoaiSoModelView(AuthenticatedView):
    column_display_pk = True
    can_delete = False
    can_create = False
    can_export = False
    can_edit = False


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')


# ======================= USER ======================= #
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


admin.add_view(KhachHangModelView(KhachHang, db.session))
admin.add_view(LoaiSoModelView(LoaiSo, db.session))
admin.add_view(SoTietKiemModelView(SoTietKiem, db.session))
admin.add_view(LoaiKyHanModelView(LoaiKyHan, db.session))
admin.add_view(LogoutView(name="Logout"))
# admin.add_view(ModelView(STKCoKyHan, db.session))
# admin.add_view(ModelView(STKKhongKyHan, db.session))

if __name__ == "__main__":
    db.create_all()