import sys


def read_py(file_path):
    
    fpr = open(file_path, 'r')
    text_data = fpr.read()
    fpr.close()

    return text_data


def write_py(file_path, processed_text):

    fpw = open(file_path, 'w')
    fpw.write(processed_text)
    fpw.close()


def process_py(file_path):

    text_data = read_py(file_path)
    
    processed_text = insert_line_num(text_data)
    
    write_py(file_path, processed_text)


def get_indentations(str_0):
    
    space_num = len(str_0) - len(str_0.lstrip())
    spaces = str()
    
    for _ in range(space_num):
        spaces += ' '

    return spaces
    
    
def insert_line_num(text_data):

    text_list_splited = text_data.split('\n')
    
    # Initiate
    order = 1
    delta = 0

    while (order + delta) <= len(text_list_splited):

        if text_list_splited[order+delta-1] == '':
            order += 1
            continue
        
        spaces = get_indentations(text_list_splited[order+delta-1])
        
        text_list_splited.insert(order+delta, '\n')
        text_list_splited.insert(order+delta+1, spaces + ('print(%d)' % order))
        text_list_splited.insert(order+delta+2, '\n')
        
        delta += 3
        order += 1

    processed_text = str()
    for elem in text_list_splited:
        processed_text += elem

    return processed_text


if __name__ == '__main__':

    process_py(sys.argv[1])
