import tkinter as tk

def show_entry_fields():
    print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))

master = tk.Tk()
master.title("Agha Sadegh")


tk.Label(master, 
         text="Text Search").grid(row=0, column=0)
e1 = tk.Entry(master)
e1.grid(row=0, column=1)


tk.Label(master, 
         text="Item to Select").grid(row=0, column=2)
e2 = tk.Entry(master)
e2.grid(row=0, column=3)


tk.Button(master, 
          text='GET URLS', 
          command=master.quit).grid(row=0, 
                                    column=4, 
                                    sticky=tk.W, 
                                    pady=4)
tk.Button(master, 
          text='Exit', command=master.quit).grid(row=3, 
                                                       column=0, 
                                                       sticky=tk.W, 
                                                       pady=4)

tk.mainloop()


