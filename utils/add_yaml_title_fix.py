# this script was used to add a title to the top 
# of the mark down files. 

import os 

def fix_file(filename: str): 
    data = None 
    with open(filename, 'r') as f: 
        data = f.read() 
    
    # get the end of the first line.
    end_of_the_first_line = data.find('\n')
    first_line = data[:end_of_the_first_line]
    new_title = first_line.replace(':', '').replace('>', '').replace('EXERCISE','').strip()
    complete_title_block = f'---\ntitle: "{new_title}"\n---\n\n'

    new_data = complete_title_block + data

    with open(filename, 'w') as f: 
        f.write(new_data)
    
    print(f"[+] successfully updated {filename}")


if __name__ == '__main__': 
    all_md_filenames = os.listdir()
    for single_file in all_md_filenames:
        if not single_file.endswith('.md'):
            continue
        fix_file(single_file)