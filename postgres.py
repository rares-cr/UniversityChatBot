import os
import pg8000
from datetime import datetime
import random


class PGWrapper:
    def __init__(self, config, autocommit=True):
        self.__autocommit = autocommit
        self.__config = config

    def __enter__(self):
        return self.connect()

    def __exit__(self, type, value, traceback):
        self.close()

    def _fetchdict(self):
        # This should be a helper function for the query method. It gets the column names
        # from the cursor.
        results = []
        if self.cursor.description:
            cols = [h[0] for h in self.cursor.description]
            for row in self.cursor.fetchall():
                results.append({a: b for a, b in zip(cols, row)})
        return results

    def connect(self):
        self.cnx = pg8000.connect(**self.__config)
        self.cnx.autocommit = self.__autocommit
        self.cursor = self.cnx.cursor()
        return self

    def close(self):
        try:
            self.cursor.close()
            self.cnx.close()
        except Exception:
            pass

    def query(self, sql, parameters=tuple()):
        # This library is pretty lame, but it has the advantage that is super simple and small. It doesn`t need any extra complications.
        # However, it also returns the data from the db as list of tuples without headers. Below I call fetchdict to transform it in a list of dicts.
        exception = None
        for i in range(3):
            try:
                self.cursor.execute(sql, parameters)
                results = self._fetchdict()
                return results
            except Exception as e:
                exception = e
                self.close()
                self.connect()
        raise exception

    def commit(self):
        self.cnx.commit()

    def rollback(self):
        self.cnx.rollback()

    # def upload_students(self, students):
    #     for student in students:
    #         print(student.student_id, student.first_name)
    #         self.query(
    #             f"""
    #                 INSERT INTO msg.students (student_id, first_name, last_name, middle_name) VALUES
    #                 (%s, %s, %s, %s)
    #             """,
    #             (
    #                 student.student_id,
    #                 student.first_name,
    #                 student.last_name,
    #                 student.middle_name,
    #             ),
    #         )

    # def upload_teams(self, teams):
    #     for team in teams:
    #         self.query(
    #             f"""
    #                 INSERT INTO msg.teams (team_name) VALUES (%s)
    #             """,
    #             (team.name,),
    #         )
    #         for student in team.team_members:
    #             student_data = self.query(
    #                 f"""SELECT * FROM msg.students WHERE student_id = %s""",
    #                 (student.student_id,),
    #             )
    #             is_existing_student = True if len(student_data[0]) > 0 else False
    #             if is_existing_student:
    #                 self.query(
    #                     f"""
    #                         INSERT INTO msg.teams_students (student_id, team_name) VALUES (%s, %s)
    #                     """,
    #                     (student.student_id, team.name,),
    #                 )
    #             else:
    #                 print(
    #                     f"Student {student.student_id} doesn`t exist in the database."
    #                 )

    def initiate_conversation(
        self, from_team_name, to_team_name, message
    ):

        max_conv_id = self.query(
            f"""
            select max(conversation_id) as max_conv_id
            from msg.conversations
            """
        )[0]['max_conv_id']
        max_conv_id = max_conv_id if max_conv_id else 1
        max_conv_id = (max_conv_id + 1) #to avoid collisions

        _ = self.query(
            f""" 
                INSERT INTO msg.conversations (conversation_id) VALUES (%s)
            """, (max_conv_id,))
        self.query(
            f"""INSERT INTO msg.messages (from_team, to_team, date_sent, message, received_reply, conversation_id) VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                from_team_name,
                to_team_name,
                datetime.now(),
                message,
                False,
                max_conv_id,
            ),
        )

    def reply_to_message(
        self, previous_message, reply_message
    ):
        _ = self.query(
            f"""
                INSERT INTO msg.messages (from_team, to_team, date_sent, message, received_reply, conversation_terminated, conversation_id) VALUES
            (%s, %s, %s, %s, %s, %s, %s)
        """, (previous_message['to_team'], previous_message['from_team'], datetime.now(), reply_message, False, False, previous_message['conversation_id'])
        )

        _ = self.query(
            f""" 
                UPDATE msg.messages SET received_reply = True where message_id = %s
            """, (previous_message['message_id'],)
        )

    def get_next_message_in_conversation(self, team, conversation_id):
        message_result = self.query(
            f"""
            SELECT
                message_id, from_team, to_team, date_sent, message, received_reply, conversation_terminated, conversation_id, conversation_terminated
            FROM msg.messages
            WHERE conversation_id = %s
            AND to_team = %s
            AND conversation_terminated is False
            ORDER BY date_sent desc
            LIMIT 1
        """, (conversation_id, team)
        )
        if len(message_result) == 0:
            return None

        return message_result[0]

    def get_all_unreplied_conversations(self, team):
        conversations = self.query(
            f"""
            select distinct conversation_id
            from msg.messages
            where to_team = %s
            and received_reply = False
            and not conversation_terminated
            """, (team,)
        )

        return conversations

    def terminate_conversation(self, conversation_id):
        self.query(
            f"UPDATE msg.messages SET conversation_terminated = True WHERE conversation_id = %s",
            (conversation_id,),
        )

    def get_all_teams(self):
        return self.query("select array_agg(team_name) from msg.teams")[0]['array_agg']
