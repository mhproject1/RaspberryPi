##########################################################################################
### import ###

from tkinter import *
from tkinter import messagebox

### MySQLdb에 접속한다 ###
import MySQLdb
##########################################################################################
def SUBMIT():  
    # button event로 button을 누르면 
    # 메세지 박스의 제목이 MYSQL DB COMMIT고
    # 내용은 Your context was saved!을 출력한다
    messagebox.showinfo("MYSQL DB COMMIT", "Your context Refresh!")

    ### Text 위젯의 데이터를 삭제한다 ###
    # db에서 데이터를 읽어와서 출력할 때
    # 출력이 남아있음을 방지하기 위해서 이미 출력된 것들을 제거하고 새로 출력해야한다
    # 예를들어 21:34:54 ~ ~
    #        21:36:51 ~ ~ 이라는 방명록 두 개의 기록이 이미 존재할 때
    # 새로운 방명록 기록인 22:34:17을 추가하면
    # 22:34:17 ~ ~
    # 21:34:54 ~ ~
    # 21:36:51 ~ ~
    # 21:34:54 ~ ~
    # 21:36:51 ~ ~ 
    # 와 같이 출력이 밀리게 되므로 기존의 두 개의 기록을 지우고 다시 출력해주기 위해
    # delete() 함수를 사용해서 제거한다
    e1.delete(1.0,END)
    e2.delete(1.0,END)
    e3.delete(1.0,END)

    ### db에 데이터를 가져온다 ###
    # database랑 연결된 connection MySQLdb로부터 Dictionary Cursor 생성
    # Dictionary Cursor란 Key와 Value를 한 쌍으로 갖는 자료형으로, 
    # DictCursor 옵션을 주면 Row결과를 Dictionary형태로 리턴한다
    # cur.execute로 db 쿼리문을 실행한다
    db = MySQLdb.connect("localhost", "pi", "test", "test")
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT date_format(gtime,'%H:%i:%s'), gname, gtext FROM GUESTBOOK")    
    
    while True:
        # cur.fetchone() : 가져온 db 데이터를 한 줄씩 읽어온다
        # GUESTBOOK 테이블에 저장된 데이터 값을 insert() method를 사용해서 읽어온다
        # >>> 과제 3-1.py ### db에 데이터를 삽입한다 ###
        GUEST = cur.fetchone()
        if not GUEST: break

        ############################################################
        # Text 입력창에서 입력한 문자의 개수가 어느정도 커지면
        # 줄바꿈을 해주기 위해서 fetchone으로 얻어온 Text 크기의
        # 라인 수를 계산해서 현재 Text 위젯의 한 줄 개수(45)로 나눈다
        # Text 위젯의 크기가 달라지면 le/45에서 45를 수정된 개수로 수정해야함
        # len() 함수로 얻어온 Text의 길이에서 Text위젯의 한 줄 개수를 나눈 숫자가
        # 소숫점일 가능성이 매우 크므로 변수를 integer 형식으로 변환시켜야 한다
        # 예를들어 변환시킨 intTexT가 1이면 읽어온 gtext가 2줄이라는 뜻이다
        # gtext는 두줄이지만 gtime과 gname은 한줄이므로 출력되는 라인을 맞춰주기 위해
        # gtime과 gname에도 널문자를 하나씩 추가해줘야 한다
        # intTexT가 0보다 크면 2줄 이상이라는 뜻이므로
        # nul이라는 변수에 intTexT-1의 개수만큼 \n를 추가한다
        le = len(GUEST["gtext"])
        TexT = le / 45        
        intTexT = int(TexT)
        nul = ''
        
        if intTexT > 0:
            while intTexT > 0:
                nul = nul + "\n"
                intTexT = intTexT-1
        ############################################################
        
        e1.insert(1.0, GUEST["date_format(gtime,'%H:%i:%s')"] + "\n\n" + str(nul))
        e2.insert(1.0, GUEST["gname"] + "\n\n" + str(nul))
        e3.insert(1.0, GUEST["gtext"] + "\n\n")
        print(GUEST["date_format(gtime,'%H:%i:%s')"], GUEST["gname"], GUEST["gtext"])
##########################################################################################    

# tkinter widget setting
GBT = Tk()
GBT.title("Guestbook using MySQL")
GBT.geometry("640x640+100+100")

B1 = Button(GBT, text="Refresh", command=SUBMIT)
B1.grid(row=0, column=0)

Label(GBT, text="Time", background="white").grid(row=1, column=0)
e1 = Text(GBT, width=10, height=35, borderwidth=0, background="lightgray")
e1.grid(row=2, column=0)

Label(GBT, text="Name", background="white").grid(row=1, column=3)
e2 = Text(GBT, width=20, height=35, borderwidth=0, background="lightgray")
e2.grid(row=2, column=3)

Label(GBT, text="Contents", background="white").grid(row=1, column=5)
e3 = Text(GBT, width=45, height=35, borderwidth=0, background="lightgray")
e3.grid(row=2, column=5)
##########################################################################################

# database랑 연결된 connection MySQLdb로부터 Dictionary Cursor 생성
# cur.execute로 db 쿼리문을 실행한다
db = MySQLdb.connect("localhost", "pi", "test", "test")
cur = db.cursor(MySQLdb.cursors.DictCursor)
cur.execute("SELECT date_format(gtime,'%H:%i:%s'), gname, gtext FROM GUESTBOOK")

### 프로그램이 실행되자마자 읽어온 데이터를 텍스트에 삽입한다 ###
while TRUE:
    #cur.fetchone() : 읽어온 db 데이터를 한 줄씩 읽어온다
    # GUESTBOOK 테이블에 저장된 데이터 값을 insert() method를 사용해서 읽어온다
    GUEST = cur.fetchone()
    if not GUEST: break
    ############################################################
    le = len(GUEST["gtext"])
    TexT = le / 45
    intTexT = int(TexT)
    nul = ''
    if intTexT > 0:
        while intTexT > 0:
            nul = nul + "\n"
            intTexT = intTexT-1
    ############################################################
    e1.insert(1.0, GUEST["date_format(gtime,'%H:%i:%s')"] + "\n\n" + str(nul))
    e2.insert(1.0, GUEST["gname"] + "\n\n" + str(nul))
    e3.insert(1.0, GUEST["gtext"] + "\n\n")

GBT.mainloop()
##########################################################################################
