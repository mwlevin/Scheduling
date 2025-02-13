import math

class Course:
    def __init__(self, num, name):
        self.name = name.strip()
        self.num = num.upper().strip()
        self.num_semester = dict()
        self.num_year = dict()
    
    def setFreq(self, years, freq, semester, semester_set):
        
        semester = semester.strip().lower()
        self.freq = freq
        
        for y in years:
            self.num_year[y] = math.floor(freq)
        
        for s in semester_set:
            if (semester == "f" or semester == "s") and not s[0].lower() == semester:
                # must not be taught
                self.num_semester[s] = 0
            elif semester == 'b' or s[0] == semester:
                # must be taught
                self.num_semester[s] = 1
            else:
                # no constraint
                self.num_semester[s] = -1
        
        #print(self.num, semester, self.num_semester)
            
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return self.num
    def __str__(self):
        return str(self.num)+" "+str(self.name)
        
        