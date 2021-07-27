import datetime
import locale
import math

# needed to deal with German date format
locale.setlocale(locale.LC_TIME, "de_DE")

input_filename = "Gewicht.csv"

with open("Gewicht.csv") as f:
    csv_lines = f.read().split("\n")
print(f"Read data from {input_filename}")

# remove header
csv_lines = csv_lines[1:]
print("Removed header line")

# remove empty last line if it exists
if csv_lines[-1] == "":
    csv_lines = csv_lines[:-1]

# in order to match the correct date to the right line
current_date = None
output_lines = []
# basic modifications of lines
for line in csv_lines:
    if line.startswith('"'):  # date line
        # slice away overhead
        line = line[2:-2]
        # convert to date
        current_date = datetime.datetime.strptime(line, "%d %b %Y").date()
    else:  # measurement line
        line = line.split(",")
        # only time, weight, body fat are interesting, the rest gets dropped right away
        line = line[:2] + [line[4]]
        # remove weight measurement unit
        line[1] = line[1][:-3]
        # prepend date and append seconds
        line[0] = f"{current_date.strftime('%Y-%m-%d')} {line[0]}:00"
        # if no body fat data exists, delete it
        if line[2] == "--":
            line = line[:2]
        # turn line into comma separated string
        line = ",".join(line)
        # append to output
        output_lines += [line]

del csv_lines  # no longer needed, get rid of it

num_output_files = math.ceil(len(output_lines) / 300)

print(
    f"There are {len(output_lines)} measurements, so {num_output_files} are created to have no more than 300 entries per file")

for file_index in range(num_output_files):
    output_filename = f"withingsWeight{file_index}.csv"
    file_lines = output_lines[0+file_index*300:300+(file_index*300)]
    with open(output_filename, "w") as f:
        f.write("Date,Weight,Fat\n")
        f.write("\n".join(file_lines))
    print(f"Created {output_filename} containing {len(file_lines)} entries")
