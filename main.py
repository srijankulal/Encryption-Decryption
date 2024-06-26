import base64
from caesarcipher import CaesarCipher
from tkinter import *
from tkinter import messagebox


def main():
    #Text and key for texting   #"*can be re-config depending on user*"
    key=10
    root=Tk()
    root.title('En|De')
    root.geometry('550x470')
    root.config(bg="#B4B4F8")
    icon=PhotoImage(file="./Image/data-encryption.png")
    root.iconphoto(False,icon)
    def reset():
        T1.delete(1.0,END)
        T2.delete(1.0,END)
        en.deselect()
        de.deselect()
        v.set(0)
    Label(root,text="Encryption and Decryption",fg="#000080",bg="#B4B4F8",font=("Calibri",15,"bold"),justify='left').place(x=10,y=10)
    Label(root,text="Text to be processed:",fg="#333333",bg="#B4B4F8",font=("Mongolian Baiti",11,"bold")).place(x=10,y=50)
    T1=Text(root,font=("Tunga ",10),bg="#CCCCF7")
    T1.place(x=10,y=80,width=525,height=100)
    v=IntVar()
    v.set(0)
    Label(root,text="Option: ",fg="#333333",font=("Mongolian Baiti",10,"bold"),bg="#B4B4F8").place(x=10,y=180)
    Frame(root,bd=10,bg="#BDBDFD").place(x=8,y=200,width=525,height=60)
    en=Radiobutton(root,text="Encrypt",font=("Mongolian Baiti",11),bg="#BDBDFD",fg="#333333" ,variable=v,value=1,cursor="hand2")
    en.place(x=10,y=205)
    de=Radiobutton(root,text="Decrypt",font=("Mongolian Baiti",11),bg="#BDBDFD",fg="#333333",variable=v,value=2,cursor="hand2")
    de.place(x=10,y=230)
    
    def check_opt():
        text=T1.get(1.0, END)
        T2.delete(1.0,END)
        if (v.get()==1):
            if not text.strip():
                messagebox.showerror("Error","Enter the text")
                return
            msg=encrypt(text,key)
            T2.insert("1.0",msg)
        elif(v.get()==2):
            if not text.strip():
                messagebox.showerror("Error","Enter the text")
                return
            msg=decrypt(text,key)
            T2.insert("1.0",msg)
        else:
            messagebox.showerror("Option","Select the option")
            
    def on_enter(e):
        b1.config(background='#252597', foreground= "#000080",font=("Mongolian Baiti",12))
    def on_enter2(e):
        b2.config(background='#252597', foreground= "#000080",font=("Mongolian Baiti",12))
    def on_leave(e):
        b1.config(background= '#5353E8', foreground= '#333333',font=("Mongolian Baiti",11))
    def on_leave2(e):
        b2.config(background= '#5353E8', foreground= '#333333',font=("Mongolian Baiti",11))
    b1=Button(root, text="Encrypt/Decrypt",font=("Mongolian Baiti",11),bg="#5353E8",fg="#333333",cursor="hand2",activebackground="#626567",activeforeground="white",command=check_opt)
    b1.place(x=10,y=270)
    b1.bind('<Enter>', on_enter)
    b1.bind('<Leave>', on_leave)
    b2=Button(root,text="Reset",font=("Mongolian Baiti",11),bg="#5353E8",fg="#333333",cursor="hand2",activebackground="#626567",activeforeground="white",command=reset)
    b2.place(x=140,y=270)
    b2.bind('<Enter>', on_enter2)
    b2.bind('<Leave>', on_leave2)
    Label(root,text="Output:",fg="#333333",font=("Mongolian Baiti",11,"bold"),bg="#B4B4F8").place(x=10,y=310)
    T2=Text(root,font=("Tunga ",10),bg="#CCCCF7")
    
    T2.place(x=10,y=340,width=525,height=100)
    
    root.mainloop()




















# #encrypt 
def encrypt(msg,key):
    org_text=msg
    cc_text=CaesarCipher(org_text,offset=key)
    cc_text=cc_text.encoded
    #Byte form of CC_text
    cc_text_byte=cc_text.encode('utf-8')
    cc_text_hex=cc_text_byte.hex()#conversion to hex
    cc_hex=str(cc_text_hex)
    #conversion of org_text to hex
    text=org_text.encode('utf-8')#to convert string to byte form"b'..."
    key_factor=len(org_text)
    hex_text=text.hex()
    #hex to binary of org-txt
    binary=bin(int(hex_text,16))[2:]#bin converts int to binary "0b101010" and int(x,16)converts hex to int with base 16 and [2:] slice notation starts from 3 to remove 0b..
    #decimal conversion
    dec=int(binary,2)
    #hex to binary of cc-txt
    cc_binary=bin(int(cc_text_hex,16))[2:]
    #decimal of cc-txt
    cc_dec=int(cc_binary,2)
    #for diff of txt binary 
    nth = (int(((dec-cc_dec)%key))) if (cc_dec<dec) else (int((cc_dec-dec)%key))
    nth_value=key_factor+nth
    keyfact_bin=bin(key_factor)
    keyfact_bin_fin=str(keyfact_bin[2:])
    for _ in range(1,nth):
        
        keyfact_bin_fin+=keyfact_bin[2:]
        
    keyfact_bin_fin=bin(int(keyfact_bin_fin,2))[2:]
    out=bin(int(cc_binary,2)+int(keyfact_bin_fin,2))[2:]
    hex_out=hex(int(out,2))[2:]
    i=0
    for i in range(len(hex_out)):
        if(i==nth):
            hex_out=hex_out[:i]+str(nth_value)+']'+hex_out[i:]
            break
        
    separate='`'
    hex_out= ((str(hex_out)+separate+str(nth)).encode('utf-8')).hex()
    en_hex=bytes.fromhex(hex_out)
    en_base64 = base64.b64encode(en_hex)
    return ( en_base64.decode('utf-8') )








#decode
def decrypt(msg,key):
    text=msg
    en_str=text 
    de_byte = en_str.encode('utf-8')#into utf-8
    de_base64 = base64.b64decode(de_byte)#decode from base64
    de_hex=de_base64.hex()#byte to hex
    de_out=(bytes.fromhex(de_hex)).decode('utf-8')#hex to byte and decode utf-8
    #to separate the required data from hex
    index=de_out.find('`')
    hex_out=de_out[:index]
    nth=de_out[index+1:index+2]
    i=int(nth)
    size=de_out[index+2:index+3]
    for _ in range(i,len(hex_out)):
        if(hex_out[_]==']'):
            loc=_
            break
    nth_value=hex_out[i:loc]
    hex_out=hex_out.replace(f'{nth_value}]',"",1)#f-string remove, nth_value and ]
    out=bin(int(hex_out,16))[2:]
    key_factor=int(nth_value)-int(nth)
    keyfact_bin=bin(key_factor)
    keyfact_bin_fin=str(keyfact_bin[2:])
    for _ in range(1,int(nth)):
            
            keyfact_bin_fin+=keyfact_bin[2:]
            
    keyfact_bin_fin=bin(int(keyfact_bin_fin,2))[2:]
    cc_binary=bin(int(out,2)-int(keyfact_bin_fin,2))[2:]
    cc_hex=hex(int(cc_binary,2))[2:]
    cc_byte=(bytes.fromhex(cc_hex)).decode('utf-8')
    text=(CaesarCipher(cc_byte,offset=key)).decoded
    return text




if __name__ == "__main__":
    main()