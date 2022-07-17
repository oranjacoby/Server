import random

import mysql.connector, requests
from flask import Flask, url_for, redirect, render_template, request, session, Blueprint, flash, jsonify

app = Flask(__name__)
app.secret_key = '123'

users = {"user1": {"UserName": "Yossi","First Name": "Yossi","Last Name": "Abuksis", "Email": "yossi@gmail.com"},
         "user2": {"UserName": "Salim","First Name": "Salim", "Last Name": "Toama", "Email": "salim@gmail.com"},
         "user3": {"UserName": "Shalom","First Name": "Shalom", "Last Name": "Tikva", "Email": "shalom@gmail.com"},
         "user4": {"UserName": "Vincent","First Name": "Vincent", "Last Name": "Enyeama", "Email": "Vincent@gmail.com"},
         "user5": {"UserName": "Ayelet", "First Name": "Ayelet", "Last Name": "Shaked", "Email": "ayeletsha@gmail.com"}
         }

assignment_4 = Blueprint(
    'assignment_4',
    __name__,
    static_folder='static',
    static_url_path='/assignment4',
    template_folder='templates'
)


##################### Arseni's function ##################################
def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         password='oran1994',
                                         database='usersdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        connection.commit()
        return_value = True
    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


@app.route('/assignment_4')
def users():
    usersTable = interact_db(query="select * from usersdb.users", query_type='fetch')
    if session.get('messages'):
        x = session['messages']
        session.pop('messages')
        return render_template('assignment4.html', users=usersTable, messages = x)
    else:
        return render_template('assignment4.html', users=usersTable)



@app.route('/insertUser', methods=['GET','POST'])
def insertUsers():
    if request.method == 'POST':
        userName = request.form['firstName']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        check_input = "SELECT userName FROM usersdb.users WHERE userName='%s';" % userName
        answer = interact_db(query=check_input, query_type='fetch')
        if len(answer) == 0:
            query = "insert into usersdb.users(userName, firstName ,lastName, email)\
                            value ('%s', '%s', '%s','%s');" % (userName,firstName ,lastName, email)
            interact_db(query=query, query_type='commit')
            flash('user added!!! ')
            return redirect('/assignment_4')
        else:
            flash('the user name is taken, please try another name')
            return redirect('/assignment_4')
    return render_template('assignment4.html', req_method=request.method)



@app.route('/deleteUser', methods=['POST'])
def deleteUsers():
    userName = request.form['userName']
    check = "SELECT userName FROM usersdb.users WHERE userName='%s';" % userName
    answer = interact_db(query=check, query_type='fetch')
    if len(answer) > 0:
        query = "delete from usersdb.users where userName='%s';" % userName
        interact_db(query=query, query_type='commit')
        flash('user deleted ')
        return redirect('/assignment_4')
    else:
        flash('the user you are trying to delete does not exist')
        return redirect('/assignment_4')


@app.route('/updateUser', methods=['GET','POST'])
def updateUsers():
        username = request.form['userName']
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        email = request.form['email']
        query = " UPDATE usersdb.users SET firstName='%s' ,lastName='%s', email='%s' WHERE userName='%s';"%\
                (firstname, lastname, email,username)
        interact_db(query=query, query_type='commit')
        return redirect('/assignment_4')




@app.route('/home')
@app.route('/')
def main():
    return render_template('Home Page.html')

@app.route('/Contact')
def contact():
    return render_template('Contact.html')

@app.route('/Home Page')
def home():
    return render_template('Home Page.html')

@app.route('/assignment3_1')
def assignment3_1():
    hapoel = ("Yossi Abuksis", "Salim Toama", "Shalom Tikva", "Vincent Enyeama")
    return render_template('assignment3_1.html', hapoel=hapoel)

@app.route('/Contact Me')
def Contact_Me():
    return redirect('/Contact')

@app.route('/Hapoel')
def hapoel():
    return redirect(url_for('home'))

@app.route('/assignment3_2' , methods = ['GET','POST'])
def assignment3_2():
    current_method = request.method
    if current_method == 'GET':
        if 'user_name' in request.args:
            user_name = request.args['user_name']
            if user_name is '':
                return render_template('assignment3_2.html', search=True, users=users, find=True)
            user_dic = {}
            for user in users.values():
                if user['UserName'] == user_name:
                    user_dic[1] = user
            if len(user_dic) != 0:
                return render_template('assignment3_2.html', search=True, find=True, users=user_dic)
            else:
                return render_template('assignment3_2.html', find=False, search=True)
        return render_template('assignment3_2.html')
    elif current_method == 'POST':
        session['login'] = True
        users[request.form['email']] = {'First Name': request.form['firstName'],
                                            'Last Name': request.form['lastName'],
                                            'Email': request.form['email'],
                                            'User Name': request.form['userName']}
        session['userName'] = request.form['userName']
        return render_template('assignment3_2.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['login'] = False
    return render_template('Home Page.html')

@app.route('/assignment4/users', methods=['GET', 'POST'])
def assignment4_return():

    usersTable = interact_db(query="select * from usersDB.users", query_type='fetch')
    ans = {}
    i = 0
    print(9999999)

    for user in usersTable:
        i += 1
        user = {
            'user': user.userName,
            'first name': user.firstName,
            'last name': user.lastName,
            'email': user.email,
        }
        ans[f'user{i}'] = user
    return jsonify(ans)


@app.route('/assignment4/outer_source', methods=['GET', 'POST'])
def outer_source():
    if "id" in request.args:
        if request.args['id'] == '':
            return render_template('PartB.html', user = -1)
        id = int(request.args['id'])
        res = requests.get(f'https://reqres.in/api/users/{id}')
        user = res.json()
        return render_template('PartB.html', user= user)
    else:
        return render_template('PartB.html', user=-1)

@app.route('/assignment4/restapi_users', defaults={'user_id': -1})
@app.route('/assignment4/restapi_users/<int:user_id>')
def get_user_func(user_id):
    ret = {}
    query = f'select * from users where id= {user_id}'
    userss = interact_db(query, query_type='fetch')
    if len(userss) == 0:
        ret = {
            'status': 'failed',
            'message': 'no user'
        }
    else:
        for user in userss:
            ret[f'user_{user.id}'] = {
                'status': 'succeed',
                'First Name': user.firstName,
                'User Name': user.userName,
                'Last Name': user.lastName,
                'Email': user.email,
            }
    return jsonify(ret)

if __name__ == '__main__':
    app.run(debug=True)


