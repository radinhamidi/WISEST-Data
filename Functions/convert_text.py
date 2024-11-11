import fitz
from unidecode import unidecode
import re

# function that check the proportion of characters in two strings that are the same
def check_similarity(str1, str2):
    n = min(len(str1), len(str2))
    count = 0
    for i in range(n):
        if str1[i] == str2[i]:
            count += 1
    return count/len(str1)

def combine_short_line(lst):
    i = 0
    new_lst = []
    while i < len(lst):
        if i != len(lst) - 1 and len(lst[i + 1]) + len(lst[i]) < 2000:
            new_line = lst[i] + lst[i+1]
            new_lst.append(new_line)       
            i += 2
        else:
            new_lst.append(lst[i])
            i += 1
    return new_lst

def convert_to_text(paper_ID, pdf_path):
    doc = fitz.open(pdf_path)

    plain_text = ""
    output = []
    for page in doc:
        output += page.get_text("blocks")

    #previous_block_id = 0 # Set a variable to mark the block id
    for block in output:
        if block[6] == 0: # We only take the text
            #if previous_block_id != block[5]: # Compare the block number
            plain_text = plain_text + unidecode(block[4]) + '\n'

    lst = plain_text.split('\n\n')


    text = ''
    for line in lst:
        # remove '\n' in the line
        stripped_line = line.replace('\n', '')

        # if the proportion of number in the line is greater than 30%, then print it
        if len(stripped_line) != 0 and sum(c.isdigit() for c in stripped_line)/len(stripped_line) > 0.3:

            stripped_line = ''
            
        # if the line begins with Fig then print it
        if len(stripped_line) != 0 and stripped_line[0:3] == 'Fig':

            stripped_line = ''
            
        # if the line begins with Table then print it
        if len(stripped_line) != 0 and stripped_line[0:5] == 'Table':
            stripped_line = ''
            
        text += stripped_line + '\n\n'
    
    lst = text.split('\n\n')

    # remove all the '' in the lst 
    lst = list(filter(None, lst))

    
    dup_lst = []
    i = 0
    while i < len(lst):
        j = i + 1

        while j < len(lst):
            if check_similarity(lst[i], lst[j]) >= 0.9:
                if lst[i] not in dup_lst:
                    dup_lst.append(lst[i])
                if lst[j] not in dup_lst:
                    dup_lst.append(lst[j])
                break
            else:
                j += 1
        i += 1

    # remove all items in dup_lst from lst
    for item in dup_lst:
        lst.remove(item)

    # for each item of the list, remove all the websites and email addresses in it
    for i in range(len(lst)):
        lst[i] = re.sub(r'\S*@\S*\s?', '', lst[i]) # remove email addresses
        lst[i] = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', lst[i]) # remove websites

    lst = combine_short_line(lst)
    lst = combine_short_line(lst)
    lst = combine_short_line(lst)
    lst = combine_short_line(lst)
    lst = combine_short_line(lst)
    lst = combine_short_line(lst)
    lst = combine_short_line(lst)

    # remove all items in the lst starting with [
    new_lst = []
    for item in lst:
        if item[0] != '[':
            new_lst.append(item)
    lst = new_lst

    text = ''
    for line in lst:
        text += line + '\n'

    txt_file_path = '../Data/text/' + str(paper_ID) + '_text' + '.txt'
    # save text as txt file
    with open(txt_file_path, 'w') as f:
        f.write(text)
    
    return text