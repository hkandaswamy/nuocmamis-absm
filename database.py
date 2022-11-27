import pymysql
import sql_credentials

# Create database connection
connection = pymysql.connect(
    host=sql_credentials.host,
    port=sql_credentials.port,
    user=sql_credentials.user,
    password=sql_credentials.password,
    db='users',
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()


# Create test Table "users"

sql = '''
CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    `userType` int(11) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1 ;
'''
cursor.execute(sql)
connection.commit()



def insert_new_user(_email, _password, _userType):
    # Create a new record
    sql = "INSERT INTO `users` (`email`, `password`, `userType`) VALUES (%s, %s)"
    cursor.execute(sql, (_email, _password, _userType))
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()


def get_user(_email):
    # Read a single record
    sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
    cursor.execute(sql, (_email,))
    result = cursor.fetchone()
    if result is None:
        return {
            "success": False
        }
    else:
        return {
            "success": True,
            "user": result
        }
