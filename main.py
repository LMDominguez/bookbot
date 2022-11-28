path_to_file = "books/frankenstein.txt"
test_string = "This is a test string"

with open(path_to_file) as f:
    file_contents = f.read()

    def get_num_words(string):
        words_as_list = string.split()
        return(len(words_as_list))
    
    def count_letters(string):
        dict = {}
        lower_case = string.lower()
        for i in range(len(lower_case)):
            char_in_dict = False
            for j in dict:
                if lower_case[i] == j:
                    char_in_dict = True
            if char_in_dict == False:
                dict[lower_case[i]] = 1
            else:
                dict[lower_case[i]] += 1
        return(dict)

    def create_report(int, dict):
        print(f"--- Begin report of {path_to_file} ---")
        print(f"{int} words found in the document \n")
        list_of_dict = []
        for char in dict:
            if char.isalpha() == True:
                new_dict = {}
                new_dict[char] = dict[char]
                list_of_dict.append(new_dict)
        sorted_list = []
        for j in range(len(list_of_dict)):
            max_value = 0
            for i in range(len(list_of_dict)):
                curr_key = list(list_of_dict[i].keys())[0]
                curr_value = list_of_dict[i][curr_key]
                if curr_value >= max_value and list_of_dict[i] not in sorted_list:
                    max_value = curr_value
                    max_key = curr_key
                curr_max_dict = {max_key: max_value} 
            sorted_list.append(curr_max_dict)
        print(sorted_list)
        for i in range(len(sorted_list)):
            curr_key = list(sorted_list[i].keys())[0]
            curr_value = sorted_list[i][curr_key]
            print(f"the '{curr_key}' was found {curr_value} times")
            


        print("--- End report ---")

num_words = get_num_words(file_contents)
letter_count = count_letters(file_contents)
create_report(num_words, letter_count)