# aolug2 UIN : 662418466
# Ayokunle Olugboyo
#

import sqlite3
import matplotlib.pyplot as plt


## function to help open the queries with fetchone
def open_queries1(dbConn, queries):
    sql = queries
    dbcursor = dbConn.cursor()
    dbcursor.execute(sql)
    rows = dbcursor.fetchone()
    return rows


## function to help open the queries with fetchall
def open_queries(dbConn, queries):
    sql = queries
    dbcursor = dbConn.cursor()
    dbcursor.execute(sql)
    rows = dbcursor.fetchall()
    return rows


##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):

    #dbCursor = dbConn.cursor()

    print("General stats:")
    ## queries to the number 0f stations
    row = open_queries1(dbConn, "Select count(*) From Stations;")
    print("  # of stations:", f"{row[0]:,}")

    ## queries to get the number of stops
    row = open_queries1(dbConn, "select count(*) from stops;")
    print("  # of stops:", f"{row[0]:,}")

    ## queries to the number of ride entries
    row = open_queries1(dbConn, "select count(*) from ridership;")
    print("  # of ride entries:", f"{row[0]:,}")

    ## queries for the date range
    row = open_queries1(
        dbConn,
        "select distinct date(Ride_Date) from Ridership order by date(Ride_date) asc limit 1;"
    )
    begin = row[0]
    row = open_queries1(
        dbConn,
        "select distinct date(Ride_Date) from Ridership order by date(Ride_date) desc limit 1;"
    )
    end = row[0]
    print("  date range:", begin, "-", end)

    ## queries for the number of riders
    row = open_queries1(dbConn, "select sum(num_riders) from ridership;")
    print("  Total ridership:", f"{row[0]:,}")
    ## saving the total num riders so I can use it to get the percentage
    totals = row[0]

    ## queries for the weekday riders
    row = open_queries1(
        dbConn,
        "select sum(num_riders) from ridership where type_of_day = 'W';")
    percentage = (row[0] / totals) * 100
    print("  Weekday ridership:", f"{row[0]:,}", f"({percentage:.2f}%)")

    ## queries for the saturday riders
    row = open_queries1(
        dbConn,
        "select sum(num_riders) from ridership where type_of_day = 'A';")
    percentage = (row[0] / totals) * 100
    print("  Saturday ridership:", f"{row[0]:,}", f"({percentage:.2f}%)")

    ## queries for the sunday riders
    row = open_queries1(
        dbConn,
        "select sum(num_riders) from ridership where type_of_day = 'U';")
    percentage = (row[0] / totals) * 100
    print("  Sunday/holiday ridership:", f"{row[0]:,}", f"({percentage:.2f}%)")


#################################################################################################
#################################### function for commad 1 ######################################
#################################################################################################
def command_1(dbConn):
    command = input("\nEnter partial station name (wildcards _ and %): ")
    sql = "select station_ID, station_name from stations where station_name like " + f"'{command}'" + "order by station_name asc;"
    ## calling open_queries function
    rows = open_queries(dbConn, sql)
    if not rows:
        print("**No stations found...")
    else:
        for i in range(len(rows)):
            print(rows[i][0], ":", rows[i][1])


#################################################################################################
#################################### function for commad 2 ######################################
#################################################################################################
def command_2(dbConn):
    row = open_queries1(dbConn, """select sum(num_riders) from ridership;""")
    sql = """select station_name, sum(ridership.num_riders) from stations join ridership on stations.station_ID = ridership.station_ID group by station_Name order by station_Name asc;"""
    ## calling open_queries function
    rows = open_queries(dbConn, sql)
    print("** ridership all stations **")
    if not rows:
        print("**No stations found...")
    else:
        for i in range(len(rows)):
            percentage = (rows[i][1] / row[0]) * 100
            station_name = rows[i][0]
            ridership = rows[i][1]
            print(station_name, ":", f"{ridership:,}", f"({percentage:.2f}%)")


#################################################################################################
#################################### function for commad 3 ######################################
#################################################################################################
def command_3(dbConn):
    print("** top-10 stations **")
    row = open_queries1(dbConn, """select sum(num_riders) from ridership;""")
    sql = """select station_name, sum(ridership.num_riders) from stations join ridership on stations.station_ID = ridership.station_ID group by station_Name order by sum(ridership.num_riders) desc limit 10;"""
    ## calling open_queries function
    rows = open_queries(dbConn, sql)
    if not rows:
        print("**No stations found...")
    else:
        for i in range(len(rows)):
            percentage = (rows[i][1] / row[0]) * 100
            station_name = rows[i][0]
            ridership = rows[i][1]
            print(station_name, ":", f"{ridership:,}", f"({percentage:.2f}%)")


