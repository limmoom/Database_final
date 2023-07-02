from db import sharedata
db = sharedata.getValue('dbObj')
def listAllPatMedicine(patid):
    res = []
    sql = "select * from `medicial_orders` where `patient_id` = %(patid)s"
    params = {"patid":patid}
    result = db.query(sql,params)
    for order in result:
        medid = order[1]
        docid = order[4]
        sql_med = "select * from `medicine` where `medicine_id` = %(medid)s"
        params_med = {"medid":medid}
        result_med = db.query(sql_med,params_med)
        sql_doc = "select `doctor_name` from `doctor` where `doctor_id` = %(docid)s"
        params_doc = {"docid":docid}
        result_doc = db.query(sql_doc,params_doc)
        phid = result_med[0][0]
        sql_ph = "select `pharmacy_name` from `pharmacy` where `pharmacy_id` = %(phid)s"
        params_ph = {"phid":phid}
        result_ph = db.query(sql_ph,params_ph)
        res.append((result_doc[0][0],docid,result_med[0][2],medid,result_med[0][3],result_ph[0][0],order[3],order[5]))
    return res

print(listAllPatMedicine('2xx'))

