from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as MessageBox
import mysql.connector as mysql

#fonction ajouter
def insert():
    id = e_id.get()
    Nom = e_Nom.get();
    prix = e_prix.get();
    classement=e_classement.get();

    if(id=="" or Nom=="" or prix=="" or classement==""):
        MessageBox.showinfo("insert Status", "All fields are required")
    else:
        con = mysql.connect(host="localhost", user="root", password="", db="biblioteque")
        cursor = con.cursor()
        cursor.execute("INSERT INTO biblioteque VALUES('"+ id +"','"+ Nom +"','"+ prix +"','"+ classement +"')")
        cursor.execute("commit");
  #supprimer le champ apres l'ajout de donner     
        e_id.delete(0, 'end')
        e_Nom.delete(0, 'end')
        e_prix.delete(0, 'end')
        e_classement.delete(0, 'end')
        MessageBox.showinfo("Insert status, inserer succes")
        con.close();

 #fonction supprimer       
def delete():
    if(e_id.get() ==""):
        MessageBox.sohwinfo("Delete status", "Id a ete supprimer")
    else:
        con = mysql.connect(host="localhost", user="root", password="", db="biblioteque")
        cursor = con.cursor()
        cursor.execute("DELETE from biblioteque WHERE id='"+ e_id.get() +"'")
        cursor.execute("commit");
  #supprimer le champ apres supprimer de donner     
        e_id.delete(0, 'end')
        e_Nom.delete(0, 'end')
        e_prix.delete(0, 'end')
        e_classement.delete(0, 'end')
        MessageBox.showinfo("delete, supprimer avec succes")
        con.close();

 #fonction pour la mise a jour
def update():
    for i in rows:
       trv.insert('', 'end', values=i)
    id = e_id.get()
    Nom = e_Nom.get();
    prix = e_prix.get();
    classement=e_classement.get();

    if(id=="" or Nom=="" or prix=="" or classement==""):
        MessageBox.showinfo("Update Status", "All fields are required")
    else:
        con = mysql.connect(host="localhost", user="root", password="", db="biblioteque")
        cursor = con.cursor()
        #cursor.execute(f"update biblioteque set Nom='{Nom}' and prix='{prix}' and classement='{classement}' where id={id}")
        cursor.execute("UPDATE biblioteque SET Nom='"+ Nom +"', prix='"+ prix +"', classement='"+ classement +"' where id='"+ id +"'")
        cursor.execute("commit");
  #supprimer le champ apres la mise ajour de donner     
        e_id.delete(0, 'end')
        e_Nom.delete(0, 'end')
        e_prix.delete(0, 'end')
        e_classement.delete(0, 'end')
        show()
        MessageBox.showinfo("Update status, mise a jour avec succes")
        con.close();
        
def get():
    if(e_Nom.get() ==""):
        MessageBox.sohwinfo("fetch status", "ecrire le Nom")
    else:
        con = mysql.connect(host="localhost", user="root", password="", db="biblioteque")
        cursor = con.cursor()
        cursor.execute("SELECT * from biblioteque where Nom='"+ e_Nom.get() +"'")
        rows = cursor.fetchall()

        for row in rows:
            e_Nom.insert(0, row[1])
            e_prix.insert(0, row[2])
            e_classement.insert(0, row[3])

        con.close();
def show():
    for i in rows:
       trv.insert('', 'end', values=i)

def quit():
    global root
    root.destroy()
con = mysql.connect(host="localhost", user="root", password="", db="biblioteque")
cursor = con.cursor()
#interface
root = Tk()
wrapper1 = LabelFrame(root, text="Liste des donnees")

wrapper3 = LabelFrame(root, text="table de donner")

wrapper1.pack(fill="both", expand="yes", padx=20, pady=10)

wrapper3.pack(fill="both", expand="yes", padx=20, pady=10)

trv = ttk.Treeview(wrapper1, columns=(1,2,3,4), show="headings", height="6")
trv.pack()

trv.heading(1, text="id")
trv.heading(2, text="Nom")
trv.heading(3, text="prix")
trv.heading(4, text="classement")

query = "SELECT * from biblioteque"
cursor.execute(query)
rows = cursor.fetchall()

root.geometry("800x700")
root.title("Base+de+donner+biblioteque")

#fonction pour la mise en forme
id = Label(wrapper3, text='Entre ID', font=('bold', 10))
id.place(x=20,y=30)

Nom = Label(wrapper3, text='Entre Nom', font=('bold', 10))
Nom.place(x=20,y=60)

prix = Label(wrapper3, text='Entre Prix', font=('bold', 10))
prix.place(x=20,y=90)

classement = Label(wrapper3, text='Entre Classement', font=('bold', 10))
classement.place(x=20,y=120);

e_id = Entry(wrapper3)
e_id.place(x=150,y=30)

e_Nom = Entry(wrapper3)
e_Nom.place(x=150,y=60)

e_prix = Entry(wrapper3)
e_prix.place(x=150,y=90)

e_classement = Entry(wrapper3)
e_classement.place(x=150,y=120)


#fonction boutton
insert = Button(wrapper3, text="Insert", font=("italic", 10), bg='white', command=insert)
insert.place(x=600,y=30)

delete = Button(wrapper3, text="Supprimer", font=("italic", 10), bg='white', command=delete)
delete.place(x=300,y=30)

update = Button(wrapper3, text="Mis a jour", font=("italic", 10), bg='white', command=update)
update.place(x=400,y=30)

get = Button(wrapper3, text="Get", font=("Italic", 10), bg='white', command=get)
get.place(x=500,y=30)

quit = Button(wrapper3, text="Quiter", font=("Italic", 10), bg='white', command=quit)
quit.place(x=400,y=90)

lbl = Label(wrapper3, text="Recherche")
lbl.pack(side=tk.LEFT, padx=20, pady=130)
ent = Entry(wrapper3)
ent.pack(side=tk.LEFT, padx=6, pady=130)



root.mainloop()

