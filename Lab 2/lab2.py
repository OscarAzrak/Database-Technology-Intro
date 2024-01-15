import sqlite3
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
import math

connection1 = sqlite3.connect('mondial.db')
cursor1 = connection1.cursor()
"""-Question 2a-"""
def query_a():
    # Here we test some concurrency issues.
    xy = "SELECT year, population " \
         "FROM popdata"
    print("U1: (start) "+ xy)
    try:
        cursor1.execute(xy)
        data = cursor1.fetchall()
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        exit()
    xs = []
    ys = []
    for r in data:
        # you access ith component of row r with r[i], indexing starts with 0
        # check for null values represented as "None" in python before conversion and drop
        # row whenever NULL occurs
        print("Considering tuple", r)
        if (r[0] != None and r[0] != None):
            xs.append(float(r[0]))
            ys.append(float(r[1]))
        else:
            print("Dropped tuple ", r)
    print("xs:", xs)
    print("ys:", ys)
    return [xs, ys]

"""-Question 2b-"""
def query_b():
    # Here we test some concurrency issues.
    xy = "SELECT year, SUM(population) " \
         "FROM popdata " \
         "GROUP BY year"

    print("U1: (start) " + xy)
    try:
        cursor1.execute(xy)
        data = cursor1.fetchall()
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        exit()
    xs = []
    ys = []
    for r in data:
        # you access ith component of row r with r[i], indexing starts with 0
        # check for null values represented as "None" in python before conversion and drop
        # row whenever NULL occurs
        print("Considering tuple", r)
        if (r[0] != None and r[0] != None):
            xs.append(float(r[0]))
            ys.append(float(r[1]))
        else:
            print("Dropped tuple ", r)
    print("xs:", xs)
    print("ys:", ys)
    return [xs, ys]

"""-Question 2c-"""

