from tkinter import *
from tkinter import filedialog
import tkinter.ttk as tkk
import pygame
import time
from mutagen.mp3 import MP3


class Music(Tk):
    def __init__(self):
        super().__init__()
        self.stopped = False
        self.songs = {}
        pygame.mixer.init()
        self.paused = False

        # create playlist box
        self.plb = Listbox(self, bg="#42f5d1", fg="#7842f5", width=60, selectbackground="#ff8000",
                           selectforeground='black')
        self.plb.pack(pady=10, padx=10)
        self.seekf = LabelFrame(self)
        self.seekf.pack()
        self.seektime = Label(self.seekf, text='00:00')
        self.seektime.grid(row=0, column=0, padx=20)
        self.seekttime = Label(self.seekf, text='00:00')
        self.seekttime.grid(row=0, column=2, padx=20)
        self.seeklen = tkk.Scale(self.seekf, from_=0, to=100, value=0, orient=HORIZONTAL, length=200,
                                 command=self.slide)
        self.seeklen.grid(row=0, column=1, pady=20)

        self.bb_img = PhotoImage(file='images/bb.png', )
        self.fb_img = PhotoImage(file='images/fb.png')
        self.pyb_img = PhotoImage(file='images/pyb.png')
        self.pab_img = PhotoImage(file='images/pab.png')
        self.sb_img = PhotoImage(file='images/sb.png')
        # create Buttons
        self.cf = Frame(self.seekf)

        self.cf.grid(column=1, pady=20)
        self.pyb = Button(self.cf, image=self.pyb_img, borderwidth=0, command=self.play)
        self.bb = Button(self.cf, image=self.bb_img, borderwidth=0, command=self.previous_song)
        self.fb = Button(self.cf, image=self.fb_img, borderwidth=0, command=self.next_song)
        self.pab = Button(self.cf, image=self.pab_img, borderwidth=0, command=lambda: self.pause(self.paused))
        self.sb = Button(self.cf, image=self.sb_img, borderwidth=0, command=self.stop)

        self.bb.grid(row=0, column=1, padx=10)
        self.fb.grid(row=0, column=5, padx=10)
        self.pyb.grid(row=0, column=3, padx=10)
        self.pab.grid(row=0, column=2, padx=10)
        self.sb.grid(row=0, column=4, padx=10)

        self.menu = Menu(self)
        self.config(menu=self.menu)

        self.add_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='Songs', menu=self.add_menu)
        self.add_menu.add_command(label="Add File", command=self.add_song)
        self.add_menu.add_command(label="Add folder", command=self.add_many_songs)
        self.audf = LabelFrame(self, text='Volume')
        self.audf.pack(pady=20)
        self.audioscale = tkk.Scale(self.audf, from_=0, to=1, value=0.75, orient=HORIZONTAL, command=self.vol)
        self.audioscale.grid(row=0, column=1)
        self.low_aud = PhotoImage(file='C:\\Users\\adith\\Documents\\new\\images\\Volume_Hight-512.png')
        self.high_aud = PhotoImage(file='C:\\Users\\adith\\Documents\\new\\images\\Volume_Low-512.png')

        Label(self.audf, image=self.low_aud).grid(row=0, column=2)
        Label(self.audf, image=self.high_aud).grid(row=0, column=0)
        self.add_menu.add_command(
            label="Remove songs", command=self.remove_song)
        self.add_menu.add_command(
            label="Remove all songs", command=self.remove_all_songs)
        self.sbar = Label(self, text='', bd=1, relief=GROOVE, anchor=E)
        self.sbar.pack(fill=X, side=BOTTOM, ipady=2)

    def add_song(self):
        song_path = filedialog.askopenfilename(initialdir="F:\God Songs", title=" Choose a Song",
                                               filetypes=(('mp3 Files', '*.mp3'),))
        self.songs[song_path.split('/')[-1].split('.')[0]] = song_path
        self.l.config(text=song_path.split('/')[-1].split('.')[0])
        self.plb.insert(END, song_path.split('/')[-1].split('.')[0])
        print(self.songs)

    def add_many_songs(self):
        songs = filedialog.askopenfilenames(
            initialdir="F:\God Songs", title=" Choose a Song", filetypes=(('mp3 Files', '*.mp3'),))
        for song in songs:
            self.songs[song.split('/')[-1].split('.')[0]] = song
            self.plb.insert(END, song.split('/')[-1].split('.')[0])
        print(self.songs)

    def remove_song(self):
        self.song = self.plb.get(ACTIVE)
        self.plb.delete(ANCHOR)
        print(self.song)
        del self.songs[self.song]
        print("deleted")

    def remove_all_songs(self):
        self.plb.delete(0, END)
        self.songs = {}
        print('All songs Deleted')

    def play(self):

        self.seeklen.config(value=0)
        self.song = self.plb.get(ACTIVE)
        self.stopped = False
        song = self.songs[self.song]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.sbar.config(text='Playing...')
        self.play_time()

    def stop(self):
        self.seeklen.config(value=0)
        pygame.mixer.music.stop()
        self.sbar.config(text='Stopped')
        self.stopped = True

    def pause(self, paused):
        if self.paused:
            # unpause
            pygame.mixer.music.unpause()
            self.paused = False
            self.sbar.config(text='Playing...')

        else:
            # pause
            pygame.mixer.music.pause()

            self.paused = True
            self.sbar.config(text='Paused')

    def next_song(self):
        # self.seek
        self.seeklen.config(value=0)
        next_one = self.plb.curselection()
        next_one = next_one[0] + 1
        song = self.plb.get(next_one)
        song = self.songs[song]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.plb.selection_clear(0, END)
        self.plb.activate(next_one)
        self.plb.selection_set(next_one, last=None)

    def previous_song(self):
        self.seeklen.config(value=0)
        next_one = self.plb.curselection()
        next_one = next_one[0] - 1
        song = self.plb.get(next_one)
        song = self.songs[song]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        self.plb.selection_clear(0, END)
        self.plb.activate(next_one)
        self.plb.selection_set(next_one, last=None)

    def play_time(self):
        self.current = self.song

        if self.stopped:
            return
        # curt = pygame.mixer.music.get_pos() / 1000
        # con_curt = time.strftime('%M:%S', time.gmtime(curt))
        self.song = self.plb.get(ACTIVE)
        song = self.songs[self.song]
        song_mut = MP3(song)
        self.song_len = song_mut.info.length
        if self.current != self.song:
            return
        if int(self.seeklen.get()) == int(self.song_len):
            self.stop()


        elif self.paused:
            pass
        else:

            self.next_time = int(self.seeklen.get()) + 1
            self.seeklen.config(to=self.song_len, value=self.next_time)
            self.con_curt = time.strftime('%M:%S', time.gmtime(int(self.seeklen.get())))
            self.seektime.config(text=f"{self.con_curt}")
            print(self.seeklen.get())

        self.con_songlen = time.strftime('%M:%S', time.gmtime(self.song_len))
        if self.seeklen.get() > 0:
            self.seektime.config(text=f"{self.con_curt}")
            self.seekttime.config(text=f'{self.con_songlen}')

        self.seektime.after(1000, self.play_time)

    def vol(self, x):
        pygame.mixer.music.set_volume(self.audioscale.get())

    def slide(self, x):
        self.song = self.plb.get(ACTIVE)

        song = self.songs[self.song]
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0, start=self.seeklen.get())


m = Music()
m.title('MP3 Player')
m.geometry('500x450')
m.mainloop()
