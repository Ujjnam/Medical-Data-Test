import pandas as pd
import oracledb
connStr = "myusr/mypass123@localhost:1521/xepdb1"
conn = cur = None
conn = oracledb.connect(connStr)
cur = conn.cursor()
df = pd.read_excel()
# from sqlalchemy import create_engine,text
# db_url = "oracle+oracledb://myuser:mypass123@localhost:1521/?service_name=xepdb1"
# engine = create_engine(db_url, echo=False)
#
# with engine.connect() as conn:
#     result = conn.execute(text("SELECT * FROM EMP"))
#     for row in result:
#         print(row)
#
# df = pd.read_sql(text("SELECT * FROM EMP"), engine)
# print(df)

