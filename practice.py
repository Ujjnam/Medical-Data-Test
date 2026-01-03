import pandas as pd
import oracledb
conStr = 'myuser/mypass123@localhost:1521/xepdb1'
cur=conn=None
try :
    conn = oracledb.connect(conStr)
    cur = conn.cursor()
    sqlQuery = """ SELECT EMPNO,CHECKSUM(EMPNO || ENAME ||SAL) AS SRC_CS 
                   FROM EMP
                   GROUP BY EMPNO"""
    df_source = pd.read_sql(sqlQuery,conn)

    sqlQuery = """ SELECT EMPNO,CHECKSUM(EMPNO || ENAME ||SAL) AS TARGET_CS 
                   FROM EMPN
                   GROUP BY EMPNO"""
    df_target = pd.read_sql(sqlQuery,conn)

    for empno_src,empno_target,cs_value_src,cs_value_target in zip(df_source['EMPNO'],df_target['EMPNO'],df_source['SRC_CS'],df_target['TARGET_CS']):
        if(empno_src == empno_target) and (cs_value_src != cs_value_target):
            print('Value mismatch found!')
            print(f'Employee number={empno_src}; Source checksum={cs_value_src};Target checksum={cs_value_target}')

except oracledb.DatabaseError as e:
    print('Unable to connect to DB. Check credentials.', e)
except Exception as err:
    print('Unknown error. Please try again', err)
else:
    print('Connected to DB succesfully.')
finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()

