import pandas as pd
import oracledb

con_str = 'myuser/mypass123@localhost:1521/xepdb1'
cur=conn=None
try :
    conn = oracledb.connect(con_str)
    cur = conn.cursor()
    # TEST IF THERE ARE ANY DUPLICATE RECORDS IN TARGET SYSTEM
    def test_checkDuplicates():
        df = pd.read_sql(""" SELECT * FROM MEDICAL_DATA""",conn)
        count = df.duplicated().sum()
        assert count == 0, "Duplication found - Please verify the target"
    test_checkDuplicates()

    # TEST IF ALL THE RECORDS ARE LOADED INTO TARGET
    def test_dataCompleteness():
        df_src = pd.read_excel('MEDICAL_DATA.xlsx')
        df_tgt = pd.read_sql(""" SELECT * FROM MEDICAL_DATA """,conn)
        print(len(df_src),len(df_tgt))
        assert (len(df_src) == len(df_tgt)), "Record count mismatch found - Please verify source and target"
    test_dataCompleteness()

    # TEST IF PATIENT_NAME IS POPULATED MANDATAROLY
    def test_patientIdForNullValues():
        df_tgt = pd.read_sql(""" SELECT * FROM MEDICAL_DATA """,conn)
        null_count = df_tgt['PATIENT_NAME'].isnull().sum()
        assert null_count == 0, "Patient_name has null value - Please check"
    test_patientIdForNullValues()

    # TEST PRIMARY KEY UNIQUENESS
    def test_uniqueValuesCheck():
        df_tgt = pd.read_sql(""" SELECT * FROM MEDICAL_DATA """, conn)
        total_count = df_tgt['PATIENT_ID'].count()
        unique_count = df_tgt['PATIENT_ID'].nunique()
        assert not total_count == unique_count, "patient_id values are not unique - Please check"
    test_uniqueValuesCheck()

except Exception as err:
    print('Unknown error. Please try again.', err)
else:
    print('Connected to DB succesfully.')
finally:
    if(cur):
        cur.close()
    if(conn):
        conn.close()