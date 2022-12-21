import flet as ft
from flet import *
import threading
from firebase import Firebase
import random
import requests
import time
from twilio.rest import Client 
import matplotlib
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import threading
import ctypes

global database,auth,firebase,pas,current_page,multi_task
multi_task=None
current_page=-1
def kill_thread(thread):
    """
    thread: a threading.Thread object
    """
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
        print('Exception raise failure')
def pas():
    pass
firebaseConfig = {
'apiKey': "AIzaSyCzfKlBmQQMaohi0T-oG2w5fUdUjeeH96Y",
'authDomain': "sagar-test-we.firebaseapp.com",
'databaseURL': "https://sagar-test-we-default-rtdb.firebaseio.com",
'storageBucket': "sagar-test-we.appspot.com",
}

firebase=Firebase(firebaseConfig)

auth=firebase.auth()

database=firebase.database()



def main(page:Page):
    global number,OTP
    page.title='Elections 2022'
    page.scroll='auto'
    page.vertical_alignment='center'
    page.horiznotal_alingement='Centre'
    def show_live_vote():
        global counts,color,total,current_page
        def update_vote():
            global counts,color,total
            if current_page==1:
                if database.child('TOTAL').get().val()==total:
                    pass
                else:
                    total=database.child('TOTAL').get().val()
                    ax.clear()
                    party_name = ["BJP", "BSP", "CONGRESS", "CPIM","JDU",'RJD',"NOTA"]
                    party_name2=[]
                    counts=[]
                    di={}
                    for i in party_name:
                        di['value']=database.child(i).get().val()
                        counts.append(di['value'])
                    party_name2=[]
                    for i in party_name:
                        party_name2.append(f"{i} ({counts[party_name.index(i)]})")
                    party_name.append('TOTAL')
                    counts.append(0)
                    party_name2.append(f"TOTAL ({total})")
                    patches, texts = plt.pie(counts, colors=color, shadow=True, startangle=90)
                    plt.legend(patches, party_name2, loc="best")

                    page.update()

                update_vote()
            else:
                pass
        page.controls.clear()
        page.add(ft.Row([ft.Column([ft.Text("", size=200, weight=ft.FontWeight.W_800),ft.ProgressRing(), ft.Text("Loading Data...",size=20, weight=ft.FontWeight.W_800)],horizontal_alignment=ft.CrossAxisAlignment.CENTER,)],alignment='center'))
        fig,ax=plt.subplots()
        party_name = ["BJP", "BSP", "CONGRESS", "CPIM","JDU",'RJD',"NOTA"]
        counts=[]
        di={}
        party_name2=[]
        total=database.child('TOTAL').get().val()
        for i in party_name:
            di['value']=database.child(i).get().val()
            counts.append(di['value'])
        for i in party_name:
            party_name2.append(f"{i} ({counts[party_name.index(i)]})")
        color=['orange','blue','green','red','cyan','pink','black','violet']
        party_name.append('TOTAL')
        counts.append(0)
        party_name2.append(f"TOTAL ({total})")
        patches, texts = plt.pie(counts, colors=color, shadow=True, startangle=90)
        if current_page==1:
            page.controls.clear()
            plt.legend(patches, party_name2, loc="best")
            page.add(ft.ResponsiveRow(page.add(ft.Row([ft.Text("", size=50, weight=ft.FontWeight.W_800, selectable=True)],alignment='center'))))
            page.add(ft.ResponsiveRow([MatplotlibChart(fig, expand=True,col={"sm": 12, "md": 12, "xl": 6})],alignment='center'))
            page.update()
            threading.Thread(target=update_vote()).start()
        else:
            pass
    def load_about():
        page.add(ft.Row([ft.Text("""
Welcome to Online Voting System

This website is created by Sagar Kumar

Features of this site:
1. Vote from anywhere anytime
2. Shows live vote

Why to use Online Voting System over offline voting system?

1. Cost: It is much cheaper to make a website and deploy  it online than make multiple EVM’s(Electronic voting machine).
2. Security: The vote is stored on multiple servers so if someone tries to hack and manipulate the votes he/she has to hack into all those servers.
3. Speed: Online voting systems can provide faster results, as votes are counted and tabulated automatically in real-time.
4. Convenience: With online voting, users can cast their votes from anywhere they just need a internet connection. 
5. Voter Participation: In 2019 elections voter participation was just 67% and still it was highest of all time by implementing online voting system we can increase voter participation to 95%.
5. Legitimacy: Online voting system is more legitimate because votes are shown live so no one can decrease the vote count of a party.
6. Environmental friendly: Paper ballot and EVM’s have no use after elections due to which increases waste. Also they need to be transported to polling stations.

Overall, the benefits of online voting systems include Cost, Security, Speed, Convenience , and Environmental friendly. By highlighting these points in the about section of your website, you can demonstrate the value and superiority of your live voting system compared to traditional offline voting methods.

""")],alignment='center'))
    def change_page(name):
        global current_page,multi_task
        if current_page==name:
            pass
        else:
            try:
                kill_thread(multi_task)
            except:
                pass
            page.controls.clear()
            current_page=name
            if name==0:
                multi_task=threading.Thread(target=initialize)
                multi_task.start()
            if name==1:
                multi_task=threading.Thread(target=show_live_vote)
                multi_task.start()
            if name==2:
                load_about()
            page.update()
    #--------------------------------------------------------------------------------

    #--------------------------------------------------------------------------------
    def retur():
        def return_home():
            def open_dlg(e):
                page.dialog = dlg_modal
                dlg_modal.open = True
                page.update()
            def close_dlg(e):
                dlg_modal.open = False
                if e=='yes':
                    initialize()
                else:
                    pass
                page.update()
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Do You Want To Exit"),
                content=ft.Text("Please Confirm"),
                actions=[
                    ft.TextButton("Yes", on_click=lambda e:close_dlg('yes')),
                    ft.TextButton("No", on_click=lambda e:close_dlg('no')),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )
            open_dlg('pass')
        return_home()
    def extract_vote():
        global c1,c2,c3,c4,c5,c6,c7,user_number
        data=database.child('users').child(user_number).get().val()
        if data==None:
            pass
        else:
            open_banner("You can't vote twice")
            initialize()
            return 'invalid'
        di={c1:'BJP',c2:'RJD',c3:'JDU',c4:'CONGRESS',c5:'BSP',c6:'CPIM',c7:'NOTA'}
        for i in list(di.keys()):
            if i.value==True:
                party=di[i]
                total=database.child('TOTAL').get().val()
                total+=1
                database.child('TOTAL').set(total)
                party_vote=database.child(party).get().val()
                party_vote+=1
                database.child(party).set(party_vote)
                database.child('users').update({str(user_number):""})
    def proceed_voting():
        global database,auth,firebase
        def submit_vote():
            def open_dlg(e):
                global c1,c2,c3,c4,c5,c6,c7
                di={c1:'BJP',c2:'RJD',c3:'JDU',c4:'CONGRESS',c5:'BSP',c6:'CPIM',c7:'NOTA'}
                for i in list(di.keys()):
                    if i.value==True:
                        break
                    if i==c7 and i.value==False:
                        open_banner('No Party Selected')
                        return
                page.dialog = dlg_modal
                dlg_modal.open = True
                page.update()
            def close_dlg(e):
                global database,user_number
                dlg_modal.open = False
                if e=='yes':
                    status=extract_vote()
                    if status=='invalid':
                        return
                    page.controls.clear()
                    page.add(ft.ResponsiveRow(page.add(ft.Row([ft.Text("", size=50, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
                        page.add(ft.Row([ft.Text("Your vote is", size=44, weight=ft.FontWeight.W_800, selectable=True,col={'md':4})],alignment='center')),
                    page.add(ft.Row([ft.Text("registered Successfully", size=36, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
                    page.add(ft.Row([ft.Text("", size=10, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
                    page.add(ft.Row([ft.ElevatedButton(text="Return Home",col={"md":3},on_click=lambda e:[initialize()])],alignment='center'))))
                else:
                    pass
                page.update()
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Please confirm"),
                content=ft.Text("Your vote is valuable to us"),
                actions=[
                    ft.TextButton("Yes", on_click=lambda e:close_dlg('yes')),
                    ft.TextButton("No", on_click=lambda e:close_dlg('no')),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: print("Modal dialog dismissed!"),
            )
            open_dlg('pass')
        page.controls.clear()
        def check_selection(sel):
            global c1,c2,c3,c4,c5,c6,c7
            li=[c1,c2,c3,c4,c5,c6,c7]
            for i in li:
                if i==sel:
                    pass
                else:
                    i.value=False
            page.update()
        def initialize2():
            global c1,c2,c3,c4,c5,c6,c7
            page.add(ft.ResponsiveRow(
                page.add(ft.Row([ft.Text("Vote here", size=50, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
                page.add(ft.Row([ft.Text("Click the circle of the party you want to vote", size=20, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
                page.add(ft.Row([ft.Text("", size=10, weight=ft.FontWeight.W_800, selectable=True)],alignment='center'))))
            c1 = ft.Checkbox(label="BJP(Bhartiya Janta Party)       ", value=False,on_change=lambda e:check_selection(c1))
            c2 = ft.Checkbox(label="RJD(Rashtriya Janta Party)    ", value=False,on_change=lambda e:check_selection(c2))
            c3 = ft.Checkbox(label="JDU(Janta Dal United)            ", value=False,on_change=lambda e:check_selection(c3))
            c4 = ft.Checkbox(label="CONGRESS                               ", value=False,on_change=lambda e:check_selection(c4)) 
            c5 = ft.Checkbox(label="BSP(Bahuja Samaj Party)       ",value=False,on_change=lambda e:check_selection(c5))
            c6 = ft.Checkbox(label="CPIM                                         ",value=False,on_change=lambda e:check_selection(c6))
            c7 = ft.Checkbox(label="NOTA(None Of The Above)    ",value=False,on_change=lambda e:check_selection(c7))
            rt=ft.ElevatedButton(text="   Return Home  ",on_click=lambda e:[retur()])
            b = ft.ElevatedButton(text="  Submit Vote    ",on_click=lambda e:[submit_vote()])
            page.add(ft.ResponsiveRow([ft.Row([c1],alignment='center'), 
                ft.Row([c2],alignment='center'),
                ft.Row([c3],alignment='center'),
                ft.Row([c4],alignment='center'),
                ft.Row([c5],alignment='center'),
                ft.Row([c6],alignment='center'),
                ft.Row([c7],alignment='center'),
                ft.Text("", size=10, weight=ft.FontWeight.W_800, selectable=True)],alignment='center'))
            page.add(ft.Row([rt,b],alignment='center'))
        initialize2()

    #--------------------------------------------------------------------------------
    
    def numbercheck():
        global number
        value=number.value
        new_value=""
        for i in value:
            try:
                int(i)
                new_value+=i
            except:
                pass
        if len(new_value)>10:
            number.value=new_value[0::9]
        else:
            number.value=new_value
        page.update()
    def close_banner_after(e):
        time.sleep(e)
        close_banner()
    def open_banner(txt):
        page.banner = ft.Banner(
                bgcolor=ft.colors.AMBER_100,
                leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
                content=ft.Text(
                    txt
                ),
                actions=[
                    ft.TextButton("Ok",on_click=lambda e:close_banner())
                ],
            )
        page.banner.open=True
        [page.update(),threading.Thread(target=lambda:close_banner_after(5)).start()]
    def close_banner():
        page.banner.open=False
        page.update()
    def check_number():
        global number,OTP,database
        if len(str(number.value))<10:
            print(number.value)
            open_banner('Incorrect Number')
            page.update()
            return
        data_ret=database.child('users').child(str(number.value)).get().val()
        if data_ret==None:
            status='not exist'
        else:
            status='exist'
        if status=='exist':
            open_banner("You can't vote twice")
            page.update()
            return
        else:
            def check_otp_():
                if OTP.value==otp_data:
                    global user_number
                    user_number=number.value
                    proceed_voting()
                else:
                    open_banner('Wrong OTP')
            num=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            sm=['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
            otp_data=random.choice(num)+random.choice(num)+random.choice(num)+random.choice(num)+random.choice(sm)+random.choice(sm)+random.choice(sm)+random.choice(sm)
            random.shuffle(list(otp_data))
            otp_data=''.join(otp_data)

            account_sid = 'ACb5c7b0b149c375a103851584d32c3370' 
            auth_token = '72ccd0ac8ced247d9c9caf0ffd18351a' 
            client = Client(account_sid, auth_token)
            client.messages.create(
                              body=f'{otp_data} is your OTP for 2022 Election',
                              from_='+12057517397',
                              to=f'+918709158470'
                          )
            page.snack_bar = SnackBar(ft.Text(f"OTP sent"))
            page.snack_bar.open=True
            OTP=ft.TextField(label="Enter OTP",border="underline",max_length=len(str(otp_data)),on_submit=lambda e:[check_otp_()],col={"md":4})
            verify=ft.ElevatedButton(text="Verify OTP",col={"md":2},on_click=lambda e:[check_otp_()])
            change_number=ft.ElevatedButton(text="Change Number",col={"md":2},on_click=lambda e:[initialize()])
            page.controls.clear()
            page.add(ft.ResponsiveRow(
                page.add(ft.Row([ft.Text("Welcome", size=50, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
                page.add(ft.Row([ft.Text("Voter", size=50, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
                page.add(ft.ResponsiveRow([
                    number],alignment='center')),
                page.add(ft.ResponsiveRow([
                    OTP],alignment='center')),
                page.add(ft.ResponsiveRow([
                    verify,change_number],alignment='center'))))
            number.disabled=True
            OTP.focus()
            page.update()
    number=ft.TextField(label="Enter Phone Number",border="underline",max_length=10,prefix_text="+91 ",on_submit=lambda e:[check_number()],on_change=lambda e:[numbercheck()],col={"md":4})
    send_otp=ft.ElevatedButton(text="Send OTP",col={"md":3},on_click=lambda e:[check_number()])
    def initialize():
        page.controls.clear()
        page.add(ft.ResponsiveRow(
            page.add(ft.Row([ft.Text("Welcome", size=50, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
            page.add(ft.Row([ft.Text("Voter", size=50, weight=ft.FontWeight.W_800, selectable=True)],alignment='center')),
            page.add(ft.ResponsiveRow([
                number],alignment='center')),
            page.add(ft.ResponsiveRow([
                send_otp],alignment='center'))))
        number.disabled=False
        number.focus()
        page.update()
    page.navigation_bar = ft.NavigationBar(
    destinations=[
        ft.NavigationDestination(icon=ft.icons.HOW_TO_VOTE_OUTLINED,selected_icon=ft.icons.HOW_TO_VOTE, label="Vote Here"),
        ft.NavigationDestination(icon=ft.icons.PIE_CHART_OUTLINE, label="Live vote count"),
        ft.NavigationDestination(
            icon=ft.icons.INFO_OUTLINE,
            label="About",
        ),
    ],on_change=lambda e:[change_page(page.navigation_bar.selected_index)])
    initialize()

ft.app(target=main,view=flet.WEB_BROWSER)
