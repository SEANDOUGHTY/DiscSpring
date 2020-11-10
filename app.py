from flask import Flask, redirect, url_for, render_template, request, Response
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import random
import io
from discspring import *

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        data = request.form

        #return f"<p>{data}</p>"
        return render_template("index.html")
    else:
        return render_template("index.html")


@app.route('/force.png', methods=["POST", "GET"])
def force_png():
    data = request.form
    print("DEBUG DEBUG")
    print(data)
      
    spring = spring_from_web(data)

    now = datetime.now()
    folder_string = "static/images/" + now.strftime("%y%m%d_%H%M%S")
    Path(folder_string).mkdir(parents=True, exist_ok=True)
    plot_force(spring, 0, folder_string)

    return "/" + folder_string + "/force_run1.png"

@app.route('/stress.png', methods=["POST", "GET"])
def stress_png():
    data = request.form
    print("DEBUG DEBUG")
    spring = spring_from_web(data)

    now = datetime.now()
    folder_string = "static/images/" + now.strftime("%y%m%d_%H%M%S")
    Path(folder_string).mkdir(parents=True, exist_ok=True)
    plot_stress(spring, 0, folder_string)

    return "/" + folder_string + "/stress_run1.png"


def spring_from_web(data):
    constructor  = []
    
    for n in data:
        print(data[n])
        if data[n].isnumeric():
            constructor.append(float(data[n]))
        else:
            constructor.append(0)

    return DiscSpring(constructor, "Ti-6Al-4V", 108500, 0.34)

if __name__ == "__main__":
    app.run()