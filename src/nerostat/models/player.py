from datetime import date
from typing import Optional, List

from pydantic import BaseModel


class TablePlayerModel(BaseModel):
    id_player: int
    nationality: int
    player_name: str
    player_country: str
    player_country_flag: str
    shirt_number: int
    weight: int
    height: int
    birth: date
    age: int


class TablePlayerPriceModel(BaseModel):
    player_price: int
    info_update_date: Optional[date] = "2022-01-01"
    currency:  str


class TablePlayerTeamModel(BaseModel):
    id_team: int
    team_name: str
    team_image: str
    team_country: str
    team_country_flag: str


class TablePlayerTournamentModel(BaseModel):
    id_tournament: int
    tournament_name: str
    tournament_image: str
    tournament_country: str
    tournament_country_flag: str


class TablePlayerSeasonModel(BaseModel):
    id_season: int
    is_current: int
    period: str


class TablePlayerStatModel(BaseModel):
    _90s: float
    rating: float
    game_started: int
    minutes: int
    yellow_card: int
    red_card: int
    goals: int
    assists: int
    expected_goals: float
    expected_non_penalty_goals: float
    expected_assists: float
    dribbles_pg_succ: float
    dribbles_perc_succ: float
    shots_pg: float
    shots_in_target_pg: float
    shots_acc_perc: float
    passes_pg: float
    passes_to_target_pg: float
    passes_acc_perc: float
    shot_creating_actions: float
    goal_creating_actions: float
    aerial_won_pg: float
    aerial_won_perc: float
    tackles_pg: float
    interceptions_pg: float
    blocked_shots_pg: float


class TablePlayerPositionsModel(BaseModel):
    GK: int
    DL: int
    DC: int
    DR: int
    DMC: int
    ML: int
    MC: int
    MR: int
    AML: int
    AMC: int
    AMR: int
    FW: int


class PaginationInfoModel(BaseModel):
    total: int
    offset: int
    limit: int


class TableCountryModel(BaseModel):
    id_country: int
    name: str
    img: str
    short_name: str

    class Config:
        orm_mode = True


class PlayerRequest(BaseModel):
    name: Optional[str] = None
    weight_from: Optional[int]
    weight_to: Optional[int]
    height_from: Optional[int]
    height_to: Optional[int]
    nationality: Optional[int] = None


class PlayerInfo(BaseModel):
    player: TablePlayerModel
    player_price: TablePlayerPriceModel
    player_team: TablePlayerTeamModel
    player_tournament: TablePlayerTournamentModel
    player_season: TablePlayerSeasonModel
    player_stat: TablePlayerStatModel
    player_positions: TablePlayerPositionsModel


class PlayerResponseModel(BaseModel):
    players: List[PlayerInfo]
    total: int
    offset: int
    limit: int
