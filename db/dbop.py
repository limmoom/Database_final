import curuser
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


def addPatient(usr, pwd, name, id, phone):
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
        params = {"username": username, "pwd": encrypt_pwd, "name": name, "title": title, "dept": dept, "fee": fee}
        result = db.execute(sql, params, commit=True)
        if result == "connect_error" or result == "execute_error":
            return result
    else:
        return "user_exist"
    return result


def findregdate(patient, doctor):
    """
    查找挂号单
    """
    sql = "select * from `registration_form` where patient_id=%(patient)s and doctor_id=%(doctor)s order by Registration_date desc"
    params = {"patient": patient, "doctor": doctor}
    result = db.query(sql, params)
    if not result:
        return "date_different"
    curdate = datetime.datetime.now().date()
    regdate = result[0][2].date()
    if curdate == regdate:
        return "date_same"
    else:
        return "date_different"


def guahao(patient, doctor):
    """
    挂号
    """
    date_ok = findregdate(patient, doctor)
    if date_ok == "date_same":
        return "date_same"
    elif date_ok == "date_different":
        sql = "insert into `registration_form`(`patient_id`,`doctor_id`) values(%(patient)s,%(doctor)s)"
        params = {"patient": patient, "doctor": doctor}
        result = db.execute(sql, params, commit=True)
        if result == "connect_error" or result == "execute_error":
            return result
        return "already_reg"


def listAllDoctors(currentPage, numPage, options='', searchinfo=''):
    '''
    列出所有医生
    :param currentPage: 当前页码
    :param numPage: 总的页数
    :param keyword: 关键词
    :return:
    '''
    if not options:
        sql = "select * from `doctor` limit %(cur)s, %(nxt)s"
        params = {"cur": currentPage, "nxt": numPage}
    elif options == '医生科室':
        sql = "select * from `doctor` where doctor_dept=%(dept)s limit %(cur)s, %(nxt)s"
        params = {"dept": searchinfo, "cur": currentPage, "nxt": numPage}
    elif options == '医生职称':
        sql = "select * from `doctor` where doctor_title=%(title)s limit %(cur)s, %(nxt)s"
        params = {"title": searchinfo, "cur": currentPage, "nxt": numPage}
    elif options == '医生姓名':
        sql = "select * from `doctor` where doctor_name=%(name)s limit %(cur)s, %(nxt)s"
        params = {"name": searchinfo, "cur": currentPage, "nxt": numPage}
    elif options == '医生编号':
        sql = "select * from `doctor` where doctor_id=%(id)s limit %(cur)s, %(nxt)s"
        params = {"id": searchinfo, "cur": currentPage, "nxt": numPage}
    result = db.query(sql, params)
    return result


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
    else:
        sql = "select count(*) from `doctor`"
        params = {}
    result = db.query(sql, params)
    return result


def totalpatPages(docid):
    sql = "select count(*) from `registration_form` where doctor_id=%(docid)s and already = False"
    params = {"docid": docid}
    result = db.query(sql, params)
    return result


def listAllPatients(currentPage, numPage, docid):
    '''
    列出所有患者
    :param currentPage: 当前页码
    :param numPage: 总的页数
    :param keyword: 关键词
    :return:
    '''
    result = []
    sql1 = "select * from `registration_form` where doctor_id=%(docid)s and already = False or already is null limit %(cur)s, %(nxt)s"
    params1 = {"docid": docid, "cur": currentPage, "nxt": numPage}
    result1 = db.query(sql1, params1)
    patientid = [i[1] for i in result1]
    for i in range(len(patientid)):
        sql2 = "select * from `patient` where patient_id=%(id)s"
        params2 = {"id": patientid[i]}
        result2 = db.query(sql2, params2)
        result.append((result2[0][0], result2[0][1], result1[i][2], result2[0][2]))
    return result


def jiaohao(docid, patid, regdate):
    sql = "update `registration_form` set already = True where doctor_id=%(docid)s and patient_id=%(patid)s and Registration_date=%(regdate)s"
    params = {"docid": docid, "patid": patid, "regdate": regdate}
    result = db.execute(sql, params, commit=True)
    if result == "connect_error" or result == "execute_error":
        return result
    return "already_jiaohao"


