import csv


with open('some.csv', 'w') as f:
    reader = csv.reader(f)
    writer = csv.writer(f)
    writer.writerows([["this is another text"]])
    # for row in reader:
        # print row