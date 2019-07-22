from tkinter import *
import subprocess
import argparse, os
from time import time
from scipy.io import savemat
from fnc.extractFeature import extractFeature
from fnc.matching import matching


 
window = Tk()
 
window.title("Iris comparison app")
 
window.geometry('350x200')

#field 1

def popupmsg(msg):
    popup = Tk()
    popup.wm_title("Output message")
    label = Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()
 
lbl1 = Label(window, text="Voter Eye ID to be enrolled: ")
 
lbl1.grid(column=0, row=3)
 
txt1 = Entry(window,width=10)
 
txt1.grid(column=1, row=3)

lbl_name= Label(window, text="Voter Name: ")

lbl_name.grid(column=0, row=0)

txt_name = Entry(window,width=10)
 
txt_name.grid(column=1, row=0)

id_name = dict()
 
def clicked_enroll():

   id_name[str(txt1.get())[0]]=str(txt_name.get())
   #------------------------------------------------------------------------------
   #	Argument parsing
   #------------------------------------------------------------------------------
   parser = argparse.ArgumentParser()

   parser.add_argument("--file", type=str,
                       help="Path to the file that you want to verify.")

   parser.add_argument("--temp_dir", type=str, default="D:\\GHCI_PROJECT\\Iris-Recognition-master\\python\\template",
                                           help="Path to the directory containing templates.")

   args = parser.parse_args()


   ##-----------------------------------------------------------------------------
   ##  Execution
   ##-----------------------------------------------------------------------------
   start = time()
   args.file = "D:\\GHCI_PROJECT\\eyes\\"+str(txt1.get())+".jpg"

   # Extract feature
   print('>>> Enroll for the file ', args.file)
   template, mask, file = extractFeature(args.file)

   # Save extracted feature
   basename = os.path.splitext(os.path.basename(file))[0]
   out_file = os.path.join(args.temp_dir, "%s.mat" % (basename))
   savemat(out_file, mdict={'template':template, 'mask':mask})
   print('>>> Template is saved in %s' % (out_file))

   end = time()
   print('>>> Enrollment time: {} [s]\n'.format(end-start))

 
btn1 = Button(window, text="Enroll", command=clicked_enroll)
 
btn1.grid(column=2, row=3)

#field 2

lbl2 = Label(window, text="Voter Eye ID to be verified: ")
 
lbl2.grid(column=0, row=6)
 
txt2 = Entry(window,width=10)
 
txt2.grid(column=1, row=6)
 
def clicked_verify():

   #------------------------------------------------------------------------------
   #	Argument parsing
   #------------------------------------------------------------------------------
   parser = argparse.ArgumentParser()

   parser.add_argument("--file", type=str,
                       help="Path to the file that you want to verify.")

   parser.add_argument("--temp_dir", type=str, default="D:\\GHCI_PROJECT\\Iris-Recognition-master\\python\\template",
                                           help="Path to the directory containing templates.")

   parser.add_argument("--thres", type=float, default=0.38,
                                           help="Threshold for matching.")

   args = parser.parse_args()


   ##-----------------------------------------------------------------------------
   ##  Execution
   ##-----------------------------------------------------------------------------
   # Extract feature
   start = time()
   args.file = "D:\\GHCI_PROJECT\\eyes\\"+str(txt2.get())+".jpg"
   print('>>> Start verifying {}\n'.format(args.file))
   template, mask, file = extractFeature(args.file)



   # Matching
   result = matching(template, mask, args.temp_dir, args.thres)

   if result == -1:
           print('>>> No registered sample.')
           popupmsg("Voter not registered.")

   elif result == 0:
           print('>>> No sample matched.')
           popupmsg("Voter not matched.")

   else:
           print('>>> {} samples matched (descending reliability):'.format(len(result)))
           for res in result:
                   print("\t", res)
           result_temp=str(result[0])
           popupmsg("Voter ID = "+str(result_temp[0:2])+"\n"+"Voter Name = "+str(id_name[result_temp[0]]))
           


   # Time measure
   end = time()
   print('\n>>> Verification time: {} [s]\n'.format(end - start))

      

btn2 = Button(window, text="Verify", command=clicked_verify)
 
btn2.grid(column=2, row=6)
 
window.mainloop()
