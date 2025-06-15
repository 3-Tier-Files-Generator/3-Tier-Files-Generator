from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pyodbc
import os
# import socket
# print(socket.gethostname())

class ConnectDatabase:
    def __init__(self, window):
        
        # region submit button function
        def page():

            global us
            global ps


            # region store user data
            ServerName = self.host_entry.get()
            DatabaseName = self.port_entry.get()
            # endregion store user data

            # region validation
            if self.port_entry.get() == '' or self.host_entry.get() == '':
                messagebox.showerror('Error', 'Please fill out both fields')

            elif self.host_entry.get() != '' and self.port_entry.get() != '':
                messagebox.showinfo('Entered data',
                                     'Server Name: ' + self.host_entry.get() + '\nDatabase Name: ' + self.port_entry.get())
                try:
                    with pyodbc.connect(
                            "Driver={SQL Server Native Client 11.0};"
                            "Server=" + ServerName + ";"
                                                     "Database=" + DatabaseName + ";"
                                                                                  "Trusted_Connection=yes;") as conn:
                        cursor = conn.cursor()
                        # region Get Table name
                        try:
                            cursor.execute("Select SYSOBJECTS.name as tablename from SYSOBJECTS where XTYPE='U'")
                            tablenameLength = cursor.fetchall()
                            # messagebox.showinfo('table count', len(tablenameLength))
                            tablename = []
                            temp = 0

                            for row in cursor.tables():
                                if int(len(tablenameLength)) == temp:
                                    break
                                else:
                                    temp = temp + 1
                                    tablename.append(str(row.table_name))
                                    # print(str(row.table_name),tablename,'\n')

                            # region Check for folder of ent dal bal
                            pathFolder = ['./App_Code', './App_Code/ENT', './App_Code/DAL', './App_Code/BAL']
                            isdir1 = os.path.isdir(pathFolder[0])
                            isdir2 = os.path.isdir(pathFolder[1])
                            isdir3 = os.path.isdir(pathFolder[2])
                            isdir4 = os.path.isdir(pathFolder[3])
                            isfolderdirectory = [isdir1, isdir2, isdir3, isdir4]

                            # region If folder doesn't exist then Create Multiple Folders
                            root_path = './'
                            for i in range(4):
                                if (isfolderdirectory[i] == False):
                                    os.mkdir(os.path.join(root_path, pathFolder[i]))

                            # endregion If folder doesn't exist then Create Multiple Folders

                            # endregion Check for folder of ent dal bal

                            # region Tab
                            t1 = '\n\t'
                            t2 = '\n\t\t'
                            t3 = '\n\t\t\t'
                            t4 = '\n\t\t\t\t'
                            t5 = '\n\t\t\t\t\t'
                            t6 = '\n\t\t\t\t\t\t'
                            t7 = '\n\t\t\t\t\t\t\t'
                            t8 = '\n\t\t\t\t\t\t\t\t'
                            t9 = '\n\t\t\t\t\t\t\t\t\t'
                            # endregion Tab

                            if (len(tablenameLength) == 0):
                                messagebox.showinfo('Error!!!', 'Incorrect Table name or Database name')

                            # region Message table
                            messagebox.showinfo('Table Name', 'There are total ' + str(
                                len(tablenameLength)) + ' tables in your database :-\n\n' + str(tablename))
                            # endregion Message table

                            # region Code to Create Files
                            for i in range(0, int(len(tablenameLength))):

                                # region Static variables
                                projectname = DatabaseName
                                # endregion Static variables

                                # messagebox.showinfo('Table Name', tablename[i])
                                # print(i,tablename, tablename[i], tablenameLength[i], len(tablenameLength))

                                # region Procedure
                                delete = '"PR_' + tablename[i] + '_DeleteByPK";'
                                insert = '"PR_' + tablename[i] + '_Insert";'
                                update = '"PR_' + tablename[i] + '_UpdateByPK";'
                                selectAll = '"PR_' + tablename[i] + '_SelectAll";'
                                selectByPK = '"PR_' + tablename[i] + '_SelectByPK";'
                                selectForDDL = '"PR_' + tablename[i] + '_SelectForDropDownList";'
                                # endregion Procedure

                                # region SqlQuery for column name and datatype
                                cursor.execute(
                                    "SELECT C.Name As ColumnName, Ty.Name As DataType from sys.tables as T inner join sys.columns as C on T.object_id = c.object_id Inner Join sys.types as Ty on C.system_type_id = Ty.system_type_id where T.Name = '" +
                                    tablename[i] + "'")
                                data = cursor.fetchall()
                                # for row in data[:len(tablenameLength)]:
                                #     print("data of table " + str((i + 1)) + " is: ", row.ColumnName, row.DataType)
                                # print("\n")
                                # endregion SqlQuery for column name and datatype

                                # region Code to create ENT file
                                entFileName = tablename[i] + 'ENT.cs'
                                path = './App_Code/ENT/'
                                with open(os.path.join(path, entFileName), 'w') as ent_file:
                                    ent_file.write(
                                        'using System;\nusing System.Collections.Generic;\nusing System.Data.SqlTypes;\nusing System.Linq;\nusing System.Web;\n')
                                    ent_file.write(
                                        '\n/// <summary>\n/// Summary description for ' + tablename[
                                            i] + 'ENT\n/// </summary>\n\n')
                                    ent_file.write('namespace ' + projectname + '.ENT\n')
                                    ent_file.write('{' + t1 + 'public class ' + tablename[i] + 'ENT' + t1 + '{' + t1)
                                    ent_file.write(t1 + '#region Constructor ' + t1 + 'public ' + tablename[
                                        i] + 'ENT()' + t1 + '{' + t2 + '//' + t2 + '// TODO: Add constructor logic here' + t2 + '//' + t1 + '}' + t1 + '#endregion Constructor' + t1)

                                    for row in data[:len(data)]:
                                        if row.DataType == 'int':
                                            ent_file.write('\n\t#region ' + row.ColumnName + '\n\n\tprotected ')
                                            ent_file.write(
                                                'SqlInt32 _' + row.ColumnName + ';\n\n\t' + 'public SqlInt32 ' + row.ColumnName + '\n\t{\n\t\tget\n\t\t{\n\t\t\treturn _' + row.ColumnName + ';\n\t\t}\t\t\n')
                                            ent_file.write(
                                                '\t\tset\n\t\t{\n\t\t\t_' + row.ColumnName + '= value;\n\t\t}\n\t}\n')
                                            ent_file.write('\n\t#endregion ' + row.ColumnName + '\n')
                                        if row.DataType == 'varchar':
                                            ent_file.write('\n\t#region ' + row.ColumnName + '\n\n\tprotected ')
                                            ent_file.write(
                                                'SqlString _' + row.ColumnName + ';\n\n\t' + 'public SqlString ' + row.ColumnName + '\n\t{\n\t\tget\n\t\t{\n\t\t\treturn _' + row.ColumnName + ';\n\t\t}\t\t\n')
                                            ent_file.write(
                                                '\t\tset\n\t\t{\n\t\t\t_' + row.ColumnName + '= value;\n\t\t}\n\t}\n')
                                            ent_file.write('\n\t#endregion ' + row.ColumnName + '\n')
                                        if row.DataType == 'date' or row.DataType == 'datetime':
                                            ent_file.write('\n\t#region ' + row.ColumnName + '\n\n\tprotected ')
                                            ent_file.write(
                                                'SqlDateTime _' + row.ColumnName + ';\n\n\t' + 'public SqlDateTime ' + row.ColumnName + '\n\t{\n\t\tget\n\t\t{\n\t\t\treturn _' + row.ColumnName + ';\n\t\t}\t\t\n')
                                            ent_file.write(
                                                '\t\tset\n\t\t{\n\t\t\t_' + row.ColumnName + '= value;\n\t\t}\n\t}\n')
                                            ent_file.write('\n\t#endregion ' + row.ColumnName + '\n')
                                        if row.DataType == 'decimal':
                                            ent_file.write('\n\t#region ' + row.ColumnName + '\n\n\tprotected ')
                                            ent_file.write(
                                                'SqlDecimal _' + row.ColumnName + ';\n\n\t' + 'public SqlDecimal ' + row.ColumnName + '\n\t{\n\t\tget\n\t\t{\n\t\t\treturn _' + row.ColumnName + ';\n\t\t}\t\t\n')
                                            ent_file.write(
                                                '\t\tset\n\t\t{\n\t\t\t_' + row.ColumnName + '= value;\n\t\t}\n\t}\n')
                                            ent_file.write('\n\t#endregion ' + row.ColumnName + '\n')
                                        if row.DataType == 'boolean':
                                            ent_file.write('\n\t#region ' + row.ColumnName + '\n\n\tprotected ')
                                            ent_file.write(
                                                'SqlBoolean _' + row.ColumnName + ';\n\n\t' + 'public SqlBoolean ' + row.ColumnName + '\n\t{\n\t\tget\n\t\t{\n\t\t\treturn _' + row.ColumnName + ';\n\t\t}\t\t\n')
                                            ent_file.write(
                                                '\t\tset\n\t\t{\n\t\t\t_' + row.ColumnName + '= value;\n\t\t}\n\t}\n')
                                            ent_file.write('\n\t#endregion ' + row.ColumnName + '\n')
                                    ent_file.write('\n\t}\n}\n')
                                # endregion Code to create ENT file

                                # region Code to create DAL file
                                dalFileName = tablename[i] + 'DAL.cs'
                                path = './App_Code/DAL/'
                                with open(os.path.join(path, dalFileName), 'w') as dal_file:
                                    # region Using Files
                                    dal_file.write('using ' + projectname + '.ENT;\n')
                                    dal_file.write(
                                        'using System;\nusing System.Collections.Generic;\nusing System.Data;\nusing System.Data.SqlClient;\nusing System.Data.SqlTypes;\nusing System.Linq;\nusing System.Web;\n')
                                    dal_file.write(
                                        '\n/// <summary>\n/// Summary description for ' + tablename[
                                            i] + 'DAL\n/// </summary>\n\n')
                                    # endregion Using Files

                                    # region Namespace started

                                    dal_file.write('namespace ' + projectname + '.DAL\n')
                                    # region Public Class
                                    dal_file.write(
                                        '{' + t1 + 'public class ' + tablename[
                                            i] + 'DAL : DatabaseConfig' + t1 + '{' + t1 + '')
                                    # region Constructor
                                    dal_file.write(t2 + '#region Constructor ' + t2 + 'public ' + tablename[
                                        i] + 'DAL()' + t2 + '{' + t3 + '//' + t3 + '// TODO: Add constructor logic here' + t3 + '//' + t2 + '}' + t2 + '#endregion Constructor' + t2 + '')
                                    # endregion Constructor

                                    # region Local Variable Message
                                    dal_file.write(t2 + '#region Local Variables')
                                    dal_file.write(
                                        t2 + 'protected string _Message;\n' + t2 + 'public string Message' + t2 + '{' + t3 + 'get' + t3 + '{' + t4 + 'return _Message;' + t3 + '}' + t3 + 'set' + t3 + '{' + t4 + '_Message = value;' + t3 + '}' + t2 + '}')
                                    dal_file.write(t2 + '#endregion Local Variables')
                                    # endregion Local Variable Message

                                    # region 1 Insert Operation
                                    dal_file.write('\n' + t2 + '#region Insert Operation')
                                    dal_file.write(
                                        t2 + 'public Boolean Insert(' + tablename[i] + 'ENT ent' + tablename[i] + ')')
                                    dal_file.write(t2 + '{')
                                    dal_file.write(
                                        '' + t3 + 'using (SqlConnection objConn = new SqlConnection(ConnectionString))')
                                    dal_file.write('' + t3 + '{')
                                    dal_file.write(
                                        t4 + 'objConn.Open();' + t4 + 'using (SqlCommand objCmd = objConn.CreateCommand())')
                                    dal_file.write(t4 + '{')
                                    dal_file.write(t5 + 'try')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + '#region Prepare Command')
                                    dal_file.write(t6 + 'objCmd.CommandType = CommandType.StoredProcedure;')
                                    dal_file.write(t6 + 'objCmd.CommandText = ' + insert)
                                    dal_file.write(t6 + 'objCmd.Parameters.Add("@' + tablename[
                                        i] + 'ID", SqlDbType.Int).Direction = ParameterDirection.Output;')

                                    for row in data[1:len(data)]:
                                        if (row.DataType == "varchar"):
                                            dal_file.write(
                                                t6 + 'objCmd.Parameters.AddWithValue("@' + row.ColumnName + '", SqlDbType.VarChar).Value = ' + 'ent' +
                                                tablename[i] + '.' + row.ColumnName + ';')
                                        if (row.DataType == "int"):
                                            dal_file.write(
                                                t6 + 'objCmd.Parameters.AddWithValue("@' + row.ColumnName + '", SqlDbType.Int).Value = ' + 'ent' +
                                                tablename[i] + '.' + row.ColumnName + ';')
                                        if (row.DataType == "date"):
                                            dal_file.write(
                                                t6 + 'objCmd.Parameters.AddWithValue("@' + row.ColumnName + '", SqlDbType.Date).Value = ' + 'ent' +
                                                tablename[i] + '.' + row.ColumnName + ';')
                                        if (row.DataType == "datetime"):
                                            dal_file.write(
                                                t6 + 'objCmd.Parameters.AddWithValue("@' + row.ColumnName + '", SqlDbType.DateTime).Value = ' + 'ent' +
                                                tablename[i] + '.' + row.ColumnName + ';')
                                        if (row.DataType == "decimal"):
                                            dal_file.write(
                                                t6 + 'objCmd.Parameters.AddWithValue("@' + row.ColumnName + '", SqlDbType.Decimal).Value = ' + 'ent' +
                                                tablename[i] + '.' + row.ColumnName + ';')
                                        if (row.DataType == "boolean"):
                                            dal_file.write(
                                                t6 + 'objCmd.Parameters.AddWithValue("@' + row.ColumnName + '", SqlDbType.Boolean).Value = ' + 'ent' +
                                                tablename[i] + '.' + row.ColumnName + ';')
                                    dal_file.write(t6 + '#endregion Prepare Command')
                                    dal_file.write('\n' + t6 + 'objCmd.ExecuteNonQuery();')
                                    dal_file.write(
                                        '\n' + t6 + 'if (objCmd.Parameters["@' + tablename[i] + 'ID"] != null)')
                                    dal_file.write(t7 + 'ent' + tablename[i] + '.' + tablename[
                                        i] + 'ID = Convert.ToInt32(objCmd.Parameters["@' + tablename[
                                                       i] + 'ID"].Value);')
                                    dal_file.write('\n' + t6 + 'return true;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (SqlException sqlex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = sqlex.Message.ToString();' + t6 + 'return false;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (Exception ex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = ex.Message.ToString();' + t6 + 'return false;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'finally')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(
                                        t6 + 'if (objConn.State == ConnectionState.Open)' + t7 + 'objConn.Close();')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t4 + '}')
                                    dal_file.write('' + t3 + '}')
                                    dal_file.write(t2 + '}')
                                    dal_file.write(t2 + '#endregion Insert Operation')
                                    # endregion 1 Insert Operation

                                    # region 2 Delete Operation
                                    dal_file.write('\n' + t2 + '#region Delete Operation')
                                    dal_file.write(t2 + 'public Boolean Delete(SqlInt32 ' + tablename[i] + 'ID)')
                                    dal_file.write(t2 + '{')
                                    dal_file.write(
                                        '' + t3 + 'using (SqlConnection objConn = new SqlConnection(ConnectionString))')
                                    dal_file.write('' + t3 + '{')
                                    dal_file.write(
                                        t4 + 'objConn.Open();' + t4 + 'using (SqlCommand objCmd = objConn.CreateCommand())')
                                    dal_file.write(t4 + '{')
                                    dal_file.write(t5 + 'try')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + '#region Prepare Command')
                                    dal_file.write(t6 + 'objCmd.CommandType = CommandType.StoredProcedure;')
                                    dal_file.write(t6 + 'objCmd.CommandText = ' + delete)
                                    dal_file.write(
                                        t6 + 'objCmd.Parameters.AddWithValue("@' + tablename[i] + 'ID", ' + tablename[
                                            i] + 'ID);')
                                    dal_file.write(t6 + '#endregion Prepare Command')
                                    dal_file.write('\n' + t6 + 'objCmd.ExecuteNonQuery();')
                                    dal_file.write('\n' + t6 + 'return true;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (SqlException sqlex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = sqlex.Message.ToString();' + t6 + 'return false;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (Exception ex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = ex.Message.ToString();' + t6 + 'return false;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'finally')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(
                                        t6 + 'if (objConn.State == ConnectionState.Open)' + t7 + 'objConn.Close();')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t4 + '}')
                                    dal_file.write('' + t3 + '}')
                                    dal_file.write(t2 + '}')
                                    dal_file.write(t2 + '#endregion Delete Operation')

                                    # endregion 2 Delete Operation

                                    # region 3 Update Operation
                                    dal_file.write('\n' + t2 + '#region Update Operation')
                                    dal_file.write(
                                        t2 + 'public Boolean Update(' + tablename[i] + 'ENT ent' + tablename[i] + ')')
                                    dal_file.write(t2 + '{')
                                    dal_file.write(
                                        '' + t3 + 'using (SqlConnection objConn = new SqlConnection(ConnectionString))')
                                    dal_file.write('' + t3 + '{')
                                    dal_file.write(
                                        t4 + 'objConn.Open();' + t4 + 'using (SqlCommand objCmd = objConn.CreateCommand())')
                                    dal_file.write(t4 + '{')
                                    dal_file.write(t5 + 'try')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + '#region Prepare Command')
                                    dal_file.write(t6 + 'objCmd.CommandType = CommandType.StoredProcedure;')
                                    dal_file.write(t6 + 'objCmd.CommandText = ' + update)

                                    for row in data[:len(data)]:
                                        dal_file.write(
                                            t6 + 'objCmd.Parameters.AddWithValue("@' + row.ColumnName + '", ent' +
                                            tablename[
                                                i] + '.' + row.ColumnName + ');')
                                    dal_file.write(t6 + '#endregion Prepare Command')
                                    dal_file.write('\n' + t6 + 'objCmd.ExecuteNonQuery();')
                                    dal_file.write('\n' + t6 + 'return true;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (SqlException sqlex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = sqlex.Message.ToString();' + t6 + 'return false;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (Exception ex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = ex.Message.ToString();' + t6 + 'return false;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'finally')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(
                                        t6 + 'if (objConn.State == ConnectionState.Open)' + t7 + 'objConn.Close();')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t4 + '}')
                                    dal_file.write('' + t3 + '}')
                                    dal_file.write(t2 + '}')
                                    dal_file.write(t2 + '#endregion Update Operation')
                                    # endregion 3 Update Operation

                                    # region 4 Select Operation

                                    dal_file.write(t2 + '#region Select Operation\n')

                                    # region Select All
                                    dal_file.write('\n' + t2 + '#region SelectAll')
                                    dal_file.write(t2 + 'public DataTable SelectAll()')
                                    dal_file.write(t2 + '{')
                                    dal_file.write(
                                        '' + t3 + 'using (SqlConnection objConn = new SqlConnection(ConnectionString))')
                                    dal_file.write('' + t3 + '{')
                                    dal_file.write(
                                        t4 + 'objConn.Open();' + t4 + 'using (SqlCommand objCmd = objConn.CreateCommand())')
                                    dal_file.write(t4 + '{')
                                    dal_file.write(t5 + 'try')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + '#region Prepare Command')
                                    dal_file.write(t6 + 'objCmd.CommandType = CommandType.StoredProcedure;')
                                    dal_file.write(t6 + 'objCmd.CommandText = ' + selectAll)
                                    dal_file.write(t6 + '#endregion Prepare Command')
                                    dal_file.write('\n' + t6 + '#region ReadData and Set Controls')
                                    dal_file.write(t6 + 'DataTable dt = new DataTable();')
                                    dal_file.write(t6 + 'using (SqlDataReader objSDR = objCmd.ExecuteReader())')
                                    dal_file.write(t6 + '{')
                                    dal_file.write(t7 + 'dt.Load(objSDR);')
                                    dal_file.write(t6 + '}')
                                    dal_file.write(t6 + 'return dt;')
                                    dal_file.write(t6 + '#endregion ReadData and Set Controls')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (SqlException sqlex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = sqlex.Message.ToString();' + t6 + 'return null;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (Exception ex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = ex.Message.ToString();' + t6 + 'return null;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'finally')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(
                                        t6 + 'if (objConn.State == ConnectionState.Open)' + t7 + 'objConn.Close();')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t4 + '}')
                                    dal_file.write('' + t3 + '}')
                                    dal_file.write(t2 + '}')
                                    dal_file.write(t2 + '#endregion SelectAll')
                                    # endregion Select All

                                    # region Select For Dropdown
                                    dal_file.write('\n' + t2 + '#region SelectForDropdown')
                                    dal_file.write(t2 + 'public DataTable SelectForDropdownList()')
                                    dal_file.write(t2 + '{')
                                    dal_file.write(
                                        '' + t3 + 'using (SqlConnection objConn = new SqlConnection(ConnectionString))')
                                    dal_file.write('' + t3 + '{')
                                    dal_file.write(
                                        t4 + 'objConn.Open();' + t4 + 'using (SqlCommand objCmd = objConn.CreateCommand())')
                                    dal_file.write(t4 + '{')
                                    dal_file.write(t5 + 'try')
                                    dal_file.write(t5 + '{')

                                    dal_file.write(t6 + '#region Prepare Command')
                                    dal_file.write(t6 + 'objCmd.CommandType = CommandType.StoredProcedure;')
                                    dal_file.write(t6 + 'objCmd.CommandText = ' + selectForDDL)
                                    dal_file.write(t6 + '#endregion Prepare Command')

                                    dal_file.write('\n' + t6 + '#region ReadData and Set Controls')
                                    dal_file.write(t6 + 'DataTable dt = new DataTable();')
                                    dal_file.write(t6 + 'using (SqlDataReader objSDR = objCmd.ExecuteReader())')
                                    dal_file.write(t6 + '{')
                                    dal_file.write(t7 + 'dt.Load(objSDR);')
                                    dal_file.write(t6 + '}')
                                    dal_file.write(t6 + 'return dt;')
                                    dal_file.write(t6 + '#endregion ReadData and Set Controls')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (SqlException sqlex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = sqlex.Message.ToString();' + t6 + 'return null;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (Exception ex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = ex.Message.ToString();' + t6 + 'return null;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'finally')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(
                                        t6 + 'if (objConn.State == ConnectionState.Open)' + t7 + 'objConn.Close();')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t4 + '}')
                                    dal_file.write('' + t3 + '}')
                                    dal_file.write(t2 + '}')
                                    dal_file.write(t2 + '#endregion SelectForDropdown')
                                    # endregion Select For Dropdown

                                    # region Select By PK
                                    dal_file.write('\n' + t2 + '#region SelectBYPK')
                                    dal_file.write(
                                        t2 + 'public ' + tablename[i] + 'ENT SelectByPK(SqlInt32 ' + tablename[
                                            i] + 'ID)')
                                    dal_file.write(t2 + '{')
                                    dal_file.write(
                                        '' + t3 + 'using (SqlConnection objConn = new SqlConnection(ConnectionString))')
                                    dal_file.write('' + t3 + '{')
                                    dal_file.write(
                                        t4 + 'objConn.Open();' + t4 + 'using (SqlCommand objCmd = objConn.CreateCommand())')
                                    dal_file.write(t4 + '{')
                                    dal_file.write(t5 + 'try')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + '#region Prepare Command')
                                    dal_file.write(t6 + 'objCmd.CommandType = CommandType.StoredProcedure;')
                                    dal_file.write(t6 + 'objCmd.CommandText = ' + selectByPK)
                                    dal_file.write(
                                        t6 + 'objCmd.Parameters.AddWithValue("@' + tablename[i] + 'ID",' + tablename[
                                            i] + 'ID);')
                                    dal_file.write(t6 + '#endregion Prepare Command\n')
                                    dal_file.write(t6 + '#region ReadData and Set Controls')
                                    dal_file.write(
                                        t6 + tablename[i] + 'ENT ent' + tablename[i] + ' = new ' + tablename[
                                            i] + 'ENT();')
                                    dal_file.write(t6 + 'using(SqlDataReader objSDR = objCmd.ExecuteReader())')
                                    dal_file.write(t6 + '{')
                                    dal_file.write(t7 + 'while (objSDR.Read())')
                                    dal_file.write(t7 + '{')
                                    for row in data[:len(data)]:
                                        if (row.DataType == "varchar"):
                                            dal_file.write(
                                                t8 + 'if (!objSDR["' + row.ColumnName + '"].Equals(DBNull.Value))')
                                            dal_file.write(t8 + '{')
                                            dal_file.write(t9 + 'ent' + tablename[
                                                i] + '.' + row.ColumnName + ' = Convert.ToString(objSDR["' + row.ColumnName + '"]);')
                                            dal_file.write(t8 + '}')
                                        if (row.DataType == "int"):
                                            dal_file.write(
                                                t8 + 'if (!objSDR["' + row.ColumnName + '"].Equals(DBNull.Value))')
                                            dal_file.write(t8 + '{')
                                            dal_file.write(t9 + 'ent' + tablename[
                                                i] + '.' + row.ColumnName + ' = Convert.ToInt32(objSDR["' + row.ColumnName + '"]);')
                                            dal_file.write(t8 + '}')
                                        if (row.DataType == "date" or row.DataType == "datetime"):
                                            dal_file.write(
                                                t8 + 'if (!objSDR["' + row.ColumnName + '"].Equals(DBNull.Value))')
                                            dal_file.write(t8 + '{')
                                            dal_file.write(t9 + 'ent' + tablename[
                                                i] + '.' + row.ColumnName + ' = Convert.ToDateTime(objSDR["' + row.ColumnName + '"]);')
                                            dal_file.write(t8 + '}')
                                        if (row.DataType == "boolean"):
                                            dal_file.write(
                                                t8 + 'if (!objSDR["' + row.ColumnName + '"].Equals(DBNull.Value))')
                                            dal_file.write(t8 + '{')
                                            dal_file.write(t9 + 'ent' + tablename[
                                                i] + '.' + row.ColumnName + ' = Convert.ToBoolean(objSDR["' + row.ColumnName + '"]);')
                                            dal_file.write(t8 + '}')
                                        if (row.DataType == "decimal"):
                                            dal_file.write(
                                                t8 + 'if (!objSDR["' + row.ColumnName + '"].Equals(DBNull.Value))')
                                            dal_file.write(t8 + '{')
                                            dal_file.write(t9 + 'ent' + tablename[
                                                i] + '.' + row.ColumnName + ' = Convert.ToDecimal(objSDR["' + row.ColumnName + '"]);')
                                            dal_file.write(t8 + '}')
                                    dal_file.write(t7 + '}')
                                    dal_file.write(t6 + '}')
                                    dal_file.write('\n' + t6 + 'return ent' + tablename[i] + ';')
                                    dal_file.write(t6 + '#endregion ReadData and Set Controls')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (SqlException sqlex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = sqlex.Message.ToString();' + t6 + 'return null;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'catch (Exception ex)')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(t6 + 'Message = ex.Message.ToString();' + t6 + 'return null;')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t5 + 'finally')
                                    dal_file.write(t5 + '{')
                                    dal_file.write(
                                        t6 + 'if (objConn.State == ConnectionState.Open)' + t7 + 'objConn.Close();')
                                    dal_file.write(t5 + '}')
                                    dal_file.write(t4 + '}')
                                    dal_file.write('' + t3 + '}')
                                    dal_file.write(t2 + '}')
                                    dal_file.write(t2 + '#endregion SelectBYPK')
                                    # endregion Select By PK

                                    dal_file.write(t2 + '#endregion Select Operation')

                                    # endregion 4 Select Operation

                                    dal_file.write(t1 + '}\n}')
                                    # endregion Public Class

                                    # endregion Namespace started

                                # endregion Code to create DAL file

                                # region Code to create BAL file
                                balFileName = tablename[i] + 'BAL.cs'
                                path = './App_Code/BAL/'
                                with open(os.path.join(path, balFileName), 'w') as bal_file:
                                    # region import statement :
                                    bal_file.write(
                                        'using ' + projectname + '.ENT;\nusing ' + projectname + '.DAL;\nusing System;\nusing System.Collections.Generic;\nusing System.Data;\nusing System.Data.SqlTypes;\nusing System.Linq;\nusing System.Web;\n')
                                    bal_file.write(
                                        '\n/// <summary>\n/// Summary description for ' + tablename[
                                            i] + 'BAL\n/// </summary>\n\n')
                                    # endregion import statement:

                                    # region namespace:
                                    bal_file.write('namespace ' + projectname + '.BAL\n')

                                    # region public class:
                                    bal_file.write('{\n\tpublic class ' + tablename[i] + 'BAL' + t1 + '{' + t1)
                                    # region  constructor:
                                    bal_file.write(t2 + '#region Constructor' + t2 + 'public ' + tablename[
                                        i] + 'BAL()' + t2 + '{' + t3 + '//' + t3 + '// TODO: Add constructor logic here' + t3 + '//' + t2 + '}' + t2 + '#endregion Constructor')
                                    bal_file.write('\n')
                                    # endregion constructor:

                                    # region  local variable:
                                    bal_file.write(t2 + '#region Local Variable')
                                    bal_file.write('\n')
                                    bal_file.write(t2 + 'protected string _Message;')
                                    bal_file.write('\n')
                                    bal_file.write(t2 + 'public string Message')
                                    bal_file.write(t2 + '{')
                                    bal_file.write(t3 + 'get')
                                    bal_file.write(t3 + '{')
                                    bal_file.write(t4 + 'return _Message;')
                                    bal_file.write(t3 + '}')
                                    bal_file.write(t3 + 'set')
                                    bal_file.write(t3 + '{')
                                    bal_file.write(t4 + ' _Message = value;')
                                    bal_file.write(t3 + '}')
                                    bal_file.write(t2 + '}')
                                    bal_file.write(t2 + '#endregion Local Variable\n')
                                    # endregion local variable:

                                    # region  insert operation:
                                    bal_file.write(t2 + '#region Insert Operation')
                                    bal_file.write(
                                        t2 + 'public Boolean Insert(' + tablename[i] + 'ENT ent' + tablename[i] + ')')
                                    bal_file.write(t2 + '{')
                                    bal_file.write(
                                        t3 + tablename[i] + 'DAL dal' + tablename[i] + ' = new ' + tablename[
                                            i] + 'DAL();')
                                    bal_file.write(t3 + 'if (dal' + tablename[i] + '.Insert(ent' + tablename[i] + '))')
                                    bal_file.write(t3 + '{')
                                    bal_file.write(t4 + 'return true;')
                                    bal_file.write(t3 + '}')
                                    bal_file.write(t3 + 'else')
                                    bal_file.write(t3 + '{')
                                    bal_file.write(t4 + 'Message = dal' + tablename[i] + '.Message;')
                                    bal_file.write(t4 + 'return false;')
                                    bal_file.write(t3 + '}')
                                    bal_file.write(t2 + '}')
                                    bal_file.write(t2 + '#endregion Insert Operation\n')
                                    # endregion insert operation:

                                    # region  update operation:
                                    bal_file.write(t2 + '#region Update Operation')
                                    bal_file.write(
                                        t2 + 'public Boolean Update(' + tablename[i] + 'ENT ent' + tablename[i] + ')')
                                    bal_file.write(t2 + '{')
                                    bal_file.write(
                                        t3 + tablename[i] + 'DAL dal' + tablename[i] + ' = new ' + tablename[
                                            i] + 'DAL();')
                                    bal_file.write(t3 + 'if (dal' + tablename[i] + '.Update(ent' + tablename[i] + '))')
                                    bal_file.write(t3 + '{')
                                    bal_file.write(t4 + 'return true;')
                                    bal_file.write(t3 + '}')
                                    bal_file.write(t3 + 'else')
                                    bal_file.write(t3 + '{')
                                    bal_file.write(t4 + 'Message = dal' + tablename[i] + '.Message;')
                                    bal_file.write(t4 + 'return false;')
                                    bal_file.write(t3 + '}')
                                    bal_file.write(t2 + '}')
                                    bal_file.write(t2 + '#endregion Update Operation\n')
                                    # endregion Update operation:

                                    # region  Delete operation:
                                    bal_file.write(t2 + '#region Delete Operation')
                                    bal_file.write(t2 + 'public Boolean Delete(SqlInt32 ' + tablename[i] + 'ID)')
                                    bal_file.write(t2 + '{')
                                    bal_file.write(
                                        t3 + tablename[i] + 'DAL dal' + tablename[i] + ' = new ' + tablename[
                                            i] + 'DAL();')
                                    bal_file.write(t3 + 'if (dal' + tablename[i] + '.Delete(' + tablename[i] + 'ID))')
                                    bal_file.write(t3 + '{')
                                    bal_file.write(t4 + 'return true;')
                                    bal_file.write(t3 + '}')
                                    bal_file.write(t3 + 'else')
                                    bal_file.write(t3 + '{')
                                    bal_file.write(t4 + 'Message = dal' + tablename[i] + '.Message;')
                                    bal_file.write(t4 + 'return false;')
                                    bal_file.write(t3 + '}')
                                    bal_file.write(t2 + '}')
                                    bal_file.write(t2 + '#endregion Delete Operation\n')
                                    # endregion Delete operation:

                                    # region  select operation
                                    bal_file.write(t2 + '#region Select Operation\n')

                                    # region  select all
                                    bal_file.write(t2 + '#region Select All')
                                    bal_file.write(t2 + 'public DataTable SelectAll()')
                                    bal_file.write(t2 + '{')
                                    bal_file.write(
                                        t3 + tablename[i] + 'DAL dal' + tablename[i] + ' = new ' + tablename[
                                            i] + 'DAL();')
                                    bal_file.write(t3 + 'return dal' + tablename[i] + '.SelectAll();')
                                    bal_file.write(t2 + '}')
                                    bal_file.write(t2 + '#endregion Select All\n')
                                    # endregion select all

                                    # region  SelectForDropdownList
                                    bal_file.write(t2 + '#region SelectForDropdownList')
                                    bal_file.write(t2 + 'public DataTable SelectForDropdownList()')
                                    bal_file.write(t2 + '{')
                                    bal_file.write(
                                        t3 + tablename[i] + 'DAL dal' + tablename[i] + ' = new ' + tablename[
                                            i] + 'DAL();')
                                    bal_file.write(t3 + 'return dal' + tablename[i] + '.SelectForDropdownList();')
                                    bal_file.write(t2 + '}')
                                    bal_file.write(t2 + '#endregion SelectForDropdownList\n')
                                    # endregion SelectForDropdownList

                                    # region  SelectByPK
                                    bal_file.write(t2 + '#region SelectByPK')
                                    bal_file.write(
                                        t2 + 'public ' + tablename[i] + 'ENT SelectByPK(SqlInt32 ' + tablename[
                                            i] + 'ID)')
                                    bal_file.write(t2 + '{')
                                    bal_file.write(
                                        t3 + tablename[i] + 'DAL dal' + tablename[i] + ' = new ' + tablename[
                                            i] + 'DAL();')
                                    bal_file.write(
                                        t3 + 'return dal' + tablename[i] + '.SelectByPK(' + tablename[i] + 'ID);')
                                    bal_file.write(t2 + '}')
                                    bal_file.write(t2 + '#endregion SelectByPK\n')
                                    # endregion SelectByPK

                                    bal_file.write(t2 + '#endregion Select Operation')
                                    # endregion  select operation
                                    bal_file.write(t1 + '}\n}')
                                    # endregion public class:

                                    # endregion namespace:

                                # endregion Code to create BAL fil

                                # region Database Config
                                DatabaseConfigFileName = 'DatabaseConfig.cs'
                                path = './App_Code/'
                                with open(os.path.join(path, DatabaseConfigFileName), 'w') as databaseConfig_file:
                                    databaseConfig_file.write(
                                        'using System;\nusing System.Collections.Generic;\nusing System.Configuration;\nusing System.Linq;\nusing System.Web;\n')
                                    databaseConfig_file.write(
                                        '\n/// <summary>\n/// Summary description for DataConfig' + '\n/// </summary>\n\n')
                                    databaseConfig_file.write('namespace ' + DatabaseName + '\n')
                                    databaseConfig_file.write('{' + t1 + 'public class DatabaseConfig' + t1 + '{' + t1)
                                    databaseConfig_file.write(
                                        t2 + '#region Constructor ' + t2 + 'public DatabaseConfig()' + t2 + '{' + t3 + '//' + t3 + '// TODO: Add constructor logic here' + t3 + '//' + t2 + '}' + t2 + '#endregion Constructor' + t2)
                                    databaseConfig_file.write(t2 + '#region Connection String')
                                    databaseConfig_file.write(
                                        t2 + 'public static string ConnectionString = ConfigurationManager.ConnectionStrings["' + DatabaseName + 'ConnectionString"].ConnectionString.ToString();')
                                    databaseConfig_file.write(t2 + '#endregion Connection String')
                                    databaseConfig_file.write(t1 + '}\n}')
                                # endregion Database Config

                            # endregion Code to Create Files
                            window.quit()
                        except(pyodbc.OperationalError, pyodbc.InterfaceError) as e:
                            messagebox.showinfo('Error!!!', e)
                except(pyodbc.OperationalError, pyodbc.InterfaceError) as e:
                    print(e)
                    messagebox.showwarning('Database OR Server Name is Invalid',
                                           'Please Enter Valid Server Name Or Database Name.')
            # endregion validation

        # endregion submit button function
        
        self.window = window
        # self.window.attributes('-fullscreen', True)
        self.window.geometry("1366x720+0+0")
        self.window.title("Three Tier File Generator")
        self.window.iconbitmap('images/books.ico')
        self.window.resizable(False, False)
        self.database_frame = ImageTk.PhotoImage \
            (file='images/connect_database_frame_new.png')

        self.image_panel = Label(self.window, image=self.database_frame)
        self.image_panel.pack(fill='both', expand='yes')

        self.txt = "Three Tier File Generator"
        self.count = 0
        self.text = ''
        self.color = ["#4f4e4d", "#f29844", "red2"]
        self.heading = Label(self.window, text=self.txt, font=("yu gothic ui", 30, "bold"), bg="white", fg="#4f4e4d",
                             bd=5, relief=FLAT)
        self.heading.place(x=485, y=200
                           , width=450)
        self.slider()
        self.heading_color()

        #     ==================Declaring Labels

        # ==================Host Label and Entry==================
        self.host_label = Label(self.window, text="Server Name", bg="white", fg="#4f4e4d",
                                font=("yu gothic ui", 13, "bold"))
        self.host_label.place(x=505, y=299)

        self.host_entry = Entry(self.window, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui semibold", 12))
        self.host_entry.place(x=530, y=332, width=380)
        

        # ==================Port Label and Entry==================
        self.port_label = Label(self.window, text="Database Name", bg="white", fg="#4f4e4d",
                                font=("yu gothic ui", 13, "bold"))
        self.port_label.place(x=505, y=395)

        self.port_entry = Entry(self.window, relief=FLAT, bg="white", fg="#6b6a69", font=("yu gothic ui semibold", 12))
        self.port_entry.place(x=530, y=428, width=380)

        self.login = ImageTk.PhotoImage \
            (file='images/submit_button.png')

        self.login_button = Button(self.window, image=self.login, relief=FLAT, borderwidth=0, background="white",
                                   activebackground="white", cursor="hand2", command=page)
        self.login_button.place(x=640, y=490)

    def slider(self):
        pass
        # if self.count >= len(self.txt):
        #     self.count = -1
        #     self.text = ''
        #     self.heading.config(text=self.text)
        #
        # else:
        #     self.text = self.text + self.txt[self.count]
        #     self.heading.config(text=self.text)
        #
        # self.count += 1
        #
        # self.heading.after(130, self.slider)

    def heading_color(self):
        pass
        # fg = random.choice(self.color)
        # self.heading.config(fg=fg)
        # self.heading.after(75, self.heading_color)


def win():
    window = Tk()
    ConnectDatabase(window)
    window.mainloop()


if __name__ == '__main__':
    win()