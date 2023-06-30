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

# findregform('231','111')

def totalPages(options, searchInfo):
    if options == '医生科室':
        sql = "select count(*) from `doctor` where doctor_dept=%(dept)s"
        params = {"dept": searchInfo}
    elif options == '医生职称':
        sql = "select count(*) from `doctor` where doctor_title=%(title)s"
        params = {"title": searchInfo}
    elif options == '医生姓名':
        sql = "select count(*) from `doctor` where doctor_name=%(name)s"
        params = {"name": searchInfo}
    elif options == '医生编号':
        sql = "select count(*) from `doctor` where doctor_id=%(id)s"
        params = {"id": searchInfo}
    result = db.query(sql, params)
    return result[0][0]

print(totalPages('医生科室','测试科室1'))