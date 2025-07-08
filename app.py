from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# ===================== MODELS =====================
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    plate = db.Column(db.String(20))

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(10))
    end = db.Column(db.String(10))
    distance = db.Column(db.Integer)
    std_time = db.Column(db.Integer)
    price_per_km = db.Column(db.Integer)
    total_cost = db.Column(db.Integer)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(50))
    driver_plate = db.Column(db.String(20))
    start = db.Column(db.String(10))
    end = db.Column(db.String(10))
    distance = db.Column(db.Integer)
    date = db.Column(db.String(20))
    actual_time = db.Column(db.Integer)
    std_time = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    telat = db.Column(db.Integer)

# ===================== ROUTES =====================
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/drivers', methods=['GET', 'POST'])
def drivers():
    if request.method == 'POST':
        name = request.form['name']
        plate = request.form['plate']
        db.session.add(Driver(name=name, plate=plate))
        db.session.commit()
        return redirect('/drivers')
    all = Driver.query.all()
    return render_template('drivers.html', drivers=all)

@app.route('/routes', methods=['GET', 'POST'])
def routes():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']
        distance = int(request.form['distance'])
        std_time = int(request.form['std_time'])
        price_per_km = int(request.form['price'])
        total = distance * price_per_km
        db.session.add(Route(start=start, end=end, distance=distance, std_time=std_time, price_per_km=price_per_km, total_cost=total))
        db.session.commit()
        return redirect('/routes')
    all = Route.query.all()
    return render_template('routes.html', routes=all)

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        name = request.form['driver_name']
        plate = request.form['driver_plate']
        start = request.form['start']
        end = request.form['end']
        distance = int(request.form['distance'])
        date = request.form['date']
        actual_time = int(request.form['actual_time'])
        std_time = int(request.form['std_time'])
        cost = int(request.form['cost'])
        telat = max(0, actual_time - std_time)
        db.session.add(Transaction(driver_name=name, driver_plate=plate, start=start, end=end,
                                   distance=distance, date=date, actual_time=actual_time,
                                   std_time=std_time, cost=cost, telat=telat))
        db.session.commit()
        return redirect('/transactions')
    all = Transaction.query.all()
    return render_template('transactions.html', trans=all)

@app.route('/reports')
def reports():
    from sqlalchemy import func

    # Paling sering telat
    telat_list = db.session.query(Transaction.driver_name, func.count().label('total'))\
        .filter(Transaction.telat > 0).group_by(Transaction.driver_name)\
        .order_by(func.count().desc()).all()

    # Cost tertinggi
    cost_list = db.session.query(Transaction.driver_name, func.sum(Transaction.cost).label('total_cost'))\
        .group_by(Transaction.driver_name).order_by(func.sum(Transaction.cost).desc()).all()

    # Jarak tempuh terjauh
    distance_list = db.session.query(Transaction.driver_name, func.sum(Transaction.distance).label('total_dist'))\
        .group_by(Transaction.driver_name).order_by(func.sum(Transaction.distance).desc()).all()

    # Grafik
    names = []
    distances = []
    costs = []
    data = db.session.query(Transaction.driver_name, func.sum(Transaction.distance), func.sum(Transaction.cost)).group_by(Transaction.driver_name).all()
    for d in data:
        names.append(d[0])
        distances.append(d[1])
        costs.append(d[2])

    plt.figure(figsize=(8,4))
    plt.bar(names, distances, label='Distance', color='skyblue')
    plt.plot(names, costs, label='Cost', color='red', marker='o')
    plt.xlabel('Driver')
    plt.ylabel('Value')
    plt.title('Driver vs Distance & Cost')
    plt.legend()
    plt.tight_layout()
    plt.savefig('static/driver_graph.png')

    return render_template('reports.html', telat=telat_list, cost=cost_list, dist=distance_list)

if __name__ == '__main__':
    if not os.path.exists('database.db'):
        with app.app_context():
            db.create_all()
    app.run(debug=True)

    