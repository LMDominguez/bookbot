#This section takes a PDF and converts its content to text
import PyPDF2, os   #pip install PyPDF2
import json
import readJSON


pdf_name = "calcPackage.pdf"
output_txt = "PDF_extracted_text.txt"
read_pdf = PyPDF2.PdfFileReader(pdf_name)
number_of_pages = read_pdf.getNumPages()

### ------------------CLASSES-----------------------------###
class Member:
    def __init__(self, id, name, shape,notes,Sp1,Sp2,Sp3,Sp4):
        self.ID = id
        self.Name = name
        self.Shape = shape
        self.Notes = notes
        self.L1_ft = Sp1
        self.L2_ft = Sp2
        self.L3_ft = Sp3
        self.L4_ft = Sp4

class Load:
    pass
    def __init__(self, member, type, unit, start_mag, end_mag, start_pos, end_pos, ):
        self.member = member
        self.type = type
        self.type = dur_factor

class UDL(Load):
    pass
    def __init__ (self, member_id, type, dur_factor, start_loc, end_loc):
        super.__init__(member_id)

###----------------WRITE PDF TO TEXT FUNCTION - ACTIVATE FOR WHEN NEW PDF TO TXT NEEDED-------------------------------------###

def write_file():
    if os.path.exists(output_txt):
        os.remove(output_txt)
    with open(pdf_name, "rb") as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        for i in range (0, number_of_pages):
            page = read_pdf.pages[i]
            page_content = page.extractText()
            with open(output_txt, "a") as f:
                #f.write(f"PG_{i+1}_START\n")
                f.write(page_content)
                #f.write(f"\nPG_{i+1}_END\n")
                f.write(f"\n")
                if i+1 == number_of_pages:
                    f.write(f"\nEND_OF_DOCUMENT\n")
write_file()

###---------------------------------------PDF REFORMATTING FUNCTIONS------------------------------------------###

def output_as_list():
    with open(output_txt, "r") as f:
        output_list = f.readlines() #creates list of each line as string
        return output_list


def get_page_ends():
    whole_list = output_as_list()
    page_ends_list = []
    curr_pg_number = 1
    for i in range(len(whole_list)):           
        if whole_list[i] == f"PG_{curr_pg_number}_END\n":
            #print(f"reading page {curr_pg_number}")
            page_ends_list.append(i+1)
            print(whole_list[i])
            print(i+1)
            curr_pg_number += 1
                #print(f"Page {curr_pg_number} ends on line {i} adding index {i} to list of page ends")
    #print(page_ends_list)
    return(page_ends_list)

def get_new_member_line(whole_list):
    new_member_line = []
    for i in range(len(whole_list)):
        if whole_list[i] == "Design Results\n":
            new_member_line.append(i+1)
    return(new_member_line)

def get_num_of_members(whole_list):
    new_member_line = get_new_member_line(whole_list)
    length = len(new_member_line)
    return (length)

def create_member_lists(whole_list, member_starts): #function creates list for each member (NOT PAGE)
    list_of_lists = []
    new_list = []
    j_end = len(member_starts)
    for j in range(j_end):
        start_range = member_starts[j]-1
        if j != j_end-1:
            end_range = member_starts[j+1]-1
        else:
            end_range = len(whole_list)
        for i in range(start_range,end_range):
            new_list.append(whole_list[i])

        list_of_lists.append(new_list)
        new_list = []
    return (list_of_lists)

def get_indiv_member_lists(mem, member_list):
    for item in member_list[mem]:
        print (item)
    return member_list[mem]

    
### ---------------------------PDF PARSE FUNCTIONS----------------###
def get_name(lst): #NOT USED, SEE JSON INSTEAD
    name = ""
    for i in range(len(lst)):
        if lst[i] == "PASSED\n" or lst[i] == "FAILED\n":
            name = lst[i+1]
    return(name)

def get_shape(lst): #NOT USED, SEE JSON INSTEAD
    shape = ""
    for i in range(len(lst)):
        if lst[i] == "PASSED\n" or lst[i] == "FAILED\n":
            shape = lst[i+2]
            #print(f"the get_shape() function collected the shape: {shape}")
    return(shape)

def get_notes(lst): #NOT USED, SEE JSON INSTEAD
    notes = ""
    for i in range(len(lst)):
        if lst[i] == "Member Notes\n":
            notes = lst[i+1]
            #print(f"the get_notes() function collected the notes: {notes}")
    return(notes)

