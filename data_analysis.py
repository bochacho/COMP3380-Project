import tkinter as tk
from tkinter import Scrollbar, Widget, ttk, messagebox, Label, Entry, Button, LabelFrame, Frame, Canvas, Text
import sqlite3
import tkinter
from tkinter.constants import RIGHT, W, Y
import csv


class data_analysis():
    # It initializes the UI with a title and pre-defined size
    def __init__(self):
        self.number_of_rows_to_show = 50
        self.connection = sqlite3.connect(
            "FinalProject.db")  # Link to the main database
        self.cursor = self.connection.cursor()
        self.root = tkinter.Tk()
        self.root.title("IMDB Search")
        self.root.geometry('800x600')
        self.root.grid_propagate(False)
        self.build_form()

    def getAllMovieIDs(self):
        sql = "SELECT id, title FROM movies LIMIT 1000"
        movie_ids = self.cursor.execute(sql)
        movie_id_list = []
        title_list = []

        for row in movie_ids:
            movie_id_list.append(row[0])
            title_list.append(row[1])

        return movie_id_list, title_list

    def getAllGenreIDs(self):
        sql = "SELECT genre_id, genre_name FROM genre_master"
        genre_ids = self.cursor.execute(sql)
        genre_id_list = []
        genre_name_list = []

        for row in genre_ids:
            genre_id_list.append(row[0])
            genre_name_list.append(row[1])

        return genre_id_list, genre_name_list

    def getAllTitleTypeIDs(self):
        sql = "SELECT type_id, type_name FROM title_type_master"
        type_ids = self.cursor.execute(sql)
        type_id_list = []
        type_name_list = []

        for row in type_ids:
            type_id_list.append(row[0])
            type_name_list.append(row[1])

        return type_id_list, type_name_list

    def getAllPeopleIDs(self):
        sql = "SELECT people_id, name FROM people LIMIT 1000"
        people_ids = self.cursor.execute(sql)
        people_id_list = []
        people_name_list = []

        for row in people_ids:
            people_id_list.append(row[0])
            people_name_list.append(row[1])

        return people_id_list, people_name_list

    def getAllRoleIDs(self):
        sql = "SELECT role_id, role_name FROM role_master"
        role_ids = self.cursor.execute(sql)
        role_id_list = []
        role_name_list = []

        for row in role_ids:
            role_id_list.append(row[0])
            role_name_list.append(row[1])

        return role_id_list, role_name_list

    def getAllRegionIDs(self):
        sql = "SELECT region_id, region_code FROM region_master"
        region_ids = self.cursor.execute(sql)
        region_id_list = []
        region_code_list = []

        for row in region_ids:
            region_id_list.append(row[0])
            region_code_list.append(row[1])

        return region_id_list, region_code_list

    def search_movie_by_rating(self):
        sql = ""
        if self.rating_logic.get() == '=':
            sql = "SELECT a.title, b.type_name, a.runtime, a.year_published, a.average_rating, a.number_of_votes from movies as a, title_type_master as b where b.type_id = a.title_type_id and a.average_rating = ? LIMIT ?"
        elif self.rating_logic.get() == '>':
            sql = "SELECT a.title, b.type_name, a.runtime, a.year_published, a.average_rating, a.number_of_votes from movies as a, title_type_master as b where b.type_id = a.title_type_id and a.average_rating > ? LIMIT ?"
        elif self.rating_logic.get() == '<':
            sql = "SELECT a.title, b.type_name, a.runtime, a.year_published, a.average_rating, a.number_of_votes from movies as a, title_type_master as b where b.type_id = a.title_type_id and a.average_rating < ? LIMIT ?"

        movie_data = self.cursor.execute(
            sql, (self.rating.get(), self.number_of_rows_to_show))

        data_set = []
        rowCount = 0
        for row in movie_data:
            rowCount = rowCount + 1
            data_set.append(row)

        if len(data_set) == 0:
            # destroy the table frame containing the earlier table if any
            if hasattr(self, 'frame_canvas'):
                try:
                    self.frame_canvas.grid_forget()
                    self.frame_canvas.destroy()
                except:
                    # No operation
                    True
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            heading = ['Title', 'Type', 'Duration', 'Year', 'Rating', 'Votes']
            self.add_table(data_set, heading, "of type " +
                           self.movie_type.get())

    def export_to_csv_by_type(self):
        filename = "export.csv"
        sql = "SELECT a.title, b.type_name, a.runtime, a.year_published, a.average_rating, a.number_of_votes from movies as a, title_type_master as b where b.type_id = a.title_type_id and b.type_name = ? LIMIT ?"
        movie_data = self.cursor.execute(
            sql, (self.movie_type.get(), self.number_of_rows_to_show))
        data_set = []
        rowCount = 0
        for row in movie_data:
            rowCount = rowCount + 1
            data_set.append(row)

        heading = ['Title', 'Type', 'Duration', 'Year', 'Rating', 'Votes']
        # writing to csv file
        with open(filename, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile, delimiter='\t')

            # writing the fields
            csvwriter.writerow(heading)

            # writing the data rows
            csvwriter.writerows(data_set)
        messagebox.showinfo('Done', 'Exported data into CSV file')

    def search_movie_by_type(self):
        sql = "SELECT a.title, b.type_name, a.runtime, a.year_published, a.average_rating, a.number_of_votes from movies as a, title_type_master as b where b.type_id = a.title_type_id and b.type_name = ? LIMIT ?"
        movie_data = self.cursor.execute(
            sql, (self.movie_type.get(), self.number_of_rows_to_show))
        data_set = []
        rowCount = 0
        for row in movie_data:
            rowCount = rowCount + 1
            data_set.append(row)

        if len(data_set) == 0:
            # destroy the table frame containing the earlier table if any
            if hasattr(self, 'frame_canvas'):
                try:
                    self.frame_canvas.grid_forget()
                    self.frame_canvas.destroy()
                except:
                    # No operation
                    True
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            heading = ['Title', 'Type', 'Duration', 'Year', 'Rating', 'Votes']
            self.add_table(data_set, heading, "of type " +
                           self.movie_type.get())

    def search_movie_by_person_role(self):
        sql = "SELECT a.title, b.type_name, a.runtime, a.year_published, a.average_rating, a.number_of_votes FROM " + \
            "movies as a, title_type_master as b, people as c, role_relations as d, role_master as e WHERE " + \
            "b.type_id = a.title_type_id and d.role_id = e.role_id and e.role_name = ? and a.id = d.movie_id and c.name = ? and c.people_id = d.people_id LIMIT ?"

        movie_data = self.cursor.execute(
            sql, (self.role.get(), self.people.get(), self.number_of_rows_to_show))
        data_set = []
        rowCount = 0
        for row in movie_data:
            rowCount = rowCount + 1
            data_set.append(row)

        if len(data_set) == 0:
            # destroy the table frame containing the earlier table if any
            if hasattr(self, 'frame_canvas'):
                try:
                    self.frame_canvas.grid_forget()
                    self.frame_canvas.destroy()
                except:
                    # No operation
                    True
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            heading = ['Title', 'Type', 'Duration', 'Year', 'Rating', 'Votes']
            self.add_table(data_set, heading, "of type " +
                           self.movie_type.get())

    def search_movie_by_region(self):
        sql = "SELECT a.title, b.type_name, a.runtime, a.year_published, a.average_rating, a.number_of_votes from movies as a, title_type_master as b, region_master as c, movie_region_language as d where b.type_id = a.title_type_id and a.id = d.movie_id and d.region_id = c.region_id and c.region_code = ? LIMIT ?"
        movie_data = self.cursor.execute(
            sql, (self.region.get(), self.number_of_rows_to_show))

        data_set = []
        rowCount = 0
        for row in movie_data:
            rowCount = rowCount + 1
            data_set.append(row)

        if len(data_set) == 0:
            # destroy the table frame containing the earlier table if any
            if hasattr(self, 'frame_canvas'):
                try:
                    self.frame_canvas.grid_forget()
                    self.frame_canvas.destroy()
                except:
                    # No operation
                    True
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            heading = ['Title', 'Type', 'Duration', 'Year', 'Rating', 'Votes']
            self.add_table(data_set, heading, " from the region " +
                           self.region.get())

    def search_movie_by_genre(self):
        sql = "SELECT a.title, b.type_name, a.runtime, a.year_published, a.average_rating, a.number_of_votes from movies as a, title_type_master as b, genre_master as c, genre_relations as d where b.type_id = a.title_type_id and c.genre_id = d.genre_id and d.movie_id = a.id and (c.genre_name = ? or c.genre_name = ?) LIMIT ?"
        movie_data = self.cursor.execute(
            sql, (self.genre1.get(), self.genre2.get(), self.number_of_rows_to_show))

        data_set = []
        rowCount = 0
        for row in movie_data:
            rowCount = rowCount + 1
            data_set.append(row)

        if len(data_set) == 0:
            # destroy the table frame containing the earlier table if any
            if hasattr(self, 'frame_canvas'):
                try:
                    self.frame_canvas.grid_forget()
                    self.frame_canvas.destroy()
                except:
                    # No operation
                    True
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            heading = ['Title', 'Type', 'Duration', 'Year', 'Rating', 'Votes']
            self.add_table(data_set, heading, " of genre " +
                           self.genre1.get() + " and " + self.genre2.get())

    def search_movie_by_year(self):
        sql = "SELECT count(movies.title), people.name from " +\
            "people JOIN role_relations on people.people_id = role_relations.people_id JOIN movies on " + \
            "movies.id = role_relations.movie_id where role_relations.role_id = 2 AND " + \
            "movies.year_published BETWEEN 1900 AND 1920 GROUP by people.people_id, people.name"

        movie_data = self.cursor.execute(sql)

        data_set = []
        rowCount = 0
        messageText = "Results:\n"
        for row in movie_data:
            messageText += "%s Directed %d number of movies\n" % (
                row[1], row[0])
            rowCount = rowCount + 1
            data_set.append(row)

        # destroy the table frame containing the earlier table if any
        if hasattr(self, 'frame_canvas'):
            try:
                self.frame_canvas.grid_forget()
                self.frame_canvas.destroy()
            except:
                # No operation
                True

        if len(data_set) == 0:
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            messagebox.showinfo('Result', messageText)

    def search_comedy_movie_by_year(self):
        sql = "SELECT people.name, count(movies.title) as totalMovies, role_master.role_name " + \
            "FROM people JOIN role_relations on role_relations.people_id = people.people_id " + \
            "JOIN movies on movies.id = role_relations.movie_id JOIN role_master on " + \
            "role_master.role_id = role_relations.role_id JOIN genre_relations on genre_relations.movie_id = movies.id " + \
            "JOIN genre_master on genre_master.genre_id = genre_relations.genre_id where genre_master.genre_id = 4 and " +\
            "movies.year_published BETWEEN 1890 AND 1920 GROUP BY people.people_id ORDER BY role_name, totalMovies DESC"

        movie_data = self.cursor.execute(sql)

        data_set = []
        rowCount = 0
        messageText = "Results:\n"
        for row in movie_data:
            messageText += "%s worked in %d movies as %s\n" % (
                row[0], row[1], row[2])
            rowCount = rowCount + 1
            data_set.append(row)

        # destroy the table frame containing the earlier table if any
        if hasattr(self, 'frame_canvas'):
            try:
                self.frame_canvas.grid_forget()
                self.frame_canvas.destroy()
            except:
                # No operation
                True

        if len(data_set) == 0:
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            messagebox.showinfo('Result', messageText)

    def search_by_movies_not_worked(self):
        sql = "SELECT DISTINCT outM.title from movies outM JOIN role_relations on " +\
            "role_relations.movie_id = outM.id JOIN people on people.people_id = role_relations.people_id " + \
            "where people.people_id not in (SELECT people.people_id from movies inM JOIN role_relations on " + \
            "role_relations.movie_id = inM.id JOIN people on people.people_id = role_relations.people_id where inM.id = 122)"

        movie_data = self.cursor.execute(sql)

        data_set = []
        rowCount = 0
        messageText = "Results:\n"
        for row in movie_data:
            messageText += "%s\n" % (
                row[0])
            rowCount = rowCount + 1
            data_set.append(row)

        # destroy the table frame containing the earlier table if any
        if hasattr(self, 'frame_canvas'):
            try:
                self.frame_canvas.grid_forget()
                self.frame_canvas.destroy()
            except:
                # No operation
                True

        if len(data_set) == 0:
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            messagebox.showinfo('Result', messageText)

    def search_by_movies_with_5_rating(self):
        sql = "SELECT  count(movies.title), people.name from movies, people, role_relations where people.people_id = role_relations.people_id and role_relations.role_id = 7 and role_relations.movie_id = movies.id and movies.average_rating > '5' and people.people_id = 122"

        movie_data = self.cursor.execute(sql)

        data_set = []
        rowCount = 0
        messageText = "Results:\n"
        for row in movie_data:
            messageText += "%s got more than 5 rating in %d movies" % (
                row[1], row[0])
            rowCount = rowCount + 1
            data_set.append(row)

        # destroy the table frame containing the earlier table if any
        if hasattr(self, 'frame_canvas'):
            try:
                self.frame_canvas.grid_forget()
                self.frame_canvas.destroy()
            except:
                # No operation
                True

        if len(data_set) == 0:
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            messagebox.showinfo('Result', messageText)

    def search_by_movies_type_each_year(self):
        sql = "SELECT count(outerM.title), outerM.year_published, genre_master.genre_name " + \
            "from movies outerM JOIN genre_relations on genre_relations.movie_id =outerM.id JOIN genre_master on genre_master.genre_id = genre_relations.genre_id " + \
            "where outerM.year_published between 1905 and 1925 " + \
            "GROUP BY outerM.year_published, genre_master.genre_name " + \
            "ORDER BY outerM.year_published, count(outerM.title) DESC"

        movie_data = self.cursor.execute(sql)

        data_set = []
        rowCount = 0
        messageText = "Results:\n"
        for row in movie_data:
            messageText += "%d number of %s movies in the year %s\n" % (
                row[0], row[2], row[1])
            rowCount = rowCount + 1
            data_set.append(row)

        # destroy the table frame containing the earlier table if any
        if hasattr(self, 'frame_canvas'):
            try:
                self.frame_canvas.grid_forget()
                self.frame_canvas.destroy()
            except:
                # No operation
                True

        if len(data_set) == 0:
            messagebox.showerror(
                "Sorry", "Unable to find any move with the search criteria")
        else:
            messagebox.showinfo('Result', messageText)

    def search_by_rating_interface(self, row):
        Label(self.top_frame, text="List all movies whose rating is ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        self.rating_logic = tk.StringVar()
        combo_1 = ttk.Combobox(
            self.top_frame, textvariable=self.rating_logic, width=5, state='readonly')
        combo_1['values'] = (
            '>', '=', '<')
        combo_1.grid(column=1, row=row, padx=5, sticky=W)
        combo_1.current(1)

        self.rating = tk.StringVar()
        combo_2 = ttk.Combobox(
            self.top_frame, textvariable=self.rating, width=5, state='readonly')
        combo_2['values'] = (
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
        combo_2.grid(column=2, row=row, padx=5, sticky=W)
        combo_2.current(0)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_movie_by_rating)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_by_type_interface(self, row):
        Label(self.top_frame, text="List all movies of type ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        self.movie_type = tk.StringVar()
        combo_1 = ttk.Combobox(
            self.top_frame, textvariable=self.movie_type, width=10, state='readonly')
        type_id_list, type_name_list = self.getAllTitleTypeIDs()
        combo_1['values'] = type_name_list
        combo_1.grid(column=1, row=row, padx=5, sticky=W)
        combo_1.current(0)

        export_btn = Button(
            self.top_frame, text="Export", command=self.export_to_csv_by_type)
        export_btn.grid(column=3, row=row, padx=5, sticky=W)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_movie_by_type)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_by_people_role_interface(self, row):
        Label(self.top_frame, text="List all movies where ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        self.people = tk.StringVar()
        combo_1 = ttk.Combobox(
            self.top_frame, textvariable=self.people, width=20, state='readonly')
        people_id_list, people_name_list = self.getAllPeopleIDs()
        people_name_list.sort()
        combo_1['values'] = people_name_list
        combo_1.grid(column=1, row=row, padx=5, sticky=W)
        combo_1.current(1)

        Label(self.top_frame, text=" worked as ", font=(
            "Arial", 12)).grid(column=2, row=row, padx=5, sticky=W)

        self.role = tk.StringVar()
        combo_2 = ttk.Combobox(
            self.top_frame, textvariable=self.role, width=15, state='readonly')
        role_id_list, role_name_list = self.getAllRoleIDs()
        role_name_list.sort()
        combo_2['values'] = role_name_list
        combo_2.grid(column=3, row=row, padx=5, sticky=W)
        combo_2.current(0)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_movie_by_person_role)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_by_region_interface(self, row):
        Label(self.top_frame, text="List all movies from the region ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        self.region = tk.StringVar()
        combo_1 = ttk.Combobox(
            self.top_frame, textvariable=self.region, width=10, state='readonly')
        region_id_list, region_code_list = self.getAllRegionIDs()
        region_code_list.sort()
        combo_1['values'] = region_code_list
        combo_1.grid(column=1, row=row, padx=5, sticky=W)
        combo_1.current(0)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_movie_by_region)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_by_genre_interface(self, row):
        Label(self.top_frame, text="List all movies with genre ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        self.genre1 = tk.StringVar()
        combo_1 = ttk.Combobox(
            self.top_frame, textvariable=self.genre1, width=20, state='readonly')
        genre_id_list, genre_name_list = self.getAllGenreIDs()
        genre_name_list.sort()
        combo_1['values'] = genre_name_list
        combo_1.grid(column=1, row=row, padx=5, sticky=W)
        combo_1.current(0)

        Label(self.top_frame, text=" as well as ", font=(
            "Arial", 12)).grid(column=2, row=row, padx=5, sticky=W)

        self.genre2 = tk.StringVar()
        combo_2 = ttk.Combobox(
            self.top_frame, textvariable=self.genre2, width=15, state='readonly')
        combo_2['values'] = genre_name_list
        combo_2.grid(column=3, row=row, padx=5, sticky=W)
        combo_2.current(0)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_movie_by_genre)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_movies_by_person_as_director_interface(self, row):
        Label(self.top_frame, text="List number of movies where ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        Label(self.top_frame, text="someone worked as a Director", font=(
            "Arial", 12)).grid(column=1, row=row, padx=5, sticky=W)
        Label(self.top_frame, text=" between 1900 and 1920", font=(
            "Arial", 12)).grid(column=2, row=row, padx=5, sticky=W)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_movie_by_year)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_movies_comedy_between_years_interface(self, row):
        Label(self.top_frame, text="List all Comedy movies where ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        Label(self.top_frame, text="someone worked between ", font=(
            "Arial", 12)).grid(column=1, row=row, padx=5, sticky=W)
        Label(self.top_frame, text=" 1890 and 1920", font=(
            "Arial", 12)).grid(column=2, row=row, padx=5, sticky=W)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_comedy_movie_by_year)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_by_movies_not_worked_interface(self, row):
        Label(self.top_frame, text="List all movies in which ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        Label(self.top_frame, text="no one from the movie Conjuring", font=(
            "Arial", 12)).grid(column=1, row=row, padx=5, sticky=W)

        Label(self.top_frame, text=" has ever worked on", font=(
            "Arial", 12)).grid(column=2, row=row, padx=5, sticky=W)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_by_movies_not_worked)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_by_movies_with_5_rating_interface(self, row):
        Label(self.top_frame, text="List all movies which ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        Label(self.top_frame, text=" has more than 5 rating where ", font=(
            "Arial", 12)).grid(column=1, row=row, padx=5, sticky=W)

        Label(self.top_frame, text="Charles Chaplin worked", font=(
            "Arial", 12)).grid(column=2, row=row, padx=5, sticky=W)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_by_movies_with_5_rating)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def search_by_movies_type_each_year_interface(self, row):
        Label(self.top_frame, text="List count of movies published ", font=(
            "Arial", 12)).grid(column=0, row=row, padx=5, sticky=W)

        Label(self.top_frame, text=" each year between ", font=(
            "Arial", 12)).grid(column=1, row=row, padx=5, sticky=W)

        Label(self.top_frame, text="1905 and 1925", font=(
            "Arial", 12)).grid(column=2, row=row, padx=5, sticky=W)

        search_btn = Button(
            self.top_frame, text="Find", command=self.search_by_movies_type_each_year)
        search_btn.grid(column=5, row=row, padx=5, sticky=W)

    def add_table(self, data, column_headings=[], table_heading=''):
        # destroy the table frame containing the earlier table if any
        if hasattr(self, 'frame_canvas'):
            try:
                self.frame_canvas.grid_forget()
                self.frame_canvas.destroy()
            except:
                # No operation
                True

        # Create a frame for the canvas with non-zero row&column weights
        self.frame_canvas = LabelFrame(
            self.root, text='Details of the movies ' + table_heading)
        self.frame_canvas.grid(
            row=2, column=0, pady=(5, 0), padx=10, sticky='nw')
        self.frame_canvas.grid_rowconfigure(0, weight=1)
        self.frame_canvas.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.frame_canvas.grid_propagate(False)

        # Add a canvas in that frame
        canvas = tk.Canvas(self.frame_canvas, bg="yellow")
        canvas.grid(row=0, column=0, sticky="news")

        # Link a scrollbar to the canvas
        vsb = tk.Scrollbar(self.frame_canvas, orient="vertical",
                           command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        # Create a frame to contain the buttons
        frame_buttons = tk.Frame(canvas, bg="blue")
        canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

        start_row = 1
        rows = len(data)
        columns = len(column_headings)

        headings = [[Label] for j in range(columns)]
        for i in range(0, columns):
            headings[i] = Label(frame_buttons, text=str(column_headings[i]), fg='blue',
                                font=('Arial', 12, 'bold'))
            headings[i].grid(row=0, column=i, sticky='news')

        columns = len(data[0])

        # buttons = [[tk.Button() for j in range(columns)] for i in range(rows)]
        elements = [[tk.Label() for j in range(columns)] for i in range(rows)]

        for i in range(0, rows):
            for j in range(0, columns):
                elements[i][j] = tk.Label(frame_buttons, text=str(data[i][j]), width=len(str(data[i][j]).strip()),
                                          font=('Arial', 12))
                elements[i][j].grid(row=i + start_row, column=j, sticky='news')

        # Update buttons frames idle tasks to let tkinter calculate buttons sizes
        frame_buttons.update_idletasks()

        # Resize the canvas frame to show exactly 5-by-5 buttons and the scrollbar
        first5columns_width = sum([elements[0][j].winfo_width()
                                   for j in range(0, columns)])
        first5rows_height = sum([elements[i][0].winfo_height()
                                for i in range(0, 10)])

        self.frame_canvas.config(width=first5columns_width + vsb.winfo_width() + 20,
                                 height=first5rows_height)

        # Set the canvas scrolling region
        canvas.config(scrollregion=canvas.bbox("all"))

    def build_form(self):
        self.top_frame = LabelFrame(self.root, text="Choose the Query")
        self.top_frame.grid(row=0, column=0, sticky=W, padx=10)

        self.search_by_rating_interface(1)
        self.search_by_type_interface(2)
        self.search_by_people_role_interface(3)
        self.search_by_region_interface(4)
        self.search_by_genre_interface(5)
        self.search_movies_by_person_as_director_interface(6)
        self.search_movies_comedy_between_years_interface(7)
        self.search_by_movies_not_worked_interface(8)
        self.search_by_movies_with_5_rating_interface(9)
        self.search_by_movies_type_each_year_interface(10)

        self.root.mainloop()


# The main route to run the program
if __name__ == "__main__":
    form = data_analysis()
