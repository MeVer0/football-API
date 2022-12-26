from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Country(Base):
    __tablename__ = 'country'

    id_country = Column(Integer, primary_key=True)
    name = Column(String(20))
    code = Column(String(4))
    img = Column(String(150))

    tournament = relationship('Tournament')
    player = relationship('Player', backref='country_player')


class Currency(Base):
    __tablename__ = 'currency'

    currency_name = Column(String(20), primary_key=True)
    exchange_rate = Column(Float)

    player_price_history = relationship("Player_price_history")


class TournamentTable(Base):
    __tablename__ = 'tournament_table'

    id_tournament_table = Column(Integer, primary_key=True,)
    id_stage = Column(Integer, ForeignKey('stage.id_stage'))
    id_team = Column(String(30), ForeignKey('team.id_team'))
    table_rank = Column(Integer)
    away_played = Column(Integer)
    away_win = Column(Integer)
    away_draw = Column(Integer)
    away_loss = Column(Integer)
    away_goal_for = Column(Integer)
    away_goal_against = Column(Integer)
    away_goal_diff = Column(Integer)
    away_points = Column(Integer)
    home_played = Column(Integer)
    home_win = Column(Integer)
    home_draw = Column(Integer)
    home_loss = Column(Integer)
    home_goal_for = Column(Integer)
    home_goal_against = Column(Integer)
    home_goal_diff = Column(Integer)
    home_points = Column(Integer)
    form = Column(String(11))


class Player(Base):
    __tablename__ = 'player'

    id_player = Column(Integer, primary_key=True)
    id_team = Column(Integer, ForeignKey('team.id_team'))
    name = Column(String)
    id_country = Column(Integer, ForeignKey('country.id_country'))
    img = Column(String)
    shirt_number = Column(Integer)
    weight = Column(Integer)
    height = Column(Integer)
    birth = Column(Date)

    player_price_history = relationship("Player_price_history", back_populates="player", uselist=False)


class Player_parse_sourse(Base):
    __tablename__ = 'player_parse_sourse'

    id_parse_source = Column(Integer, primary_key=True)
    id_player = Column(Integer)
    whoscored = Column(String(200))
    fbref = Column(String(200))
    transfermarkt = Column(String(200))


class Player_price_history(Base):
    __tablename__ = 'player_price_history'

    primary_key = Column(Integer, primary_key=True)
    date = Column(Date)
    id_player = Column(Integer, ForeignKey('player.id_player'))
    id_team = Column(Integer, ForeignKey('team.id_team'))
    price = Column(Integer)
    currency_name = Column(String(20), ForeignKey('currency.currency_name'))

    player = relationship("Player", back_populates="player_price_history")
    team = relationship("Team", back_populates="player_price_history")


class Season(Base):
    __tablename__ = 'season'

    id_season = Column(Integer, primary_key=True)
    period = Column(String)
    id_tournament = Column(Integer, ForeignKey('tournament.id_tournament'))
    is_current = Column(Integer)

    player_stat = relationship('PlayerStat', back_populates='season')


class Stage(Base):
    __tablename__ = 'stage'

    id_stage = Column(Integer, primary_key=True)
    id_season = Column(Integer)
    name = Column(String(40))

    tournament_table = relationship('TournamentTable')


# class Tournament_table_pars_sourse(Base):
#     __tablename__ = 'tournament_table_pars_sourse'
#
#     primary_key = Column(Integer, primary_key=True)
#     name = Column(String(50))
#     year = Column(String(50))
#     id_tournament = Column(Integer, ForeignKey('tournament.id_tournament'))
#     fbref_link = Column(String(80))
#     whoscored_link = Column(String(80))


class Team(Base):
    __tablename__ = 'team'

    id_team = Column(Integer, primary_key=True )
    name = Column(String(30))
    alternative_name = Column(String(30))
    img = Column(String(150))
    city = Column(String(20))
    id_tournament = Column(Integer)

    player = relationship('Player')
    player_price_history = relationship("Player_price_history", back_populates="team", uselist=False)
    player_stat = relationship('PlayerStat')
    player_stat_gk = relationship('PlayerStatGk')


class Tournament(Base):
    __tablename__ = 'tournament'

    id_tournament = Column(Integer, primary_key=True)
    id_country = Column(Integer, ForeignKey('country.id_country'))
    name = Column(String(30))
    alternative_name = Column(String(30))
    img = Column(String(150))

    season = relationship('Season')
    stage_pars_sourse = relationship('Tournament_table_pars_sourse')


class PlayerStat(Base):
    __tablename__ = 'player_stat'

    id_player = Column(Integer, primary_key=True)
    id_season = Column(Integer)
    id_team = Column(Integer, ForeignKey('team.id_team'))
    _90s = Column(Float)
    rating = Column(Float)
    game_started = Column(Integer)
    minutes = Column(Integer)
    yellow_card = Column(Integer)
    red_card = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    expected_goals = Column(Float)
    expected_assists = Column(Float)
    expected_non_penalty_goals = Column(Float)
    dribbles_pg_succ = Column(Float)
    dribbles_perc_succ = Column(Integer)
    shots_pg = Column(Float)
    shots_in_target_pg = Column(Integer)
    shots_acc_perc = Column(Float)
    passes_pg = Column(Float)
    passes_to_target_pg = Column(Integer)
    passes_acc_perc = Column(Float)
    shot_creating_actions = Column(Integer)
    goal_creating_actions = Column(Integer)
    aerial_won_pg = Column(Integer)
    aerial_won_perc = Column(Float)
    tackles_pg = Column(Float)
    interceptions_pg = Column(Integer)
    blocked_shots_pg = Column(Integer)

    season = relationship('Season', back_populates='player_stat')


class PlayerStatGk(Base):
    __tablename__ = 'player_stat_gk'

    id_player = Column(Integer, primary_key=True)
    id_team = Column(Integer, ForeignKey('team.id_team'))
    rating = Column(Float)
    game_started = Column(Integer)
    minutes = Column(Integer)
    yellow = Column(Integer)
    red = Column(Integer)
    goals = Column(Integer)
    assists = Column(Integer)
    goals_against = Column(Integer)
    goals_against_per_90 = Column(Float)
    shots_on_target_against = Column(Integer)
    saves = Column(Integer)
    save_perc = Column(Float)
    clean_sheets = Column(Integer)
    clean_sheets_perc = Column(Float)
    penalty_kicks_attempted = Column(Integer)
    penalty_kicks_allowed = Column(Integer)
    penalty_kicks_saved = Column(Integer)
    penalty_save_perc = Column(Float)


class PlayerPosition(Base):
    __tablename__ = 'player_position'

    id_player = Column(Integer, primary_key=True)
    GK = Column(Integer)
    DL = Column(Integer)
    DC = Column(Integer)
    DR = Column(Integer)
    DMC = Column(Integer)
    ML = Column(Integer)
    MC = Column(Integer)
    MR = Column(Integer)
    AML = Column(Integer)
    AMC = Column(Integer)
    AMR = Column(Integer)
    FW = Column(Integer)