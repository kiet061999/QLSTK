from app import app, login, dao, models
from flask_login import login_user, logout_user, login_required
from flask import render_template, request, redirect, url_for, jsonify
from flask_paginate import Pagination, get_page_args
from app.models import *
from app.admin import *
import json
import hashlib


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def user_login():
    return render_template("login/login.html")


@login.user_loader
def user_load(user_id):
    return dao.load(user_id)


@app.route("/login", methods=['get', 'post'])
def login():
    errmsg = ""
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = dao.validate_user(username.strip(), password)
        if user and user.user_role == Role.ADMIN:
            login_user(user=user)
            return redirect("/admin")
        else:
            if user and user.user_role == Role.USER:
                login_user(user=user)
                return redirect("/")
            else:
                errmsg = "Username or password is incorrect!"
                return render_template("login/login.html", errmsg=errmsg)

    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/add-customer")
@login_required
def load_customer_add():
    return render_template("customer/add-customer.html")


@app.route("/edit-customer", methods=["get", "post"])
@login_required
def customer_edit():
    errmsg = ""
    customer_id = request.args.get("customer_id")
    customer = None

    if customer_id:
        customer = dao.get_customer(customer_id)

    if request.method == 'post':
        name = request.form('name')
        idcard = request.form('idcard')
        addr = request.form('addr')
        birthday = request.form('birthday')
        gender = request.form('gender')
        phone_num = request.form('phone_num')

        if customer_id:
            if dao.edit_customer(customer_id=customer_id,
                                 name=name,
                                 id_card=idcard,
                                 address=addr,
                                 birthday=birthday,
                                 gender=gender,
                                 phone=phone_num):
                return redirect(url_for('customer_list'))
        else:
            errmsg = "Something Wrong!"

    return render_template("customer/edit-customer.html",
                           customer=customer,
                           errmsg=errmsg)


@app.route("/customer-list")
@login_required
def customer_list():
    list_cus = dao.load_customer_list()

    list_total = len(list_cus)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination_customers = list_cus[offset: offset + per_page]
    pagination = Pagination(page=page,
                            per_page=per_page,
                            total=list_total,
                            css_framework='bootstrap4')
    return render_template("customer/list-customer.html",
                           customers=pagination_customers,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@app.route("/search-customer")
@login_required
def search_customer():
    errmsg = ""
    cmnd = request.args.get("search_customer_by_id_card")
    maKH = request.args.get("search_customer_by_id")
    customer = dao.find_customer(kw_cmnd=str(cmnd).strip(), kw_makh=str(maKH).strip())
    if customer is None:
        errmsg = "Customer's not found!"
    return render_template("customer/search-customer.html", customer=customer, errmsg=errmsg)


@app.route("/add-customer", methods=['get', 'post'])
@login_required
def add_customer_main():
    try:
        name = request.form('name')
        idcard = request.form('idcard')
        addr = request.form('addr')
        birthday = request.form('birthday')
        gender = request.form('gender')
        phone_num = request.form('phone_num')

        # data = json.loads(request.data)
        # name = data.get('name')
        # idcard = data.get('idcard')
        # addr = data.get('addr')
        # birthday = data.get('birthday')
        # gender = data.get('gender')
        # phone_num = data.get('phone_num')

        dao.add_customer(name, idcard, addr, birthday, gender, phone_num)
        return jsonify({"status": 200, "message": "Successful"})
    except Exception as ex:
        return jsonify({"status": 500, "error": ex})


@app.route("/passbook-list")
@login_required
def passbook_list():
    list_passb = dao.load_passbook_list()

    list_total = len(list_passb)
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    pagination_passbooks = list_passb[offset: offset + per_page]
    pagination = Pagination(page=page,
                            per_page=per_page,
                            total=list_total,
                            css_framework='bootstrap4')
    return render_template("passbook/list-passbook.html",
                           passbooks=pagination_passbooks,
                           page=page,
                           per_page=per_page,
                           pagination=pagination)


@app.route("/search-passbook")
@login_required
def search_passbook():
    ma_so = request.args.get("search_passbook")
    passbook = dao.find_passbook_by_id(str(ma_so))
    return render_template("passbook/search-passbook.html", passbook=passbook)


@app.route("/about-us")
def about_us():
    return render_template("contact.html")


@app.context_processor
def common_data():
    return {
        'gender': Gender,
        'role': Role,
        'passbook_type': PassbookType,
        'type': dao.load_type_book()
    }


if __name__ == "__main__":
    app.run(debug=True)
