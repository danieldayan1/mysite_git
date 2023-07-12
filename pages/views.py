from django.shortcuts import redirect, render, get_object_or_404  , HttpResponse
from django.urls import reverse  
from django.views.decorators.clickjacking import xframe_options_exempt,xframe_options_deny
from django.views.generic import ListView
import pickle,os,random , csv , statistics
import re , functools , random , copy 
from abc import abstractmethod , ABCMeta

from .models import User , Projects
from .forms import *
from .templates import *
from .static import *



def Home(request):
    context = {'message':'WELCOME TO DANIEL DAYAN SITE !!'}
    if request.method=='GET':
        myName = request.GET.get('myName')
        password = request.GET.get('password')
        try:
            user = get_object_or_404(User,name=myName,password=password)
            context = {'message':f'HI {user.name} !! WELCOME TO DANIEL DAYAN SITE !!'}
        except:
            context = {'message':'WELCOME TO DANIEL DAYAN SITE !!'}
    return render(request,'Home.html',context)

@xframe_options_exempt
def form(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        form.age = request.POST['age']     
        if form.is_valid():
            form.save()
            return render(request,'add_user.html',{})
        else:
            context = {'form':form , 'errors':form.errors}
            return render(request,'form.html',context)
    else:
        return render(request,'form.html',{'form':form})

@xframe_options_exempt
def CV(request):
    return render(request,'CV.html',{})

@xframe_options_exempt
def contact(request):
    return render(request,'contact.html',{})

@xframe_options_exempt
def carusel(request):
    return  render(request,'carusel.html',{})

@xframe_options_deny
def view_one(request):
    return HttpResponse("<h1>Can't display in this version!</h1>")

@xframe_options_exempt
def  advanced(request,id):
    if id==1:
        return render(request,'projects/advanced.html',{})
    else:
        request.session['work'] = id
        url = projects_python(request)
        return redirect("../"+url)

class ListProjects(ListView):
    model = Projects
    context_object_name = 'projects'


def projects_python(request):

    match request.session['work']:
        case 2:
            return 'projects/project_calculator'
        case 3:
            return 'projects/project_pyramid'
        case 4:
            return 'projects/project_tests'
        case 5:
            return 'projects/project_myLibrary'
        case 6:
            return 'projects/project_react_products'
        case 7: 
            return 'projects/project_react_python_products'
        case 8:
            return 'projects/sudoku'
        case 9:
            return 'projects/flights'
        case 10:
            return 'projects/pictures'
        case _:
            return redirect('../Home')
        
    return render(request,'projects/projects-python.html',context)

def project_books(request):
    result="<p><h1>-----BOOKS-----</h1><br>"
    try:
        if request.method == 'POST':
            try:
                path = str(request.POST["file"])
                file = open(path)
            except IOError:
            #default file
                path = os.path.join(os.path.dirname(__file__),r'static\python\books.txt')
                result = f"File not found . Choose from default file : {path} . <br> " 
                file = open(path)
            name = " "
            year = 0
            money = 0
            pay_on_time = False
            dic = {}
            line = file.readline()
            while(len(line)>0):
                list1 = line.split(" ")
                name = list1[0]
                year = list1[1]
                money = list1[2]
                pay_on_time = True if list1[3]==list1[1] else False
                dic[name] = [year,money,pay_on_time]
                line = file.readline()
            for key in dic:
                if dic[key][2]== True and int(dic[key][1])>=8000:
                    result += " customer {0}  is: VIP <br>".format(key)
                else:
                    result += " cutomer {0}  is: REGULAR".format(key)
            file.close()
        else:
            return render(request,"projects/project_books.html",{})
    except:
        result = "Something wrong with the file  . Please try again !"
        return render(request,"projects/project_books.html",{'result':result})
    finally:
        result += '</p>'
        # return render(request,"projects/project_books.html",{'result':result})
    return HttpResponse(result)

def project_calculator(request): 

    def calc_reg(*args):
        result = 0
        if args[2]==r'+':
            result = args[0] + args[1]
        elif args[2]==r'-':
            result = args[1]-args[0] if args[0]<args[1] else args[0]-args[1]
        elif args[2]==r'*':
            result = args[0]*args[1]
        elif args[2] == '\\':
            result = args[1]/args[0] if args[0]<args[1] else args[0]/args[1]
        elif args[2]==r'^':
            result = pow(args[0],args[1])
        return result


    content="<p><h1>-----CALCULATOR-----</h1><br>"
    try:
        if request.method == 'POST':
            num1 = int(request.POST['num1'])
            operator = str(request.POST['operator'])
            num2 = int(request.POST['num2'])
            content += "The result  {0} {1} {2} = {3}".format(num1,operator,num2,calc_reg(num1,num2,operator))
        else:
            return render(request,'projects/project_calculator.html',{})
    except:
        content += '<p>Wrong input . Please try again .</p>'
    return HttpResponse(content)

def project_pyramid(request):
    
    if request.method == 'POST':
        num = int(request.POST['num'])
        if num>0:
            s=''
            for row in range(num):
                #spaces
                for j in range(num-row-1):
                    s += " "
                #stars
                for k in range(row*2+1):
                    s += '*'
                s += '<br>'
            return HttpResponse(s)
        else:
            s = 'Wrong input . Please try again !'
            return render(request,'projects/project_pyramid.html',{'result':s})
   
    return render(request,'projects/project_pyramid.html',{})
  
def project_orders(request):
   
    content = '<h1>------ORDERS------<h1><br>'

    def getCustomerID(name):
        cust_id = " "
        path = str(request.POST['custFile'])
        try:
            cust_file = open(path)
        except IOError:
            #default file
            path = os.path.join(os.path.dirname(__file__),r'static\python\Cust.csv')
            content = f"File not found . Choose from default file : {path} . <br> "
            cust_file = open(path)
        
        line = cust_file.readline()
        while len(line)>0 :
            l = line.split(",")
            if l[1]==name:
                cust_id = l[0]
                break
            line = cust_file.readline()
        cust_file.close()

        return cust_id

    def getOrders(cust_id):
        orders = []
        path = request.POST['ordersFile']
        try:
            orders_file = open(path)
        except IOError:
            #default file
            path = os.path.join(os.path.dirname(__file__),r'static\python\Orders.csv')
            content = f"File not found . Choose from default file : {path} . <br> "
            orders_file = open(path)

        line = orders_file.readline()
        while len(line)>0 :
            l = line.split(",")
            if l[1]==cust_id:
                orders.append(l[3])
            line = orders_file.readline()
        orders_file.close()

        return orders

    def output_sum(list1):
        result=0
        list2 = list(map(int,list1))
        for i in range(0,len(list2)) :
            result = result + list2[i]
        return "Total orders: {0}$".format(result) +'<br>'


    if request.method == 'POST':
        name = str(request.POST['name'])
        if len(name) >0 :
            cust_id= getCustomerID(name)
            if len(cust_id) >0:
                orders_list = getOrders(cust_id)
                if len(orders_list) >0 :
                    content += output_sum(orders_list)
                    return HttpResponse(content)
                else:
                    content = "No orders found ! TRY AGAIN !"  
            else:
                content = "WRONG NAME ! TRY AGAIN !"   
    else:
        return render(request,'projects/project_orders.html',{})

    return render(request,'projects/project_orders.html',{'result':content})
    
def project_phone_book(request):

    result = '<h1>-------PHONE BOOK--------</h1><br>'
    phone_book = {}
    if request.method == 'POST':
        path = str(request.POST["file"])
        try:
            file = open(path)
        except IOError:
            #default file
            path = os.path.join(os.path.dirname(__file__),r'static\python\phones.csv')
            result += f"File not found . Choose from default file : {path} . <br> " 
            file = open(path)
            
        line = file.readline()
        while(len(line)>0):
            list1 = line.split(",")
            if list1[0]=='phone':
                phone_book[list1[1]]=list1[2]
            elif list1[0]=='request':
                if list1[1] in phone_book.keys():
                    result += "The request number of {0} is {1} . <br>".format(list1[1],phone_book[list1[1]])
                else:
                    result += "unknown number ! . <br>"
            elif list1[0]=='del':
                if list1[1] in phone_book.keys():
                    del phone_book[list1[1]]
                    result += "number deleted ! . <br>"
                else:
                    result += "unknown number ! . <br>"
            else :
                break
            line = file.readline()
        return HttpResponse(result)

    return render(request,'projects/project_phone_book_.html',{})
        
def project_tests(request):
    global questions 
    questions = []
    global result
    result = []
    result.append('-------TEST--------')
    result.append("Create Test : ")
    global final_result
    final_result = []

    '''
    CLASS TEST CREATE TEST WITH QUESTIONS AND ANSWERS AND CALCULATE THE STUDENT'S GRADE
    '''
    class Test:
        #CONSTRACTOR
        def __init__(self):
            global result
            p = request.POST['test']
            if not(os.path.exists(p)):
                p = os.path.join(os.path.dirname(__file__),r'static\python\test.txt')
                result.append(f"File not found . Choose from default file : {p} . ")
            self._path = p
            self.create_test()

        def get_Path(self):
            #RETURN PATH FOR TEST FILE
            return _path
        
        def __eq__(self,test2):
            #CHACK WHENEVER 2 TESTS HAVE SIMILAR QUESTION AND ANSWER
            file_test_self = open(self._path,"rb")
            dic_test_self = pickle.load(file_test)
            file_test_test2 = open(test2.getPath(),"rb")
            dic_test_test2 = pickle.load(file_test)
            count=0
            for i in dic_test.keys():
                if (dic_test_self[i][0]==dic_test_test2[i][0]) and (dic_test_self[i][1]==dic_test_test2[i][1]):
                    return True
            return False

        def __str__(self):
            #RETURN FOR PRINT PATH FOR TEST FILE
            return self._path
            
        
        def create_test(self):
            #CREATE TEST WITH QUESTIONS AND ANSWERS FOR THE FIRST TIME
            global result
            try:
                dic={}
                f_out_test =  open(self._path,'wb') 
                for i in range(1,11):
                    num1 = random.randint(1,10)
                    num2 = random.randint(1,10)
                    o = random.randint(1,4)
                    if o == 1:
                        operator = r'+'
                        result1 = num1+num2
                    elif o == 2:
                        operator = r'-'
                        result1 = num1-num2
                    elif o == 3:
                        operator = r'*'
                        result1 = num1*num2
                    else:
                        operator = '\\'
                        result1 = num1//num2
                    dic[i] = [f"{num1}{operator}{num2}"+"=",result1]
                pickle.dump(dic,f_out_test)
                f_out_test.close()
                self.print_test()
            except:
                result.append("Error accured . Try again. ")


        def print_test(self):
            #PRINT TEST TO THE SCREEN AND RECEIVE ANSWERS FROM STUDENT
            global result
            try:

                file_test = open(self._path,"rb")
                dic_test = pickle.load(file_test)
                
                for i in dic_test.keys():
                    questions.append(dic_test[i][0]) 
                file_test.close()
                start_calc_grade()
            except:
                result.append("Something wrong with the file . Try again. ")


        def start_calc_grade(self,req):
            #PRINT TEST TO THE SCREEN AND RECEIVE ANSWERS FROM STUDENT
            global result
            s=" "
            grade = 0
            try:
                file_student_answers = open(os.path.join(os.path.dirname(__file__),r'static\python\student_answers.txt'),'w')
                file_test = open(self._path,"rb")
                dic_test = pickle.load(file_test)
                for i in range(0,10):
                    key = f"answer{i}"
                    answer = str(req.POST[key])
                    s = s+","+answer
                file_student_answers.write(s)
                # file_student_answers.write(answer)
                file_test.close()
                file_student_answers.close()
        
            except:
                result.append("Something wrong with the file . Try again. ")
            finally:
                final_result.append("Finish test. ")
                self.calc_grade()

        def calc_grade(self):
            #CLACULATE AND PPRINT STUDENT GRADE
            global result
            grade = 0
            try:
                file_student_answers = open(os.path.join(os.path.dirname(__file__),r'static\python\student_answers.txt'),"r")
                file_test = open(self._path,"rb")
                dic_test = pickle.load(file_test)
                l_student_answers = file_student_answers.read().split(",")
                for i in dic_test.keys():
                    try:
                        if int(l_student_answers[i]) == dic_test[i][1]:
                            grade+=1
                    except:
                        pass
                file_test.close()
                file_student_answers.close()
            except:
                result.append("something wrong with the file . try again. ")
            finally:
                final_result.append("student grade is: {0} ".format(grade))     

    
    global test 
    if request.method == 'GET':
        return render(request,'projects/project_tests.html',{})
    else:
        if request.POST.get("file"):
           test = Test()
           return render(request,'projects/project_tests.html',{'result':result,'questions':questions})
       
        elif request.POST.get("questions"):
           test.start_calc_grade(request)
           return render(request,'projects/project_tests.html',{'final_result':final_result})
        else:
           return render(request,'projects/project_tests.html',{})
        # return HttpResponse(result)
        


def project_diamonds(request):

    global result
    result = "<h1>-----DIAMONDS-----</h1><br>"


    """
    This 2 functions extract the data from the file and transform the data to the right type . 
    Arguments: path to the file . 
    Result : a dictionary with all the lines from the file orgenized as values in the dictionary .
    """
    def extract_data(num_rows=0):
        global result
        path = request.POST['file']
        try:
            csv_file = open(path)
        except IOError:
                #default file
            path = os.path.join(os.path.dirname(__file__),r'static\python\diamonds.csv')
            result += f"File not found . Choose from default file : {path} . <br> "
            csv_file = open(path)
        csv_reader = csv.reader(csv_file)
        rows=[]
        columns=[]
        data = {}

        #file lines
        for row in csv_reader:
            rows.append(row)
        #file columns
        columns = list(zip(*rows))
        #build data
        for column in columns:
            data[column[0]] = column[1:] if num_rows==0  else column[1:num_rows]
        
        prepare_data(data)
        return data 
    def prepare_data(data):
        
        def transform_column_type(data , col):
            try: #try to transform column to float
                return  list(map(float,data[col]))
            except :
                try:#try to transform column to int
                    return  list(map(int,data[col])) 
                except :#try to transform column to str
                    return  list(map(str,data[col])) 

        #transform columns type
        for col in data.keys():
            data[col] = transform_column_type(data,col)
    ###########################################################################################
    """
    This func calculate the max value in a specific column from the file.
    Arguments: 
    1. the dictionary typed in the first 2 funcs .
    2. the column from the file who needs to calculated.
    Result : the max value of the column
    """
    def find_max(data,col):
        try:
            return max(data[col])
        except:
            return 0
    ###########################################################################################
    """
    This func calculate the average value in a specific column from the dictionary.
    Arguments: 
    1. the dictionary typed in the first 2 funcs .
    2. the column from the file who needs to calculated.
    result : the average value of the column
    """
    def find_avg(data,col):
        try:
            return round(sum(data[col])/len(data[col]),2)
        except:
            return 0
    ###########################################################################################
    """
    This func count how many times sepcific value found in a specific column from the file.
    Arguments: 
    1. the dictionary typed in the first 2 funcs .
    2. the column from the file who needs to calculated.
    3. the value to chack in the column .
    result : number of times sepcific value found in the column
    """
    def find_count_val(data,col,val):
        try:
            return data[col].count(val)
        except:
            return 0
    ###########################################################################################
    """
    This func find how many values found in a specific column from the file.
    Arguments: 
    1. the dictionary typed in the first 2 funcs .
    2. the column from the file who needs to calculated.
    result : number of values found in the column
    """
    def find_diff_values(data,col):
        try:
            return len(set(data[col]))
        except:
            return 0
    ###########################################################################################
    """
    This func running on the lines from  the file and chack if the values from col1 are equal to specific value ,
    And then calculate the median value from col2 found in thus lines .  
    Arguments : 
    1. the dictionary typed in the first 2 funcs .
    2. col1 - the column from the file who his values needs to be compare to the value .
    3. col2 - the column from the file who his median needs to be caculated .
    4. val - the value needs to compare to col1 values .
    reult: The median of col2 corect values
    """
    def find_median_by_value(data,col1,col2,val):
        l=[]
        try:
            #build a list from the right col2 values
            for x,y in list(zip(data[col1],data[col2])):
                if x==val:
                    l.append(y) 
        
            mid = statistics.median(l)
            return mid
        except:
            return 0
    ###########################################################################################   
    """
    This func running on the lines from  the file and chack how many differnet values in col1 ,
    And then calculate the average value from col2 for each type in col1 .  
    Arguments : 
    1. the dictionary typed in the first 2 funcs .
    2. col1 - the column from the file who his values needs to be compare to the value .
    3. col2 - the column from the file who his median needs to be caculated .
    reult: The average of col2 corect values for each type in col1 .
    """
    def find_avg_by_values(data,col1,col2):

        s=''
        try:
            #find col1 differnt types
            for x in list(set(data[col1])):
                l=[]
                #build a list from the right col2 values for each col1 type
                for y,z in list(zip(data[col1],data[col2])):
                    if y==x:
                        l.append(z)

                if len(l)>0:
                    avg = sum(l)/len(l)
                    s+=f'The average {col2} for {col1}:{x} is:{round(avg,2)} <br>' 
        except ZeroDivisionError:
            s='no input found . please try again'
        except:
            s = 'general error with the file . please try again.'
        finally:
            return s


    if request.method == 'POST':
        data = extract_data()

        result += f"1.max price: {find_max(data,'price')} <br>"
        result += f"2.average price: {find_avg(data,'price')} <br>"
        result += f"3.number of Ideal diamonds: {find_count_val(data,'cut','Ideal')} <br>"
        result += f"4.number of colors: {find_diff_values(data,'color')} <br>"
        result += "5.The median carat for PREMIUM diamonds is: {0} <br>".format(find_median_by_value(data,'cut','carat','Premium'))
        result += "6.{0} <br>".format(find_avg_by_values(data,'cut','carat'))
        result += "7.{0} <br>".format(find_avg_by_values(data,'color','price'))
        
        return HttpResponse(result)

    return render(request,'projects/project_diamonds.html',{})

def project_REGEX(request):

    global result 
    result = ""
  
    def phone_validate():
        global result   
        phone = str(request.POST['phone'])
        pattern2 = r"^(\d{3}-)(\d{7})$"
        pc = re.compile(pattern2)
        m = pc.match(phone)
        if m:
            result += "ok "+m[1]+" "+m[2]
        else:
            result += "wrong"
        return result
    def mail_validate():
        global result
        mail = str(request.POST['mail'])
        patern = r'^(http|https|ftp)://(.*)(\.com)$'
        m = re.search(patern,mail)
        if m:
            result += "yes"
        else:
            result += "no"
            return result
    def replace_nums_regex():
        global result
        s = "i have 3 books and 4 bags , so give me 5 !"
        nums = ["zero","one","two","three","four","five","six","seven","eight","nine","ten"]
        new_s = re.sub(r"(\d)",lambda m:nums[int(m.group(1))],s)
        result += f"SENTENCE BEFORE REGEX REPLACE: {s} <br>"
        result += f"SENTENCE AFTER REGEX REPLACE: {new_s} <br>"
        return result

    if request.method == 'POST':
        result += phone_validate() + '<br>'
        result += mail_validate() + '<br>'
        result += replace_nums_regex() + '<br>'
        return HttpResponse(result)
    else:
        return render(request,'projects/project_REGEX.html',{})


def project_nested_func(request):

    global result
    result=""


    def printmsg1(msg,style):
        global result
        def print_stars():
            result += "********" +"<br>"

        def print_eq():
            global result
            result += "========" + '<br>'

        if msg=='*':
            return print_stars
        return print_eq
    def call_printmsg1():
        global result
        try:
            msg , style = str(request.POST['msg']) , str(request.POST['sytle'])
        except:
            msg , style = "hello","*"
        my_print_func = printmsg1(msg,style)
        my_print_func()
        result += msg +'<br>'
        my_print_func()
        return result
    
    def printmsg2(msg,style):
        #CLOSER
        def print_style():
            global result
            result += style*4 + '<br>'

        return print_style
    def call_printmsg2():
        global result
        try:
            msg , style = str(request.POST['msg']) , str(request.POST['sytle'])
        except:
            msg , style = "hello","*"
        my_print_func = printmsg2(msg,style)
        my_print_func()
        result += msg+ '<br>'
        my_print_func()
        return result

    def genfilterby(num):
        def inner(t):
            return list(filter(lambda x:x%num==0,t)) 
        return inner
    def call_genfilterby():
        fil=genfilterby(3)
        z=[2,3,4,5,6,7,8] 
        return "return calc func for: {0} is: {1} <br>".format(z,fil(z))

    def wraper_adding_stars(style):
        #DECORATOR
        @functools.wraps(my_adding_stars)
        def inner(s):
            global result
            result += style*6 +'<br>'
            my_adding_stars(s) 
            result+= style*6 + '<br>'
        return inner
    def my_adding_stars(s):
        global result
        result +=  s + '<br>'
    def call_wraper_adding_stars():
        adding_stars = wraper_adding_stars('*')
        adding_stars("hello")
        return result



    if request.method == 'POST':
        result += call_printmsg1() +'<br>'
        result += call_printmsg2() +'<br>'
        result += call_genfilterby() + '<br>'
        result += call_wraper_adding_stars() + '<br>'
        return HttpResponse(result)
    return render(request,'projects/project_nested_func.html',{})


    #     try:
    #         msg , style = input("type your message and style: ").split(" ")
    #     except:
    #         msg , style = "hello","*"
    #     my_print_func = printmsg2(msg,style)
    #     my_print_func()
    #     print(msg)
    #     my_print_func()

def project_generator_copy(request):

    global result
    result="<h1>-----GENERATOR+COPY------</h1><br>"

    def print_random_num(n):
        for i in range(n):
            x = random.randint(0,n)
            yield x 

    generator = print_random_num(20)
    l1 = [x for x in generator] 
    l2 = copy.deepcopy(l1)
    l1.append([1,2,3])
    result += f"l1  - {l1}" + '<br>'
    result += f"l2 - l1 copy - {l2}" +'<br>'
    return HttpResponse(result)


def project_OOP(request):

    global result
    result = ''

    class Rectangle(object):

        __counter = 0

        def __init__(self,w=0,h=0,):
            self.__width = w
            self.__height = h
            Rectangle.__counter+=1

        def SetSize(self,w=0,h=0):
            self.__width = w
            self.__height = h

        def __str__(self):
            return f"Rectangle width is:{self.__width} and height:{self.__height}"

        @staticmethod
        def get_counter():
            return Rectangle.__counter
    class RoundRectangle(Rectangle):
        def __init__(self,w,h,a):
            super().__init__(w,h)
            self.__angle = a
        
        def SetAngle(self,a):
            self.__angle=a

        def __str__(self):
            s = super().__str__()+f" and angle:{self.__angle}"
            return s
    def call_Rectangle():
        global result
        r1 = Rectangle(20,10)
        r2 = Rectangle(15,15)
        r3 = RoundRectangle(10,20,30)
        r1.SetSize(20,20)
        result += str(r1) +'<br>' +str(r2) +'<br>' +str(r3) + '<br>' + str(Rectangle.get_counter()) + '<br>'
        return result

    class MyString():     
        def __init__(self,text):
            self.__text = text
                        
        def __str__(self):
            return self.__text
        
        def __add__(self,string2):
            s = self.__text + "-" + str(string2)
            return MyString(s)

        @property
        def text(self):
            return self.__text

        @text.setter
        def text(self,t):
            self.__text =t 
    class MyStringAbs(metaclass = ABCMeta):     
        def __init__(self,text):
            self.__text = text
        
        @abstractmethod
        def __add__(self,string2):
            pass

        @property
        def text(self):
            return self.__text

        @text.setter
        def text(self,t):
            self.__text =t 
    class MyStringEx(MyStringAbs):     

        def __init__(self,t):
            super().__init__(t)

        def __add__(self, other):   
            string =   MyStringEx(self._MyStringAbs__text+ '*' + other._MyStringAbs__text)
            string = re.sub('-','*',string._MyStringAbs__text)
            return string

        def __str__(self):
            return self._MyStringAbs__text
    def call_MyStrings():
        global result
        s1 = MyString("I") 
        s2 = MyString("Love") 
        s3 = MyString("Python") 
        s4 = s1+s2+s3 

        s5 = MyStringEx(str(s4))
        s6 = MyStringEx('Ex')
        #setter
        s6.text = 'Extra'
        s7 = s5+s6
        
        for s in [s4,s7]:
            result += str(s)+'<br>'
        
        return result

    class zoo(object):

        def __init__(self,n):
            if isinstance(n,str):
                self.name = n
            self.__animals = []

        def add_animal(self,animal):
            if isinstance(animal,str):
                self.__animals.append(animal)

        @property
        def animals(self):
            return self.__animals

        @animals.setter
        def animals(self,a):
            self.__animals = a

        def sell_animal(self,animal_sold):
            if animal_sold in self.__animals:
                self.__animals.remove(animal_sold)

        def sort_animals(self):
            self.__animals.sort(key=lambda a: a[0])            
    def call_zoo():
        z = zoo('rishon zoo')
        z.add_animal("Ape")
        z.add_animal("Cat")
        z.add_animal("Bear")
        z.add_animal("Emu")
        z.sort_animals()

        return z.__dict__


    result += call_Rectangle() +'<br>'
    result += call_MyStrings() +'<br>'
    result += str(call_zoo())
    return HttpResponse(result)



def project_myLibrary(request):
    return HttpResponse('<a href ="https://github.com/danieldayan1/myLibrary1_git">library project </a>')

def project_react_products(request):
    return HttpResponse('<div><a href ="https://github.com/danieldayan1/products_react_GIT">react products project </a></div>')

def project_react_python_products(request):
    return HttpResponse('<div><a href ="https://github.com/danieldayan1/products_react_django_git">react + python products project </a></div>')

def sudoku(request):
    return HttpResponse('<div><a href ="https://github.com/danieldayan1/REACT_-SUDUKO_-GAME_GIT">react sudoku game</a></div>')

def flights(request):
    return HttpResponse('<div><a href ="https://github.com/danieldayan1/flights_react_django_git">react flights site</a></div>')

def pictures(request):
    return HttpResponse('<div><a href ="https://github.com/danieldayan1/express_courses_git">express pictures site</a></div>')