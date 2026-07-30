from flask import Flask, request, render_template_string
import pickle
import numpy as np

app = Flask(__name__)

# Load Model
with open("GradientBoosting_model.pkl", "rb") as file:
    model = pickle.load(file)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Stock Price Prediction</title>

<style>

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:'Segoe UI',sans-serif;
}

body{

background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
height:100vh;
display:flex;
justify-content:center;
align-items:center;
overflow:hidden;
}

.circle{
position:absolute;
border-radius:50%;
background:rgba(255,255,255,0.07);
animation:float 10s infinite;
}

.circle:nth-child(1){
width:250px;
height:250px;
top:-70px;
left:-70px;
}

.circle:nth-child(2){
width:180px;
height:180px;
bottom:-50px;
right:-50px;
}

@keyframes float{
50%{
transform:translateY(25px);
}
}

.container{

width:430px;
background:rgba(255,255,255,.12);
backdrop-filter:blur(20px);
padding:35px;
border-radius:20px;
box-shadow:0 15px 35px rgba(0,0,0,.3);
color:white;
animation:fade 1s;
}

@keyframes fade{
from{
opacity:0;
transform:translateY(30px);
}
to{
opacity:1;
transform:translateY(0);
}
}

h1{

text-align:center;
margin-bottom:25px;
font-size:30px;
}

input{

width:100%;
padding:14px;
margin:10px 0;
border:none;
border-radius:10px;
font-size:16px;
outline:none;
}

button{

width:100%;
padding:14px;
margin-top:18px;
border:none;
border-radius:10px;
background:#00d4ff;
font-size:18px;
font-weight:bold;
cursor:pointer;
transition:.3s;
color:#111;
}

button:hover{

background:#00ffb3;
transform:scale(1.05);

}

.result{

margin-top:25px;
padding:15px;
border-radius:10px;
background:rgba(255,255,255,.15);
text-align:center;
font-size:22px;
font-weight:bold;
animation:pop .5s;
}

@keyframes pop{

from{
transform:scale(.8);
opacity:0;
}

to{
transform:scale(1);
opacity:1;
}

}

.footer{

margin-top:20px;
text-align:center;
font-size:14px;
opacity:.8;

}

</style>

</head>

<body>

<div class="circle"></div>
<div class="circle"></div>

<div class="container">

<h1>📈 Stock Price Predictor</h1>

<form method="POST">

<input type="number" step="any" name="Open" placeholder="Open Price" required>

<input type="number" step="any" name="High" placeholder="High Price" required>

<input type="number" step="any" name="Low" placeholder="Low Price" required>

<input type="number" step="any" name="Close" placeholder="Close Price" required>

<button type="submit">Predict</button>

</form>

{% if prediction %}

<div class="result">

Predicted Value<br><br>

₹ {{prediction}}

</div>

{% endif %}

<div class="footer">

Gradient Boosting Regression Model

</div>

</div>

</body>

</html>

"""

@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None

    if request.method == "POST":
        try:
            Open = float(request.form["Open"])
            High = float(request.form["High"])
            Low = float(request.form["Low"])
            Close = float(request.form["Close"])

            features = np.array([[Open, High, Low, Close]])

            pred = model.predict(features)[0]

            prediction = round(float(pred), 2)

        except Exception as e:
            prediction = str(e)

    return render_template_string(HTML, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
