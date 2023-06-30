import sharedata, dbClass
import hashlib
import datetime

db = sharedata.getValue('dbObj')

def findPatient(usr):
    """
    查找用户
    """
    sql = "select * from `patient` where patient_id=%(usr)s"
    params = {"usr": usr}
    result = db.query(sql, params)
    if result:
        return result
    else:
        return "no_user"

def findDoctor(usr):
    """
    查找医生
    """
    sql = "select * from `doctor` where doctor_id=%(usr)s"
    params = {"usr": usr}
    result = db.query(sql, params)
    if result:
        return result
    else:
        return "no_user"

def pwdEncryption(pwd):
    """
    密码加密
    """
    # 创建SHA-256哈希对象
    sha256_hash = hashlib.sha256()
    # 将密码编码为字节流并更新哈希对象
    sha256_hash.update(pwd.encode('utf-8'))
    # 获取哈希值的十六进制表示
    hashed_password = sha256_hash.hexdigest()
    # 返回加密后的密码
    return hashed_password

def addPatient(usr,pwd,name,id,phone):
    """
    添加用户
    """
    result_name = findPatient(usr)
    if result_name == "connect_error" or result_name == "execute_error":
        return result_name
    elif result_name == "no_user":
        sql = "insert into `patient` values(%(usr)s,%(name)s,%(idnumber)s,300,%(phone)s,%(pwd)s)"
        params = {"usr": usr, "pwd": pwd, "name": name, "idnumber": id, "phone": phone}
        result = db.execute(sql, params, commit=True)
        if result == "connect_error" or result == "execute_error":
            return result
    else:
        return "user exists"
    return result

def findfee(title):
    """
    查找挂号费
    """
    sql = "select fee from `title` where title=%(title)s"
    params = {"title": title}
    result = db.query(sql, params)
    if result:
        return result
    else:
        return "no_fee"


def addDoctor(username, encrypt_pwd, name, title, dept):
    """
    添加医生
    """
    result_name = findDoctor(username)
    fee = findfee(title)
    if result_name == "connect_error" or result_name == "execute_error":
        return result_name
    elif result_name == "no_user":
        sql = "insert into `doctor` values(%(username)s,%(name)s,%(title)s,%(fee)s,%(pwd)s,%(dept)s)"
        params = {"username": username, "pwd": encrypt_pwd, "name": name, "title": title, "dept": dept,"fee":fee}
        result = db.execute(sql, params, commit=True)
        if result == "connect_error" or result == "execute_error":
            return result
    else:
        return "user_exist"
    return result

def findregdate(patient,doctor):
    """
    查找挂号单
    """
    sql = "select * from `registration_form` where patient_id=%(patient)s and doctor_id=%(doctor)s order by Registration_date desc"
    params = {"patient": patient, "doctor": doctor}
    result = db.query(sql, params)
    curdate = datetime.datetime.now().date()
    regdate = result[0][2].date()
    if curdate == regdate:
        return "date_same"
    else:
        return "date_different"

def guahao(patient,doctor):
    """
    挂号
    """
    date_ok = findregdate(patient,doctor)
    if date_ok == "date_same":
        return "date_same"
    elif date_ok == "date_different":
        sql = "insert into `registration_form`(`patient_id`,`doctor_id`) values(%(patient)s,%(doctor)s)"
        params = {"patient": patient, "doctor": doctor}
        result = db.execute(sql, params, commit=True)
        if result == "connect_error" or result == "execute_error":
            return result
        return "already_reg"


