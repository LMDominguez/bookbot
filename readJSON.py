import json, os

source_proj = "ForteData" 

json_data = []
test_list = ["this", "is", "a", "test","List"]

with open(f"{source_proj}.4wF", "r") as f:
    json_data = f.read()
    print(json_data)

python_data = json.loads(json_data)

###------------------------------------------TESTS-----------------------------------------###

#print all data as list
#print(python_data)

#print a whole dictionary in the list
#print(python_data[3])

#print the particular item in a given dictionary
#print(python_data[3]["MemberIDTag"])

#Dig deep...
#get name for a particular member
print(python_data[0]["MemberManagerData"]["MemberContainers"][0]["Members"][0]["MemberName"])

#get name for all members

###--------------------STSRT OF FUNCTIONS-----------------------------###
def get_member_ids(data):
    containers = data[0]["MemberManagerData"]["MemberContainers"]
    members = []
    for container in containers:
        loop_members = container["Members"] #this is a list
        for member in loop_members:
            members.append(member["MemberID"])
    return(members)

def get_member_names(data):
    containers = data[0]["MemberManagerData"]["MemberContainers"]
    members = []
    for container in containers:
        loop_members = container["Members"] #this is a list
        for member in loop_members:
            members.append(member["MemberName"])
    return(members)

def get_member_notes(data):
    containers = data[0]["MemberManagerData"]["MemberContainers"]
    members = []
    for container in containers:
        loop_members = container["Members"] #this is a list
        for member in loop_members:
            members.append(member["Notes"])
    return(members)

def get_member_ProductLabel(data):
    containers = data[0]["MemberManagerData"]["MemberContainers"]
    members = []
    for container in containers:
        loop_members = container["Members"] #this is a list
        for member in loop_members:
            members.append(member["ProductLabel"])
    return(members)

def get_member_type(data):
    type_list = []
    for i in range(1,len(data)):
        if data[i]["SpansData"] == None:
            type_list.append("Column")
        else:
            type_list.append("Beam")
    return(type_list)

def get_lengths_list(data, types):
    lengths_list = []
    end_range = len(types)
    for i in range(1,end_range+1):
        if types[i-1] == "Beam":
            span_lengths = []
            span_dicts = [data[i]["SpansData"]["Spans"]]
            for j in range(len(span_dicts[0])):
                SpanLength = round(span_dicts[0][j]["SpanLength"]/12,2)
                span_lengths.append(SpanLength)
            lengths_list.append(span_lengths)
        if types[i-1] == "Column":
            height_data = data[i]["HeightAndSupportsData"]
            wall_height = height_data["WallHeight"]
            top_pate_height = height_data["TopPlateSize"]
            btm_plate_height = height_data["BottomPlateSize"]
            member_height = round((wall_height - top_pate_height - btm_plate_height)/12,2)
            lengths_list.append([member_height])
    #clean the list
    for i in range(len(lengths_list)):
        if len(lengths_list[i]) == 1:
            lengths_list[i] = lengths_list[i][0]
    return(lengths_list)
    
def get_span(lengths_list, span):
    print(f"Getting Span DATA..................for lengths list \n {lengths_list}")
    print(f"span = {span}")
    span_list = []
    for length in lengths_list: #this list contains ints, floats, and lists
        if not isinstance(length, list) and span == 1:
            span_list.append(length)
        elif isinstance(length, list) and span <= len(length):
            span_list.append(length[span-1])
        else:
            span_list.append('N/A')
    return(span_list)

###--------------------END OF FUNCTIONS-----------------------------###


#may need to create own id
new_IDs = []
all_IDs = get_member_ids(python_data)
all_names = get_member_names(python_data)
all_notes = get_member_notes(python_data)
all_labels = get_member_ProductLabel(python_data)
member_type_list = get_member_type(python_data)
lengths_list = get_lengths_list(python_data, member_type_list)
for i in range(len(all_IDs)):
    new_IDs.append(i+1)

#this dictionary only works for 4 or less spans. may need to code a loop for more spans and cleaner code


span_1 = get_span(lengths_list,1) #takes a list of lengths and a span
span_2 = get_span(lengths_list,2)
span_3 = get_span(lengths_list,3)
span_4 = get_span(lengths_list,4)

span_dict = {
    1: span_1,
    2: span_2,
    3: span_3,
    4: span_4
}

print("TESTING JSON READER..........................")
print(span_dict)
print(len(span_dict[4]))




