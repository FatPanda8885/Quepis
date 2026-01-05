import pymysql
import output
import config

CONFIG = config.get_config()

def setup():
    global db_litebans, db_auth,CONFIG
    try:
        db_litebans = pymysql.connect(host=CONFIG.get('litebans', 'database_host'),
                            user=CONFIG.get('litebans', 'database_user'),
                            password=CONFIG.get('litebans', 'database_password'),
                            database=CONFIG.get('litebans', 'database_name'))
        db_auth = pymysql.connect(host=CONFIG.get('auth', 'database_host'),
                            user=CONFIG.get('auth', 'database_user'),
                            password=CONFIG.get('auth', 'database_password'),
                            database=CONFIG.get('auth', 'database_name'))
        output.info_output("Database connections established successfully.")
    except Exception as e:
        output.error_output(f"Failed to connect to databases: {e}")
        raise e


def search_uuid(uuid):
    conn = db_litebans
    cursor = conn.cursor()
    sql = "SELECT uuid, reason, active FROM litebans_bans"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if row[0] == uuid:
            if row[2] == b'\x01':  # active == 1 表示有效封禁
                return True, row[1]
            # 如果 active == 0，则继续循环查找其他记录

    return False, "User not found or no active ban"






def match_uuid(username):
    conn = db_auth
    return_info = None
    cursor = conn.cursor()
    sql = "SELECT uuid,name,password FROM playerdata"
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        if row[1] == username:
            return_info =  row[0]
            break
        else:
            return_info = False, "username not found"

    return return_info


if __name__=='__main__':
    setup()
