from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np

app = Flask(__name__)

model=pickle.load(open('model.pkl','rb'))


@app.route('/')
def hello_world():
    return render_template("heart_predict.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        ag = request.form['age']
        sx = request.form['sex']
        if sx == 0:
            m,f = 1,0
        else:
            m,f = 0,1
        cpt = request.form['chestpain_type']
        if cpt == "ATA":
            ata,asy,nap,ta = 1,0,0,0
        elif cpt == "ASY":
            ata,asy,nap,ta = 0,1,0,0
        elif cpt == "TA":
            ata,asy,nap,ta = 0,0,0,1
        else:
            ata,asy,nap,ta = 0,0,1,0
        rbp = request.form['resting_bp']
        ctl = request.form['cholestrol']
        fbs = request.form['fasting_bs']
        reg = request.form['resting_ecg']
        if reg == "ST":
            st,n,lvh = 1,0,0
        elif reg == "LVH":
            st,n,lvh = 0,0,1
        else:
            st,n,lvh = 0,1,0
        mhr = request.form['max_hr']
        ea = request.form['excercise_angina']
        if ea == "Y":
            ye,no = 1,0
        else:
            ye,no = 0,1
        op = request.form['oldpeak']
        sts = request.form['st_slope']
        if sts == "Up":
            up,d,fl = 1,0,0
        elif sts == "Flat":
            up,d,fl = 0,0,1
        else:
            up,d,fl = 0,1,0

        data = np.array([[ag,rbp,ctl,fbs,mhr,op,f,m,asy,ata,nap,ta,lvh,n,st,no,ye,d,fl,up]])
        output = model.predict(data)

        return render_template('heart.html', prediction=output)


if __name__ == '__main__':
    app.run(debug=True)