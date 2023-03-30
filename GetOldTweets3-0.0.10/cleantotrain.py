import csv
from pythainlp.tokenize import word_tokenize

# Open the CSV file for reading
with open('cleanUp-ลำไย.csv', 'r',encoding='utf-8') as input_file:
    reader = csv.reader(input_file)
    
    # Open a new CSV file for writing
    with open('ลำไยCleanUp.csv', 'w', newline='',encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        
        # Loop through each row in the input CSV file
        for row in reader:
            words = word_tokenize(row[0])
            # Check if the condition is true (in this example, we're checking if the second column contains the word "True")
            for i in range(len(words)):
                if words[i] == "ลำไย" :
                # Write the row to the output CSV file
                    writer.writerow(row)
                    break