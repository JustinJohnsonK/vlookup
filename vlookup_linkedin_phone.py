import pandas as pd
import time

start_time = time.time()

listOfNumbers = []
listOfIds = []


def readPhone(fileName, columns):
    """
    Remove Duplicates
    Read the phone_number-linkedin file
    create two lists
    listOfNumbres containing phone numbers
    listOfIds containing likedin ids
    """
    global listOfNumbers
    listOfNumbers = []
    global listOfIds
    listOfIds = []
    
    numbers = pd.read_csv(fileName, usecols=columns)
    numbers_length = len(numbers)

    # removing duplicates
    numbers.drop_duplicates(subset = None, inplace = True)
    print("{} duplicates found in {}".format((numbers_length - len(numbers)), fileName))

    listOfNumbers = numbers.eval(columns[0]).tolist()
    listOfIds = numbers.eval(columns[1]).tolist()


def compareWithPhone(sheet, phoneNumbers, Linkedin):
    """
    Compare sheet with phone
    generator statement to iterate through sheet
    Search for matching phone numbers in main file 
    """

    gener_loop = ([index, row] for index, row in sheet.iterrows() if ((pd.isna(row['LINKEDIN'])) and 
    (row[phoneNumbers] != "nan" or row[phoneNumbers] != "NaN") and 
    (row[phoneNumbers] in listOfNumbers)))

    i = 0
    length = len(sheet)

    while(i < length):
        try:
            index_row = next(gener_loop)
            index = index_row[0]
            row = index_row[1]
            tempIndex = listOfNumbers.index(row[phoneNumbers])
            sheet[Linkedin][index] = listOfIds[tempIndex]  
            i += 1
        except:
            print("Value of i = {} and Value Length = {}".format(i, length))
            return


def writeIntoFile(sheet, inputFileName):
    """
    Wriiting output to a new file
    file name format = inputFileName-result.csv
    """

    if('.csv' in inputFileName):
        inputFileName = inputFileName.replace('.csv', '')
    
    fileName = inputFileName + '-result.csv'
    
    sheet.to_csv(fileName, sep='\t')


def readFile(FileName):
    """
    Reading the Main input file
    """

    sheet = pd.read_csv(FileName)
    return sheet


def ct():
    """
    Just to simplify the calculation of current time
    """
    return(time.time())


def inputDetails():

    pass


def Main():

    FileName = input("Enter the file name...")

    try:
        sheet = readFile(FileName)
    except:
        print("Error in reading file. Please check the file name.")
        return

    number = int(input("Enter the number of files to compare..."))
    listOfFiles = []
    print("Enter the csv file in the order of priority...")

    i = 1
    while(i <= number):
        file = input("Enter name of file {} to compare...".format(i))
        listOfFiles.append(file)
        i += 1

    n = 0
    while(n < number):

        currentPhoneFile = listOfFiles[n]
        print("The column names in {} are {}".format(currentPhoneFile, list(sheet.head(0))))
        phone_number_column = input("Enter the column name containing phone numbers in {} ...".format(currentPhoneFile))
        linkedin_column = input("Enter the column name containing linkedin ids in {} ...".format(currentPhoneFile))
        file_columns = [phone_number_column, linkedin_column]

        readPhone(currentPhoneFile, file_columns)

        compare_time = ct()
        compareWithPhone(sheet, phone_number_column, linkedin_column)
        print("Time to Compare {} = {}".format(currentPhoneFile, ct() - compare_time))

        n += 1

    writeIntoFile(sheet, FileName)

    print("Total time = ", ct() - start_time)
    

if __name__ == '__main__':
Main()
