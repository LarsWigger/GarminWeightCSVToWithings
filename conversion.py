import datetime
import locale

# needed to deal with German date format
locale.setlocale(locale.LC_TIME, "de_DE")

filename = "Gewicht.csv"

with open("Gewicht.csv") as f:
    csv_lines = f.read().split("\n")
print(f"Read data from {filename}")

# remove header
csv_lines = csv_lines[1:]
print("Removed header line")

# remove empty last line if it exists
if csv_lines[-1] == "":
    csv_lines = csv_lines[:-1]

# basic modifications of lines
for index, line in enumerate(csv_lines):
    if line.startswith('"'):  # date line
        # slice away overhead
        line = line[2:-2]
        # convert to date
        line = datetime.datetime.strptime(line, "%d %b %Y").date()
    else:  # measurement line
        line = line.split(",")
        # only time, weight, body fat are interesting, the rest gets dropped right away
        line = line[:2] + [line[4]]
        # remove weight measurement unit
        line[1] = line[1][:-3]
        # append seconds
        line[0] = line[0] + ":00"
    # apply changes to line
    csv_lines[index] = line

print(csv_lines[-5:])
