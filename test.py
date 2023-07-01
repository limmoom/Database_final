from db import sharedata
db = sharedata.getValue('dbObj')
def listAllPatients(currentPage, numPage, docid):
    '''
    列出所有患者
    :param currentPage: 当前页码
    :param numPage: 总的页数
    :param keyword: 关键词
    :return:
    '''
    result = []
    sql1 = "select * from `registration_form` where doctor_id=%(docid)s limit %(cur)s, %(nxt)s"
    params1 = {"docid": docid, "cur": currentPage, "nxt": numPage}
    result1 = db.query(sql1, params1)
    patientid = [i[1] for i in result1]
    for i in range(len(patientid)):
        sql2 = "select * from `patient` where patient_id=%(id)s"
        params2 = {"id": patientid[i]}
        result2 = db.query(sql2, params2)
        result.append((result2[0][0],result2[0][1],result1[i][2],result2[0][2]))
    return result
