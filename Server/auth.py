from flask import Blueprint
auth = Blueprint('auth', __name__)

@auth.route('/logout')
def logout():
    return "<p>Logout</p"