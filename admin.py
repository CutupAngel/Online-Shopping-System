from main import app, mysql, MySQLdb, render_template, request, redirect, url_for, session, loggedin, hashlib, os

# http://localhost:5000/pythonlogin/admin/ - admin home page, view all accounts
@app.route('/pythonlogin/admin/', methods=['GET', 'POST'])
def admin():
    # Check if admin is logged-in
    if not admin_loggedin():
        return redirect(url_for('login'))
    msg = ''
    # Retrieve all accounts from the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts')
    accounts = cursor.fetchall()
    return render_template('admin/index.html', accounts=accounts)

# http://localhost:5000/pythonlogin/admin/account - create or edit account
@app.route('/pythonlogin/admin/account/<int:id>', methods=['GET', 'POST'])
@app.route('/pythonlogin/admin/account', methods=['GET', 'POST'], defaults={'id': None})
def admin_account(id):
    # Check if admin is logged-in
    if not admin_loggedin():
        return redirect(url_for('login'))
    page = 'Create'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Default input account values
    account = {
        'username': '',
        'password': '',
        'email': '',
        'activation_code': '',
        'rememberme': '',
        'role': 'Member'
    }
    roles = ['Member', 'Admin'];
    # GET request ID exists, edit account
    if id:
        # Edit an existing account
        page = 'Edit'
        # Retrieve account by ID with the GET request ID
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (id,))
        account = cursor.fetchone()
        if request.method == 'POST' and 'submit' in request.form:
            # update account
            password = account['password']
            if account['password'] != request.form['password']:
                 hash = request.form['password'] + app.secret_key
                 hash = hashlib.sha1(hash.encode())
                 password = hash.hexdigest();
            cursor.execute('UPDATE accounts SET username = %s, password = %s, email = %s, activation_code = %s, rememberme = %s, role = %s WHERE id = %s', (request.form['username'],password,request.form['email'],request.form['activation_code'],request.form['rememberme'],request.form['role'],id,))
            mysql.connection.commit()
            return redirect(url_for('admin'))
        if request.method == 'POST' and 'delete' in request.form:
            # delete account
            cursor.execute('DELETE FROM accounts WHERE id = %s', (id,))
            mysql.connection.commit()
            return redirect(url_for('admin'))
    if request.method == 'POST' and request.form['submit']:
        # Create new account
        hash = request.form['password'] + app.secret_key
        hash = hashlib.sha1(hash.encode())
        password = hash.hexdigest();
        cursor.execute('INSERT INTO accounts (username,password,email,activation_code,rememberme,role) VALUES (%s,%s,%s,%s,%s,%s)', (request.form['username'],password,request.form['email'],request.form['activation_code'],request.form['rememberme'],request.form['role'],))
        mysql.connection.commit()
        return redirect(url_for('admin'))
    return render_template('admin/account.html', account=account, page=page, roles=roles)

# http://localhost:5000/pythonlogin/admin/emailtemplate - admin email template page, edit the existing template
@app.route('/pythonlogin/admin/emailtemplate', methods=['GET', 'POST'])
def admin_emailtemplate():
    # Check if admin is logged-in
    if not admin_loggedin():
        return redirect(url_for('login'))
    # Get the template directory path
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    # Update the template file on save
    if request.method == 'POST':
        content = request.form['content'].replace('\r', '')
        open(template_dir + '/activation-email-template.html', mode='w', encoding='utf-8').write(content)
    # Read the activation email template
    content = open(template_dir + '/activation-email-template.html', mode='r', encoding='utf-8').read()
    return render_template('admin/email-template.html', content=content)
    
# http://localhost:5000/pythonlogin/admin/clientreports -report template page, edit the existing template
@app.route('/pythonlogin/admin/clientreports', methods=['GET', 'POST'])
def client_reports():
    # Check if admin is logged-in
    if not admin_loggedin():
        return redirect(url_for('login'))
    # Get the template directory path
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
  # Update the template file on save
    if request.method == 'POST':
        content = request.form['content'].replace('\r', '')
        open(template_dir + '/clientreports.html', mode='w', encoding='utf-8').write(content)
    # Read the activation email template
    content = open(template_dir + '/clientreports.html', mode='r', encoding='utf-8').read()
    return render_template('admin/clientreports.html', content=content)

# http://localhost:5000/pythonlogin/admin/loginreports -report template page, edit the existing template
@app.route('/pythonlogin/admin/loginreports', methods=['GET', 'POST'])
def login_reports():
    # Check if admin is logged-in
    if not admin_loggedin():
        return redirect(url_for('login'))
    # Get the template directory path
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
  # Update the template file on save
    if request.method == 'POST':
        content = request.form['content'].replace('\r', '')
        open(template_dir + '/loginreports.html', mode='w', encoding='utf-8').write(content)
    # Read the activation email template
    content = open(template_dir + '/loginreports.html', mode='r', encoding='utf-8').read()
    return render_template('admin/loginreports.html', content=content)
    
    
  #  http://localhost:5000/pythonlogin/admin/usagereports -report template page, edit the existing template
@app.route('/pythonlogin/admin/usagereports', methods=['GET', 'POST'])
def usage_reports():
    # Check if admin is logged-in
    if not admin_loggedin():
        return redirect(url_for('login'))
    # Get the template directory path
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
  # Update the template file on save
    if request.method == 'POST':
        content = request.form['content'].replace('\r', '')
        open(template_dir + '/usagereports.html', mode='w', encoding='utf-8').write(content)
    # Read the activation email template
    content = open(template_dir + '/usagereports.html', mode='r', encoding='utf-8').read()
    return render_template('admin/usagereports.html', content=content)


# Admin logged-in check function
def admin_loggedin():
    if loggedin() and session['role'] == 'Admin':
        # admin logged-in
        return True
    # admin not logged-in return false
    return False
