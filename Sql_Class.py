import sqlite3


class SqlClass:
    # constructor for SQL class
    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name
        self.c = self.connection.cursor()

    # SQL query to add a table to the db
    def add_table(self):
        query = """CREATE TABLE {t_name}(
        rid integer PRIMARY KEY, biacromial_di real, biiliac_di real, bitrochanteric_di real, chest_depth real,
        chest_di real, elbow_di real, wrist_di real, knee_di real, ankle_di real, shoulder_gir real, chest_gir real,
        waist_gir real, navel_gir real, hip_gir real, thigh_gir real, bicep_gir real, forearm_gir real,
        knee_gir real, calf_gir real, ankle_gir real, wrist_gir real, age real, weight real, height real,
        gender integer)""".format(t_name=self.table_name)

        self.c.execute(query)
        self.connection.commit()

    # SQL query to ass a respondent to the db
    def add_respondent(self, res):
        query = """INSERT INTO {t_name} VALUES (:rid, :biacromial_di, :biiliac_di, :bitrochanteric_di,
                    :chest_depth, :chest_di, :elbow_di, :wrist_di, :knee_di, :ankle_di, :shoulder_gir, :chest_gir,
                    :waist_gir, :navel_gir, :hip_gir, :thigh_gir, :bicep_gir, :forearm_gir, :knee_gir, :calf_gir,
                    :ankle_gir, :wrist_gir, :age, :weight, :height, :gender)""".format(t_name=self.table_name)

        self.c.execute(query, {'rid': res.rid, 'biacromial_di': res.biacromial_di, 'biiliac_di': res.biiliac_di,
                   'bitrochanteric_di': res.bitrochanteric_di, 'chest_depth': res.chest_depth,
                   'chest_di': res.chest_di, 'elbow_di': res.elbow_di, 'wrist_di': res.wrist_di, 'knee_di': res.knee_di,
                   'ankle_di': res.ankle_di, 'shoulder_gir': res.shoulder_gir, 'chest_gir': res.chest_gir,
                   'waist_gir': res.waist_gir, 'navel_gir': res.navel_gir, 'hip_gir': res.hip_gir,
                   'thigh_gir': res.thigh_gir, 'bicep_gir': res.bicep_gir, 'forearm_gir': res.forearm_gir,
                   'knee_gir': res.knee_gir, 'calf_gir': res.calf_gir, 'ankle_gir': res.ankle_gir,
                   'wrist_gir': res.wrist_gir, 'age': res.age, 'weight': res.weight, 'height': res.height,
                   'gender': res.gender})

        self.connection.commit()

    # SQL query to remove a respondent from the db
    def remove_respondent(self, rid):
        with self.connection:
            query = "DELETE FROM {t_name} WHERE rid = :rid".format(t_name=self.table_name)
            self.c.execute(query, {'rid': rid})

    # SQL query to get the associated data for specified RID
    def get_respondent_id(self, rid):
        # row factory returns data as a tuple based on keys
        self.connection.row_factory = sqlite3.Row
        c = self.connection.cursor()
        query = "SELECT * FROM {t_name} WHERE rid = :rid".format(t_name=self.table_name)
        c.execute(query, {'rid': rid})
        return c.fetchone()

    # SQL Query to get the count of rows in the db
    def get_count(self):
        query = "SELECT COUNT(*) from {t_name}".format(t_name=self.table_name)
        self.c.execute(query)
        return self.c.fetchone()

    # SQL Query to get list of all table names
    def get_table_names(self):
        query = "SELECT * FROM sqlite_master WHERE type='table'"
        self.c.execute(query)
        return self.c.fetchone()

    # SQL Query to remove a row from table where rid == del_rid
    def remove_respondent(self, del_rid):
        query = "DELETE FROM {t_name} WHERE rid = {del_rid}".format(t_name=self.table_name, del_rid=del_rid)
        self.c.execute(query)
        self.connection.commit()

    # SQL Query checks to see if the RID is in the table
    def check_in_db(self, rid_check):
        query = "SELECT count(*) FROM respondent_dimensions where rid={rid_check}".format(rid_check=rid_check)
        self.c.execute(query)

        # if value is 0, RID is not in DB and returns false
        if self.c.fetchone()[0] == 0:
            return False

        # else, RID is in DB and returns True
        else:
            return True

    # SQL Query to find the maximum RID in the table
    def get_max(self):
        query = "SELECT MAX(RID) from {t_name}".format(t_name=self.table_name)
        self.c.execute(query)
        return self.c.fetchone()