from re import A
from flask import Flask, render_template, request, flash, redirect
import psycopg2
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
conn = psycopg2.connect(database="201901422_db", user="postgres", password="admin", host="localhost", port="5432")
cur = conn.cursor()
cur.execute("set search_path to \"project\"")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    AN = db.Column(db.Integer, primary_key=True)
    FN = db.Column(db.String(), nullable=False)
    DOB = db.Column(db.String(), nullable=False)
    G = db.Column(db.String(), nullable=False)
    TD = db.Column(db.Integer(), nullable=False)
    MN = db.Column(db.Integer(), nullable=False)
    EM = db.Column(db.String(), nullable=False)
    HN = db.Column(db.Integer(), nullable=False)
    SN = db.Column(db.String(), nullable=False)
    PN = db.Column(db.Integer(), nullable=False)

    def __repr__(self) -> str:
        return f"{self.AN}-{self.FN}-{self.DOB}-{self.G}-{self.TD}-{self.MN}-{self.EM}-{self.HN}-{self.SN}-{self.PN}"
    
class Re(db.Model):
    ri = db.Column(db.Integer, primary_key=True)
    pi = db.Column(db.Integer(), nullable=False)
    vi = db.Column(db.Integer(), nullable=False)
    da = db.Column(db.String(), nullable=False)
    dn = db.Column(db.Integer(), nullable=False)
    si = db.Column(db.Integer(), nullable=False)

    def __repr__(self) -> str:
        return f"{self.ri}-{self.pi}-{self.vi}-{self.da}-{self.dn}-{self.si}"

@app.route('/')
def default():
    return render_template("main.html")

@app.route('/person', methods=['GET', 'POST'])
def personadd():
    if request.method == "POST":
        AN = request.form["ADN"]
        FN = request.form["FDN"]
        DOB = request.form["DDOB"]
        G = request.form["GD"]
        TD = request.form["TDD"]
        MN = request.form["MDN"]
        EM = request.form["EDM"]
        HN = request.form["HDN"]
        SN = request.form["SDN"]
        PN = request.form["PDN"]
        str = "insert into person(person_id,person_name,\"DOB\",gender," \
          "taken_doses,mobile_no,email,house_number,street_name,pincode) " \
          "values(" + AN + ",'" + FN + "','" + DOB + "','" + G + "'," + TD + "," + MN \
          + ",'" + EM + "'," + HN + ",'" + SN + "'," + PN + ")"
        cur.execute(str)
        conn.commit()
        todo = Todo(AN=AN,FN=FN,DOB=DOB,G=G,TD=TD,MN=MN,EM=EM,HN=HN,SN=SN,PN=PN)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)


@app.route('/registration', methods=['GET', 'POST'])
def registrationadd():
    if request.method == "POST":
        pi = request.form["pdi"]
        vi = request.form["vdi"]
        da = request.form["dda"]
        dn = request.form["ddn"]
        si = request.form["sdi"]
        s = "select max(reg_id) from registration_details"
        cur.execute(s)
        rows = cur.fetchall()
        for r in rows:
            ri = str(r[0])
        ri = int(ri) + 1
        s = "insert into registration_details values(" + str(ri) + "," + pi + "," + vi + ",'" + da + "'," + dn + "," + si + ")"
        cur.execute(s)
        conn.commit()
        re = Re(ri=ri,pi=pi,vi=vi,da=da,dn=dn,si=si)
        db.session.add(re)
        db.session.commit()
    allRe = Re.query.all()
    return render_template("index2.html", allRe=allRe)


@app.route('/update_person/<int:AN>', methods=['GET', 'POST'])
def update_person(AN):
    if request.method == "POST":
        AN = request.form["ADN"]
        FN = request.form["FDN"]
        DOB = request.form["DDOB"]
        G = request.form["GD"]
        TD = request.form["TDD"]
        MN = request.form["MDN"]
        EM = request.form["EDM"]
        HN = request.form["HDN"]
        SN = request.form["SDN"]
        PN = request.form["PDN"]
        todo = Todo.query.filter_by(AN=AN).first()
        todo.AN = AN
        todo.FN = FN
        todo.DOB = DOB
        todo.G = G 
        todo.TD = TD
        todo.MN = MN 
        todo.EM = EM
        todo.HN = HN
        todo.SN = SN
        todo.PN = PN
        str = "update person set person_name='" + FN + "',\"DOB\"='" + DOB + "',gender='" + G + "',taken_doses=" + TD + ",mobile_no=" + MN + ",email='" + EM + "',house_number=" + HN + ",street_name='" + SN + "',pincode=" + PN + " where person_id='" + AN + "'"
        cur.execute(str)
        conn.commit()
        db.session.add(todo)
        db.session.commit()
        return redirect("/person")
    todo = Todo.query.filter_by(AN=AN).first()
    return render_template("update_person.html", todo=todo)

@app.route('/update_registration/<int:ri>', methods=['GET', 'POST'])
def update_registration(ri):
    if request.method == "POST":
        ri = request.form["rdi"]
        pi = request.form["pdi"]
        vi = request.form["vdi"]
        da = request.form["dda"]
        dn = request.form["ddn"]
        si = request.form["sdi"]
        re = Re.query.filter_by(ri=ri).first()
        re.ri = ri
        re.pi = pi
        re.vi = vi
        re.da = da
        re.dn = dn
        re.si = si
        str = "update registration_details set person_id='" + pi + "',vaccine_id='" + vi + "',date='" + da + "',dose_number='" + dn + "',slot_id='" + si + "' where reg_id='" + ri + "'"
        cur.execute(str)
        conn.commit()
        db.session.add(re)
        db.session.commit()
        return redirect("/registration")
    re = Re.query.filter_by(ri=ri).first()
    return render_template("update_registration.html", re=re)

@app.route('/delete_person/<int:AN>')
def delete_person(AN):
    todo = Todo.query.filter_by(AN=AN).first()
    s = "delete from person where person_id=" + str(AN)
    cur.execute(s)
    conn.commit()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/person")

@app.route('/delete_registration/<int:ri>')
def delete_registration(ri):
    re = Re.query.filter_by(ri=ri).first()
    s = "delete from registration_details where reg_id=" + str(ri)
    cur.execute(s)
    conn.commit()
    db.session.delete(re)
    db.session.commit()
    return redirect("/registration")

@app.route('/query1', methods=['GET', 'POST'])
def query1():
    if request.method == "POST":
        ans = request.form["ands"]
        s = "select sum(available_doses) from slot_details where  center_id = " + str(ans)
        cur.execute(s)
        rows = cur.fetchall()
        for r in rows:
            ans = str(r[0])
    else:
        ans = ""
    return render_template("query1.html",ans=ans)

@app.route('/query2', methods=['GET', 'POST'])
def query2():
    if request.method == "POST":
        ans = request.form["ands"]
        s = "select count(*) from record_details where vaccination_date=" + "'"+ ans +"'"
        cur.execute(s)
        rows = cur.fetchall()
        for r in rows:
            ans = str(r[0])
    else:
        ans = ""
    return render_template("query2.html",ans=ans)

if __name__ == "__main__":
    app.run(debug=True,port=8000) 