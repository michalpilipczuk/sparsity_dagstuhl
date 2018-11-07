import csv, codecs, cStringIO

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def read_file(filename="./invitees-raw.csv"):
  file = open(filename, mode="r")
  r = UnicodeReader(file, delimiter=",", quotechar="\"")
  res = []
  for row in r:
    res.append({
        'firstname': row[0],
        'surname': row[1],
        'affiliation': row[2],
        'country': row[3],
        'email': row[4],
        'junior': row[5],
        'female': row[6],
        'industry': row[7],
        'homepage': row[8], 
        'topic': row[9],
        'round': row[10]})
  file.close()
  return res

def output_csv(r, filename="./invitees.csv"):
  res = []
  for x in r:
    res.append([x['surname'], x['firstname'], x['affiliation'], x['country'], x['email'], x['junior'], x['female'], x['industry'], x['homepage'], x['topic'], x['round']])
  file = open(filename, mode="w")
  w = UnicodeWriter(file, delimiter=",", quotechar="\"")
  for x in res:
    w.writerow(x)
  file.close()

def output_latex(r, filename="./invitees.tex"):
  file = codecs.open(filename, mode="w", encoding="utf-8")
  #file.write("\\subsection*{First round invitees}\n\n")
  second_output= False
  for x in r:
   # if x['round'] == '2' and not second_output:
   #   second_output = True
   #   file.write("\\subsection*{Second round invitees}\n\n")
    tags = []
    if x['female']: 
      tags.append(u'female')
    if x['industry']:
      tags.append(u'industry')
    if x['junior']:
      tags.append(u'junior')
    file.write(u"\\invitee{%s %s}{%s}{%s}{%s}{%s}{%s}{%s}\n\n" % (x['firstname'], x['surname'], x['affiliation'], x['country'], x['email'], x['homepage'], x['topic'], u' '.join(tags)))
  file.close()


r = read_file()
output_csv(r)
output_latex(r)
