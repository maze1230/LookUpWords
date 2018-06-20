import lookup as lu
import word
import helper as hl
import os

import csv

OUTPUT_DIRECTORY = './output/'

if __name__ == '__main__':
    hl.synonym_api_init()
    print("Look up meanings of the words.")
    fn = input("Input the name of the file to save -> ")
    try:
        with open(OUTPUT_DIRECTORY + fn, mode='x', newline='') as csvf:
            csvwriter = csv.writer(csvf, quoting=csv.QUOTE_ALL)
            csvwriter.writerow(
                ["Word", "Meaning", "Synonym", "Sentence_en", "Sentence_ja"])
            print("ok")
    except FileExistsError:
        pass

    with open(OUTPUT_DIRECTORY + fn, mode='a', newline='') as csvf:
        csvwriter = csv.writer(csvf, quoting=csv.QUOTE_ALL)
        name = input("Input a word(-1 to end) -> ")

        while name != "-1":
            w = word.Word(name)
            try:
                try:
                    w.mean = hl.choose_from_list(
                        lu.meaning(name) + lu.meaning_fast(name))

                except LookupError:
                    w.mean = hl.choose_from_list(lu.meaning_fast(name))
                    print(w.mean)

                finally:
                    os.system('clear')
                    w.synonym = hl.choose_from_list(lu.synonym(name), 15)
                    # w.synonym = list(map(hl.first, w.synonym))
                    os.system('clear')
                    w.sentence_en, w.sentence_ja = hl.choose_from_list(
                        lu.sentence(name, 150))[0]
                    csvwriter.writerow(w.to_csv())
                    os.system('clear')

            except LookupError:
                print("There isn't this word.")
                pass
            name = input("Input a word(-1 to end) -> ")
