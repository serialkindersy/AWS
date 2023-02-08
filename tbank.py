import sys
import os.path
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Float, default=0)
    transactions = db.relationship('Transaction', backref='account', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    amount = db.Column(db.Float)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
with app.app_context():
    db.create_all()


@app.route('/account/<int:account_id>', methods=['POST'])
def add_account():
    account = Account(balance=0)
    db.session.add(account)
    db.session.commit()
    return {'id': account.id}, 201

@app.route('/account/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if account is None:
        return "Account not found", 404
    db.session.delete(account)
    db.session.commit()
    return "Account deleted", 200


@app.route('/account/<int:account_id>/deposit', methods=['POST'])
def deposit(account_id):
    account = Account.query.get(account_id)
    if account is None:
        return "Account not found", 404

    amount = request.form.get('amount')
    if amount is None:
        return "Missing amount", 400

    account.balance += amount
    db.session.commit()
    return "Success", 200
'''@app.route('/account/add', methods=['POST'])
def add_account():
    balance = request.form.get('balance', type=float)
    account = Account(balance=balance)
    db.session.add(account)
    db.session.commit()
    return "Success", 200

@app.route('/account/<int:account_id>/delete', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.get(account_id)
    if account is None:
        return "Account not found", 404
    db.session.delete(account)
    db.session.commit()
    return "Success", 200'''


@app.route('/account/<int:account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
    account = Account.query.get(account_id)
    if account is None:
        return "Account not found", 404

    amount = request.form.get('amount')
    if amount is None:
        return "Missing amount", 400

    if account.balance < amount:
        return "Insufficient funds", 400

    account.balance -= amount
    db.session.commit()
    return "Success", 200

@app.route('/account/<int:account_id>/statement', methods=['GET'])
def statement(account_id):
    account = Account.query.get(account_id)
    if account is None:
        return "Account not found", 404

    transactions = Transaction.query.filter_by(account_id=account_id).all()
    response = []
    for transaction in transactions:
        response.append({
            'date': transaction.date,
            'amount': transaction.amount,
            'balance': transaction.balance,
        })
    return response, 200

if __name__ == '__main__':
    '''with app.app_context():
        db.create_all()'''
    app.run()
