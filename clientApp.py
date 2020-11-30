from tkinter import *
from tkinter import ttk
from client import sendmsg
import json
import os
import vobject

def main(access,username):

    def findPeople(dct,org):
        ret = ""
        for k,sub_dict in dct.items():
            if "Email" in sub_dict.keys():
                ret = ret + "\n" + org+"~"+k+"~"+sub_dict.get("Email","")+"~"+sub_dict.get("Phone no","")
            elif isinstance(sub_dict,dict):
                ret = ret + "\n" + findPeople(sub_dict,org+"."+k)
        return ret

    def createContact(ret):
        ret = ret.split('\n')
        for person in ret:
            card = vobject.vCard()
            if person=='':
                continue
            person = person.split('~')
            card.add('FN').value = person[1]
            card.add('Email').value = person[2]
            if access == '1':
                card.add('Tel').value = person[3]
            org = person[0].split('.')
            print(org)
            if len(org)>3:
                card.add('Office').value = org[1]
                card.add('Position').value = org[-1]
            elif len(org)>1:
                card.add('Position').value = org[-1]

            card.useBegin = True
            card.serialize()
            card.prettyPrint()
            # with open(name+'.vcf','w') as file:
                # file.write(card.serialize())

    def export():
        createContact(findPeople(organizationHeirarchy,""))
        expButton.config(text="Exported!",state='disabled',bg="white",fg="#212F3C",relief="flat")

    def recursiveInsert(data,parent=''):
        idx = 0
        for k,v in data.items():
            if isinstance(v,dict):
                organizationTree.insert(parent,str(idx),k,text=k,tag=('parent',))
                idx += 1
                recursiveInsert(v,k)
            else:
                organizationTree.insert(parent,'end',v,text=k,values=(v,),tag=('leaf',))

    def recursiveSearch(dct,name):
        ret = ""
        for k,sub_dict in dct.items():
            if k==name:
                ret =  json.dumps(sub_dict,indent=1)
            elif isinstance(sub_dict,dict):
                ret = ret + recursiveSearch(sub_dict,name)
        return ret

    def clickOn(event):
        if len(organizationTree.selection())==0:
            return
        print(organizationTree.selection())
        if "@" not in organizationTree.selection()[0] and all(str(i) not in organizationTree.selection()[0] for i in range(10)):
            dlButton.config(state='normal',bg="orange",fg="black",relief="raised")
        else:
            dlButton.config(state='disabled',bg="#f8f8f8",relief="flat")

    def download():
        for select in organizationTree.selection():
            direct = os.getcwd()
            with open(os.path.join(direct,select+'.json'),'w') as file:
                file.write(recursiveSearch(organizationHeirarchy,select))
                print("File written")
        dlButton.config(text="Downloaded!",state='disabled',bg="white",fg="#212F3C",relief="flat")

    def setupTree(organizationHeirarchy):
        recursiveInsert(organizationHeirarchy)
        organizationTree.tag_configure('parent', background="#fafafa")
        organizationTree.tag_configure('leaf', background="#f2f2f2")

    def sendQuery():
        treeLabel.config(text="No Query",fg="#283747")
        organizationTree.delete(*organizationTree.get_children())
        query = queryBox.get()
        global organizationHeirarchy
        organizationHeirarchy = eval(sendmsg(query))
        # print("organizationHeirarchy =",organizationHeirarchy)
        if len(organizationHeirarchy) == 0:
            expButton.config(text="Export as vCard",state='disabled',bg="#f8f8f8",fg="black",relief="flat")
            dlButton.config(text="Download data",state='disabled',bg="#f8f8f8",fg="black",relief="flat")
            treeLabel.config(text="Invalid Query!",fg="#E74C3C")
            setupTree({'No Data' : 'Waiting for Valid Query'})
        else:
            expButton.config(text="Export as vCard",state='normal',bg="orange",fg="black",relief="raised")
            dlButton.config(text="Download data",fg="black",bg="#f8f8f8",relief="flat")
            treeLabel.config(text="Result",fg="#239B56")
            setupTree(organizationHeirarchy)



    root = Tk()
    root.title("App")
    root.geometry("1366x768")
    root.configure(background="white")


    # App Banner
    bannerLabel = Label(root,text="Office Bearers DB",font="Helvetica 20 bold",relief="groove",bg="#F8F9F9",fg="#283747",width=15)
    bannerLabel.place(x=520,y=10)

    # Access Level Label
    if access:
        accessLevel = username[:username.index('@')] + "\nAccess: Full"
        fg = "#188C48"
    else:
        accessLevel = "Guest\nAccess: Limited"
        fg = "#DEA402"
    accessLabel = Label(root,text=accessLevel,font="Helvetica 15",bg="#F8F9F9",fg=fg)
    accessLabel.place(x=1210,y=0)

    # Query Label
    queryLabel = Label(root,text="Query:",font="Helvetica 15",bg="#F8F9F9",fg="#283747")
    queryLabel.place(x=200,y=90)

    # Search Box
    queryBox = Entry(root,width=60,highlightbackground="black",highlightthickness=2,highlightcolor="orange",font="Helvetica 15")
    queryBox.place(x=300,y=90)

    # Send Button
    sendButton = Button(root,text="Send",command=sendQuery,width=10,fg="black",bg="orange",relief="raised",font="Helvetica 12 bold")
    sendButton.place(x=1000,y=87)

    # Organization Tree

    # tree label
    treeLabel = Label(root,text="Query Status: NA",font="Helvetica 15 bold",relief="flat",bg="#F8F9F9",fg="#283747",width=15)
    treeLabel.place(x=560,y=140)

    # organization tree frame
    treeFrame = Frame(root,width=1000)
    treeFrame.place(x=190,y=190)

    # vertical scrollbar
    verscrlbar = ttk.Scrollbar(treeFrame,orient="vertical")
    verscrlbar.grid(row=0,column=1,sticky="NSEW")

    # horizontal scrollbar
    horscrlbar = ttk.Scrollbar(treeFrame,orient="horizontal")
    horscrlbar.grid(row=1,column=0,sticky="NWSE")

    style = ttk.Style()
    style.configure("mystyle.Treeview",font=('Courier New', 15),rowheight=40) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", fg="black", font=('Impact', 18)) # Modify the font of the headings

    organizationTree = ttk.Treeview(treeFrame, selectmode='extended', xscrollcommand=horscrlbar.set, yscrollcommand=verscrlbar.set, style="mystyle.Treeview")

    organizationTree.grid(row=0,column=0)
    verscrlbar.config(command=organizationTree.yview)
    horscrlbar.config(command=organizationTree.xview)

    organizationTree['columns'] = ('heading',)
    organizationTree.column('heading',width=800,minwidth=800,stretch=True, anchor='center') #n, ne, e, se, s, sw, w, nw, or center
    organizationTree.heading('heading',text='Details',anchor='center')
    # organizationTree['show'] = 'tree'
    setupTree({'No Data' : 'Waiting for Query'})

    #Download button
    dlButton = Button(root,text="Download data",command=download,width=15,fg="black",bg="#f8f8f8",relief="flat",font="Helvetica 12 bold",state='disabled')
    dlButton.place(x=480,y=650)

    #Download button
    expButton = Button(root,text="Export as vCard",command=export,width=15,fg="black",bg="#f8f8f8",relief="flat",font="Helvetica 12 bold",state='disabled')
    expButton.place(x=720,y=650)

    organizationTree.bind("<Double-1>",clickOn)


    root.mainloop()
