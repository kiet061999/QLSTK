import enum
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Enum
from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class Role(enum.Enum):
    ADMIN = 1
    USER = 2


class Gender(enum.Enum):
    MALE = 0
    FEMALE = 1
    UNKNOWN = -1


class PassbookType(enum.Enum):
    DEMAND = 1
    TERM = 2


class KhachHang(db.Model):
    __tablename__ = "khachhang"

    maKH = Column(Integer, primary_key=True, autoincrement=True)
    cmnd = Column(String(15), primary_key=True)
    tenKH = Column(String(50), nullable=False)
    diaChi = Column(String(50), nullable=True)
    ngaySinh = Column(DateTime, nullable=False)
    gioiTinh = Column(Enum(Gender), default=Gender.UNKNOWN)
    sDT = Column(Integer, nullable=False)

    soTietKiems = relationship('SoTietKiem', backref='khachhang', lazy=True)

    def __str__(self):
        return self.tenKH


class LoaiSo(db.Model):
    __tablename__ = "loaiso"

    maLoaiSo = Column(Integer, primary_key=True, autoincrement=True)
    tenLoaiSo = Column(String(50), nullable=False)
    soThang = Column(Integer, nullable=False)
    lai = Column(Float, nullable=False)

    soTietKiemkkh = relationship('SoTietKiemKhongKyHan', backref='loaiso', lazy=True)
    soTietKiemckh = relationship('SoTietKiemCoKyHan', backref='loaiso', lazy=True)

    def __str__(self):
        return self.tenLoaiSo


class SoTietKiem(db.Model):
    __tablename__ = "sotietkiem"

    maSo = Column(Integer, primary_key=True, autoincrement=True)
    maKH = Column(Integer, ForeignKey(KhachHang.maKH))
    soDu = Column(Float(50), nullable=False)
    ngayLapSo = Column(DateTime, nullable=False)
    chuThich = Column(String(200), nullable=True)
    active = Column(Boolean, default=1)
    # maLoaiSo = Column(Integer, ForeignKey(LoaiSo.maLoaiSo), nullable=False, default=1)
    lai = Column(Float)

    phieuguis = relationship("PhieuGui", backref='sotietkiem', lazy=True)
    phieuruts = relationship("PhieuRut", backref='sotietkiem', lazy=True)

    def __str__(self):
        return str(self.maSo)


class SoTietKiemCoKyHan(SoTietKiem):
    __tablename__ = "stkcokyhan"

    ma = Column(Integer,  ForeignKey(SoTietKiem.maSo), primary_key=True)
    ngayDaoHan = Column(DateTime, nullable=False)
    maLoaiSo = Column(Integer, ForeignKey(LoaiSo.maLoaiSo), nullable=False, default=2)
    loaiSo = Column(Enum(PassbookType), default=PassbookType.TERM)

    def __str__(self):
        return str(self.maSo)


class SoTietKiemKhongKyHan(SoTietKiem):
    __tablename__ = "stkkhongkyhan"

    ma = Column(Integer, ForeignKey(SoTietKiem.maSo), primary_key=True)
    maLoaiSo = Column(Integer, ForeignKey(LoaiSo.maLoaiSo), nullable=False, default=1)
    loaiSo = Column(Enum(PassbookType), default=PassbookType.DEMAND)

    def __str__(self):
        return str(self.maSo)


class PhieuGui(db.Model):
    __tablename__ = "phieugui"

    maPhieuGui = Column(Integer, primary_key=True, autoincrement=True)
    maSo = Column(Integer, ForeignKey(SoTietKiem.maSo), primary_key=True)
    ngayGui = Column(DateTime, default=datetime.now())
    soTienGui = Column(Float)

    def __str__(self):
        return str(self.maPhieuGui)

    # def info(self):
    #     return {
    #             'maPhieuGui': self.maPhieuGui,
    #             'maSo': self.maSo
    #     }


class PhieuRut(db.Model):
    __tablename__ = "phieurut"

    maPhieuRut = Column(Integer, primary_key=True, autoincrement=True)
    maSo = Column(Integer, ForeignKey(SoTietKiem.maSo), primary_key=True)
    ngayRut = Column(DateTime, default=datetime.now())
    soTienRut = Column(Float)

    def __str__(self):
        return self.maPhieuRut

    # def info(self):
    #     return {
    #             'maPhieuRut': self.maPhieuRut,
    #             'maSo': self.maSo
    #     }


# ======================= USER ======================= #
class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    user_role = Column(Enum(Role), default=Role.USER)

    def __str__(self):
        return self.name
# ===================== END_USER ===================== #


if __name__ == "__main__":
    db.create_all()
