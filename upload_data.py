import csv
import sqlite3
import sys


class upload_data():
    def __init__(self):
        self.connection = sqlite3.connect("FinalProject.db") # Link to the main database
        self.cursor = self.connection.cursor()
        csv.field_size_limit(sys.maxsize)
        self.displayDataChunk = 10000

    # Clear the table all the time before re-uploading
    # This will allow us to overwrite the data without having duplicates
    def clearTabley(self, tableName):
        sql = "DELETE FROM '" + tableName + "'"
        self.cursor.execute(sql)
        sql = "DELETE FROM sqlite_sequence WHERE name = '" + tableName + "'" # Delete the Auto Incremented column
        self.cursor.execute(sql)

        self.connection.commit()

    def search(self, list, data):
        for i in range(len(list)):
            if list[i] == data:
                return True
        return False

    def getTitleIDByName(self, titleName):
        sql = "SELECT type_id FROM title_type_master WHERE type_name = '" + titleName + "'"
        title_ids = self.cursor.execute(sql)

        for row in title_ids:
            title_id = row[0]
            return title_id

    def getAllRegionIDs(self):
        sql = "SELECT region_id, region_code FROM region_master"
        region_ids = self.cursor.execute(sql)
        region_id_list = []
        region_code_list = []

        for row in region_ids:
            region_id_list.append(row[0])
            region_code_list.append(row[1])

        return region_id_list, region_code_list

    def getAllLanguageIDs(self):
        sql = "SELECT language_id, language_code FROM language_master"
        language_ids = self.cursor.execute(sql)
        language_id_list = []
        language_code_list = []

        for row in language_ids:
            language_id_list.append(row[0])
            language_code_list.append(row[1])

        return language_id_list, language_code_list

    def getAllMovieIDs(self):
        sql = "SELECT id, original_id FROM movies"
        movie_ids = self.cursor.execute(sql)
        movie_id_list = []
        movie_original_id_list = []

        for row in movie_ids:
            movie_id_list.append(row[0])
            movie_original_id_list.append(row[1])

        return movie_id_list, movie_original_id_list

    def getAllPeopleIDs(self):
        sql = "SELECT people_id, original_id FROM people"
        people_ids = self.cursor.execute(sql)
        people_id_list = []
        people_original_id_list = []

        for row in people_ids:
            people_id_list.append(row[0])
            people_original_id_list.append(row[1])

        return people_id_list, people_original_id_list

    def getAllRoleIDs(self):
        sql = "SELECT role_id, role_name FROM role_master"
        role_ids = self.cursor.execute(sql)
        role_id_list = []
        role_original_name_list = []

        for row in role_ids:
            role_id_list.append(row[0])
            role_original_name_list.append(row[1])

        return role_id_list, role_original_name_list

    def getAllGenreIDs(self):
        sql = "SELECT genre_id, genre_name FROM genre_master"
        genre_ids = self.cursor.execute(sql)
        genre_id_list = []
        genre_original_name_list = []

        for row in genre_ids:
            genre_id_list.append(row[0])
            genre_original_name_list.append(row[1])

        return genre_id_list, genre_original_name_list        

    def loadMovies(self):
        movie_basic_file = 'imdb_datasets/title.basics.tsv'

        # First clear the table
        self.clearTable('movies')

        with open(movie_basic_file, newline='') as basic_data_csv:
            data_reader = csv.reader(basic_data_csv, delimiter='\t')
            print("Loading basic movie data ...")
            count = 0

            for data in data_reader:
                count = count + 1
                if count > 2000:
                    break

                # Ignore the first row as it contains headers only
                if count > 1:
                    original_id = data[0]

                    title = data[2]
                    if data[7] != '\\N':
                        runtime = data[7]
                    else:
                        runtime = ''

                    if data[5] != '\\N':
                        year_published = data[5]
                    else:
                        year_published = ''

                    is_adult = data[4]

                    title_type = data[1]
                    title_id = self.getTitleIDByName(title_type)

                    movie = (original_id, title, title_id,
                             runtime, year_published, is_adult)
                    sql = "INSERT INTO movies(original_id, title, title_type_id, runtime, year_published, is_adult) VALUES(?,?,?,?,?,?)"
                    self.cursor.execute(sql, movie)

            self.connection.commit()

        print("Done uploading movie data ...")

    def loadMovieRegionData(self):
        displayData = self.displayDataChunk
        movie_language_file = 'imdb_datasets/title.akas.tsv'
        # First clear the table
        self.clearTable('movie_region_language')

        print("Now loading movie region data ...")

        movie_id_list, movie_original_id_list = self.getAllMovieIDs()
        region_id_list, region_code_list = self.getAllRegionIDs()

        language_id_list, language_code_list = self.getAllLanguageIDs()

        with open(movie_language_file, newline='') as language_data_csv:
            data_reader = csv.reader(language_data_csv, delimiter='\t')
            count = 0
            print("Now loading movie region data ...")
            region_bulk_data = []
            for data in data_reader:
                count = count + 1

                # Ignore the first row as it contains headers only
                if count > 1:
                    if count > 2000:
                        break

                    original_id = data[0]
                    try:
                        movie_id = movie_id_list[
                            movie_original_id_list.index(original_id)]

                        title = data[2]

                        region_name = data[3]

                        if self.search(region_code_list, region_name) == True:
                            region_id = region_id_list[region_code_list.index(
                                region_name)]
                        else:
                            region_id = None

                        language = data[4]
                        if self.search(language_code_list, language) == True:
                            language_id = language_id_list[language_code_list.index(
                                language)]
                        else:
                            language_id = None

                        region_data = (movie_id, region_id, language_id, title)
                        region_bulk_data.append(region_data)
                        if displayData - count == 1:
                            displayData = displayData + self.displayDataChunk
                            print("%d" % (count), end=" ")
                            print(region_data)
                    except:
                        print("The movie with IMDB ID %s does not have an entry in the movie table." % (
                            original_id))
            # Do a bulk insert using executemany - this is faster
            sql = "INSERT INTO movie_region_language(movie_id, region_id, language_id, title) VALUES(?,?,?,?)"
            self.cursor.executemany(sql, region_bulk_data)
            self.connection.commit()
        print("Done uploading movie regional data ...")

    def loadMasterData(self, filepath, tableName, columnName, sourceIndex):
        # First clear the master table
        self.clearTable(tableName)

        data_list = []

        with open(filepath, newline='') as data_csv:
            data_reader = csv.reader(data_csv, delimiter='\t')
            print("Loading Master Data into the table %s ..." % (tableName))
            count = 0
            for data in data_reader:
                count = count + 1
                # Ignore the first row as it contains headers only
                if count > 1:
                    # there are instances where genre is completely missing
                    if len(data) >= sourceIndex + 1:
                        data_name = data[sourceIndex]
                        if data_name != '\\N':
                            # Check for comma delimited data which requires to be further seperated
                            multi_data = data_name.split(",")

                            for single_data in multi_data:
                                # see if it is not a duplicate data
                                if self.search(data_list, single_data) != True:
                                    data_list.append(single_data)

            if len(data_list) > 0:
                for data_name in data_list:
                    print(data_name)
                    sql = "INSERT INTO " + tableName + "(" + columnName + ") VALUES('" + \
                        data_name + "')"
                    self.cursor.execute(sql)

            self.connection.commit()
            print("Loaded %d number of master data into the table %s." %
                  (len(data_list), tableName))

    def loadRoleRelations(self):
        self.clearTable('role_relations')
        movie_id_list, movie_original_id_list = self.getAllMovieIDs()
        people_id_list, people_original_id_list = self.getAllPeopleIDs()
        role_id_list, role_original_name_list = self.getAllRoleIDs()

        with open('imdb_datasets/title.principals.tsv', newline='') as title_data_csv:
            data_reader = csv.reader(title_data_csv, delimiter='\t')
            print("Loading Data into the table %s ..." % ('role_relations'))
            
            count = 0

            for data in data_reader:
                count = count + 1

                # Ignore the first row as it contains headers only
                if count > 1:
                    if count > 2000:
                        break

                    original_movie_id = data[0]                        
                    movie_id = movie_id_list[movie_original_id_list.index(original_movie_id)]

                    original_people_id = data[2]
                    people_id = people_id_list[people_original_id_list.index(original_people_id)]

                    original_role_name = data[3]
                    role_id = role_id_list[role_original_name_list.index(original_role_name)]

                    role = (role_id, people_id, movie_id)
                    sql = "INSERT INTO role_relations(role_id, people_id, movie_id) VALUES(?,?,?)"
                    self.cursor.execute(sql, role)

            self.connection.commit()

        print("Done uploading role data")           

    def loadGenreRelations(self):
        self.clearTable('genre_relations')
        movie_id_list, movie_original_id_list = self.getAllMovieIDs()
        genre_id_list, genre_original_name_list = self.getAllGenreIDs()

        with open('imdb_datasets/title.basics.tsv', newline='') as title_data_csv:
            data_reader = csv.reader(title_data_csv, delimiter='\t')
            print("Loading Data into the table %s ..." % ('genre_relations'))
            
            count = 0

            for data in data_reader:
                count = count + 1

                # Ignore the first row as it contains headers only
                if count > 1:
                    if count > 2000:
                        break

                    original_movie_id = data[0]                        
                    movie_id = movie_id_list[movie_original_id_list.index(original_movie_id)]

                    multi__data = data[8].split(",")

                    for single_data in multi__data:
                        original_genre_name = single_data
                        if single_data != '\\N':
                            genre_id = genre_id_list[genre_original_name_list.index(original_genre_name)]

                            genre = (genre_id, movie_id)
                            sql = "INSERT INTO genre_relations(genre_id, movie_id) VALUES(?,?)"
                            self.cursor.execute(sql, genre)

            self.connection.commit()

        print("Done uploading genre data")                             

    def loadPeopleData(self, filepath):
        with open(filepath, newline='') as people_csv:
            people_reader = csv.reader(people_csv, delimiter='\t')
            print("Loading people data...")
            count = 0
            for people in people_reader:
                count = count + 1

                if count > 2000:
                    break

                # Ignore the first row as it contains headers only
                if count > 1:
                    original_id = people[0]
                    name = people[1]
                    if people[2] != '\\N':
                        birth_year = people[2]
                    else:
                        birth_year = ''

                    if people[3] != '\\N':
                        death_year = people[3]
                    else:
                        death_year = ''

                    people_data = (original_id, name, birth_year, death_year)
                    sql = ''' INSERT INTO people(original_id, name, birth_year, death_year) VALUES(?,?,?,?) '''
                    self.cursor.execute(sql, people_data)
                    # print("ID: %s, Name: %s, Birth Year: %s, Death Year: %s" %
                    #      (people_data))
            self.connection.commit()
            print("Loaded %d number of people data." % (count))


if __name__ == "__main__":
    data = upload_data()
    # Uncomment the following as per your need
    # data.loadPeopleData('imdb_datasets/name.basics.tsv')

    # data.loadMasterData('imdb_datasets/title.principals.tsv',
    #                    'role_master', 'role_name', 3)

    # data.loadMasterData('imdb_datasets/title.basics.tsv',
    #                    'title_type_master', 'type_name', 1)

    # data.loadMasterData('imdb_datasets/title.basics.tsv',
    #                    'genre_master', 'genre_name', 8)

    # data.loadMasterData('imdb_datasets/title.akas.tsv',
    #                    'language_master', 'language_code', 4)

    # data.loadMasterData('imdb_datasets/title.akas.tsv',
    #                    'region_master', 'region_code', 3)
    # data.loadMovies()
    # data.loadMovieRegionData()

    #data.loadRoleRelations()
    data.loadGenreRelations()