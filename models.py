from pprint import pprint
from postgres import PGWrapper
#  psql -h sepgdb.c50u4bslwwg0.eu-west-2.rds.amazonaws.com -d sepgdb -U postgres -W

db_config = {
    "database": "rarescraciunescu",
    "user": "rarescraciunescu",
    "password": "qwerty123",
    "host": "depgdb.crhso94tou3n.eu-west-2.rds.amazonaws.com",
    "port": 5432,

}
db_con = PGWrapper(db_config)
db_con.connect()


class Module:
    """
    Class description: This abstracts a real life UCL module (like Software Engineering).
    Relationships:
        It will be contained in multiple courses.
        It will contain multiple students.
        It will contain a single module leader.
        It will contain multiple teaching assistants.
        !!!THEORY: This is an example of the composition pattern. Check 2c.
    Parameters: name
    Properties:
        Instance attributes:
            self._name (string),
            self._students (list of instances of the Student object),
            self._teaching_assistants (list of instances of TeachingAssistant object),
            self._module_leader (instance of Teacher object)
        Class attributes:
            cls._all_modules (a list of all Module instances)
    Calling Module('some_name') will actually call the __init__ function which will return an instance of the Module class.
    """

    _all_modules = []

    def __init__(self, name):
        """
        Constructor of the Module class
        Parameters: name
        Returns: an instance of the class Module
        """
        self._name = name
        self._students = []
        self._teaching_assistants = []
        self._courses = []
        self._module_leader = None

        Module._all_modules.append(self)

    def get_name(self):
        return self._name

    def set_name(self, name):
        """
        We need to make sure that name is a string
        """
        assert isinstance(name, str)
        self._name = name

    def get_students(self):
        return self._students

    def add_student_to_module(self, student):
        """
        We need to make sure that student parameter is an instance of the Student class
        """
        assert isinstance(student, Student)
        self._students.append(student)

    def get_tas(self):
        return self._teaching_assistants

    def add_ta_to_module(self, ta):
        """
        We need to make sure that ta is an instance of the TeachingAssistant class
        """
        assert isinstance(ta, TeachingAssistant)
        self._teaching_assistants.append(ta)

    def get_teaching_assistants(self):
        return self._teaching_assistants

    def get_courses_of_module(self):
        return self._courses

    def add_module_to_course(self, course):
        """
        1. We need to make sure the course param is an instance of the Course class
        2. We need to make sure we add the module to the course's list as well
        """
        assert isinstance(course, Course)
        self._courses.append(course)
        course.add_module_to_course(self)

    def get_module_leader(self):
        return self._module_leader

    def set_module_leader(self, teacher):
        """
        We need to make sure that the module leader is an instance of the Teacher class
        """
        assert isinstance(teacher, Teacher)
        self._module_leader = teacher

    @classmethod
    def get_all_modules(cls):
        return cls._all_modules


class Course:
    """
    Class description: This abstracts a real life UCL course (like MSc Data Science).
    Relationships:
        It will contain multiple modules.
    Parameters: name
    Properties:
        Instance attributes:
            self._name (string),
            self._modules (list of instances of the Module object),
        Class attributes:
            cls._all_courses (a list of all Course instances)
    Calling Course('some_name') will actually call the __init__ function which will return an instance of the Course class.
    """

    _all_courses = []

    def __init__(self, name):
        """
        Constructor of the Course class
        Parameters: name
        Returns: an instance of the class Course
        """
        self._name = name
        self._modules = []

    def get_name(self):
        return self._name

    def set_name(self, name):
        """
        We need to assert that name is a string
        """
        assert isinstance(name, str)
        self._name = name

    def get_modules(self):
        return self._modules

    def add_module_to_course(self, module):
        """
        We need to make sure that module is an instance of the Module class
        """
        assert isinstance(module, Module)
        self._modules.append(module)

    @classmethod
    def get_all_courses(cls):
        return cls._all_courses