def get_length(lst): #NOT USED, SEE JSON INSTEAD
    length = ""
    for i in range(len(lst)):
        if lst[i] == "PASSED\n" or lst[i] == "FAILED\n":
            check_item1 = lst[i-2]
            check_item2 = lst[0]
            if check_item1[0:13] == "Member Length":
                length = lst[i-2][16:-2]
            elif check_item2[0:13] == "Member Height":
                length = lst[2][16:-2]
            else:
                length = "Length N/A"
    return(length)

def get_reaction_1(lst):
#FOR BEAMS
#First find "Loads to Supports" as starting point
#Look for load types. Invariably will begin 5 positions after "Loads to supports"
#get position of "Accessories"
#for i in range pos(Accessories + 1) to pos(Factored): create dictionary for each load type present with empty value where key = index[i]
#Get number of supports. Look for startswith "# - " until parse reaches "Lateral Bracing"
#Pass three bearing length strings. 
#For i in len(num_supports): add the next integers to list
    r1 = ""
    for i in range(len(lst)):
        if lst[i] == "Loads to Supports (lbs)\n" or lst[i] == "FAILED\n":
            shape = lst[i+2]
    return(shape)    
### ------------------------------ END PDF PARSE FY+UNCTIONS----------------###


def create_member_objects(total_members, all_names, all_notes, all_labels, span_dict):
    members = []
    for i in range(total_members):
        id = f"M{i+1}"
        name = all_names[i]
        shape = all_labels[i]
        notes = all_notes[i]
        Sp1 = span_dict[1][i]
        Sp2 = span_dict[2][i]
        Sp3 = span_dict[3][i]
        Sp4 = span_dict[4][i]
        members.append(Member(id ,name, shape, notes,Sp1,Sp2,Sp3,Sp4))
    return(members)



###---------------------------------------------VARIABLES--------------------------------------------###
#PDF VARIABLES
whole_list = output_as_list()
number_of_members = len(readJSON.all_IDs)
member_id = 1
member_starts = get_new_member_line(whole_list) # FOR PDF DATA
member_list = create_member_lists(whole_list,member_starts) #FOR PDF DATA

#import JSON variables
new_IDs = readJSON.new_IDs
all_IDs = readJSON.all_IDs
all_names = readJSON.all_names
all_notes = readJSON.all_notes
all_labels = readJSON.all_labels
member_type_list = readJSON.member_type_list
lengths_list = readJSON.lengths_list
span_dict = readJSON.span_dict

member_objects = create_member_objects(number_of_members, all_names, all_notes, all_labels, span_dict)

###-----------------------------------WRITE TO EXCEL---------------------------------###
import xlwt
from xlwt import Workbook #requires pip install xwlt

list_of_dicts = []
for member in member_objects:
    list_of_dicts.append(member.__dict__)

#syntax: wb.write(row, column, "data") where column A = 0 and row 1 = 0

#create workbook
wb = Workbook()
sheet1 = wb.add_sheet('ForteData')

dict_keys = list(list_of_dicts[0].keys())
print(dict_keys)

#write keys to sheet columns
for i in range(len(dict_keys)):
    sheet1.write(0, i, dict_keys[i])

#write keys to sheet rows
for i in range(len(list_of_dicts)):
    #parsing through dictionaries
    dict_values = list(list_of_dicts[i].values())
    for j in range(len(dict_values)):
        sheet1.write(i+1, j, dict_values[j])




#Write Header



wb.save('ForteData.xls')








###-----------------------------------ATTEMPT PANDAS DATA FRAME---------------------------------###
#this block of code is incomplete
'''
def create_data_frame(member_objects):
    with pd.ExcelWriter("exportXL.xlsx", mode="w") as writer:
        for member in member_objects:
            data_dict = member.__dict__
            data_items = data_dict.items()
            data_list = list(data_items)
            df = pd.DataFrame(data_list)
            print(df)
            df.to_excel(writer, sheet_name='ForteOutput')
'''
###----------------------------------OBJECT DICTIONARY TO JSON---------------------------------###

"""def create_json(member_objects):
    list = []
    for object in member_objects:
        list.append(object.__dict__)
    
    final = json.dumps(list, indent=2)
    output_file_name = "output.json"
    with open(output_file_name, "w") as final:
        json.dump(list, final)

    return(f"Json file '{output_file_name}' has been created")"""

###---------------------------------------------TESTS--------------------------------------------###

