# import tkinter as tk
# from tkinter import Button,Label
# #from tkinter import ttk
# from tkinter import filedialog
# #import sqlite3
# from tkinter import filedialog
# #from PIL import ImageTk, Image
# #import sqlite3 as db
from preprocessing import preprocess_single_image
from extract import extract_signature_from_image
from resize import resize_image
from siamese_in_py import train_model, make_train_dataset,predict
from chequescan import extract_data_from_cheque
import os
from customtkinter import filedialog
from customtkinter import CTkButton as Button
from customtkinter import CTkLabel as Label
import customtkinter
from tkinter import messagebox
import tkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
customtkinter.set_widget_scaling(2)
#customtkinter.set_window_scaling(125)
window = customtkinter.CTk()
window.geometry('500x500')
window.title("Signature Verification System")
# greeting = tk.Label(window,text="Hello, Welcome to our Signature Verification System. ")
# greeting.pack()


def extract_signature(): #extract and preprocess as well

    filename = filedialog.askopenfilename(title='Select image to extract')
    Label(window,text=filename).pack()

    extract_signature_from_image(filename, (300,300),15)
    Label(window,text = customtkinter.messagebox()).pack()



# def display_text():
#     global entry
#     string = tk.entry.get()
#     tk.label.configure(text=string)


# def directory():
#     root = tk.Tk()
#     root.withdraw()
#     dirname = filedialog.askdirectory(
#         parent=root, initialdir="/", title='Please select a directory')


def train():

    dirname0 = filedialog.askdirectory(parent=window,
                                       initialdir="A:/preprocessing/sathi_signatures/train",
                                       title='Please select a directory for class 0.')
    dirname1 = filedialog.askdirectory(parent=window,
                                       initialdir="A:/preprocessing/sathi_signatures/train",
                                       title='Please select a directory for class 1.')

    dir1 = dirname0.split('/')
    dir2 = dirname1.split('/')

    print(dirname0)
    print(dirname1)


    dataset,label = make_train_dataset(dirname0,dirname1)

    model = train_model(dataset,label)

    # cwd = os.getcwd()
    # temp = f'\\saved_model\\{dir1[-1]}vs{dir2[-1]}.h5'
    # save_path = os.path.join(str(cwd),temp)
    # model.save(save_path)

    # tk.Label(window,text= f"Training completed\n Model saved at: {save_path}").pack()
    # c:/saved model ma save bhairachha
    model.save(f'A:/pj/saved_model/{dir1[-1]}vs{dir2[-1]}.h5')
    
    messagebox.showinfo('Training info',f'Training completed, \nModel saved at: A:/pj/saved_model/{dir1[-1]}vs{dir2[-1]}.h5')
    #Label(window,text=f'Training completed, \nModel saved at: A:/pj/saved_model/{dir1[-1]}vs{dir2[-1]}.h5').pack()
   

def test():

    # var = tk.IntVar()

    img1 = filedialog.askopenfilename(initialdir="A:/preprocessing/sathi_signatures/test",title="Please select first image to test")
    #img2 = filedialog.askopenfilename(initialdir="A:/preprocessing/sathi_signatures/test",title="Please select second image to test")
    # Label(window,text="Enter Roll_no").pack()
    # entry = Entry(width=30).pack()
    # button = tk.Button(text="Enter", command=lambda: var.set(1))
    # button.pack()
    # button.wait_variable(var)
    # roll = entry.get()
    roll = str(49)

    path = os.path.join("A:/preprocessing/sathi_signatures/train",roll)
    lis = os.listdir(path)
    path = os.path.join(path,lis[1])

    model_path = f"A:/pj/saved_model/{roll}vs99.h5"
    
    out = predict(model_path,path,img1)

    '''so here we need to import pretrained model and throw error popup if 
    if pretrained model is not found. For that task should i use  a_vs_other
    to train the model or a_vs_b to verify a as well as b ? that is to be
    found. so .....
    '''
    messagebox.showinfo('info',f'Similarity = {out}')




def scan_cheque():
    cheque_path = filedialog.askopenfilename(initialdir="A:/preprocessing",
                                             title = "Select scanned cheque")
    Label(window,text=cheque_path).pack()
    extract_data_from_cheque(cheque_path)
    messagebox.showinfo('','extraction complete')

# def prt():
#     x_dir = directory0()
#     y_dir = directory1()
#     # print(x_dir)
#     # print(y_dir)


# def myButton1():
#     win = Tk()
#     win.title("Import images")
#     win.geometry("400x400")

#     # label1 = Label(window,win, text="Enter name/unique id")
#     # label1.pack()

#     # entry = Entry(win, width=40)
#     # entry.focus_set()
#     # entry.pack()

#     btn1 = ttk.Button(win, text="Enter", width=20)
#     btn1.pack(pady=0)

#     label2 = Label(window,win, text="Import images")
#     label2.pack(pady=0)

#     ttk.Button(win, text="select image directory", width=20,command=Train_model).pack(pady=0)


#     # def print_dir():
#     #     dir0 = directory0()
#     #     dir1 = directory1()
#     #     print(dir0)
#     #     print(dir1)

#     # prt()

#     win.mainloop()


# photo = tk.PhotoImage(file=r"E:/MINOR PROJECT/Signature/add.png")
button0 =Button(window,
    text="Extract Signature",
    width=15,
    height=2,

    command=extract_signature
)
button1 =Button(window,
    text="Train Model",
    width=15,
    height=2,

    command=train
)


button3 =Button(window,
    text="Scan Cheque",
    width=15,
    height=2,

    command= scan_cheque
    )

button4 = Button(window,
    text="Test Signature",
    width=15,
    height=2,
 
    command = test
)


button0.pack(padx=0, pady=5)
button1.pack(padx=0, pady=5)
# button2.pack(padx=0, pady=5)
button3.pack(padx=0, pady=5)
button4.pack(padx=0, pady=5)
Button(window,
       text= 'Quit',
        width = 15,
        height = 2,
        
        command=window.quit
        ).pack()

window.mainloop()