class UCLPerson:
    """
    Class description: This abstracts an UCL Person (like David or any student).
    Relationships:
        It will extend the TeachingAssistant, Teacher and Student class.
    Parameters: first_name, middle_name, last_name
    Properties:
        Instance attributes:
            self._first_name (string),
            self._middle_name (string),
            self._last_name (string),
    Calling UCLPerson('some_first_name', 'some_middle_name', 'some_last_name') will actually call the __init__ function which will return an instance of the UCLPerson class.
    """

    def __init__(self, first_name, middle_name, last_name):
        """
        Constructor of the UCLPerson class
        Parameters: first_name, middle_name, last_name
        Returns: an instance of the class UCLPerson
        """
        self._first_name = first_name
        self._middle_name = middle_name
        self._last_name = last_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        print("Look, setter set_first_name is being called.")
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        print("Look, setter set_last_name setter is being called.")
        self._last_name = last_name

    @property
    def middle_name(self):
        return self._middle_name

    @middle_name.setter
    def middle_name(self, middle_name):
        print("Look, setter set_middle_name is being called.")
        self._middle_name = middle_name

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"


class Instructor(UCLPerson):
    """
    Class description: This abstracts an Instructor which extends the UCLPerson class.
    Relationships:
        It will extend the TeachingAssistant, Teacher and Student class.
        All instructors can add students to courses, however TAs can add only to courses they belong to (overriden method in the child class)
    Parameters: first_name, middle_name, last_name
    Properties:
        Instance attributes:
            self._first_name (string),
            self._middle_name (string),
            self._last_name (string),
    Calling Instructor('some_first_name', 'some_middle_name', 'some_last_name') will actually call the __init__ function which will return an instance of the Instructor class.
    """

    def __init__(self, first_name, middle_name, last_name):
        """
        Constructor of the Instructor class
        Parameters: first_name, middle_name, last_name
        It should call the constructor of the UCLPerson class
        Returns: an instance of the class Instructor
        """
        UCLPerson.__init__(self, first_name, middle_name, last_name)

    def add_student_to_module(self, module, student):
        """
        This aims to solve number 4 with 4a and 4b constraints defined in the Business Specifications:
            a) Only teachers can add any student to any module.
            b) TAs can add students to modules that they belong to.
        Therefore, we need to loop through the module's teaching assistants and check
        if "self" is in there.

        Theory: This links to polymorphism. Check how we have a different behaviour for each of the extended classes.
        """
        if isinstance(self, Teacher):
            module.add_student_to_module(student)
        if isinstance(self, TeachingAssistant):
            modules_tas = module.get_tas()
            if self in modules_tas:
                module.add_student_to_module(student)
            else:
                print(
                    f"The ta {self.get_full_name()} is not part of module {module.get_name()}"
                )


class Teacher(Instructor):
    """
    Class description: This abstracts a Teacher which extends the Instructor class.
    Relationships:
        It is an Instructor which in turn is an UCLPerson.
        Instances of this class can be the leader of a module.
        Instances of this class can add anyone to a team including TAs.
        Instances of this class can add modules to courses.
        Instances of this class can be part of modules.
        Instances of this class can be part of teams.
    Parameters: first_name, middle_name, last_name
    Properties:
        Instance attributes:
            self._first_name (string),
            self._middle_name (string),
            self._last_name (string),
    Calling Teachers('some_first_name', 'some_middle_name', 'some_last_name') will actually call the __init__ function which will return an instance of the Teachers class.
    """

    def __init__(self, first_name, middle_name, last_name):
        """
        Constructor of the Teacher class
        Parameters: first_name, middle_name, last_name
        It should call the constructor of the Instructor class
        Returns: an instance of the class Instructor
        """
        Instructor.__init__(self, first_name, middle_name, last_name)

    def create_module(self, module_name):
        """
        This method template aims to solve part of the business spec 1.
        If a teacher creates the module, he will also become the module leader.
        """
        module = Module(module_name)
        module.set_module_leader(self)
        return module

    def create_course(self, course_name):
        """
        This method template aims to solve part of the business spec 1.
        """
        course = Course(course_name)
        return course

    def add_ta_to_module(self, module, ta):
        """
        We need to make sure module and ta are actually a Module and TeachingAssistant object
        This method template aims to solve part of the business spec 1.
        """
        assert isinstance(module, Module)
        assert isinstance(ta, TeachingAssistant)
        module.add_ta_to_module(ta)

    def add_module_to_course(self, module, course):
        module.add_module_to_course(course)


