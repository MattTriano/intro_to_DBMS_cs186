import csv
import sys
from collections import Counter
from itertools import chain
from string import punctuation

def parse_ebooks(filename):
    tmp_ebooks = open('ebook.csv', 'wb')
    tmp_ebooks.close()
    tmp_tokens = open('tokens.csv', 'wb')
    tmp_tokens.close()
    tmp_ebooks = open('ebook.csv', 'ab')
    tmp_tokens = open('tokens.csv', 'ab')
    in_book = 0
    print("the filename is: " + str(filename))
    for line in open(str(filename)):
        line = line.replace('\r\n', '')
        line = line.replace('|', '')
        try:
            if len(line.replace(' ', '')) == 0:
                continue
            if in_book == 0 and '*** START OF THE' in line:
                ebook_lines = []
                in_book = 1
            elif in_book == 1 and '*** END OF THE' in line:
                ebook_string = '\r\n'.join(ebook_lines)
                in_book = 0
                book_entry = [title, author, release, ebook_number, language, ebook_string]
                if None in book_entry:
                    book_entry = 'null'
                else:
                    ebook_tokens(tmp_tokens, ebook_number, ebook_string)
                title = author = release = ebook_number = language = ebook_string = None
                writer = csv.writer(tmp_ebooks, lineterminator = '\r\n')
                writer.writerow(book_entry)
            elif in_book == 1 :
                ebook_lines.append(line.replace(r'\r\n', ''))
            elif in_book == 0 and 'Title: ' in line:
                title = line.replace('Title: ', '')
            elif in_book == 0 and 'Author: ' in line:
                author = line.replace('Author: ', '')
            elif in_book == 0 and 'Release Date: ' in line:
                rel_date = line.replace('Release Date: ', '')
                if '[EBook' in rel_date:
                    rel_date = rel_date.split(' [EBook')
                elif '[Etext' in rel_date:
                    rel_date = rel_date.split(' [Etext')
                release = rel_date[0]
                tmp = rel_date[1]
                ebook_number = tmp.replace(']', '').replace(' #','')
            elif in_book == 0 and 'Language: ' in line:
                language = line.replace('Language: ', '')
        except IndexError:
            num = ebook_number
            print(num)
    tmp_ebooks.close()
    tmp_tokens.close()

def ebook_tokens(tokens_csv, ebook_number, ebook_string):
    ebook_string = ebook_string.replace(';', ' ').replace('!', ' ').replace('.', ' ').replace(',', ' ')
    ebook_string = ebook_string.replace('?', ' ').replace(':', ' ').replace('(', ' ').replace(')', ' ')
    ebook_string = ebook_string.replace('[', ' ').replace(']', ' ').replace('&', ' ').replace('/', ' ')
    ebook_string = ebook_string.replace('-', ' ').replace('_', ' ').replace('|', ' ').replace('$', ' ')
    all_tokens = ebook_string.lower().split(' ')
    writer = csv.writer(tokens_csv, lineterminator='\r\n')
    for token in all_tokens:
        writer.writerow([ebook_number, token])


# def countInFile(tokens, token_count_dict):
#     tmp_token_dict = {}
#     for token in set(tokens):
#         tmp_token_dict[token] = tokens.count(token)
#     token_count_dict = merge_two_dicts(tmp_token_dict, token_count_dict)
#     # tokens = ebook_string.translate(None, punctuation).lower().split()
#     return token_count_dict
#     # with open(filename) as f:
#     #     linewords = (line.translate(None, punctuation).lower().split() for line in f)


def token_counter(token_csv, token_count_csv):
    tmp_token_counts = open(token_count_csv, 'w')
    tmp_token_counts.close()
    tmp_token_counts = open(token_count_csv, 'a')
    token_counts = {}
    for line in open(token_csv):
        line = line.replace('\r\n', '')
        if len(line.split(',')) >= 2:
            token = line.split(',')[1]
            if token not in token_counts and token != '':
                token_counts[token] = 1
            elif token in token_counts:
                token_counts[token] += 1
    for key in token_counts:
        writer = csv.writer(tmp_token_counts, lineterminator='\r\n')
        row = [key, token_counts[key]]
        writer.writerow(row)
    tmp_token_counts.close()

def name_counts(popular_names, save_name, token_counts):
    try:
        tmp_name_counts = open(save_name, 'wb')
        tmp_name_counts.close()
        tmp_name_counts = open(save_name, 'ab')
        writer = csv.writer(tmp_name_counts, lineterminator='\r\n')
        names = []
        with open(popular_names, 'rb') as g:
            reader_g = csv.reader(g)
            for row in reader_g:
                name = row[0].replace('\r\n', '')
                names.append(name.lower())
        g.close()
#        for name in names:
#            print(name)
        with open(token_counts, 'rU') as f:
            reader_f = csv.reader(f)
            for row in reader_f:   
#                print(str(row))
#            row = row.replace('\n', '')
                # split_row = row.split(',)
                # print(row[0])
                if row:
                    if row[0] in names and len(row) >= 2:
                        writer.writerow([row[0].capitalize(), row[1]])
                    elif row[0] in names and len(row)== 1:
                        writer.writerow([row[0].capitalize(), 0])
        f.close()
    except IndexError:
        print("IndexError, current line is :" + str(row))
        print(str(IndexError))

def main(argv):
    print("argv is: " + str(argv))
    if argv is None:
        argv = sys.argv
    print("the total number of args passed to this script is :" + str(len(argv)))
    parse_ebooks(argv)
    token_counter('tokens.csv', 'token_counts.csv')
    name_counts('popular_names.txt', 'name_counts.csv', 'token_counts.csv')


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))


