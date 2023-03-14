import datetime

from flask import Flask
from flask import render_template, request, redirect, jsonify
from config import app, db
from controllers import User as UserController, ScannedHosts, StatusChanges,IpGroups


@app.route('/')
def hello_world():  # put application's code here
    return redirect("/login")
    # return 'Hello World!'


@app.route('/login')
def render_login():
    return render_template("login.html")


@app.route('/forgot_password')
def render_forget():
    return render_template("forgot-password.html")


@app.route('/otp')
def render_otp():
    return render_template("otp.html")


@app.route('/reset')
def render_reset():
    return render_template("reset-password.html")


@app.route('/change_password')
def render_change_password():
    return render_template("change-password.html")


@app.route('/logout')
def render_logout():
    return render_template("logout.html")


@app.route('/dashboard')
def render_dashboard():
    return render_template("dashboard.html")


@app.route('/hosts')
def render_hosts():
    return render_template("scanned-hosts.html")


@app.route('/logs')
def render_logs():
    return render_template("logs.html")


@app.route('/users')
def render_users():
    return render_template("users.html")


@app.route('/ipgroups')
def render_ipgroups():
    return render_template("ipgroups.html")


@app.route('/report')
def render_report_logs():
    return render_template("report.html")


@app.route('/report-hosts')
def render_report_hosts():
    return render_template("report-hosts.html")


@app.route('/report-logs')
def render_report():
    return render_template("report-logs.html")


# API Endpoints

@app.route("/api/admin/exist", methods=['GET'])
def admin_exist():
    return jsonify(UserController.admin_existence())


@app.route("/api/users", methods=['GET', 'POST'])
def users_management():
    if request.method == 'POST':
        data = UserController.add_user(request.form['names'], request.form['phone'], request.form['email'], request.form['user_type'],
                                       request.form['password'])
    else:
        data = UserController.load_users()
    print(data)

    return jsonify(data)


@app.route("/api/user/remove", methods=['POST'])
def user_remove():
    data = UserController.remove_user(request.form['email'])
    print(data)

    return jsonify(data)


@app.route("/api/dashboard", methods=['GET'])
def dashboard():
    """Load dashboard data  from database"""
    recent_logs = StatusChanges.recent_logs()
    recent_hosts = ScannedHosts.recent_hosts()
    total_hosts = len(ScannedHosts.load_hosts())
    gateways = len(ScannedHosts.gateways())
    active_hosts = len(ScannedHosts.filter("All", "Connected", "2022-03-01", datetime.datetime.now()))
    inactive_hosts = len(ScannedHosts.filter("All", "Disconnected", "2022-03-01", datetime.datetime.now()))
    obj = {"recent_logs": recent_logs, "gateways": gateways, "recent_hosts": recent_hosts, "total_hosts": total_hosts,
           "active_hosts": active_hosts, "inactive_hosts": inactive_hosts}
    data = StatusChanges.recent_logs()
    return jsonify(obj)


@app.route("/api/hosts", methods=['GET', 'POST'])
def hosts():
    """Save single host detected on a network"""
    if request.method == 'POST':
        data = ScannedHosts.save(request.form["hostname"], request.form["ip"])
        print(data)
    else:
        data = ScannedHosts.load_hosts()
    return jsonify(data)


@app.route("/api/hosts/filter", methods=['GET'])
def hosts_filter():
    data = ScannedHosts.filter(request.args["host_id"], request.args["status"], request.args["startdate"],
                               request.args["enddate"])
    return jsonify(data)


@app.route("/api/hosts_array", methods=['POST'])
def hosts_array():
    """Save a list of multiple hosts detected on a network with their ip address"""
    if request.method == 'POST':
        data = request.json
        resp = ScannedHosts.save_array(data["data"])
        print(f"data param {data['data']}")
        print(resp)
    return jsonify(resp)


@app.route("/api/logs", methods=['GET'])
def load_logs():
    return jsonify(StatusChanges.load_logs())


@app.route("/api/logs/filter", methods=['GET'])
def logs_filter():
    data = StatusChanges.filter(request.args["host_id"], request.args["status"], request.args["startdate"],
                                request.args["enddate"])
    return jsonify(data)


@app.route('/api/forgot_password', methods=['POST'])
def forget():
    return jsonify(UserController.forgot_password(request.form['phone']))


@app.route('/api/otp', methods=['POST'])
def verify_otp():
    print(f"User email {request.form['email']} OTP {request.form['otp']}")
    return jsonify(UserController.verify_otp(request.form['email'], request.form['otp']))


@app.route('/api/login', methods=['POST'])
def login():
    return jsonify(UserController.login(request.form['email'], request.form['password']))


@app.route('/api/reset', methods=['POST'])
def reset():
    return jsonify(UserController.reset_password(request.form['id'], request.form['password']))


@app.route("/api/discon", methods=['POST'])
def discon_hosts_array():
    if request.method == 'POST':
        data = request.json
        # data = ScannedHosts.save(request.form["hostname"], request.form["ip"])
        print(f"data param {data['data']}")
        data = ScannedHosts.update_disconnected_hosts(data['data'])
    return jsonify(data)



@app.route("/api/ipgroups", methods=['GET', 'POST'])
def ipgroups_management():
    if request.method == 'POST':
        data = IpGroups.add_ipgroup(request.form['group_name'], request.form['first_ip'], request.form['last_ip'])
    else:
        data = IpGroups.load_ipgroups()
    print(data)

    return jsonify(data)




@app.route("/api/ipgroups/remove", methods=['POST'])
def ipgroup_remove():
    data = IpGroups.remove_ipgroup(request.form['ipgroup'])
    print(data)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port=5000, host="0.0.0.0")
