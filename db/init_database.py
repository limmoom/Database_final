import dbClass


def _init_database():
    sql_ls = [
        '''use `hospital`;''',
        '''
        create table `title`(
            `title` varchar(10) primary key,
            `fee` int 
        )
        ''',
        # '''
        # create table `department`(
        #     `department_name` varchar(20) primary key,
        #     `department_telephone` varchar(20),
        #     `department_managerid` varchar(20),
        #     foreign key(`department_managerid`) references `doctor`(`doctor_id`) on delete set null
        # );
        #
        #     ''',
        '''create table `doctor`(
        `doctor_id` VARCHAR(20) primary key,
        `doctor_name` VARCHAR(20),
        `doctor_title` varchar(20),
        `doctor_fee` INT,
        `doctor_pwd` varchar(100),
        `doctor_dept` varchar(20)
    );
        ''',
        '''
create table `patient`(
	`patient_id` VARCHAR(20) primary key,
    `patient_name` varchar(20),
    `patient_idnumber` varchar(20),
    `patient_telephone` varchar(20),
    `patient_money` INT default 500,
    `patient_pwd` varchar(100)
);
        ''',
        #         '''
        # create table `admission_form`(
        # 	`doctor_id` varchar(20),
        #     `patient_id` varchar(20),
        #     `admission_date` date,
        #     `admission_department` varchar(20),
        #     foreign key(`admission_department`) references `department`(`department_name`) on delete CASCADE,
        #     primary key(`doctor_id`,`patient_id`)
        # );
        #     ''',
        '''
create table `pharmacy`(
	`pharmacy_id` int primary key auto_increment,
    `pharmacy_name` varchar(20)
);
    ''',
        '''
    create table `medicine`(
        `pharmacy_id` int ,
        `medicine_id` varchar(20) PRIMARY KEY,
        `medicine_name` varchar(20),
        `medicine_price` float,
        `medicine_stock` int,
        foreign key(`pharmacy_id`) references `pharmacy`(`pharmacy_id`) on delete cascade
    );
        ''',
        '''
    CREATE TABLE `medical_orders` (
      `medical_ordersid` INT PRIMARY KEY auto_increment,
      `medicine_id` varchar(20),
      `patient_id` varchar(20),
      `text` TEXT,
      `doctor_id` varchar(20) NOT NULL,
      `order_date` timestamp default current_timestamp
    );
        ''',
        '''
    create table `registration_form`(
        `Registration_id` int primary key auto_increment,
        `patient_id` varchar(20),
        `Registration_date` timestamp default current_timestamp,
        `doctor_id` varchar(20),
        `already` bool default false,
        foreign key(`doctor_id`) references `doctor`(`doctor_id`) on delete cascade,
        foreign key(`patient_id`) references `patient`(`patient_id`) on delete cascade
    );
        ''',
        '''
        insert into `pharmacy` (`pharmacy_name`) values ('一药房'),('二药房'),('中药房');
        ''',
        '''
        insert into `title` values('主任医师','400'),('副主任医师','200'),('主治医师','100'),('住院医师','50');
        ''', '''
INSERT INTO `medicine` VALUES
(1, 1, '扑热息痛', 24.75, 1675),
(2, 2, '布洛芬', 17.25, 1945),
(2, 3, '奥美拉唑', 31.50, 2145),
(2, 4, '阿司匹林', 42.00, 1124),
(1, 5, '阿莫西林', 25.50, 1876),
(3, 6, '藿香正气水', 59.25, 1573),
(1, 7, '辛伐他汀', 167.50, 1342),
(1, 8, '二甲双胍', 29.25, 2189),
(3, 9, '双黄连口服液', 43.75, 1512),
(2, 10, '洛沙坦', 78.50, 1782),
(1, 11, '阿托伐他汀', 19.75, 2054),
(3, 12, '云南白药', 21.25, 1196),
(1, 13, '左甲状腺素', 87.00, 1923),
(2, 14, '美托洛尔', 68.50, 1367),
(3, 15, '六味地黄丸', 45.75, 2256);


'''

        #     '''
        #     CREATE TABLE doctor_accounts (
        #     doctor_id VARCHAR(20) PRIMARY KEY,
        #   password VARCHAR(70) NOT NULL
        # );''', '''
        #     CREATE TABLE patient_accounts (
        #   patient_id VARCHAR(20) PRIMARY KEY,
        #   password VARCHAR(70) NOT NULL
        # );'''
    ]

    db = dbClass.dbClass()
    for sql in sql_ls:
        db.execute(sql, commit=True)
    db.commit()


def init_database():
    db = dbClass.dbClass()
    db.init_db()
    result = db.connectdb()
    if result:
        sql = 'select TABLE_NAME from information_schema.tables where table_schema="hospital"'
        result = db.query(sql)
        print(result)
        if len(result) == 7:  # 已经创建好数据库
            return
        else:
            _init_database()
    else:
        print("数据库连接失败")


if __name__ == '__main__':
    init_database()
