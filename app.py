from flask import Flask, render_template,request,redirect,session,flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key=os.urandom(24)

conn = mysql.connector.connect(host="localhost",user="root",password = "",database="election")
cursor=conn.cursor()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin_login')
def admin_login():
    if ('admin_id' in session):
        return redirect('admin_dashboard')
    else :
        return render_template('admin_login.html')

@app.route('/alogin_validation' ,methods=['POST'])
def alogin_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    try:
        cursor.execute("SELECT * FROM admin WHERE admin_email ='{}' and admin_password ='{}'".format(email,password))
        admins = cursor.fetchall()
        if len(admins) > 0:
            session['admin_id']=admins[0][0]
            return redirect('/admin_dashboard')
        else :
            flash("Incorrect email or password !!")
            return  redirect('/admin_login')
    except mysql.connector.Error as err:
        print(err)
        return redirect('/admin_login')

@app.route('/admin_dashboard')
def admin_dashboard():
    if ('admin_id' in session):
        return render_template('admin_dashboard.html')
    else:
        return redirect('/admin_login')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_id')
    return redirect('/')




@app.route('/voter_login')
def voter_login():
    if ('voter_id' in session):
        return redirect('voter_dashboard')
    else :
        return render_template('voter_login.html')

@app.route('/voter_register')
def voter_register():
    if ('voter_id' in session):
        return redirect('/voter_dashboard')
    else :
        return render_template('voter_reg.html')


@app.route('/voter_dashboard')
def voter_dashboard():
    if ('voter_id' in session):
        return render_template('voter_dashboard.html')
    else:
        return redirect('/voter_login')

@app.route('/vlogin_validation', methods=['POST'])
def vlogin_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    try :
        cursor.execute("SELECT * FROM voter WHERE voter_email ='{}' AND voter_pwd='{}'".format(email,password))
        voters=cursor.fetchall()
        if len(voters) > 0:
            session['voter_id']=voters[0][0]
            return redirect('/voter_dashboard')
        else :
            return redirect('/voter_login')
    except mysql.connector.Error as err:
        print(err)
        return redirect('/voter_login')

@app.route('/add_voter',methods=['POST'])
def add_voter():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    gender = request.form.get('gender')
    branch = request.form.get('branch')
    current_year = request.form.get('cyear')
    password = request.form.get('password')

    query = "INSERT INTO voter (voter_fname,voter_lname,voter_email,voter_gender,voter_branch,\
          voter_cuyear,voter_pwd) VALUES(%s, %s, %s, %s, %s, %s, %s)"

    try:
        params = (fname,lname,email,gender,branch,current_year,password)
        cursor.execute(query, params)
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
        return redirect('/voter_register')
    finally:
        cursor.execute("SELECT * FROM voter WHERE voter_email LIKE '{}'".format(email))
        add_voter = cursor.fetchall()
        print(add_voter)
        session['voter_id'] = add_voter[0][0]
        return redirect('/voter_dashboard')

@app.route('/voter_logout')
def voter_logout():
    session.pop('voter_id')
    return redirect('/')



@app.route('/candidate_login')
def candidate_login():
    if ('can_id' in session):
        return redirect('candidate_dashboard')
    else :
        return render_template('candidate_login.html')


@app.route('/candidate_register')
def candidate_register():
    if ('can_id' in session):
        return redirect('/candidate_dashboard')
    else:
        return render_template('candidate_reg.html')

@app.route('/candidate_dashboard')
def candidate_dashboard():
    if ('can_id' in session):
        return render_template('candidate_dashboard.html')
    else:
        return redirect('/candidate_login')

@app.route('/clogin_validation', methods=['POST'])
def clogin_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    try :
        cursor.execute("SELECT * FROM candidate WHERE can_email ='{}' AND can_password='{}'".format(email,password))
        candidates = cursor.fetchall()
        if len(candidates) > 0:
            session['can_id'] = candidates[0][0]
            return redirect('/candidate_dashboard')
        else :
            return redirect('/candidate_login')
    except mysql.connector.Error as err:
        print(err)
        return redirect('/candidate_login')

@app.route('/add_candidate',methods=['POST'])
def add_candidate():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    address = request.form.get('address')
    dob = request.form.get('dob')
    email = request.form.get('email')
    pno = request.form.get('pno')
    gender = request.form.get('gender')
    branch = request.form.get('branch')
    current_year = request.form.get('cy')
    cgpa = request.form.get('cgpa')
    bio = request.form.get('bio')
    password = request.form.get('password')


    ALLOWED_EXTENSIONS =['.png', '.jpg', '.jpeg']

    image_name = request.files['profile_img'].filename
    image_ext =  os.path.splitext(image_name)[1]
    if image_ext not in ALLOWED_EXTENSIONS:
        flash("Allowed Extensions are : jpg, jpeg, png ")
    image_path = "./static/candidate_images/" + image_name
    request.files['profile_img'].save(image_path)

    query = "INSERT INTO candidate(can_fname,can_lname,can_add,can_dob,can_email,can_pno,can_gen, \
            can_branch,can_cy,can_cgpa,can_bio,can_pro_img,can_password) VALUES (%s, %s, %s, %s, %s, %s, %s, \
             %s,%s,%s,%s,%s,%s)"
    try:
        params = (fname, lname, address, dob, email, pno, gender, branch, current_year, cgpa, bio, image_path[1:], password)
        cursor.execute(query, params)
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
        return redirect('/candidate_register')
    finally:
        cursor.execute("SELECT * FROM candidate WHERE can_email = '{}'".format(email))
        add_can = cursor.fetchall()
        print(add_can)
        session['can_id'] = add_can[0][0]
        return redirect('/candidate_dashboard')

@app.route('/candidate_logout')
def candidate_logout():
    session.pop('can_id')
    return redirect('/')




if __name__ == "__main__":
    app.run(debug=True)
