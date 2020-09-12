from app import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import current_user, logout_user
from flask import redirect
from app.models import *


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class STKCoKyHanModelView(AuthenticatedView):
    column_display_pk = True
    column_hide_backref = True
    can_view_details = True
    can_set_page_size = True


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


admin.add_view(KhachHangModelView(KhachHang, db.session))
admin.add_view(LoaiSoModelView(LoaiSo, db.session))
admin.add_view(SoTietKiemModelView(SoTietKiem, db.session))
admin.add_view(LoaiKyHanModelView(LoaiKyHan, db.session))
admin.add_view(STKCoKyHanModelView(STKCoKyHan, db.session))
admin.add_view(LogoutView(name="Logout"))