class TeachingAssistant(Instructor):
    """
    Class description: This abstracts a TA which extends the Instructor class.
    Relationships:
        It is a TA which in turn is an Instructor and a UCLPerson.
        Instances of this class can add students to modules that they also belong to.
        Instances of this class can be part of modules.
        Instances of this class can be part of teams.
    Parameters: first_name, middle_name, last_name
    Properties:
        Instance attributes:
            self._first_name (string),
            self._middle_name (string),
            self._last_name (string),
    Calling Teachers('some_first_name', 'some_middle_name', 'some_last_name') will actually call the __init__ function which will return an instance of the TeachingAssistant class.
    """

    def __init__(self, first_name, middle_name, last_name):
        """
        Constructor of the TeachingAssistant class
        Parameters: first_name, middle_name, last_name
        It should call the constructor of the Instructor class
        Returns: an instance of the class TeachingAssistant
        """
        Instructor.__init__(self, first_name, middle_name, last_name)


class Student(UCLPerson):
    """
    Class description: This abstracts a Student which extends the UCLPerson class.
    Relationships:
        It is a Student which in turn is an UCLPerson.
        Instances of this class can be part of modules.
        Instances of this class can be part of teams.
    Parameters: first_name, middle_name, last_name, student_id
    Properties:
        Instance attributes:
            self._first_name (string),
            self._middle_name (string),
            self._last_name (string),
            self._student_id (string),
    Calling Teachers('student_id', 'some_first_name', 'some_middle_name', 'some_last_name') will actually call the __init__ function which will return an instance of the Student class.
    """

    _all_students = []

    def __init__(self, student_id, first_name, middle_name, last_name):
        """
        Constructor of the Student class
        Parameters: first_name, middle_name, last_name
        It should call the constructor of the UCLPerson class
        Returns: an instance of the class Student
        """
        UCLPerson.__init__(self, first_name, middle_name, last_name)
        self._student_id = student_id
        Student._all_students.append(self)

    @property
    def student_id(self):
        return self._student_id

    @student_id.setter
    def student_id(self, student_id):
        """
        Even though the getter and setter have the same function name, the property decorator knows how to tell them apart. It is a requirement to have them
        the same, otherwise you should get an error 'AttributeError: can't set attribute'.
        """
        print("Look, setter set_student_id is being called.")
        self._student_id = student_id

    def get_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}/student_id:{self.student_id}"


class TeamMessageQueue:
    """
    Class description: This abstracts a TeamMessageQueue.
    Relationships:
        Every team will have its own TeamMessageQueue.
    Parameters: None
    Properties:
        Instance attributes:
            self._items (list),
    """

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)


class Message:

    """
    In this class we will model how a message will look like.
    """

    def __init__(self, message, from_team):
        self._message = message
        self._from_team = from_team

    @property
    def message(self):
        return self._message

    @property
    def from_team(self):
        return self._from_team


