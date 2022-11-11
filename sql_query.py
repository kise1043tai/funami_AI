import pyodbc
import sys
import datetime

#自分用　DBにアクセスする
class DbAccess:
    __server = 'sqltozan'  
    __database = 'iotdb'  
    __username = 'tozanadmin'  
    __password = '0526250148'

    def __init__(self,*, sv=__server,db=__database,un=__username,pw=__password):
        self.sv = sv
        self.db = db
        self.un = un
        self.pw = pw

    def __db_connection(self):
        con_str = 'DRIVER={SQL Server};SERVER='+self.sv+';DATABASE='+self.db+';UID='+self.un+';PWD='+self.pw
        cnxn = pyodbc.connect(con_str)
        return cnxn

    def db_get(self,query):
        #SELECT文まんま用
        try:
            con = self.__db_connection()
            cur = con.cursor()
            cur.execute(query)
            get_data = cur.fetchall()     
        except :
            print('query error')
            get_data = None
        finally:
            con.commit()
            con.close()
            return get_data

    def db_sql(self,query):
        #SQL文まんま用
        try:
            con = self.__db_connection()
            cur = con.cursor()
            cur.execute(query)
            get_data = cur.fetchall()     
        except :
            print('query error')
        finally:
            con.commit()
            con.close()

    def db_update(self,table,*,where='',**set):
        #UPDATE文
        #table =>表名、where =>WHERE以下の条件　where = '条件'の形で記入（省略可）、**set =>セットしたい値('カラム名'='値')の形で記入（可変長）
        try:
            query = ''
            con = self.__db_connection()
            cur = con.cursor()

            query += f'UPDATE {table} ' 
            query += 'SET '
            for i, (k, v) in enumerate(set.items()):
                if isinstance(v, datetime.datetime):
                    time_stamp = v.strftime('%Y-%m-%d %H:%M:%S')
                    query += str(k) +" = '" + str(time_stamp) + "' "
                else:
                    query += str(k) +" = '" + str(v) + "' "
                if i != len(set) - 1:
                    query += ', '
            if len(where) != 0:
                query += f'WHERE {where} '
            cur.execute(query)
        except :
            print('UPDATE ERROR')

        finally:
            con.commit()
            con.close()

    def db_insert(self,table,**set):
        #INSERT文
        #table =>表名、**set =>セットしたい値('カラム名':'値')の形で記入（可変長）
        try:
            query = ''
            con = self.__db_connection()
            cur = con.cursor()

            query += f'INSERT INTO {table}(' 
            for i, (k, v) in enumerate(set.items()):
                query += str(k) + " "
                if i != len(set) - 1:
                    query += ', '

            query += ')VALUES(' 

            for i, (k, v) in enumerate(set.items()):
                if isinstance(v, datetime.datetime):
                    time_stamp = v.strftime('%Y-%m-%d %H:%M:%S')
                    query += "'" + str(time_stamp) + "' "
                else:
                    query += "'" + str(v) + "' "
                if i != len(set) - 1:
                    query += ', '
            query += ')' 
            cur.execute(query)
        except :
            print('INSERT ERROR')

        finally:
            con.commit()
            con.close()

    def db_select(self,table,*column,where='',order='',limit=''):
        #シンプルなSELECT文のみ
        #table =>表名、*column =>必要なカラム名（可変長、省略可）、where =>WHERE以下の条件　where = '条件'の形で記入（省略可）,order =>ORDER BY以下の条件　order = '条件'の形で記入（省略可）
        #limit =>LIMIT以下の条件　limit = '条件'の形で記入、配列で入れるとOFFSETも追加（省略可）
        try:
            query = ''
            con = self.__db_connection()
            cur = con.cursor()
                        
            query += 'SELECT '
            if len(column) != 0:
                for i, v in enumerate(column):
                    query += f'{v} '
                    if i != len(column) - 1:
                        query += ', '
            else:
                 query += '* '

            query += f'FROM {table} '
            if len(where) != 0:
                query += f'WHERE {where} '
            if len(order) != 0:
                query += f'ORDER BY {order} '
            if len(limit) != 0:
                if len(limit) == 1:
                    query += f'LIMIT {limit} '
                if len(limit) >= 2:
                    query += f'LIMIT {limit[0]} OFFSET {limit[1]} '

            cur.execute(query)
            get_data = cur.fetchall()     
        except :
            print('SELECT ERROR')
            get_data = None
        finally:
            con.commit()
            con.close()
            return get_data

def main():
    dba = DbAccess()
    get = dba.db_select('iot_send_mail',limit=(1,2))
    print(get)

if __name__ == "__main__":
    sys.exit(int(main() or 0))
