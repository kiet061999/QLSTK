from app import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect
from app.models import *


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def is_visible(self):
        if current_user.user_role == Role.ADMIN:
            return True
        return False


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class SoTietKiemView(AuthenticatedView):
    column_display_pk = True
    can_create = False
    can_delete = False
    can_set_page_size = True
    can_export = True


class STKCoKyHanModelView(AuthenticatedView):
    column_display_pk = True
    column_hide_backref = False
    can_export = True
    can_view_details = True
    can_set_page_size = True


class KhachHangModelView(AuthenticatedView):
    column_display_pk = True
    column_hide_backref = True
    can_export = True
    can_view_details = True
    form_columns = ('tenKH', 'cmnd', 'diaChi', 'ngaySinh', 'gioiTinh', 'sDT')
    can_set_page_size = True


class STKKhongKyHanModelView(AuthenticatedView):
    column_hide_backref = True
    column_display_pk = True
    can_export = True
    can_view_details = True
    can_set_page_size = True


class LoaiSoModelView(AuthenticatedView):
    column_display_pk = True
    column_hide_backref = True
    can_delete = True
    can_create = True
    can_export = True
    can_edit = True
    form_columns = ('tenLoaiSo', 'soThang', 'lai')
    can_set_page_size = True


class PhieuGuiView(AuthenticatedView):
    column_display_pk = True
    column_hide_backref = False


class PhieuRutView(AuthenticatedView):
    column_display_pk = True
    column_hide_backref = False


class UserView(AuthenticatedView):
    column_display_pk = False
    # form_columns = ('name', 'active', 'username', 'user_role')
    column_hide_backref = True
    can_delete = True
    can_create = True
    can_export = False
    can_edit = True
    can_set_page_size = True


class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


admin.add_view(UserView(User, db.session))
admin.add_view(KhachHangModelView(KhachHang, db.session))
admin.add_view(LoaiSoModelView(LoaiSo, db.session))
admin.add_view(SoTietKiemView(SoTietKiem, db.session))
admin.add_view(STKKhongKyHanModelView(SoTietKiemKhongKyHan, db.session))
admin.add_view(STKCoKyHanModelView(SoTietKiemCoKyHan, db.session))
admin.add_view(PhieuGuiView(PhieuGui, db.session))
admin.add_view(PhieuRutView(PhieuRut, db.session))
admin.add_view(LogoutView(name="Logout"))
