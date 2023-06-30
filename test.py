from db import sharedata
db = sharedata.getValue('dbObj')
import datetime
def guahao(patient,doctor):
    """
    挂号
    """
    sql = "insert into `registration_form`(`patient_id`,`doctor_id`) values(%(patient)s,%(doctor)s)"
    params = {"patient": patient, "doctor": doctor}
    result = db.execute(sql, params, commit=True)
    if result == "connect_error" or result == "execute_error":
        return result
    return

#guahao('231','111')

def findregform(patient,doctor):
    """
    查找挂号单
    """
    sql = "select * from `registration_form` where patient_id=%(patient)s and doctor_id=%(doctor)s order by Registration_date desc"
    params = {"patient": patient, "doctor": doctor}
    result = db.query(sql, params)
    if not(result):
        return "OK"
    else:
        date1 = datetime.datetime.now().date()
        date2 = result[0][2].date()
        if date1 == date2:
            print("xiangtong")
        else:
            print("buxiangtong")

findregform('231','111')