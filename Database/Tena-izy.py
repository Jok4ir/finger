from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import mysql.connector
from PIL import ImageTk, Image

def update(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i, tags="unchecked")

def toggle2(event):
    for i in trv.get_children():
        trv.item(i, tags="unchecked")
    toggleCheck(event)

def toggleCheck(event):
    rowid = trv.identify_row(event.y)
    tag = trv.item(rowid, "tags")[0]
    tags = list(trv.item(rowid, "tags"))
    tags.remove(tag)
    trv.item(rowid, tags=tags)
    if tag == "checked":
        trv.item(rowid, tags="unchecked")
    else:
        trv.item(rowid, tags="checked")


def search():
    q2 = q.get()
    query = "SELECT id, Nom, Prenom, Contact FROM dbuser WHERE id LIKE '%"+ q2 +"%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)


def clear():
    query = "SELECT id, Nom, Prenom, Contact FROM dbuser"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

# def getrow():
#     #rowid = trv.identify_ro(event.y)
#     item = trv.item(trv.focus())
#     t1.set(item['values'][0])
#     t2.set(item['values'][1])
#     t3.set(item['values'][2])
#     t4.set(item['values'][3])

def showdetails(x):
    x = list(x[0])
    print(x)
    t1.set(str(x[0]))
    t2.set(str(x[1]))
    t3.set(x[2])
    t4.set(x[3])
    return

def getrow():
    q2 = q.get()
    query = "SELECT id, Nom, Prenom, Contact FROM dbuser WHERE id LIKE '%"+ q2 +"%'"
    cursor.execute(query)
    rows = cursor.fetchall()
    showdetails(rows)




def update_table():
    id = t1.get()
    Nom = t2.get()
    Prenom = t3.get()
    Contact = t4.get()

    if messagebox.askyesno("Confirme to update?", "Es tu sure de faire la mis a jour cette table"):
       query = "UPDATE dbuser SET Nom='"+ Nom +"', Prenom='"+ Prenom +"', Contact='"+ Contact +"' where id='"+ id +"'"
       cursor.execute(query)
       mydb.commit()
       clear()
    else:
       return True

def add_new():
    #id = t1.get()
    Nom = t2.get()
    Prenom = t3.get()
    Contact = t4.get()
    query = f"INSERT INTO dbuser VALUES (NULL, '{str(Nom)}', '{Prenom}', '{Contact}')"
    cursor.execute(query)
    mydb.commit()
    clear()
    update(rows)

def delete_table():
    id = t1.get()
    if messagebox.askyesno("confirm Delete?", "Vous ètes sur de supprimer"):
       query = "DELETE FROM dbuser WHERE id = "+id+""
       cursor.execute(query)
       mydb.commit()
       clear()
       update(rows)
    else:
        return True

def quit():
    global root
    root.destroy()

mydb = mysql.connector.connect(host="localhost", user="root", password="", db="dbuser")
cursor = mydb.cursor()

root = Tk()
q = StringVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()

wrapper1 = LabelFrame(root, text="Liste des donneés")
wrapper2 = LabelFrame(root, text="Recherche")
wrapper3 = LabelFrame(root, text="Manipulation")

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper2.pack(fill="both", expand="yes", padx=20, pady=10)
wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

#im_checked = ImageTk.PhotoImage(Image.open("checked.png"))
#im_unchecked = ImageTk.PhotoImage(Image.open("unchecked.png"))

trv = ttk.Treeview(wrapper1, columns=(1,2,3,4))
style = ttk.Style(trv)
style.configure('Treeview', rowheight=20)

#trv.tag_configure('checked', image=im_checked)
#trv.tag_configure('unchecked', image=im_unchecked)

trv.pack()
trv.heading('#0', text="")
trv.heading('#1', text="ID")
trv.heading('#2', text="Nom")
trv.heading('#3', text="Prenom")
trv.heading('#4', text="Contact")

trv.bind('<Button 1>', toggle2)

query = "SELECT id, Nom, Prenom, Contact FROM dbuser"
cursor.execute(query)
rows = cursor.fetchall()
update(rows)


lbl = Label(wrapper2, text="Recherche")
lbl.pack(side=tk.LEFT, padx=10)
ent = Entry(wrapper2, textvariable=q)
ent.pack(side=tk.LEFT,padx=6)
btn = Button(wrapper2, text="Recherche", command=search)
btn.pack(side=tk.LEFT, padx=6)
cbtn = Button(wrapper2, text="Supprimer", command=clear)
cbtn.pack(side=tk.LEFT, padx=6)
lbtn = Button(wrapper2, text="Voir Detail", command=getrow)
lbtn.pack(side=tk.LEFT, padx=10)

lbl1 = Label(wrapper3, text="User ID")
lbl1.grid(row=0, column=0, padx=5, pady=3)
ent1 = Entry(wrapper3, textvariable=t1)
ent1.grid(row=0, column=1, padx=5, pady=3)

lbl2 = Label(wrapper3, text="Nom")
lbl2.grid(row=1, column=0, padx=5, pady=3)
ent2 = Entry(wrapper3, textvariable=t2)
ent2.grid(row=1, column=1, padx=5, pady=3)

lbl3 = Label(wrapper3, text="Prenom")
lbl3.grid(row=2, column=0, padx=5, pady=3)
ent3 = Entry(wrapper3, textvariable=t3)
ent3.grid(row=2, column=1, padx=5, pady=3)

lbl4 = Label(wrapper3, text="Contact")
lbl4.grid(row=3, column=0, padx=5, pady=3)
ent4 = Entry(wrapper3, textvariable=t4)
ent4.grid(row=3, column=1, padx=5, pady=3)

up_btn = Button(wrapper3, text="Mis à Jour", command=update_table)
add_btn = Button(wrapper3, text="Ajouter",command=add_new)
delete_btn = Button(wrapper3, text="Supprimer", command=delete_table)
qbtn = Button(wrapper3, text="Fermer", command=quit)

qbtn.grid(row=4, column=3, padx=5, pady=3)
up_btn.grid(row=4, column=1, padx=5, pady=3)
add_btn.grid(row=4, column=0, padx=5, pady=3)
delete_btn.grid(row=4, column=2, padx=5, pady=3)



root.title("Mon Application")
root.geometry("800x900")
root.mainloop()




    
