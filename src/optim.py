from docplex.mp.model import Model
from src import Course
from src import Faculty
import time
import math

class optim:
    def __init__(self, years, willing_to_teach, initials, frequencies, special_load, required):
    
        self.overload_penalty = 200
        self.current_benefit = 5
        self.multiple_teacher_penalty = 1
        
        self.courses = set()
        self.semesters = list()
        self.faculty = list()
        self.years = years
        
        self.semesters.append("f"+str(years[0]))
        
        for i in range(1, len(years)-1):
            y = years[i]
            self.semesters.append("s"+str(y))
            self.semesters.append("f"+str(y))
            
        self.semesters.append("s"+str(years[len(self.years)-1]))
        
        
        error = False
        
        error = not self.readWillingToTeach(willing_to_teach) or error
        error = not self.readFreq(frequencies, initials) or error
        
        for i in self.faculty:
            i.setTeaching(years, 2, self.semesters)
            
        
        for c in self.courses:
            instructors = 0
            
            for i in self.faculty:
                if c in i.current_teaching or c in i.possible_teaching:
                    instructors += 1
                    
            if len(c.num_year) == 0:
                print("did not find course frequencies", c)
                error = True
                
            #print(instructors, c)
            
            if instructors == 0:
                print("no instructor for", c)
                error = True
            #print("\t", c.freq, c.num_year)
        
        
            
            
        error = not self.readSpecialTeachingLoad(special_load) or error
        error = not self.readRequired(required) or error
    
    
    
    
        if error:
            exit()
            
    def readRequired(self, required_file):
        error = False
        
        with open(required_file, "r") as f:
            headerline = True
            
            for line in f:
                if headerline:
                    headerline = False
                    continue
                    
                    
                data = line.split(",")
                
                if len(data) > 3:
                    person = self.findFaculty(data[0])
                    course = self.findCourse(data[1], data[2])
                    
                    
                    if person is None or course is None:
                        print("required file could not find", data[1], data[2], person)
                        error = True
                        continue
                        
                    if data[3].strip().isnumeric():
                        person.required[course] = int(data[3].strip())
                        print(person, course, int(data[3].strip()))
                    else:
                        person.required[course] = list()
                        for i in range(3, len(data)):
                            if len(data[i].strip()) > 0:
                                sem = self.findSemester(data[i])
                                if sem is not None:
                                    person.required[course].append(sem)
                                else:
                                    print("could not identify semester", sem, person, course.num)
                                    error = True
                        
                    
                    
        return not error
    
    def readSpecialTeachingLoad(self, special_file):
        error = False
        
        with open(special_file, "r") as f:
            headerline = True
            
            indices = dict()
            
            for line in f:
                if headerline:
                    data = line.split(",")
                    
                    for i in range(0, len(data)):
                        if len(data[i].strip() ) > 0:
                            indices[i] = self.findSemester(data[i])
                
                    headerline = False
                    continue
                    
                data = line.split(",")
                
                person = self.findFaculty(data[0])
                
                        
                if person == None:
                    print("Could not find person in special case file", data[0])
                    error = True
                    
                for i in range(1, len(data)):
                    if len(data[i].strip()) > 0:
                        person.num_semester[indices[i]] = int(data[i])
       
        return not error
    
    def findSemester(self, name):
        name = name.strip().lower().replace(' ', '').replace('fall', 'f').replace('spring', 's')
        
        for i in self.semesters:
            if i.lower() == name.lower():
                return i
        return None
           
    def findFaculty(self, name):
        for i in self.faculty:
            if i.name.lower() == name.strip().lower():
                return i
        return None
        
    def findCourse(self, num, name):
        for i in self.courses:
            if i.num.upper() == num.upper().strip() and i.name.lower() == name.lower().strip():
                return i
        return None
        
    def readFreq(self, freq_file, initials_file):

        error = False
        
        initials = dict()
        
   
        
        with open(initials_file, "r") as f:
            for line in f:
                data = line.split(",")
                if len(data) < 2:
                    continue
                    
                person = None

                for p in self.faculty:
 
                    if p.name.lower() == data[1].strip().lower():
                        person = p
                        break

                if person is not None:
                    initials[data[0].strip().upper()] = person
                
     
        #print(self.faculty)
        

        with open(freq_file, "r") as f:
            headerline = True
            for line in f:
                data = line.split(",")
                
        

                if headerline:
                    headerline = False
                    continue
                    

                freq_data = data[0].strip()
                
                if len(freq_data) > 0:

                    sem = data[1]
                    
                    if "?" in sem:
                        sem = "?"
                    
                    freq = 0
                    
                    if "1/yr" in freq_data or "1/ yr" in freq_data:
                        freq = 1
                    elif "2/yr" in freq_data or "2/ yr" in freq_data:
                        freq = 2
                    elif "1/2 yr" in freq_data or "1/2yr" in freq_data:
                        freq = 0.5
                    elif "1/3" in freq_data:
                        freq = 2.0/3
                    elif "1/4" in freq_data:
                        freq = 1.0/4
                        
                    coursenum = data[2].upper().strip()
                    coursename = data[3].strip().replace('"', '')
                    
                    

                    if not "CEGE" in coursenum:
                        coursenum = "CEGE "+str(coursenum)


                    coursenum = coursenum[0:9]

                    course = None

                    for c in self.courses:
                        if c.name.lower() == coursename.strip().lower():
                            course = c
                            break

                    if course == None:
                         
                        course = Course.Course(coursenum, coursename)
                        instructors = 0
                        
                        for i in range(5, len(data)):
                            if len(data[i].strip()) > 0 and data[i].isalpha():
                                p_init = data[i].strip().upper()
                                
                                if not p_init in initials:
                                    print("did not find", p_init)
                                    instructors = -1
                                    break
                                
                                initials[p_init].current_teaching.add(course)
                                instructors += 1
                                    
                        if instructors > 0:
                            self.courses.add(course)
                        elif instructors == -1:
                            error = True
                    
                    
                    if course is not None:
                        course.setFreq(self.years, freq, sem, self.semesters)
                    else:
                        print("course missing from freq file", course)
                        

        return not error
        
 
        
    def readWillingToTeach(self, willing_to_teach):
        
        error = False
        
        num_teachers = 0
        
        with open(willing_to_teach, "r") as f:
            firstline = False
            
            for line in f:
                data = line.split(",")
                
                if len(data) == 0:
                    if firstline:
                        break
                    else:
                        continue
                        
                if data[5].strip() == "1":
                    for i in range(0, len(data)):
                        if data[5+i].strip().isnumeric():
                            num_teachers += 1
                        else:
                            break
                        
                if data[4].strip().lower() == "is the class assigned?":
                    for i in range(0, num_teachers):
                        self.faculty.append(Faculty.Faculty(data[5+i].strip()))
                
                if data[0].strip() == "# classes":
                    firstline = True
                    continue
                elif not firstline:
                    continue
                    
                
                
                if data[1].strip().isnumeric():
                    if "/" in data[2]:
                        num = data[2].strip()[0:data[2].index("/")]
                    else:
                        num = data[2].strip()
                    name = data[3].strip().replace('"', '')
                    course = Course.Course(num, name)
                    self.courses.add(course)
                    
                    #print(name, data)
       
                    for i in range(0, num_teachers):
                        if data[5+i].strip().lower() == 'r':
                            self.faculty[i].current_teaching.add(course)
                        elif data[5+i].strip().lower() == 'w':
                            self.faculty[i].possible_teaching.add(course)
                            
        return not error
    
    def printFacultyAssign(self, output):
        with open(output, 'w') as f:
            header = ""
            for s in self.semesters:
                header += ","+str(s)
            print(header, file=f)
            
            for i in self.faculty:
                line = i.name
                
                for s in self.semesters:
                    assign = ""
                    
                    for c in self.courses:
                        if self.ilp.a[(c,s,i)].solution_value > 0.9:
                            if len(assign) > 0:
                                assign += " & "+c.num
                            else:
                                assign = c.num
                    
                    line += ","+assign
                print(line, file=f)
    
    def compare(self, c):
        return c.num
        
    def printCourseAssign(self, output):
        sorted = list()
        
        for c in self.courses:
            sorted.append(c)
            
            
        sorted.sort(key=self.compare)
        
        with open(output, 'w') as f:
            header = ",,freq"
            for s in self.semesters:
                header += ","+str(s)
            print(header, file=f)
            
            for c in sorted:
                line = c.num+","+c.name+","+str(c.freq)
                
                
                for s in self.semesters:
                    person = None

                    for i in self.faculty:
                        if self.ilp.a[(c,s,i)].solution_value > 0.9:
                            person = i
                            break
                    
                    
                    line += ","
                    
                    if person is not None:
                        line += person.name
                        
                print(line, file=f)

    def solve(self):
        self.initModel()
        
        self.ilp.solve()
        
        print(self.ilp.solve_details.status)
        
        return "infeasible" not in self.ilp.solve_details.status
        
    def initModel(self):
        self.ilp = Model()
        
        self.ilp.x = {(c,s): self.ilp.integer_var(lb=0, ub=1) for c in self.courses for s in self.semesters}
        self.ilp.a = {(c,s,i): self.ilp.integer_var(lb=0, ub=1) for c in self.courses for s in self.semesters for i in self.faculty}
        self.ilp.extra = {(s,i): self.ilp.continuous_var(lb=0,ub=1) for s in self.semesters for i in self.faculty}
        self.ilp.taught = {(c,i): self.ilp.integer_var(lb=0, ub=1) for c in self.courses for i in self.faculty}
        self.ilp.num_instructors = {c: self.ilp.integer_var(lb=0) for c in self.courses}    
        
        # specified courses
        for i in self.faculty:
            if len(i.required) > 0:
                for c in i.required.keys():
                    if isinstance(i.required[c], int):
                        self.ilp.add_constraint(sum(self.ilp.a[(c,s,i)] for s in self.semesters) >= int(i.required[c]))
                    else:
                        #print(c, i, i.required[c])
                        for s in i.required[c]:
                            self.ilp.a[(c,s,i)].lb = 1
        
        
        # faculty only teach courses that they are willing
        
        for c in self.courses:
            for i in self.faculty:
                if c not in i.current_teaching and c not in i.possible_teaching:
                    for s in self.semesters:
                        self.ilp.a[(c,s,i)].ub = 0
                        
        # limit on number of courses per faculty
        
        for i in self.faculty:
            for s in self.semesters:
                if i.num_semester[s] == 0:
                    for c in self.courses:
                        self.ilp.a[(c,s,i)].ub = 0
                else:
                    self.ilp.add_constraint(sum(self.ilp.a[(c,s,i)] for c in self.courses) <= i.num_semester[s] + self.ilp.extra[(s,i)])
                
            
            for y in self.years:
                if "f"+str(y) in self.semesters and "s"+str(y) in self.semesters:
                    self.ilp.add_constraint(sum(self.ilp.a[(c,"f"+str(y),i)] + self.ilp.a[(c,"s"+str(y),i)] for c in self.courses)  <= i.num_year[y] + self.ilp.extra[("s"+str(y), i)] + self.ilp.extra[("f"+str(y), i)])
             
        
        
        # link x and y
        for c in self.courses:
            for s in self.semesters:
                self.ilp.add_constraint(sum(self.ilp.a[(c,s,i)] for i in self.faculty) == self.ilp.x[(c,s)])
        
        
        # whether faculty teaches the course
        for i in self.faculty:
            for c in self.courses:
                if c in i.possible_teaching or c in i.current_teaching:
                    for s in self.semesters:
                        self.ilp.add_constraint(self.ilp.taught[(c,i)] >= self.ilp.a[(c,s,i)])
                    self.ilp.add_constraint(self.ilp.taught[(c,i)] <= sum(self.ilp.a[(c,s,i)] for s in self.semesters))
                        
                        
        for c in self.courses:
            self.ilp.add_constraint(self.ilp.num_instructors[c] == sum(self.ilp.taught[(c,i)] for i in self.faculty))
            
            
            
        
        # courses must be taught as specified
        for c in self.courses:
            for y in self.years:
                if "f"+str(y) in self.semesters and "s"+str(y) in self.semesters:
                    self.ilp.add_constraint(self.ilp.x[c,'f'+str(y)] + self.ilp.x[c,'s'+str(y)] >= c.num_year[y])
            
            

            #print(c, math.floor(c.freq * len(self.semesters)/2), math.ceil(c.freq * len(self.semesters)/2))
            self.ilp.add_constraint(sum(self.ilp.x[c,s] for s in self.semesters) >= math.floor(c.freq * len(self.semesters)/2))
            self.ilp.add_constraint(sum(self.ilp.x[c,s] for s in self.semesters) <= math.ceil(c.freq * len(self.semesters)/2))
                
            for s in self.semesters:
                if c.num_semester[s] == 0:
                    self.ilp.x[c, s].ub = 0
                elif c.num_semester[s] > 0 and c.freq >= 1:
                    self.ilp.x[c, s].lb = c.num_semester[s]
                    
                    
                    
        # 2 instructors for course with freq of 2
        for c in self.courses:
            if c.freq >= 2:
                self.ilp.add_constraint(self.ilp.num_instructors[c] >= 2)
        
        
        overload =  sum(self.ilp.extra[(s,i)] for s in self.semesters for i in self.faculty)
        
        current = 0
        
        for i in self.faculty:
            for c in i.current_teaching:
                for s in self.semesters:
                    current += self.ilp.a[(c,s,i)]
                    
        num_preps = sum(self.ilp.taught[(c,i)] for c in self.courses for i in self.faculty)
                    
        self.ilp.minimize(self.overload_penalty * overload - self.current_benefit  * current + self.multiple_teacher_penalty * num_preps)