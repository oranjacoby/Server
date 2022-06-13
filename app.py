from flask import Flask,url_for, redirect ,render_template

app = Flask(__name__)

@app.route('/home')
@app.route('/')
def main():
    return return render_template('Home Page.html')

@app.route('/Contact')
def exercise2():
    return render_template('Contact.html')

@app.route('/Home Page')
def forms():
    return render_template('Home Page.html')

@app.route('/assignment3')
def assignment3():
    hapoel = ("Yossi Abuksis", "Salim Toama", "Shalom Tikva", "Vincent Enyeama")
    return render_template('assignment3.html', hapoel = hapoel)

if __name__ == '__main__':
    app.run()
