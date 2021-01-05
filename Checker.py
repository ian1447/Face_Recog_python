from tkinter import *
from PIL import ImageTk, Image
import cv2
import face_recognition
from tkinter import filedialog
from datetime import datetime
from tkinter import messagebox
import os

def ask_directory():
    global students_dir
    global path
    students_dir = filedialog.askdirectory()
    path = os.path.basename(students_dir)
    status = Label(root,text=students_dir, bd=1, relief=SUNKEN, anchor=W)
    status.grid(row=1,column=0, sticky=W+E)
    if students_dir != "Not yet chosen a designated folder." & class_img != "Nothing":
        file_menu.entryconfig(3, state = NORMAL)

def open_file():
    global my_image_dir
    global new_pic
    global class_img
    my_image_dir = filedialog.askopenfilename(initialdir="/", title = "Select Image", filetypes=(("jpeg files ", "*.jpeg"),("jpg files", "*.jpg"),("all files", "*.*")))
    my_pic = Image.open(my_image_dir)
    resized_pic = my_pic.resize((550,400), Image.BICUBIC)
    new_pic = ImageTk.PhotoImage(resized_pic)
    my_label = Label(frame, image=new_pic).place(x=20,y=60)
    class_img = my_image_dir
    if students_dir != "Not yet chosen a designated folder." & class_img != "Nothing":
        file_menu.entryconfig(3, state = NORMAL)

def run_file():
    global students_dir
    global my_image_dir
    now = datetime.now()
    date = now.strftime("%m-%d-%Y")
    direc = path + " " + date + '.txt'

    try:
       outfile = open('attendance/' + direc, 'x')
    except:
        message_box = messagebox.showwarning("Warning!", "Attendance for today already exists, please delete the file first.")
        return
    
    class_image = face_recognition.load_image_file(my_image_dir)
    face_locations = face_recognition.face_locations(class_image)

    for face_locations in face_locations:
        top, right, bottom, left = face_locations

        face_image =class_image[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save(f'./Class/Images/{top}.jpg')

    students_dir = students_dir + "/"
    for j in os.listdir(students_dir):
        student_name = os.path.splitext(j)[0]
        student = students_dir + j
        my_image = face_recognition.load_image_file(student)
        my_encoding = face_recognition.face_encodings(my_image)[0]
        res = 0

        my_dir = './Class/Images/' # Folder where all your image files from the class picture resides. Ensure it ends with '
        for i in os.listdir(my_dir): # Loop over the folder to list individual files
            image = my_dir + i
            img = face_recognition.load_image_file(image)
            unknown_image = face_recognition.load_image_file(image)
            height, width, _ = img.shape
            face_locations = (0,width,height,0)
            image_encoding = face_recognition.face_encodings(unknown_image, known_face_locations=[face_locations])[0]
            results = face_recognition.compare_faces([my_encoding],image_encoding, tolerance = 0.5)
            if results [0] ==  True:
                res = 1
                break

        if res == 1:
            outfile = open('Attendance/' + direc, 'a')
            outfile.write(student_name + " is present\n")
        else:
            outfile = open('Attendance/' + direc, 'a')
            outfile.write(student_name + " is absent\n")

    for i in os.listdir(my_dir):
        delete = my_dir + i
        os.remove(delete )

    message_box = messagebox.showinfo("Finished", "Attendance Checking is complete.")


#variables
students_dir = "Not yet chosen a designated folder."
class_img = "Nothing"

root = Tk()
root.geometry("800x620")
root.title("Attendance Checker")
root.iconbitmap('icon.ico')
root.resizable(0,0)

my_menu = Menu(root)
root.config(menu=my_menu)
status = Label(root,text=students_dir, bd=1, relief=SUNKEN, anchor=W)

#Creating Menu
file_menu = Menu(my_menu, tearoff = 0)
my_menu.add_cascade(label="File", menu =file_menu)
file_menu.add_command(label="Open Class Folder", command = ask_directory)
file_menu.add_command(label="Open Class Image", command = open_file)
file_menu.add_separator()
file_menu.add_command(label="Run Program", command = run_file, state = DISABLED)

frame = LabelFrame(root,width = 600, height = 530)
frame.grid(row=0,column=0, padx=100,pady=25)
frame.pack_propagate(0)

my_label = Label(frame, text='Not yet chosen a photo').place(x=240,y=260)

status.grid(row=1,column=0, sticky=W+E)

root.mainloop()