#################################################################################################
#################################### function for commad 4 ######################################
#################################################################################################
def command_4(dbConn):
    print("** least-10 stations **")
    row = open_queries1(dbConn, """select sum(num_riders) from ridership;""")
    sql = """select station_name, sum(ridership.num_riders) from stations join ridership on stations.station_ID = ridership.station_ID group by station_Name order by sum(ridership.num_riders) asc limit 10;"""
    ## calling open_queries function
    rows = open_queries(dbConn, sql)
    if not rows:
        print("**No stations found...")
    else:
        for i in range(len(rows)):
            percentage = (rows[i][1] / row[0]) * 100
            station_name = rows[i][0]
            ridership = rows[i][1]
            print(station_name, ":", f"{ridership:,}", f"({percentage:.2f}%)")


#################################################################################################
#################################### function for commad 5 ######################################
#################################################################################################
def command_5(dbConn):
    color = input("\nEnter a line color (e.g. Red or Yellow): ")
    sql = "select stop_Name, direction, ADA from stops join StopDetails on stops.Stop_ID = StopDetails.Stop_ID join Lines on StopDetails.Line_ID = Lines.Line_ID where color like " + f"'{color}'" + "order by stop_name asc;"
    ## calling open_queries function
    rows = open_queries(dbConn, sql)
    if not rows:
        print("**No such line...")
    else:
        for i in range(len(rows)):
            if (rows[i][2] == 1):
                print(rows[i][0], ":", "direction =", rows[i][1],
                      "(accessible? Yes)")
            else:
                print(rows[i][0], ":", "direction =", rows[i][1],
                      "(accessible? No)")


#################################################################################################
#################################### function for commad 6 ######################################
#################################################################################################
def command_6(dbConn):
    print("** ridership by month **")
    x = []
    y = []
    sql = "select strftime('%m',Ride_Date) as M, (sum(Num_Riders)) from Ridership group by M Order by M asc;"
    ## calling open_queries function
    rows = open_queries(dbConn, sql)
    if not rows:
        print("**No such line...")
    else:
        for i in range(len(rows)):
            num_rider = rows[i][1]
            month = rows[i][0]
            y.append(num_rider)
            x.append(month)
            print(month, ':', f"{num_rider:,}")
        option2 = input("Plot? (y/n) ")
        plt.ylabel("number of riders(X * 10^8)")
        plt.xlabel("month")
        plt.title("monthly ridership")
        if option2 in ['y', 'Y']:
            plt.plot(x, y)
            plt.show()


#################################################################################################
#################################### function for commad 7 ######################################
#################################################################################################
def command_7(dbConn):
    print("** ridership by year **")
    x = []
    y = []
    sql = "select strftime('%Y',Ride_Date) as Y, sum(Num_Riders) from Ridership where Y between '2001' and '2021' group by Y Order by Y asc;"
    ## calling open_queries function
    rows = open_queries(dbConn, sql)
    if not rows:
        print("**No such line...")
    else:
        for i in range(len(rows)):
            num_rider = rows[i][1]
            year = rows[i][0]
            y.append(num_rider)
            x.append(year)
            print(year, ':', f"{num_rider:,}")
        option2 = input("Plot? (y/n) ")
        plt.ylabel("number of riders(X * 10^8)")
        plt.xlabel("year")
        plt.title("yearly ridership")
        if option2 in ['y', 'Y']:
            plt.plot(x, y)
            plt.show()


## function to plot graph for command_8
def graph_command8(rows1, rows2, n_year, station1_name, station2_name):
    station1x = []
    station1y = []
    station2x = []
    station2y = []
    for i in range(len(rows1)):
        station1x.append(rows1[i][0])
        station1y.append(rows1[i][1])
    for i in range(len(rows2)):
        station2x.append(rows2[i][0])
        station2y.append(rows2[i][1])
    plt.plot(station1x, station1y)
    plt.plot(station2x, station2y)
    plt.xlabel("days")
    plt.ylabel("number of riders")
    plt.title("riders each day of " + f"{n_year}")
    plt.legend([station1_name, station2_name], loc="upper right")
    plt.show()


## function to output for command_8
def output_command8(station1_ID, station2_ID, station1_name, station2_name,
                    rows1, rows2):
    print("station 1:", station1_ID, station1_name)
    for i in range(len(rows1)):
        if (i == 5): break
        print(rows1[i][0], rows1[i][1])
    last_5 = rows1[-5:]
    for i in range(len(last_5)):
        print(last_5[i][0], last_5[i][1])
    print("station 2:", station2_ID, station2_name)
    for i in range(len(rows2)):
        if (i == 5): break
        print(rows2[i][0], rows2[i][1])
    last_5 = rows2[-5:]
    for i in range(len(last_5)):
        print(last_5[i][0], last_5[i][1])