class Team:
    _all_teams = []

    def __init__(self, name, db_con, *args):
        """
        Only students, tas and teachers can be part of a team
        """
        # team_names = db_con.get_all_teams()
        # if name not in team_names:
        #     print("This is not a valid team. Your team name should be a string with the pattern <team_YOURTEAMLETTER>. An example is team_a")
        # else:
        self._name = name
        for arg in [*args]:
            assert (
                isinstance(arg, Student)
                or isinstance(arg, TeachingAssistant)
                or isinstance(arg, Teacher)
            )
        self._team_members = list(args)
        self._message_queue = TeamMessageQueue()
        self._db_con = db_con



        Team._all_teams.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def team_members(self):
        return self._team_members

    @team_members.setter
    def team_members(self, *args):
        self._team_members = list(args)

    def add_to_team(self, member):
        if member not in self._team_members:
            self._team_members.append(member)
        else:
            print(f"Member {member.get_name()} is already in the team.")

    def remove_from_team(self, member):
        if member in self._team_members:
            self.team_members.pop(self.team_members.index(member))
        else:
            print(f"Member {member.get_name()} is not in team self._name.")

    def add_message_to_queue(self, message):
        self._message_queue.enqueue(message)

    def send_message_to_team(self, team, message):
        """
        In this method we actually need to construct a message object
        that we will push to the receiving team's message queue
        Moreover, we would want the message to be a string
        """
        assert isinstance(message, str)
        message = Message(message, self)
        team.add_message_to_queue(message)

    def reply_to_next_message_in_queue(self):
        queue_item = None
        try:
            queue_item = self._message_queue.dequeue()
        except IndexError as e:
            print("There is no message in your queue")
        if queue_item:
            received_message = queue_item.message
            from_team = queue_item.from_team
            ok = None
            tries = 0
            while ok not in ["yes", "no"] and tries < 3:
                ok = input(
                    f"Your message is: {received_message}. Would you like to reply? Type yes or no."
                )
                if ok not in ["yes", "no"]:
                    print("You need to type either true or false.")
                tries += 1

            if ok == "yes":
                response_message = input("Enter your response.")
                response = Message(response_message, from_team)
                # {"response": response_message, "from_team": self}
                self.send_message_to_team(from_team, response_message)
            elif ok == "no":
                print("End of conversation.")
            else:
                print("You didn`t input the correct values too many times.")

    def network_initiate_conversation(self, team_name, message):
        """
        In this method we actually need to construct a message object
        that we will push to the receiving team's message queue
        Moreover, we would want the message to be a string
        """
        assert isinstance(message, str)
        assert isinstance(team_name, str)
        self._db_con.initiate_conversation(self.name, team_name, message)
        print("Message sent.")

    def network_reply_to_next_message_in_conversation(self, conversation_id):
        message_result = self._db_con.get_next_message_in_conversation(
            team=self.name, conversation_id=conversation_id
        )
        print(message_result)
        if message_result:
            print(
                f"Your message in conversation {message_result['conversation_id']} with team {message_result['from_team']} is: "
            )
            pprint(message_result)
            reply_message = input("What would you like to reply?")
            terminate = input(
                "Would you like to terminated the conversation after this reply? Type 1 for Yes or 0 for No "
            )
            assert terminate in ("0", "1")
            terminate = bool(int(terminate))
            self._db_con.reply_to_message(
                previous_message=message_result,
                reply_message=reply_message,
            )

            if terminate:
                self._db_con.terminate_conversation(conversation_id)
        else:
            print(f"There are no messages in conversation {conversation_id}")
    
    def network_get_all_unreplied_conversations(self):
        conversations = self._db_con.get_all_unreplied_conversations(self._name)
        return conversations

    def network_get_all_team_names(self):
        teams = self._db_con.get_all_teams()
        pprint(teams)
        return teams


