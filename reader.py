# code by Rodrigo Miranda (rodrigo.qmiranda@gmail.com)
# and Josicleda Galvincio (josicleda@gmail.com)

class data(object):
    def __init__(self, itf):
        self.itf = itf
        self.data = {}
        self.prs = []
        self.wls = []
        self.header = None
        self.reader = None
        self.load()

    # Actually reads the data
    # and stores in a dictionary
    def get_data(self):
        rows = [row for row in self.reader]
        for key in self.header:
            n = self.header.index(key)
            v = []
            for row in rows:
                try:
                    v.append(float(row[n]))
                except:
                    if not row[n] == '':
                        v.append(row[n])
            self.data[key] = v

    # This function process
    # the header previously acquired
    def get_headers(self):
        for i in self.data.keys():
            try:
                int(i)
                self.wls.append(i)
            except:
                self.prs.append(i)

    def load(self, sep=","):
        self.itf.reading_data()   # prints the reading warning
        
        self.reader = open(self.itf.csvfile, 'r')  # opens the file
        self.reader = self.reader.readlines()   # make a list from the file

        self.reader = [i.replace('\n', '').replace('\r', '').split(sep) for i in self.reader] # removes the terminator, and splits the lines
        self.header = self.reader[0]    # gets the header from the list
        self.reader = self.reader[1:]    # removes the header from the list

        # In case, the sep is ";"
        # instead of ","
        if len(self.header) == 1:
            return(self.load(sep=";"))

        # Process the data and
        # populates the data structures
        self.get_data()
        self.get_headers()