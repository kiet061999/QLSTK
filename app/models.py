from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from app import db, admin
from flask_admin.contrib.sqla import ModelView


class LoaiKyHan(db.Model):
    __tablename__ = "loaikyhan"

    maLoai = Column(Integer, primary_key=True, autoincrement=True)
    tenLoai = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class KhachHang(db.Model):
    __tablename__ = "khachhang"

    maKH = Column(Integer, primary_key=True, autoincrement=True)
    tenKH = Column(String(50), nullable=False)
    cmnd = Column(Integer, nullable=False)
    diaChi = Column(String(50), nullable=True)
    ngaySinh = Column(DateTime, nullable=False)
    gioiTinh = Column(Boolean, nullable=False)
    sDT = Column(Integer, nullable=False)

    def __str__(self):
        return self.name


class LoaiSo(db.Model):
    __tablename__ = "loaiso"

    maLoaiSo = Column(String(50),primary_key=True, nullable=False)
    tenLoaiSo = Column(String(50), nullable=False)


class SoTietKiem(db.Model):
    __tablename__ = "sotietkiem"

    maSo = Column(Integer, primary_key=True, autoincrement=True)
    soDu = Column(Float(50), nullable= False)
    ngayLapSo = Column(DateTime, nullable=False)
    chuThich = Column(String(200), nullable=False)
    maKH = Column(Integer, ForeignKey(KhachHang.maKH), nullable=False)
    maLoaiSo = Column(String(50), ForeignKey(LoaiSo.maLoaiSo), nullable=False)

    def __str__(self):
        return self.name


class STKCoKyHan(db.Model):
    __tablename__ = "stkcokyhan"

    ma = Column(Integer,  ForeignKey(SoTietKiem.maSo), primary_key=True)
    ngayDaoHan = Column(DateTime, nullable=False)
    lKyHan = Column(Integer, ForeignKey(LoaiKyHan.maLoai), nullable=False)


class STKKhongKyHan(db.Model):
    __tablename__ = "stkkhongkyhan"

    ma = Column(Integer, ForeignKey(SoTietKiem.maSo), primary_key=True)


admin.add_view(ModelView(KhachHang, db.session))
admin.add_view(ModelView(SoTietKiem, db.session))
admin.add_view(ModelView(LoaiKyHan, db.session))


if __name__ == "__main__":
    db.create_all()





