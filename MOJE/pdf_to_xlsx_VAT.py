from tika import parser # pip install tika
import csv

def Tika():

    table1 = []
    raw = parser.from_file('09.02 VAT.pdf')
    test1 = (raw["content"])
    test1 = test1.split('\n')
    c = 'Brak'
    for i, (cur, nxt) in enumerate(zip(test1, test1[1:])):

        if 'INV/' in cur:
            c = cur.split('INV/')[1] + nxt
        if ' PLN' in cur:
            d = cur.split(' PLN')[0]

            object = {
                'Invoice': c,
                'Payment': d,
            }
            table1.append(object)
    return table1
test = Tika()
print(test)

with open('Magda_VAT.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(test[0].keys())
    for row in test:
        # print(row)
        writer.writerow(row.values())
f.close()
 