#################################################################################################
#################################### function for commad 8 ######################################
#################################################################################################
def command_8(dbConn):
    year = input("\nYear to compare against? ")
    n_year = year
    year = year + "%"
    station1 = input("\nEnter station 1 (wildcards _ and %): ")
    ## queries for station 1
    sql = "select distinct stations.station_ID, stations.station_Name from ridership join stations on ridership.station_id = stations.station_id where station_name like" + f"'{station1}'" + ";"
    ## calling open_queries function
    station1_info = open_queries(dbConn, sql)
    if not station1_info:
        print("**No station found...")
    else:
        if (len(station1_info) > 1):
            print("**Multiple stations found...")
        else:
            sql = "select date(Ride_date) , sum(num_riders) from ridership join stations on ridership.station_id = stations.station_id where station_name like" + f"'{station1}'" + "and date(Ride_date) like" + f"'{year}'" + "group by date(Ride_date);"
            ## calling open_queries function
            rows1 = open_queries(dbConn, sql)
            ## queries for station 2
            station2 = input("\nEnter station 2 (wildcards _ and %): ")
            sql = "select distinct stations.station_ID, stations.station_Name from ridership join stations on ridership.station_id = stations.station_id where station_name like" + f"'{station2}'" + ";"
            ## calling open_queries function
            station2_info = open_queries(dbConn, sql)
            if not station2_info:
                print("**No station found...")
            else:
                if (len(station2_info) > 1):
                    print("**Multiple stations found...")
                else:
                    sql = "select date(Ride_date) , sum(num_riders) from ridership join stations on ridership.station_id = stations.station_id where station_name like" + f"'{station2}'" + "and date(Ride_date) like" + f"'{year}'" + "group by date(Ride_date);"
                    ## calling open_queries function
                    rows2 = open_queries(dbConn, sql)
                    ## printing the output
                    output_command8(station1_info[0][0], station2_info[0][0],
                                    station1_info[0][1], station2_info[0][1],
                                    rows1, rows2)
                    ## code to plot
                    option2 = input("Plot? (y/n) ")
                    if option2 in ['y', 'Y']:
                        graph_command8(rows1, rows2, n_year,
                                       station1_info[0][1],
                                       station2_info[0][1])


#################################################################################################
#################################### function for commad 9 ######################################
#################################################################################################
def command_9(dbConn):
    color = input("\nEnter a line color (e.g. Red or Yellow): ")
    sql = "select distinct station_Name, Latitude, Longitude from stops join StopDetails on stops.Stop_ID = StopDetails.Stop_ID join Lines on StopDetails.Line_ID = Lines.Line_ID join Stations on stops.Station_ID = stations.station_ID where color like " + f"'{color}'" + "order by station_name asc;"
    ## calling open_queries function
    rows = open_queries(dbConn, sql)
    if not rows:
        print("**No such line...")
    else:
        for i in range(len(rows)):
            x = []
            y = []
            x.append(rows[i][1])
            y.append(rows[i][2])
            p = "(" + f"{rows[i][1]}" + ", " + f"{rows[i][2]}" + ")"
            print(rows[i][0], ":", p)
        option2 = input("Plot? (y/n) ")
        if option2 in ['y', 'Y']:
            image = plt.imread("chicago.png")
            xydims = [-87.9277, -87.5569, 41.7012,
                      42.0868]  # area covered by the map:
            plt.imshow(image, extent=xydims)
            plt.title(color + " line")
            if (color.lower() == "purple-express"):
                color = "Purple"  #"Purple"  # color="#800080"
            plt.plot(x, y, "o", c=color)
            for i in range(len(rows)):
                plt.annotate(rows[i][0], (rows[i][1], rows[i][2]))
            plt.xlim([-87.9277, -87.5569])
            plt.ylim([41.7012, 42.0868])
            plt.show()


##################################################################
#
# main
#

print('** Welcome to CTA L analysis app **')

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)

while True:
    option = input("\nPlease enter a command (1-9, x to exit): ")

    ## command 1
    if option == '1':
        #print("you have entered 1")
        command_1(dbConn)
## command 2
    elif option == '2':
        #print("You have entered 2")
        command_2(dbConn)
## command 3
    elif option == '3':
        #print("You have entered 3")
        command_3(dbConn)
## command 4
    elif option == '4':
        #print("You have entered 4")
        command_4(dbConn)
## command 5
    elif option == '5':
        #print("You have entered 5")
        command_5(dbConn)
## command 6
    elif option == '6':
        #print("You have entered 6")
        command_6(dbConn)
## command 7
    elif option == '7':
        #print("You have entered 7")
        command_7(dbConn)
## command 8
    elif option == '8':
        command_8(dbConn)

## command 9
    elif option == '9':
        command_9(dbConn)
    elif option in ['X', 'x']:
        break
    else:
        print("**Error, unknown command, try again...")

#
# done
#
