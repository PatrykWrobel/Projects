from tika import parser
import csv

def Tika():
    table = []
    table1 = []
    raw = parser.from_file('10.02 EUR.pdf')
    test1 = (raw["content"])
    test1 = test1.split('\n')
    # print(test1)
    c = 'Brak parametru'
    for row in test1:
        if ' REF.' in row:
            c = row.split('REF. ')[1].split('/')[0]
            # table.append(c)w
        elif ' EUR' in row:
            d = row.split(' EUR')[0]
            object = {
                    'Invoice': c,
                    'Payment': d,
                }
            table1.append(object)
    return table1
final = Tika()
# print(final)

with open('Magda_EUR.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(final[0].keys())
    for row in final:
        print(row)
        writer.writerow(row.values()) 
f.close()

