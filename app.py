from dbcreds import *
import mariadb
#rEAD hERE I just copy pasted all o0f the error handling stuff over. 
def type_username():
  conn=None
  cursor=None
  
  try:
    conn= mariadb.connect(host=host,port=port,database=database,user=user, password=password)
    cursor = conn.cursor()
    return (conn, cursor)
  except mariadb.OperationalError as e:
    print('got an operational error')
    if(("Access Denied" in e.msg)):
      print("failed to login")
    disconnect_db()
    
def disconnect_db(conn,cursor):
  if(cursor != None):
    cursor.close()
  if(conn != None):
    conn.rollback()
    conn.close()
    
def run_query(statement,args=None):
  try:
    (conn, cursor) = type_username()
    if statement.startswith("SELECT"):
      cursor.execute(statement, args)
      result = cursor.fetchall()
      print("total of {} users".format(cursor.rowcount))
      return(result)
    else:
      cursor.execute(statement, args)
      if cursor.rowcount == 1:
        conn.commit()
        print("query successful")
      else: 
        print("query failed")
      
      # conn.commit()
      
  except mariadb.OperationalError as e:
    print('got an operational error')
    if(("Access Denied" in e.msg)):
      print("failed to login")
      
        
  except mariadb.IntegrityError as e:
    if("CONSTRAINT `user_CHECK_username`" in e.msg):
      print("error, all usernames should start with J")
    elif("CONSTRAINT `user_CHECK_age`" in e.msg):
      print("error, user is out of acceptable range")
    elif("dUPLICATE ENTRY" in e.msg):
      print("user already exists")
    else:
    # print("Integrity error")
      print(e.msg)

  except mariadb.ProgrammingError as e:
    if("SQL syntax" in e.msg):
      print("apparently you cant type")
    else:
      print("got a differnet programming error")
    print(e.msg)
    
  except RuntimeError as e:
    print('caught a runtime error')
    e.with_traceback
  # always have a catch all statement at the end, and give it an alias
  except Exception as e:
    print(e.with_traceback)
    print(e.msg)
    
  finally:
    disconnect_db(conn, cursor)
    
# blog_post = run_query("INSERT INTO blog_post (username, content, id) VALUES (?,?,?)", ['2User', '2Tweet', '2'])
# rEAD hERE above is a hard coded insert that worked, need to figure out how to make a post

blog_post = run_query("SELECT content FROM blog_post WHERE id = 2")



# print(input('Enter username'))
# rEAD hERE this allows me to type the name, but it doesnt store it. It's not connected to anything

# I dont think I can do this. I think I need to do the select where username = ? [username]
# rEAD hERE, i think i can add these in below to add the next 2 user options once I get the input for the username done
# this only gives the option of choosing what they want to do, no username though
# print('1.Create New Post')
# print('2.See Posts')

# user_choice = input('Choose from the following: ')
# if user_choice in ('1','2'):
#   create_post = (input('Create A New Post'))
#   see_posts = (input('See posts'))
  
#   if user_choice == '1':
#     print ("placeholder")
#   elif user_choice == '2':
#     print ("placeholder")
#   else:
#     print ('error')






