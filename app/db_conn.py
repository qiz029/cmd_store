import os
import mysql.connector
import datetime

connStrTpl = "mysql+pymysql://{0}:{1}@{2}/{3}"
dbUser = os.environ["DB_USER"]
dbPwd = os.environ["DB_PASSWORD"]
dbAddress = os.environ["DB_ADDR"]
dbDB = os.environ["DB_DATABASE"]

connStr = connStrTpl.format(dbUser, dbPwd, dbAddress, dbDB)

creation = "CREATE TABLE IF NOT EXISTS `commands` ( `ID` INT NOT NULL AUTO_INCREMENT, `CommandBody` VARCHAR(255), `StartTime` DATETIME NOT NULL, `TimeElapsedInSec` INT NOT NULL, `ExitCode` INT NOT NULL, `UserId` VARCHAR(255) NOT NULL, KEY `ExitCodeIndex` (`ExitCode`) USING BTREE, PRIMARY KEY (`ID`) );"
insertion = "INSERT INTO commands (CommandBody, StartTime, TimeElapsedInSec, ExitCode, UserId) VALUES (%s, %s, %s, %s, %s)"
selection = 'SELECT CommandBody, StartTime, TimeElapsedInSec, ExitCode FROM commands WHERE UserId = %s ORDER BY StartTime DESC'

config = {
        'user': dbUser,
        'password': dbPwd,
        'host': dbAddress.split(":")[0],
        'port': dbAddress.split(":")[1],
        'database': dbDB,
    }
connection = mysql.connector.connect(**config)
c = connection.cursor()
c.execute(creation)
c.close()

def writeCommandsToDb(rows):
    print("successfully connect to database")
    cursor = connection.cursor()
    for row in rows:
        timestamp = datetime.datetime.fromtimestamp(int(row['start_time']))
        start = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(insertion, (row['command'], start, row['execution_time'], row['exit_code'], row['user_id']))
    connection.commit()
    cursor.close()
    print("successfully insert data")

def getCommands(user_id):
    cursor = connection.cursor()
    cursor.execute(selection, (user_id,))
    results = cursor.fetchall()
    retVal = []
    for (command, startTime, executionTime, exitCode) in results:
        retVal.append({
            "command": command,
            "start_time": startTime,
            "execution_time": executionTime,
            "exit_code": exitCode, 
        })
    cursor.close()
    print("successfully retrieved {0} entries".format(len(retVal)))
    return retVal