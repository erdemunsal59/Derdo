from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
import glob
import random

# Seçim alanları için renkler
COLORS = ['blue', 'red', 'pink', 'cyan', 'green', 'black']
# Örnek için Resim boyutları
SIZE = 384, 384


class EtiketAraci:
    def __init__(self, master):
        # Program ayarları
        self.tmp = []
        self.parent = master
        self.parent.title("Etiket Aracı")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width=FALSE, height=FALSE)

        # Programı başlat
        self.imageDir = ''
        self.imageList = []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None
        self.currentLabelclass = ''
        self.cla_can_temp = []
        self.classcandidate_filename = 'etiket.txt'

        # Fare durumu
        self.STATE = {'click': 0, 'x': 0, 'y': 0}

        # Etiket gösterim yolu
        self.etiketIdList = []
        self.etiketId = None
        self.etiketList = []
        self.hl = None
        self.vl = None

        # ----------------- Kullanıcı Arayüzü ---------------------
        # Giriş resmi ve düğmesi
        self.srcDirBtn = Button(self.frame, text="Görüntü yükle", command=self.selectSrcDir)
        self.srcDirBtn.grid(row=0, column=0)

        # Giriş resmi ve girişi
        self.svSourcePath = StringVar()
        self.entrySrc = Entry(self.frame, textvariable=self.svSourcePath)
        self.entrySrc.grid(row=0, column=1, sticky=W + E)
        self.svSourcePath.set(os.getcwd())

        # Yükle düğmesi
        self.ldBtn = Button(self.frame, text="Resimleri yükle", command=self.loadDir)
        self.ldBtn.grid(row=0, column=2, rowspan=2, columnspan=2, padx=2, pady=2, ipadx=5, ipady=5)

        # Etiket dosyası kaydetme düğmesi
        self.desDirBtn = Button(self.frame, text="Etiket çıktı klasörü", command=self.selectDesDir)
        self.desDirBtn.grid(row=1, column=0)

        # Etiket dosyası kaydetme
        self.svDestinationPath = StringVar()
        self.entryDes = Entry(self.frame, textvariable=self.svDestinationPath)
        self.entryDes.grid(row=1, column=1, sticky=W + E)
        self.svDestinationPath.set(os.path.join(os.getcwd(), "Etiketler"))

        # Etiketleme için ana panel
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.canceletiket)  # Mevcut etiketi iptal etmek için <Escape>'e basın
        self.parent.bind("p", self.prevImage)  # Geri gitmek için 'p'ye basın
        self.parent.bind("n", self.nextImage)  # İleri gitmek için 'n'ye basın
        self.mainPanel.grid(row=2, column=1, rowspan=4, sticky=W + N)

        # Etiket Belirleme
        self.classname = StringVar()
        self.classcandidate = ttk.Combobox(self.frame, state='readonly', textvariable=self.classname)
        self.classcandidate.grid(row=2, column=2)
        if os.path.exists(self.classcandidate_filename):
            with open(self.classcandidate_filename) as cf:
                for line in cf.readlines():
                    self.cla_can_temp.append(line.strip('\n'))
        self.classcandidate['values'] = self.cla_can_temp
        self.classcandidate.current(0)
        self.currentLabelclass = self.classcandidate.get()
        self.btnclass = Button(self.frame, text='Etiketi Belirle', command=self.setClass)
        self.btnclass.grid(row=2, column=3, sticky=W + E)

        # Etiket bilgisi gösterilmesi ve etiket silinmesi
        self.lb1 = Label(self.frame, text='Etiketleme Kutusu:')
        self.lb1.grid(row=3, column=2, sticky=W + N)
        self.listbox = Listbox(self.frame, width=32, height=22)
        self.listbox.grid(row=4, column=2, sticky=N + S)
        self.btnDel = Button(self.frame, text='Sil', command=self.deletiket)
        self.btnDel.grid(row=4, column=3, sticky=W + E + N)
        self.btnClear = Button(self.frame, text='Tümünü Sil', command=self.clearetiket)
        self.btnClear.grid(row=4, column=3, sticky=W + E + S)

        # Görüntü navigasyonu için kontrol paneli
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row=6, column=1, columnspan=2, sticky=W + E)
        self.prevBtn = Button(self.ctrPanel, text='<< Önceki Resim', width=14, command=self.prevImage)
        self.prevBtn.pack(side=LEFT, padx=5, pady=3)
        self.nextBtn = Button(self.ctrPanel, text='Sonraki Resim >>', width=14, command=self.nextImage)
        self.nextBtn.pack(side=LEFT, padx=5, pady=3)
        self.progLabel = Label(self.ctrPanel, text="İlerleme:     /    ")
        self.progLabel.pack(side=LEFT, padx=5)
        self.tmpLabel = Label(self.ctrPanel, text="   Resim numarasına git")
        self.tmpLabel.pack(side=LEFT, padx=5)
        self.idxEntry = Entry(self.ctrPanel, width=5)
        self.idxEntry.pack(side=LEFT)
        self.goBtn = Button(self.ctrPanel, text='Git', command=self.gotoImage)
        self.goBtn.pack(side=LEFT)

        # Örnek pano
        self.egPanel = Frame(self.frame, border=10)
        self.egPanel.grid(row=3, column=0, rowspan=5, sticky=N)
        self.tmpLabel2 = Label(self.egPanel, text="Örnek:")
        self.tmpLabel2.pack(side=TOP, pady=5)
        self.egLabels = []
        for i in range(3):
            self.egLabels.append(Label(self.egPanel))
            self.egLabels[-1].pack(side=TOP)

        # Fare konumunu göster
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side=RIGHT)

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(4, weight=1)

    def selectSrcDir(self):
        path = filedialog.askdirectory(title="Görüntü klasörünü seçin", initialdir=self.svSourcePath.get())
        self.svSourcePath.set(path)
        return

    def selectDesDir(self):
        path = filedialog.askdirectory(title="Etiket çıktı klasörünü seçin", initialdir=self.svDestinationPath.get())
        self.svDestinationPath.set(path)
        return

    def loadDir(self):
        self.parent.focus()
        # Resim listesi girişi
        self.imageDir = os.path.join(r'./Images', '%03d' % self.category)
        self.imageDir = self.svSourcePath.get()
        if not os.path.isdir(self.imageDir):
            messagebox.showerror("Error!", message="Belirtilen dizin mevcut değil!")
            return

        extlist = ["*.JPEG", "*.jpeg", "*JPG", "*.jpg", "*.PNG", "*.png", "*.BMP", "*.bmp"]
        for e in extlist:
            filelist = glob.glob(os.path.join(self.imageDir, e))
            self.imageList.extend(filelist)
        # self.imageList = glob.glob(os.path.join(self.imageDir, '*.JPEG'))
        if len(self.imageList) == 0:
            print('Belirtilen dizinde .JPEG resmi bulunamadı!')
            return

        # Klasördeki 1. resmi kullan
        self.cur = 1
        self.total = len(self.imageList)

        # Çıkış dizini ayarları
        self.outDir = os.path.join(r'./Labels', '%03d' % self.category)
        self.outDir = self.svDestinationPath.get()
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)

        # Örnek etiketleri yükle
        self.egDir = os.path.join(r'./Examples', '%03d' % self.category)
        self.egDir = os.path.join(os.getcwd(), "Examples/001")
        if not os.path.exists(self.egDir):
            return
        filelist = glob.glob(os.path.join(self.egDir, '*.JPEG'))
        self.egList = []
        random.shuffle(filelist)
        for (i, f) in enumerate(filelist):
            if i == 1:
                break
            im = Image.open(f)
            r = min(SIZE[0] / im.size[0], SIZE[1] / im.size[1])
            new_size = int(r * im.size[0]), int(r * im.size[1])
            self.tmp.append(im.resize(new_size, Image.ANTIALIAS))
            self.egList.append(ImageTk.PhotoImage(self.tmp[-1]))
            self.egLabels[i].config(image=self.egList[-1], width=SIZE[0], height=SIZE[1])

        self.loadImage()
        print('%d yüklenen resimler %s' % (self.total, self.imageDir))

    def loadImage(self):
        # Resmi yükle
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        size = self.img.size
        self.factor = max(size[0] / 1000, size[1] / 1000., 1.)
        self.img = self.img.resize((int(size[0] / self.factor), int(size[1] / self.factor)))
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width=max(self.tkimg.width(), 400), height=max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image=self.tkimg, anchor=NW)
        self.progLabel.config(text="%04d/%04d" % (self.cur, self.total))

        # Etiketleri yükle
        self.clearetiket()
        # self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        fullfilename = os.path.basename(imagepath)
        self.imagename, _ = os.path.splitext(fullfilename)
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        etiket_cnt = 0
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                for (i, line) in enumerate(f):
                    if i == 0:
                        etiket_cnt = int(line.strip())
                        continue
                    # tmp = [int(t.strip()) for t in line.split()]
                    tmp = line.split()
                    tmp[0] = int(int(tmp[0]) / self.factor)
                    tmp[1] = int(int(tmp[1]) / self.factor)
                    tmp[2] = int(int(tmp[2]) / self.factor)
                    tmp[3] = int(int(tmp[3]) / self.factor)
                    self.etiketList.append(tuple(tmp))
                    color_index = (len(self.etiketList) - 1) % len(COLORS)
                    tmpId = self.mainPanel.create_rectangle(tmp[0], tmp[1], \
                                                            tmp[2], tmp[3], \
                                                            width=2, \
                                                            outline=COLORS[color_index])
                    self.etiketIdList.append(tmpId)
                    self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' % (tmp[4], tmp[0], tmp[1], tmp[2], tmp[3]))
                    self.listbox.itemconfig(len(self.etiketIdList) - 1, fg=COLORS[color_index])
                    self.listbox.itemconfig(len(self.etiketIdList) - 1,
                                            fg=COLORS[(len(self.etiketIdList) - 1) % len(COLORS)])

    def saveImage(self):
        if self.labelfilename == '':
            return
        with open(self.labelfilename, 'w') as f:
            f.write('%d\n' % len(self.etiketList))
            for etiket in self.etiketList:
                f.write("{} {} {} {} {}\n".format(int(int(etiket[0]) * self.factor),
                                                  int(int(etiket[1]) * self.factor),
                                                  int(int(etiket[2]) * self.factor),
                                                  int(int(etiket[3]) * self.factor), etiket[4]))
                f.write(' '.join(map(str, etiket)) + '\n')
        print('Resim No. %d kaydedildi' % (self.cur))

    def mouseClick(self, event):
        if self.STATE['click'] == 0:
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            self.etiketList.append((x1, y1, x2, y2, self.currentLabelclass))
            self.etiketIdList.append(self.etiketId)
            self.etiketId = None
            self.listbox.insert(END, '%s : (%d, %d) -> (%d, %d)' % (self.currentLabelclass, x1, y1, x2, y2))
            self.listbox.itemconfig(len(self.etiketIdList) - 1, fg=COLORS[(len(self.etiketIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    def mouseMove(self, event):
        self.disp.config(text='x: %d, y: %d' % (event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width=2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width=2)
        if 1 == self.STATE['click']:
            if self.etiketId:
                self.mainPanel.delete(self.etiketId)
            len(self.etiketIdList) % len(COLORS)
            self.etiketId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], \
                                                            event.x, event.y, \
                                                            width=2, \
                                                            outline=COLORS[len(self.etiketList) % len(COLORS)])

    def canceletiket(self, event):
        if 1 == self.STATE['click']:
            if self.etiketId:
                self.mainPanel.delete(self.etiketId)
                self.etiketId = None
                self.STATE['click'] = 0

    def deletiket(self):
        sel = self.listbox.curselection()
        if len(sel) != 1:
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.etiketIdList[idx])
        self.etiketIdList.pop(idx)
        self.etiketList.pop(idx)
        self.listbox.delete(idx)

    def clearetiket(self):
        for idx in range(len(self.etiketIdList)):
            self.mainPanel.delete(self.etiketIdList[idx])
        self.listbox.delete(0, len(self.etiketList))
        self.etiketIdList = []
        self.etiketList = []

    def prevImage(self):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def setClass(self):
        self.currentLabelclass = self.classcandidate.get()
        print('Etiket sınıfını ayarla : %s' % self.currentLabelclass)


if __name__ == '__main__':
    root = Tk()
    tool = EtiketAraci(root)
    root.resizable(width=True, height=True)
    root.mainloop()
