from sqlalchemy import create_engine

# обновим таблицу "orders"
def update_orders(df):
    engine = create_engine('postgresql://postgres@localhost:5432/postgres')
    df.to_sql('orders', con=engine, if_exists='replace')
    return print("[INFO] Data was successfully updated in table 'orders")