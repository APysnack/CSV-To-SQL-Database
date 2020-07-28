'''
Name: Alan Pysnack
JagID: J00643490
Course: ITE-490
Date: 7/27/2020
'''

import sqlite3
import csv
from Respondent import Respondent
from Sql_Class import SqlClass

# main function that asks user to enter a database name or work from ram
def main():
    user_prompt()


def user_menu(connection):
    # Name of the table that will be created
    table = 'respondent_dimensions'

    # establishes a connection to the database
    conn = sqlite3.connect(connection)

    # Creates instance of an Sql object & passes connection type (RAM or db) and table info
    sql_1 = SqlClass(conn, table)

    menu_sel = 0

    # while loop prompts the user with the user menu until they opt to exit program
    while not menu_sel == 6:
        print("")
        print("Please select one of the following options: ")
        print("--------------------------")
        print("1. Convert a CSV File to a Database")
        print("2. Add a new Respondent to the Database")
        print("3. Remove a Respondent from the Database")
        print("4. List All Respondents in the Database")
        print("5. List All Respondents in the Database and Calculate Averages")
        print("6. Exit Program")
        print("--------------------------")

        # exception handling for user selection
        try:
            menu_sel = int(input('Please enter a number between 1 - 6: '))
        except ValueError:
            try:
                menu_sel = int(input('Please enter a number between 1 - 6: '))
            except ValueError:
                print('There was en error with your input, please try again.')

        print("")

        # if user wants to read from a csv file, asks for file name
        if menu_sel == 1:
            file = input("Enter the name of the csv file you want to read from e.g. 'datafile.csv': ")

            # checks to see if table already exists
            dup = duplicate_check(sql_1)

            # if table is a duplicate, passes an offset to append to current table
            if dup:
                offset = get_count(sql_1)
                csv_to_db_xfer(file, sql_1, offset)

            # if table is not a duplicate, passes an offset of 0
            else:
                csv_to_db_xfer(file, sql_1, 0)

        # Logic to add new repsondent
        elif menu_sel == 2:
            # if table does not already exist, creates a table before adding new respondent
            if sql_1.get_table_names() is None:
                sql_1.add_table()
                add_respondent(sql_1)

            # if table already exists, adds respondent without creating new table
            else:
                add_respondent(sql_1)

        # Asks the user which RID they want to remove
        elif menu_sel == 3:
            prompt_for_removal(sql_1)

        # Logic to display all data
        elif menu_sel == 4:
            # Exception handling for request to show DB when table is not created
            if sql_1.get_table_names() is None:
                print("")
                print("The table name you're searching for currently does not exist")
            else:
                pull_from_db(sql_1)

        # Logic to display data + averages
        elif menu_sel == 5:
            # Exception handling for request to show DB when table is not created
            if sql_1.get_table_names() is None:
                print("")
                print("The table name you're searching for currently does not exist")

            # pull_from_db prints data & returns sums to be calculated by print_avg function
            else:
                mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc = pull_from_db(sql_1)
                print_average(mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc)

        # Ends program and closes connection
        else:
            print('Exiting Program')
            conn.close()


# Takes in a Respondent object and prints off individual attributes
def print_all(temp_resp):
    print(f'Respondent #:{temp_resp.rid}')
    print("Weight: {:.2f}".format(temp_resp.weight_lbs) + ' (lbs.)')
    print("Height: {:.2f}".format(temp_resp.height_inches) + ' (inches)')
    print(f'Gender: {temp_resp.gender_str}')
    print("BMI: {:.2f}".format(temp_resp.get_bmi))
    print("CPA: {:.2f}".format(temp_resp.get_cpa))
    print('----------')


# Male/female accumulators for total sum of data
def sum_total(temp_resp, mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc):

    # If Respondent is Male, accumulates male properties
    if temp_resp.gender == 1:
        mc += 1
        mh += temp_resp.height_inches
        mw += temp_resp.weight_lbs
        mbmi += temp_resp.get_bmi
        mcpa += temp_resp.get_cpa

    # else, Accumulates female properties
    else:
        fc += 1
        fh += temp_resp.height_inches
        fw += temp_resp.weight_lbs
        fbmi += temp_resp.get_bmi
        fcpa += temp_resp.get_cpa

    return mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc


