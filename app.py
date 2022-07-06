from flask import Flask,url_for, redirect ,render_template, request,session

app = Flask(__name__)
app.secret_key = '123'

users = {"user1": {"UserName": "Yossi","First Name": "Yossi","Last Name": "Abuksis", "Email": "yossi@gmail.com"},
         "user2": {"UserName": "Salim","First Name": "Salim", "Last Name": "Toama", "Email": "salim@gmail.com"},
         "user3": {"UserName": "Shalom","First Name": "Shalom", "Last Name": "Tikva", "Email": "shalom@gmail.com"},
         "user4": {"UserName": "Vincent","First Name": "Vincent", "Last Name": "Enyeama", "Email": "Vincent@gmail.com"},
         "user5": {"UserName": "Ayelet", "First Name": "Ayelet", "Last Name": "Shaked", "Email": "ayeletsha@gmail.com"}
         }

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

if __name__ == '__main__':
    app.run(debug=True)