def query_c():
    # Here we test some concurrency issues.
    xy = "SELECT year, population " \
         "FROM popdata " \
         "WHERE name='New York'" \


    print("U1: (start) " + xy)
    try:
        cursor1.execute(xy)
        data = cursor1.fetchall()
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        exit()
    xs = []
    ys = []
    for r in data:
        # you access ith component of row r with r[i], indexing starts with 0
        # check for null values represented as "None" in python before conversion and drop
        # row whenever NULL occurs
        print("Considering tuple", r)
        if (r[0] != None and r[0] != None):
            xs.append(float(r[0]))
            ys.append(float(r[1]))
        else:
            print("Dropped tuple ", r)
    print("xs:", xs)
    print("ys:", ys)
    regr = LinearRegression().fit(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
    score = regr.score(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
    a = regr.coef_[0][0]
    b = regr.intercept_[0]
    x_axle = [1980, 1990, 2000, 2010, 2020, 2030]
    y_axle = []
    for i in x_axle:
        y_axle.append(int(a)*i + int(b))

    return [xs, ys], y_axle, x_axle, a, b, score
def d_get_cities_countries():
    xycitcountr = "SELECT DISTINCT name,  country " \
                  "FROM PopData"

    print("U1: (start) " + xycitcountr)
    try:
        cursor1.execute(xycitcountr)
        data = cursor1.fetchall()
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        exit()
    xcities = []
    ycountries = []
    for r in data:
        # you access ith component of row r with r[i], indexing starts with 0
        # check for null values represented as "None" in python before conversion and drop
        # row whenever NULL occurs
        #print("Considering tuple", r)
        if (r[0] != None and r[0] != None):
            xcities.append((r[0]))
            ycountries.append((r[1]))
        #else:
         #   print("Dropped tuple ", r)
    print("xcity:", xcities)
    print("ycountries:", ycountries)
    return xcities, ycountries

def d_get_years(city):
    xy = 'select year,  population ' \
         'FROM PopData ' \
         'WHERE name = "' + city + '"';
    #print("U1: (start) " + xy)
    try:
        cursor1.execute(xy)
        data = cursor1.fetchall()
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        exit()
    xs = []
    ys = []
    for r in data:
        # you access ith component of row r with r[i], indexing starts with 0
        # check for null values represented as "None" in python before conversion and drop
        # row whenever NULL occurs
        #print("Considering tuple", r)
        if (r[0] != None and r[0] != None):
            xs.append(float(r[0]))
            ys.append(float(r[1]))
        #else:
            #print("Dropped tuple ", r)
    return [xs, ys]

def d_create_table():
    try:
        drop_q = "DROP TABLE IF EXISTS linearprediction;"
        cursor1.execute(drop_q)
        connection1.commit()
        # by default in pgdb, all executed queries for connection 1 up to here form a transaction
        # we can also explicitly start tranaction by executing BEGIN TRANSACTION
    except sqlite3.Error as e:
        print("ROLLBACK: linearprediction table does not exists or other error.")
        print("Error message:", e.args[0])
        connection1.rollback()
        pass
    create_table_query = "CREATE TABLE linearprediction( name VARCHAR2(50) not NULL ," \
                         "country VARCHAR2(50) not NULL ," \
                         "a float not NULL ," \
                         "b float not NULL ," \
                         "score float not NULL " \
                         "CONSTRAINT linearprediction " \
                         "CHECK (score >= 0) " \
                         "CHECK (1 >= score)," \
                         "CONSTRAINT linearprediction " \
                         "PRIMARY KEY (name, country) );"
    try:
        cursor1.execute(create_table_query)
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
def d_insert_table(cities, scores, countries, a_values, b_values):
    try:
        for i in range(len(cities)):
            print(cities[i])
            if (str(scores[i]) != "nan"):
                sql = 'INSERT INTO linearprediction (name, country,a,b,score) VALUES ("' + str(
                    cities[i]) + '","' + str(countries[i]) + '",' + str(a_values[i]) + ',' + str(
                    b_values[i]) + ',' + str(scores[i]) + ')'
            else:
                sql = 'INSERT INTO linearprediction (name, country,a,b,score) VALUES ("' + str(
                    cities[i]) + '","' + str(countries[i]) + '",' + str(a_values[i]) + ',' + str(
                    b_values[i]) + ',' + str(0) + ')'
            print(sql)
            cursor1.execute(sql)
            connection1.commit()

            print(cities[i])
    except sqlite3.Error as e:
        print("Error message :", e.args[0])
        connection1.rollback()



def query_d():
    #table namn: linearprediction, ska innehålla name country a b score, name är city cojuntry är country(kod) a, b, score är från C
    #fyll tabellen med värden för varje stad
    #värdena kmr från linjär regrerrar varje stad
    # Here we test some concurrency issues.

    a_values = []
    b_values = []
    scores = []
    [cities, countries] = d_get_cities_countries()
    for city in cities:
        [xs, ys] = d_get_years(city)
        regr = LinearRegression().fit(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
        score = regr.score(np.array(xs).reshape([-1, 1]), np.array(ys).reshape([-1, 1]))
        a = regr.coef_[0][0]
        b = regr.intercept_[0]
        a_values.append(a)
        b_values.append(b)
        scores.append(score)
    d_create_table()
    d_insert_table(cities, scores, countries, a_values, b_values)





"""2e"""
def e_createprediction():
    try:
        query = "DROP TABLE Prediction";
        cursor1.execute(query)
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        pass

    try:
        query = "CREATE TABLE Prediction(" \
                "name TEXT NOT NULL," \
                "country TEXT NOT NULL," \
                "population TEXT NOT NULL," \
                "year TEXT NOT NULL);"

        cursor1.execute(query)
        connection1.commit()
        print("Done creating table!")
        print()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()

def e_insertprediction():
    e_createprediction()
    query = "SELECT linearprediction.name, linearprediction.country, a, b " \
            "FROM linearprediction "
    try:
        cursor1.execute(query)
        data = cursor1.fetchall()
        #print(data)
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        exit()

    for entry in data:
        years = list(range(1950, 2051))
        for year in years:
            query = 'INSERT INTO Prediction(name, country,population, year) VALUES ("' + str(
                entry[0]) + '","' + str(entry[1]) + '",' + str(entry[2] * year + entry[3]) + ',' + str(year) + ')'
            try:
                cursor1.execute(query)
                connection1.commit()
            except sqlite3.Error as e:
                print("Error message:", e.args[0])
                connection1.rollback()
                exit()

'Question 2f'


def f_visualization():
    query = "SELECT year, population, name " \
            "FROM Prediction " \
            "WHERE population > 0"
    try:
        cursor1.execute(query)
        data = cursor1.fetchall()
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        exit()


    data2 = sorted(data, key=lambda x: x[0])
    zippeddata = zip(*data2)
    foo = list(zippeddata)

    try:
        xvals = list(map(float, foo[0]))
        yvals = list(map(float, foo[1]))
        names = list(map(str, foo[2]))
    except IndexError:
        print("Empty table, populate it please!")
        return

    plt.scatter(xvals, yvals)

    xmax = xvals[int(np.argmax(yvals))]
    ymax = max(yvals)
    maxname = names[int(np.argmax(yvals))]
    xmin = xvals[int(np.argmin(yvals))]
    #print(min(xvals))
    ymin = min(yvals)
    #print(ymin)
    minname = names[int(np.argmin(yvals))]

    textmax = "Maximum Population, Year = {}, Population = {}, City = {}".format(int(xmax), int(ymax), maxname)
    textmin = "Minimum Population, Year = {}, Population = {}, City = {}".format(int(xmin), int(ymin), minname)

    plt.axhline(ymax, color='r', linestyle='-', label=textmax)
    plt.axhline(ymin, color='y', linestyle='-', label=textmin)

    mean = np.mean(yvals)
    plt.axhline(mean, color='g', linestyle='-', label='Mean = ' + str(int(mean)))

    plt.legend()
    plt.show()

    print('done with plot')
    print(data)

def close():
    connection1.close()

# when calling python lab2.py the following functions will be executed:
#[xs, ys] = query()

def run_a():
    [xs, ys] = query_a()
    plt.scatter(xs, ys)
    plt.xlabel("year")
    plt.show()  # display figure if you run this code locally
    plt.savefig("CitypoulationRawData.png")  # save figure as image in local directory
    close()

def run_b():
    [xs, ys] = query_b()
    plt.scatter(xs, ys)
    plt.xlabel("year")
    plt.show()  # display figure if you run this code locally
    plt.savefig("TotalCityPopulationByYearIn.png")  # save figure as image in local directory
    close()

def run_c():
    [xs, ys], y_axle, x_axle, a, b, score = query_c()
    print(score)
    plt.plot(x_axle, y_axle, color='red', linewidth=2)
    plt.scatter(xs, ys)
    plt.suptitle('City population and Prediction for: New York, a= '+ str(a) + ", b= "+ str(b) + ", score= " + str(score))
    plt.xlabel("year")
    plt.show()  # display figure if you run this code locally
    plt.savefig("figure.png")  # save figure as image in local directory
    close()

def run_d():
    query_d()

def run_e_f():
    menu2 = input("1. Create new prediction\n" + "2. Populate prediction table\n" + "3. Visualize the prediction table")
    try:
        if menu2 == "1":
            e_createprediction()
        elif menu2 == "2":
            e_insertprediction()
        elif menu2 == "3":
            f_visualization()
    except:
        pass

def run_g():
    print()
    ourhypothesis = "Our hypothesis is: Big cities grow at higher rates than smaller ones"
    print(ourhypothesis)

    try:
        choice = int(input("1. Growth Analysis \n" + "2. Exit"))
        if choice < 1:
            print("Too low!")
            raise ValueError
        elif choice > 2:
            print("Too High!")
            raise ValueError
    except ValueError:
        print("Try again!")
        print()
        run_g()

    if choice == 1:
        print("Analysing the growth")
        g_analysis()

    elif choice == 2:
        return

def data_grabber(x_attr=None, y_attr=None, extras=None, table_name=None, where_condition=None, complex=None):
    if complex is not None:
        query = complex
    else:
        query_sel = "SELECT {}, {} ".format(x_attr, y_attr)
        if extras is not None:
            for extra in extras:
                query_sel += ", " + extra
            query_sel += " "

        query_from = "FROM {} ".format(table_name)

        if where_condition is not None:
            where_statement = "WHERE " + where_condition
        else:
            where_statement = ""

        query_where = "{}".format(where_statement)

        query = query_sel + query_from + query_where

    print("Your query is: " + query)
    try:
        cursor1.execute(query)
        data = cursor1.fetchall()
        connection1.commit()
    except sqlite3.Error as e:
        print("Error message:", e.args[0])
        connection1.rollback()
        return True

    data2 = sorted(data, key=lambda x: x[0])
    zippeddata = zip(*data2)
    z = list(zippeddata)
    x = list(map(float, z[0]))
    y = list(map(float, z[1]))
    return x, y

def get_big_cities(big_city_size):
    data = data_grabber("year", "population", None, "PopData", "population > " + big_city_size, None)
    return data

def get_small_cities(small_city_size):
    data = data_grabber("year", "population", None, "PopData", "population < " + small_city_size, None)
    return data
def eval_city_growth(big_city_size, small_city_size):
    years_big, pop_big = get_big_cities(big_city_size)
    years_small, pop_small = get_small_cities(small_city_size)

    first_year = max([min(years_big), min(years_small)])
    last_year = min([max(years_big), max(years_small)])


    prev_year = None
    next_year = None
    growth_list_big = []
    while len(years_big) != 0:
        i = 0
        prev_year = next_year
        while prev_year == next_year:
            try:
                prev_year = years_big[i]
                next_year = years_big[i + 1]
                i += 1
            except IndexError:
                i += 1
                break
        try:
            sliced = pop_big[:i]
        except IndexError:
            sliced = pop_big
            growth_list_big.append([years_big[0], np.average(sliced)])
            break

        growth_list_big.append([years_big[0], np.average(sliced)])
        pop_big = pop_big[i + 1:]
        years_big = years_big[i + 1:]

    prev_year = None
    next_year = None
    growth_list_small = []
    while len(years_small) != 0:
        i = 0
        prev_year = next_year
        while prev_year == next_year:
            try:
                prev_year = years_small[i]
                next_year = years_small[i + 1]
                i += 1
            except IndexError:
                i += 1
                break
        try:
            sliced = pop_small[:i]
        except IndexError:
            sliced = pop_small
            growth_list_small.append([years_small[0], np.average(sliced)])
            break

        growth_list_small.append([years_small[0], np.average(sliced)])
        pop_small = pop_small[i + 1:]
        years_small = years_small[i + 1:]

    pop_big = list(zip(*growth_list_big))[1]
    year_big = list(zip(*growth_list_big))[0]
    pop_small = list(zip(*growth_list_small))[1]
    year_small = list(zip(*growth_list_small))[0]

    growth_big = []
    growth_small = []

    for i in range(len(pop_big)):
        try:
            if math.isinf(pop_big[i + 1] / pop_big[i]) is True or pop_big[i + 1] / pop_big[i] > 5:
                pass
            else:
                growth_big.append([year_big[i + 1], ((pop_big[i + 1] / pop_big[i]) - 1)])
        except IndexError:
            pass

    for i in range(len(pop_small)):
        try:
            if math.isinf(pop_small[i + 1] / pop_small[i]) is True or (
                    (pop_small[i + 1] / pop_small[i]) - 1) < -0.9 or ((pop_small[i + 1] / pop_small[i]) - 1) > 5:
                pass
            else:
                growth_small.append([year_small[i + 1], ((pop_small[i + 1] / pop_small[i]) - 1)])
        except IndexError:
            pass

    big_years = []
    small_years = []
    growth_big_final = []
    growth_small_final = []

    for elem in growth_big:
        big_years.append(elem[0])
        growth_big_final.append(elem[1])

    for elem in growth_small:
        small_years.append(elem[0])
        growth_small_final.append(elem[1])

    return big_years, growth_big_final, small_years, growth_small_final

def g_analysis():
    while True:
    #    try:
    #        syntax_q = input("Do you want to see the syntax? y/n ")
    #        if syntax_q == "y":
    #            syntax_printer()
    #

        big_city_size = input("How big do you consider a big city to be?")
        small_city_size = input("How big do you consider a small city to be?")

        bigx, bigy, smallx, smally = eval_city_growth(big_city_size, small_city_size)

        ylower = min([min(bigy), min(smally)])
        yupper = max([max(bigy), max(smally)])

        fig, axs = plt.subplots(1, 2)
        big_plot_label = "Growth Rate of cities where population > " + big_city_size
        small_plot_label = "Growth Rate of cities where population < " + small_city_size
        axs[0].plot(bigx, bigy, label=big_plot_label)
        axs[1].plot(smallx, smally, label=small_plot_label)

        axs[0].set_ylim(ylower, yupper)
        axs[1].set_ylim(ylower, yupper)

        fig.suptitle("Growth Rates of big and small cities")
        axs[0].legend(loc=1, fontsize=6)
        axs[1].legend(loc=2, fontsize=6)
        plt.show()

def main():
    menu = input("1. Answer A\n" + "2. Answer B\n" + "3. Answer C\n" + "4. Answer D\n" + "5. Answer E and F\n" + "6. Answer G\n" + "7. Exit")
    try:
        if menu == "1":
            run_a()
        elif menu == "2":
            run_b()
        elif menu == "3":
            run_c()
        elif menu == "4":
            run_d()
        elif menu == "5":
            run_e_f()
        elif menu == "6":
            run_g()
        else:
            exit()

    except:
        pass

main()