def main():
    course1 = Course("Data Engineering MSc")
    print(course1, course1.get_name())
    course1.set_name("Software Engineering BSc")
    print(course1, course1.get_name())

    module1 = Module("software engineering")
    print(module1.get_name())
    module1.set_name("software engineering module")
    print(module1.get_name())

    print(course1.get_modules())
    module1.add_module_to_course(course1)
    module1.get_courses_of_module()
    print(course1.get_modules())
    print(module1.get_courses_of_module())

    software_engineering = Module("software_engineering")
    print(software_engineering.get_name())
    print(Module.get_all_modules())

    david = Teacher("David", None, "Alderton")
    teo = TeachingAssistant("Teo", None, "Popescu")
    louis = TeachingAssistant("Louis", "Bernard", "Alecu")
    print(david.get_full_name())
    data_engineering = david.create_module("data_engineering")
    print(Module.get_all_modules())

    david.add_ta_to_module(software_engineering, louis)
    david.add_ta_to_module(data_engineering, teo)
    for ta in data_engineering.get_tas():
        print(f"{ta.get_full_name()} is part of course {data_engineering.get_name()}")
    for ta in software_engineering.get_tas():
        print(
            f"{ta.get_full_name()} is part of course {software_engineering.get_name()}"
        )

    student1 = Student(
        "studentid1", "studentFirstName1", "studentMiddleName1", "studentLastName1"
    )
    student2 = Student(
        "studentid2", "studentFirstName2", "studentMiddleName2", "studentLastName2"
    )
    student3 = Student(
        "studentid3", "studentFirstName3", "studentMiddleName3", "studentLastName3"
    )
    student4 = Student(
        "studentid4", "studentFirstName4", "studentMiddleName4", "studentLastName4"
    )
    student5 = Student(
        "studentid5", "studentFirstName5", "studentMiddleName5", "studentLastName5"
    )
    student6 = Student(
        "studentid6", "studentFirstName6", "studentMiddleName6", "studentLastName6"
    )
    student7 = Student(
        "studentid7", "studentFirstName7", "studentMiddleName7", "studentLastName7"
    )
    student8 = Student(
        "studentid8", "studentFirstName8", "studentMiddleName8", "studentLastName8"
    )
    student9 = Student(
        "studentid9", "studentFirstName9", "studentMiddleName9", "studentLastName9"
    )

    david.add_student_to_module(software_engineering, student1)
    teo.add_student_to_module(software_engineering, student2)
    louis.add_student_to_module(data_engineering, student3)
    teo.add_student_to_module(data_engineering, student2)

    david.add_student_to_module(software_engineering, student3)
    david.add_student_to_module(software_engineering, student3)
    david.add_student_to_module(software_engineering, student4)
    david.add_student_to_module(software_engineering, student5)
    david.add_student_to_module(data_engineering, student6)
    david.add_student_to_module(data_engineering, student7)
    david.add_student_to_module(data_engineering, student8)
    david.add_student_to_module(data_engineering, student9)

    print(isinstance(student1, Student))
    print(isinstance(student1, UCLPerson))
    print(isinstance(david, Teacher))
    print(isinstance(david, Instructor))
    print(isinstance(david, UCLPerson))
    print(isinstance(david, Course))
    print(isinstance(teo, Student))
    print(isinstance(teo, TeachingAssistant))
    print(isinstance(teo, Instructor))
    print(isinstance(teo, UCLPerson))
    
    team1 = Team("team1", db_con, student1, student2, teo)
    print(
        "Team1 should contain 2 students and a ta. Check out the list: ",
        team1._team_members,
    )
    team1.remove_from_team(teo)
    print(
        "Team1 should contain 2 students and no ta anymore. Check out the list: ",
        team1._team_members,
    )
    team1 = Team("team_a", db_con, student1, student2, student3)
    team2 = Team("team_b", db_con, student4, student5, student6)
    team3 = Team("team_c", db_con, student7, student8, student9)
    print("-----------------")
    print(team1.team_members)
    print(team2.team_members)
    print(team3.team_members)
    team1.send_message_to_team(team2, "Hey, how are you?")
    team2.reply_to_next_message_in_queue()
    team1.reply_to_next_message_in_queue()
    team2.reply_to_next_message_in_queue()
    # team1 = Team("team_a", db_con)
    # team2 = Team("team_b", db_con)
    # team3 = Team("team_c", db_con)
    # team1.network_initiate_conversation(team2.name, "sal")
    # team2.network_reply_to_next_message_in_conversation(20)
    # team1.network_get_all_unreplied_conversations()

    # team2.get_all_conversations()
    # team2.get_all_team_names()
    # team2.network_reply_to_next_message_in_conversation(conversation_id=1)
    # team1.

if __name__ == "__main__":
    main()
