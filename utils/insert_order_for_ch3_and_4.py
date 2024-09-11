# this script was used to add an order to the top 
# of the mark down files. 
# 
# You can read more about `order` in quarto here: 
# https://quarto.org/docs/websites/website-navigation.html#:~:text=Order%20is%20alphabetical%20(by%20filename)%20unless%20a%20numeric%20order%20field%20is%20provided%20in%20document%20metadata

import os 

def fix_file(filename: str): 
    data = None 
    with open(filename, 'r') as f: 
        data = f.read() 
    
    # if the filename is `2.3.md` for example
    # the following variable will hold the number
    # 3.
    the_order_of_the_file = filename.strip().split('.')[1]
    
    # get the end of the first line.
    end_of_the_first_line = data.find('\n')
    new_header = f"---\norder: {the_order_of_the_file}"
    new_data = new_header + data[end_of_the_first_line:]

    with open(filename, 'w') as f: 
        f.write(new_data)
    
    print(f"[+] successfully updated {filename}")


if __name__ == '__main__': 
    all_md_filenames = os.listdir()
    for single_file in all_md_filenames:
        if not single_file.endswith('.md'):
            continue
        fix_file(single_file)