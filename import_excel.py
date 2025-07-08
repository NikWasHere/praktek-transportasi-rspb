import pandas as pd
from app import db, Driver, Route, Transaction, app
from datetime import datetime


with app.app_context():

    df_driver = pd.read_excel("data_transportasi.xlsx", sheet_name="Driver", skiprows=1)
    df_driver.columns = df_driver.columns.str.lower().str.strip()


    df_route = pd.read_excel("data_transportasi.xlsx", sheet_name="Route", skiprows=1)
    df_route.columns = df_route.columns.str.lower().str.strip()
    


    # df_trans = pd.read_excel("data_transportasi.xlsx", sheet_name="Transaction", skiprows=1)
    # df_trans.columns = df_trans.columns.str.lower().str.strip()
    df_trans = pd.read_excel("data_transportasi.xlsx", sheet_name="Transaction", skiprows=1)
    df_trans.columns = df_trans.columns.str.lower().str.strip()
    df_trans['date'] = pd.to_datetime(df_trans['date']).dt.date


    db.session.query(Transaction).delete()
    db.session.query(Route).delete()
    db.session.query(Driver).delete()

    # Import Driver
    for _, row in df_driver.iterrows():
        driver = Driver(name=row["nama"], plate=row["no. plat"])
        db.session.add(driver)

    # Import Route
    for _, row in df_route.iterrows():
        total_cost = row["jarak"] * row["price per km"]
        route = Route(
            start=row["point awal"],
            end=row["point akhir"],
            distance=row["jarak"],
            std_time=row["waktu standart"],
            price_per_km=row["price per km"],
            total_cost=total_cost
        )
        db.session.add(route)

    # Import Transaction
    for _, row in df_trans.iterrows():
        telat = max(0, row["actual time"] - row["waktu_standart"])
        trans = Transaction(
            driver_name=row["nama driver"],
            driver_plate=row["driver plat"],
            start=row["point start"],
            end=row["point end"],
            distance=row["distance"],
            date=row["date"],
            actual_time=row["actual time"],
            std_time=row["waktu_standart"],
            telat=telat,
            cost=row["total cost"]
        )
        db.session.add(trans)

    db.session.commit()
    print("✅ Semua data berhasil diimpor ke database.")
