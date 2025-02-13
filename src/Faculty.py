
class Faculty:
    def __init__(self, name):
        self.name = name.strip()
        
        self.num_year = dict()
        self.num_semester = dict()
        
        self.current_teaching = set() # set of courses
        self.possible_teaching = set() # set of courses
        
        self.required = dict()

    def setTeaching(self, years, courses_per_year, semester_set):
        
        
        for y in years:
            self.num_year[y] = courses_per_year
            
        for s in semester_set:
            # must be <=
            self.num_semester[s] = 1
            
    def __hash__(self):
        return hash(self.name)
    
    def __repr__(self):
        return self.name
        
    def __str__(self):
        return self.name