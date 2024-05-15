from sqlalchemy.orm import scoped_session, sessionmaker

from drawing_comp_backend.utils import managed_session
from drawing_comp_backend.models import db
import os
import hashlib


class Teams:
    def __init__(self, sql_engine):
        self.sql_engine = sql_engine
        self.session_factory = scoped_session(sessionmaker(bind=self.sql_engine))

    def create_team(self, team_name="newTeam"):
        with managed_session(self.session_factory) as session:
            token = hashlib.sha256(team_name.encode('utf-8')).hexdigest()
            team = db.Team(
                name=team_name,
                token=token
            )
            # team_data = {
            #     "id": team.id,
            #     "name": team.name,
            #     "token": team.token
            # }
            session.add(team)
            session.commit()
            return token

    def query_team(self, token):
        with managed_session(self.session_factory) as session:
            team = (
                session.query(db.Team).filter_by(token=token).first()
            )
            if team:
                team_data = {
                    "id": team.id,
                    "name": team.name,
                    "token": team.token
                }
                return team_data
            return None

    def query_all_teams(self):
        with managed_session(self.session_factory) as session:
            teams = session.query(db.Team).all()
            team_data = []
            for team in teams:
                team_data.append({
                    "id": team.id,
                    "name": team.name,
                    "token": team.token
                })
            return team_data