# Takes in total sum of attributes and calculates averages
def print_average(mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc):

    # Handles for divide by 0 errors when male count = 0
    if mc > 0:
        m_avg_h = '%.2f' % round(mh / mc, 2)
        m_avg_w = '%.2f' % round(mw / mc, 2)
        m_avg_bmi = '%.2f' % round(mbmi / mc, 2)
        m_avg_cpa = '%.2f' % round(mcpa / mc, 2)
    else:
        m_avg_h = 0.00
        m_avg_w = 0.00
        m_avg_bmi = 0.00
        m_avg_cpa = 0.00

    # Handles for divide by 0 errors when female count = 0
    if fc > 0:
        f_avg_h = '%.2f' % round(fh / fc, 2)
        f_avg_w = '%.2f' % round(fw / fc, 2)
        f_avg_bmi = '%.2f' % round(fbmi / fc, 2)
        f_avg_cpa = '%.2f' % round(fcpa / fc, 2)
    else:
        f_avg_h = 0.00
        f_avg_w = 0.00
        f_avg_bmi = 0.00
        f_avg_cpa = 0.00

    # Calculates total male/female combined averages
    t_avg_h = '%.2f' % round((mh + fh) / (fc + mc), 2)
    t_avg_w = '%.2f' % round((mw + fw) / (fc + mc), 2)
    t_avg_bmi = '%.2f' % round((mbmi + fbmi) / (fc + mc), 2)
    t_avg_cpa = '%.2f' % round((fcpa + mcpa) / (fc + mc), 2)

    # outputs averages
    print('Averages')
    print('----------')
    print(f'Sex --> Females: {fc} | Males: {mc} | Total: {mc + fc}')
    print(f'Height --> Females: {f_avg_h} | Males: {m_avg_h} | Total: {t_avg_h} (inches)')
    print(f'Weight --> Females: {f_avg_w} | Males: {m_avg_w} | Total: {t_avg_w} (lbs)')
    print(f'BMI --> Females: {f_avg_bmi} | Males: {m_avg_bmi} | Total: {t_avg_bmi}')
    print(f'CPA --> Females: {f_avg_cpa} | Males: {m_avg_cpa} | Total: {t_avg_cpa}')


# function to transfer input data from a CSV file to a database
def csv_to_db_xfer(file_name, sql_obj, offset):

    # an empty list of respondent objects
    resp_list = []

    # returns the count of rows in the current database to provide an offset for the RID value
    offset = get_count(sql_obj)

    # Reads data from a CSV file & puts it into a list of Respondent objects, assigns RID values
    try:
        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)

            # for each line in the csv file, translates data into a new Respondent object
            for x, line in enumerate(csv_reader):
                new_respondent = Respondent((x + 1 + offset), line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7],
                                            line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15],
                                            line[16], line[17], line[18], line[19], line[20], line[21], line[22],
                                            line[23], line[24])

                # appends list of respondents with the newly created Respondent
                resp_list.append(new_respondent)

    # exception handling for incorrect csv file names
    except IOError:
        print('Input Error, check your file name')
        return 0
    except ValueError:
        print('Value Error, the file you\'ve entered may be the incorrect file type')
        return 0
    
    # if a respondent table does not already exist in the database
    if not duplicate_check(sql_obj):
        # creates a new table in the SQL db for the respondents to be stored
        sql_obj.add_table()

    # populates the SQL table with all the Respondents in the the Respondent list
    for x, respondent in enumerate(resp_list):
        sql_obj.add_respondent(resp_list[x])

    # asks the user if they want to see the database information
    user_prompt_1(sql_obj)


# reads the data stored in the database and prints attributes
def pull_from_db(sql_obj):
    # variables to be used as accumulators for aggregate male height, female height, male weight, etc.
    mh, fh, mw, fw, mbmi, fbmi, mcpa, fcpa, mc, fc = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    # count = number of rows in the database table
    count = get_count(sql_obj)

    # iterates over each row in the table, increments the x value each pass (1, 2, 3..)
    for x, respondent in enumerate(range(count+1)):
        # if the x value is in the table, retrieves info and prints
        if sql_obj.check_in_db(x+1):
            # creates temporary holder for the tuple containing x's row information
            temp = sql_obj.get_respondent_id((x+1))

            # creates a temporary respondent and assigns it values based on the row
            temp_resp = Respondent(temp['rid'], temp['biacromial_di'], temp['biiliac_di'], temp['bitrochanteric_di'],
                                   temp['chest_depth'], temp['chest_di'], temp['elbow_di'], temp['wrist_di'],
                                   temp['knee_di'], temp['ankle_di'], temp['shoulder_gir'], temp['chest_gir'],
                                   temp['waist_gir'], temp['navel_gir'], temp['hip_gir'], temp['thigh_gir'],
                                   temp['bicep_gir'], temp['forearm_gir'], temp['knee_gir'], temp['calf_gir'],
                                   temp['ankle_gir'], temp['wrist_gir'], temp['age'], temp['weight'],
                                   temp['height'], temp['gender'])
            # prints out the information related to the temporary respondent
            print_all(temp_resp)
            # passes the temporary respondent to the sum_total function to track running totals
            mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc = sum_total(temp_resp, mh, fh, mw,
                                                                       fw, mbmi, fbmi, fcpa, mcpa, mc, fc)
        # skips over if the x value (RID) is missing from the table (e.g. if it was removed)
        else:
            continue

    # returns running total of attributes (male height, female height, etc.)
    return mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc

# Asks the user if they want to print the data/averages after transferring CSV to database
def user_prompt_1(sql_obj):
    response = input(
        "Transfer completed successfully! Would you like to see the DB and Calculated Averages? Y/N: ").lower()
    if response == 'y':
        mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc = pull_from_db(sql_obj)
        print_average(mh, fh, mw, fw, mbmi, fbmi, fcpa, mcpa, mc, fc)
    else:
        print("Goodbye!")

