import pandas as pd
import time

start_time = time.time()

listOfKeys = []
listOfData = []


def readCompareFile(fileName, columns):
    """
    Read Comparing file
    Remove Duplicates
    create two lists
    listOfKeys containing key values
    listOfData containing containing data
    """
    global listOfKeys
    listOfKeys = []
    global listOfData
    listOfData = []
    
    numbers = pd.read_csv(fileName, usecols=columns)
    numbers_length = len(numbers)

    # removing duplicates
    numbers.drop_duplicates(subset = None, inplace = True)
    print("{} duplicates found in {}".format((numbers_length - len(numbers)), fileName))

    listOfKeys = numbers.eval(columns[0]).tolist()
    listOfData = numbers.eval(columns[1]).tolist()


def compareWithFile(sheet, key_values, data_values):
    """
    Compare sheet with key values and data
    generator statement to iterate through sheet
    Search for matching keys in main file 
    """
    gener_loop = ([index, row] for index, row in sheet.iterrows() if ((pd.isna(row['data_values'])) and 
    (row[key_values] != "nan" or row[key_values] != "NaN") and 
    (row[key_values] in listOfKeys)))

    i = 0
    length = len(sheet)

    while(i < length):
        try:
            index_row = next(gener_loop)
            index = index_row[0]
            row = index_row[1]
            tempIndex = listOfKeys.index(row[key_values])
            sheet[data_values][index] = listOfData[tempIndex]  
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


def Main():
    """
    Order of execution:
    ->1.Read Main File
    ->2.Get the number of files to compare
    ->3.Input the compare csv file
    ->4.Compare with main file and enter data if matches occur
    ->5.Go to 3, if there are still files to compare
    ->6.After comparing - Write it to a new file
    ->7.Stop execution
    """

    FileName = input("Enter the Main file name...")

    try:
        sheet = readFile(FileName)
    except:
        print("Error in reading file. Please check the file name.")
        return

    number = int(input("Enter the number of files to compare..."))
    listOfFiles = []
    print("Enter the csv files in the order of priority...")

    i = 1
    while(i <= number):
        file = input("Enter name of file {} to compare...".format(i))
        listOfFiles.append(file)
        i += 1

    n = 0
    while(n < number):

        currentCompareFile = listOfFiles[n]
        print("The column names in {} are {}".format(currentCompareFile, list(sheet.head(0))))
        key_value_column = input("Enter the column name containing key values in {} ...".format(currentCompareFile))
        datas_column = input("Enter the column name containing datas in {} ...".format(currentCompareFile))
        file_columns = [key_value_column, datas_column]

        readCompareFile(currentCompareFile, file_columns)

        compare_time = ct()
        compareWithFile(sheet, key_value_column, datas_column)
        print("Time to Compare {} = {}".format(currentCompareFile, ct() - compare_time))

        n += 1

    writeIntoFile(sheet, FileName)

    print("Total time = ", ct() - start_time)
    

if __name__ == '__main__':
    Main()