def listAllPatients_already(currentPage, numPage, docid, options="", searchInfo=''):
    result = []
    if not options:
        sql1 = "select * from `registration_form` where doctor_id=%(docid)s and already= True limit %(cur)s, %(nxt)s"
        params1 = {"docid": docid, "cur": currentPage, "nxt": numPage}
    elif options == '患者姓名':
        sql1 = "select * from `registration_form` where doctor_id=%(docid)s and already= True and patient_id in (select patient_id from `patient` where patient_name = %(name)s) limit %(cur)s, %(nxt)s"
        params1 = {"docid": docid, "name": searchInfo, "cur": currentPage, "nxt": numPage}
    elif options == '患者病历卡号':
        sql1 = "select * from `registration_form` where doctor_id=%(docid)s and already= True and patient_id = %(id)s limit %(cur)s, %(nxt)s"
        params1 = {"docid": docid, "id": searchInfo, "cur": currentPage, "nxt": numPage}
    elif options == '患者身份证号':
        sql1 = "select * from `registration_form` where doctor_id=%(docid)s and already= True and patient_id in (select patient_id from `patient` where patient_idnumber = %(id)s) limit %(cur)s, %(nxt)s"
        params1 = {"docid": docid, "id": searchInfo, "cur": currentPage, "nxt": numPage}

    result1 = db.query(sql1, params1)
    patientid = [i[1] for i in result1]
    for i in range(len(patientid)):
        sql2 = "select * from `patient` where patient_id=%(id)s"
        params2 = {"id": patientid[i]}
        result2 = db.query(sql2, params2)
        result.append((result2[0][0], result2[0][1], result1[i][2], result2[0][2]))
    return result


def totalpatPages_already(docid, options, searchInfo):
    if options == '患者姓名':
        sql = "select count(*) from `registration_form` where doctor_id=%(docid)s and already = True and patient_id in (select patient_id from `patient` where patient_name = %(name)s)"
        params = {"docid": docid, "name": searchInfo}
    elif options == '患者病历卡号':
        sql = "select count(*) from `registration_form` where doctor_id=%(docid)s and already = True and patient_id = %(id)s"
        params = {"docid": docid, "id": searchInfo}
    elif options == '患者身份证号':
        sql = "select count(*) from `registration_form` where doctor_id=%(docid)s and already = True and patient_id in (select patient_id from `patient` where patient_idnumber = %(idcard)s)"
        params = {"docid": docid, "idcard": searchInfo}
    else:
        sql = "select count(*) from `registration_form` where doctor_id=%(docid)s and already = True"
        params = {"docid": docid}
    result = db.query(sql, params)
    return result


def listAllmedicines(currentPage, numPage, options="", searchInfo=""):
    '''
    列出所有药品
    :param currentPage: 当前页码
    :param numPage: 总的页数
    :param keyword: 关键词
    :return:
    '''
    if options == '药品名':
        sql = "select * from `medicine` where medicine_name = %(name)s limit %(cur)s, %(nxt)s"
        params = {"name": searchInfo, "cur": currentPage, "nxt": numPage}
    elif options == '药品编号':
        sql = "select * from `medicine` where medicine_id = %(id)s limit %(cur)s, %(nxt)s"
        params = {"id": searchInfo, "cur": currentPage, "nxt": numPage}
    else:
        sql = "select * from `medicine` limit %(cur)s, %(nxt)s"
        params = {"cur": currentPage, "nxt": numPage}
    result = db.query(sql, params)
    return result


def totalmedicinePages(options, searchInfo):
    if options == '药品名':
        sql = "select count(*) from `medicine` where medicine_name = %(name)s"
        params = {"name": searchInfo}
    elif options == '药品编号':
        sql = "select count(*) from `medicine` where medicine_id = %(id)s"
        params = {"id": searchInfo}
    else:
        sql = "select count(*) from `medicine`"
        params = {}
    result = db.query(sql, params)
    return result


def phconfirm(medid, info, docid):
    params = {"medid": medid}
    sql_pre = "select `medicine_stock` from `medicine` where `medicine_id` = %(medid)s"
    stock = db.query(sql_pre, params)[0][0]
    if stock > 0:
        sql = "update `medicine` set `medicine_stock` = `medicine_stock` - 1 where `medicine_id` = %(medid)s"
        db.execute(sql, params, commit=True)
    else:
        return "stock_error"
    sql_nxt = "insert into `medicial_orders` (`medicine_id`,`patient_id`,`text`,`doctor_id`) values (%(medid)s,%(patid)s,%(text)s,%(docid)s)"
    params_nxt = {"medid": medid, "patid": curuser.getpatientid(), "text": info, "docid": docid}
    res = db.execute(sql_nxt, params_nxt, commit=True)
    if res == "execute_error" or res == "connect_error":
        return res
    else:
        return "success"


def listAllPatMedicine(patid):
    res = []
    sql = "select * from `medical_orders` where `patient_id` = %(patid)s"
    params = {"patid": patid}
    result = db.query(sql, params)
    for order in result:
        medid = order[1]
        docid = order[4]
        sql_med = "select * from `medicine` where `medicine_id` = %(medid)s"
        params_med = {"medid": medid}
        result_med = db.query(sql_med, params_med)
        sql_doc = "select `doctor_name` from `doctor` where `doctor_id` = %(docid)s"
        params_doc = {"docid": docid}
        result_doc = db.query(sql_doc, params_doc)
        phid = result_med[0][0]
        sql_ph = "select `pharmacy_name` from `pharmacy` where `pharmacy_id` = %(phid)s"
        params_ph = {"phid": phid}
        result_ph = db.query(sql_ph, params_ph)
        res.append(
            (result_doc[0][0], docid, result_med[0][2], medid, result_med[0][3], result_ph[0][0], order[3], order[5]))
    return res