# gets the count of rows in the current table
def get_count(sql_obj):
    # if table does not exist, i = 0
    if sql_obj.get_table_names() is None:
        i = 0
    else:
        tup = sql_obj.get_count()
        i = int(tup[0])
    return i


# Asks the user for an RID to remove
def prompt_for_removal(sql_obj):
    try:
        rid = int(input("Please enter the ID Number of the Respondent you would like to remove: "))
    except ValueError:
        print("ERROR: Please enter an integer")
        return 0

    # exception handling, checks if RID the user entered is in the db
    if sql_obj.check_in_db(rid):
        sql_obj.remove_respondent(rid)
    else:
        print('This RID was not found in the database')


# checks to see if the table is a duplicate
def duplicate_check(sql_obj):
    # retrieves name of tables in db
    name_tuple = sql_obj.get_table_names()

    # if the table is empty return false
    if name_tuple is None:
        return False

    # else if the table used in the instance is in the list of tables, it is a duplicate
    elif sql_obj.table_name in name_tuple:
        return True

    # else return false
    else:
        return False


# Adds a new respondent to the database
def add_respondent(sql_obj):
    print("----------------------------")
    print("Please enter the following comma separated values for this respondent:")
    print("----------------------------")
    str = "Biacromial Diam., Biiliac Diam., Bitrochanteric Diam., Chest Depth, Chest Diam, Elbow Diam., " \
          "Wrist Diam., Knee Diam., Ankle Diam., Shoulder Girth, Chest Girth, Waist Girth, Navel Girth, " \
          "Hip Girth, Thigh Girth, Bicep Girth, Forearm Girth, Knee Girth, Calf Girth, Ankle Girth, " \
          "Wrist Girth, Age, Weight, Height, Gender (1 for Male, 0 for Female)"

    print(str)
    print("----------------------------")
    # retrieves input from the user in the form of csv
    user_resp = input("Enter your comma separated values here: ").split(',')

    # if the table is currently empty, new_rid = 1
    if sql_obj.get_max()[0] is None:
        new_rid = 1

    # else assigns an id of the current max RID in the database + 1
    else:
        new_rid = (sql_obj.get_max()[0] + 1)

    #  creates a new respondent with the above RID and the user's csv values
    new_respondent = Respondent(new_rid, user_resp[0], user_resp[1], user_resp[2], user_resp[3], user_resp[4],
                                user_resp[5], user_resp[6], user_resp[7], user_resp[8], user_resp[9],
                                user_resp[10], user_resp[11], user_resp[12], user_resp[13], user_resp[14],
                                user_resp[15], user_resp[16], user_resp[17], user_resp[18], user_resp[19],
                                user_resp[20], user_resp[21], user_resp[22], user_resp[23], user_resp[24])
    sql_obj.add_respondent(new_respondent)

    # prints out the users input for verification purposes
    print("Respondent successfully added to the Database!")
    print("------------------------------")
    print(f'RID: {new_respondent.rid}')
    print(f'Biacromial Diameter: {new_respondent.biacromial_di}')
    print(f'Biiliac Diameter: {new_respondent.biiliac_di}')
    print(f'Bitrochanteric Diameter: {new_respondent.bitrochanteric_di}')
    print(f'Chest Depth: {new_respondent.chest_depth}')
    print(f'Chest Diameter: {new_respondent.chest_di}')
    print(f'Elbow Diameter: {new_respondent.elbow_di}')
    print(f'Wrist Diameter: {new_respondent.wrist_di}')
    print(f'Knee Diameter: {new_respondent.knee_di}')
    print(f'Ankle Diameter: {new_respondent.ankle_di}')
    print(f'Shoulder Girth: {new_respondent.shoulder_gir}')
    print(f'Chest Girth: {new_respondent.chest_gir}')
    print(f'Waist Girth: {new_respondent.waist_gir}')
    print(f'Navel Girth: {new_respondent.navel_gir}')
    print(f'Hip Girth: {new_respondent.hip_gir}')
    print(f'Thigh Girth: {new_respondent.thigh_gir}')
    print(f'Bicep Girth: {new_respondent.bicep_gir}')
    print(f'Forearm Girth: {new_respondent.forearm_gir}')
    print(f'Knee Girth: {new_respondent.knee_gir}')
    print(f'Calf Girth: {new_respondent.calf_gir}')
    print(f'Ankle Girth: {new_respondent.ankle_gir}')
    print(f'Wrist Girth: {new_respondent.wrist_gir}')
    print(f'Age: {new_respondent.age}')
    print(f'Weight: {new_respondent.weight}')
    print(f'Height: {new_respondent.height}')
    print(f'Gender: {new_respondent.gender_str}')


# Asks user if they want to use RAM or a db file and passes input as an argument to main menu
def user_prompt():
    print("To use a db file, type the name of the database (e.g. \'datafile.db\')")
    print("If you wish to use RAM, type \'RAM\'")
    db_name = input("Enter Input Here: ").lower()
    if db_name == 'ram':
        user_menu(':memory:')
    else:
        user_menu(db_name)

main()