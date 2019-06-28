from tkinter import *
import recommender


class App(Frame):

    ratingbox = {}
    movieName = {}
    userRating = ''
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.layout()

    def layout(self):

        self.movieLabel = Label(self.master, text='Movie')
        self.movieLabel.grid(row=0, column=1)

        self.ratingLabel = Label(self.master, text='Rating')
        self.ratingLabel.grid(row=0, column=2)
       
        self.entries = [Entry() for i in range(0,20)]
        rowno = 0
        for i in range(0,20):
            rowno += 1 - i%2
            colno = 1 + i%2
            self.entries[i].grid(row=rowno,column=colno,padx=20,pady=10)
        
        self.GetRec = Button(text='Get Recommendations', command = self.passData)
        self.GetRec.grid(row = 11, columnspan = 3)

    def passData(self):
        for n in range(0, 20):
            if self.entries[n].get() == '':
                continue
            if n%2 == 0:
                self.userRating += self.entries[n].get() + ':'
            else:
                self.userRating += self.entries[n].get() + ','

        self.userRating = self.userRating[:-1]
        self.display()

    def display(self):
        for title in recommender.SimpleRecommender(self.userRating).recommendations:
            Label(self.master, text=title).grid(columnspan = 3)
     

def main():
    root = Tk()
    root.title("MOVIE RECOMMENDER")
    app = App(root)
    root.mainloop()






if __name__ == '__main__':
    main()
