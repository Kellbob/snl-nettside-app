from tkinter import *
import requests
from bs4 import BeautifulSoup
from functools import partial
import webbrowser

class tkinter_window():
    def __init__(self, root):

        self.url = "https://snl.no/.search?query="

        self.root = root
        self.bg_color = "#%02x%02x%02x" % (19,19,19)

        self.Label_1,self.Label_2,self.Label_3,self.Label_4,self.Label_5,self.Label_6 = Label(),Label(),Label(),Label(),Label(),Label()
        self.alle_labels_1 = (self.Label_1,self.Label_2,self.Label_3,self.Label_4,self.Label_5,self.Label_6)
        self.Label_7,self.Label_8,self.Label_9,self.Label_10,self.Label_11,self.Label_12 = Label(),Label(),Label(),Label(),Label(),Label()
        self.alle_labels_2 = (self.Label_7,self.Label_8,self.Label_9,self.Label_10,self.Label_11,self.Label_12)
        self.Label_13,self.Label_14,self.Label_15,self.Label_16,self.Label_17,self.Label_18 = Label(),Label(),Label(),Label(),Label(),Label()
        self.alle_labels_3 = (self.Label_13,self.Label_14,self.Label_15,self.Label_16,self.Label_17,self.Label_18)
        self.alle_labels = self.alle_labels_1+self.alle_labels_2+self.alle_labels_3
        self.mini_liste = self.alle_labels[1:-1]
        self.l = [x for x in range(75,521,25)]

        for nummer, d in enumerate(self.alle_labels):
            self.alle_labels[nummer].config(fg="white", bg=self.bg_color)
            if nummer % 2 == 0:
                self.alle_labels[nummer].place(x=10,y=self.l[nummer])
            else:
                self.alle_labels[nummer].place(x=15,y=self.l[nummer])

        root.config(bg=self.bg_color)
        root.title('snl.no')
        root.geometry('525x675+400+50')
        root.resizable(width = False, height = False)
        root.attributes("-alpha", 0.99)

        self.search_bar = Entry(self.root, width=40)
        self.search_bar.place(x=10,y=15)
        self.search_bar.config(borderwidth=0,cursor='xterm')
        self.search_bar.bind("<Return>", self.search_snl)

    def search_snl(self, event):
        self.search = self.search_bar.get()
        for nummer in range(len(self.alle_labels)):
            self.alle_labels[nummer].config(text="")
        try:
            self.text_box.destroy()
        except: pass
        try:
            self.url = "https://snl.no/.search?query="
            self.url += self.search
            self.page = requests.get(self.url)
            self.soup = BeautifulSoup(self.page.content, 'html.parser')
            self.result = self.soup.find(id="content")
            self.title_elements = self.result.find_all("header", class_="reading-tip__header")
            if self.title_elements == []:
                self.alle_labels[0].config(text="Det du søkte etter finnes ikke, eller du skrev feil.")
            else:
                for nummer, tit_elm in enumerate(self.title_elements):
                    self.beskrivelse = tit_elm.find('p',class_='reading-tip__tagline')
                    self.title = tit_elm.find('a', class_='reading-tip__title-link')
                    if None in (self.beskrivelse,self.title):
                        continue
                    self.alle_labels[nummer].config(text=self.title.text.strip()+"        "+self.beskrivelse.text.strip())
                    self.alle_labels[nummer].bind("<Button-1>", partial(self.go_to_website, tit_elm.find('a')['href']))
        finally:
            self.search_bar.delete(0,END)

    def go_to_website(self, value, event):
        for nummer in range(len(self.alle_labels)):
            self.alle_labels[nummer].config(text="")
        self.url = value
        self.page = requests.get(self.url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.result = self.soup.find(id="content")
        self.page_title = self.result.find('h1', class_='page-title__heading')
        self.start_info = self.result.find_all('div', class_='article-text article-text--snl')
        self.alle_labels[0].config(text=self.page_title.text.strip())
        self.hele_text = ""
        try:
            for nummer, paragraf in enumerate(self.start_info):
                self.inhold = paragraf.find('p')
                self.hele_text += "  "+self.inhold.text.strip()+"\n"
        except: pass
        self.text_box = Text(self.root, height=27, width=70)
        self.text_box.place(x=10,y=100)
        self.text_box.insert(END,self.hele_text)
        self.text_box.config(background=self.bg_color, fg="white", state=DISABLED)
        self.alle_labels[-1].config(text=self.url)
        self.alle_labels[-1].bind('<Button-1>', self.open_website)

    def open_website(self, event):
        webbrowser.open(self.url,new=1)

if __name__ == '__main__':
    master = Tk()
    my_win = tkinter_window(master)
    master.mainloop()
