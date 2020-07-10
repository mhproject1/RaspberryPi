##########################################################################################
### import ###

from tkinter import *
from tkinter import messagebox

### MySQLdb에 접속한다 ###
import MySQLdb
##########################################################################################

def Guestbook():
    # button event로 button을 누르면 
    # 메세지 박스의 제목이 MYSQL DB COMMIT고
    # 내용은 Your context was saved!을 출력한다
    messagebox.showinfo("MYSQL DB COMMIT", "Your context was saved!")

    ### Text에 입력된 문자열을 get 메소드로 읽어오면 ###
    ### text\n 형태로 읽어오게 되는데, db에 저장하기 위해서 ###
    ### \n를 제거하는 과정이다 ###
    # e1, e2 Text에 입력된 문자열을 읽어온다
    # e1, e2에 저장된 문자열의 마지막 인덱스를 제거한다
    GBNAME = e1.get(1.0, END)
    GBNAME = GBNAME[:-1]
    GBTEXT = e2.get(1.0, END)
    GBTEXT = GBTEXT[:-1]    
    
    ### db에 데이터를 삽입한다 ###
    # database랑 연결된 connection MySQLdb로부터 Dictionary Cursor 생성
    # Dictionary Cursor란 Key와 Value를 한 쌍으로 갖는 자료형으로, 
    # DictCursor 옵션을 주면 Row결과를 Dictionary형태로 리턴한다
    # execute() : db 쿼리문을 실행한다
    # commit() : db를 저장한다
    db = MySQLdb.connect("localhost", "pi", "test", "test")
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("insert into GUESTBOOK(gname, gtext) values(%s, %s)", (GBNAME, GBTEXT))
    db.commit()
    
    ### db 쿼리문을 실행한다 ###
    # cur.execute로 db 쿼리문을 실행한다
    # cur.description으로 col에 대한 field명을 읽어온다 >> gtime, gname, gtext
    # 읽어온 데이터를 출력한다.
    # data_format(TIME, '%H,%i,%s') : TIMESTAMP의 시간부분만 출력한다
    cur.execute("SELECT * FROM GUESTBOOK")
    d = cur.description 
    print("SELECT date_format(gtime,'%H:%i:%s'), gname, gtext FROM GUESTBOOK");

    ### 읽어온 데이터를 출력한다 ###
    # cur.fetchone() : 읽어온 db 데이터를 한 줄씩 읽어온다
    # if not GUEST: break : 마지막 라인되면 끝
    # cur.fetchone() 1) <-
    # print 1)	     2)
    #   	     3)
    # cur.fetchone() 1)
    # print 2)	     2) <-
    # 		     3)
    # cur.fetchone() 1)
    # print(3)	     2)
    # break          3) <-
    while True:
        GUEST = cur.fetchone()
        if not GUEST: break
        print(GUEST["gtime"], GUEST["gname"], GUEST["gtext"])   
##########################################################################################

# tkinter widget setting
GB = Tk()
GB.title("Guestbook using MySQL")
GB.geometry("640x640+100+100")

Label(GB, text="Name :").grid(row=0, column=0)
e1 = Text(GB, width=55, height=1)
e1.grid(row=0, column=1)

Label(GB, text="content :").grid(row=1, column=0)
e2 = Text(GB, width=55, height=34)
e2.grid(row=1, column=1)

Button(GB, text="Submit", command=Guestbook).grid(row=2, column=1)

GB.mainloop()
##########################################################################################
