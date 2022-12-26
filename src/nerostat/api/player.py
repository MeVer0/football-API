from fastapi import APIRouter, Query, Depends
from starlette.requests import Request
from nerostat.functions import get_sql_query_by_params, get_validate_query_string_params, \
    get_player_response_model_data, get_limit_and_offset
from ..models.player import PlayerResponseModel
from sqlalchemy.orm import Session
from ..database import get_session


router = APIRouter(
    prefix="/api/v1/getPlayersByStat"
)

base_query = '(' \
             'SELECT ' \
             'player.id_player as id_player,' \
             'player.id_country as nationality, ' \
             'player.name as player_name, ' \
             'player.img as player_image, ' \
             'player_country.name as player_country, ' \
             'player_country.img as player_country_flag, ' \
             'player.shirt_number, ' \
             'player.weight, ' \
             'player.height, ' \
             'player.birth, ' \
             'TIMESTAMPDIFF(YEAR, player.birth, now()) as age, ' \
             'IFNULL(player_price.price,0), ' \
             'IFNULL(player_price.price_date, "2022-01-01"), ' \
             'IFNULL(player_price.currency_name, "EUR"), ' \
             'team.id_team, ' \
             'team.name as team_name, ' \
             'team.img as team_image, ' \
             'team_country.name as team_country, ' \
             'team_country.img as team_country_flag, ' \
             'tournament.id_tournament, ' \
             'tournament.name as tournament_name, ' \
             'tournament.img as tournament_image, ' \
             'tournament_country.name as tournament_country, ' \
             'tournament_country.img as tournament_country_flag, ' \
             'season.id_season, ' \
             'season.is_current, ' \
             'season.period, ' \
             'player_stat._90s, ' \
             'player_stat.rating, ' \
             'player_stat.game_started, ' \
             'player_stat.minutes, ' \
             'player_stat.yellow_card, ' \
             'player_stat.red_card, ' \
             'player_stat.goals, ' \
             'player_stat.assists, ' \
             'player_stat.expected_goals, ' \
             'player_stat.expected_non_penalty_goals, ' \
             'player_stat.expected_assists, ' \
             'player_stat.dribbles_pg_succ, ' \
             'player_stat.dribbles_perc_succ, ' \
             'player_stat.shots_pg, ' \
             'player_stat.shots_in_target_pg, ' \
             'player_stat.shots_acc_perc, ' \
             'player_stat.passes_pg, ' \
             'player_stat.passes_to_target_pg, ' \
             'player_stat.passes_acc_perc, ' \
             'player_stat.shot_creating_actions, ' \
             'player_stat.goal_creating_actions, ' \
             'player_stat.aerial_won_pg, ' \
             'player_stat.aerial_won_perc, ' \
             'player_stat.tackles_pg, ' \
             'player_stat.interceptions_pg, ' \
             'player_stat.blocked_shots_pg, ' \
             'player_position.GK, ' \
             'player_position.DL, ' \
             'player_position.DC, ' \
             'player_position.DR, ' \
             'player_position.DMC, ' \
             'player_position.ML, ' \
             'player_position.MC, ' \
             'player_position.MR, ' \
             'player_position.AML, ' \
             'player_position.AMC, ' \
             'player_position.AMR, ' \
             'player_position.FW ' \
             'FROM season ' \
             'LEFT JOIN tournament ON tournament.id_tournament = season.id_tournament ' \
             'LEFT JOIN country AS tournament_country ON tournament_country.id_country = tournament.id_country ' \
             'LEFT JOIN player_stat ON player_stat.id_season = season.id_season ' \
             'LEFT JOIN team ON team.id_team = player_stat.id_team ' \
             'LEFT JOIN tournament AS team_regular_tournament ON team_regular_tournament.id_tournament = team.id_tournament ' \
             'LEFT JOIN country AS team_country ON team_country.id_country = team_regular_tournament.id_country ' \
             'LEFT JOIN player ON player_stat.id_player = player.id_player ' \
             'LEFT JOIN player_position ON player_position.id_player = player.id_player ' \
             'LEFT JOIN country AS player_country ON player_country.id_country = player.id_country ' \
             'LEFT JOIN (SELECT player_price_history.id_player, player_price_history.date as price_date, player_price_history.id_team, player_price_history.price, player_price_history.currency_name FROM player_price_history WHERE date = (SELECT max(max_date.date) FROM player_price_history AS max_date WHERE max_date.id_player = player_price_history.id_player)) as player_price ON player_price.id_player = player_stat.id_player ' \
             'WHERE player.id_player IS NOT NULL) as main '


@router.get('/', response_model=PlayerResponseModel)
def main(request: Request,
         page: int = Query(1),
         sort_by: str = Query(default='main.rating'),
         desc: int = Query(default=1),
         session: Session = Depends(get_session)):

    query_params_list = get_validate_query_string_params(request.query_params._list)
    limit, offset = get_limit_and_offset(page)

    if len(query_params_list) != 0:

        sql_query_params = get_sql_query_by_params(query_params_list)
        total = session.execute("SELECT COUNT(*) FROM " + base_query + "WHERE " + sql_query_params).first()[0]
        if desc == 1:
            query = session.execute(
                "SELECT * FROM " + base_query + "WHERE " + sql_query_params + f' ORDER BY main.{sort_by} DESC LIMIT {limit} OFFSET {offset}').all()
            return get_player_response_model_data(query, total, limit, offset)
        else:
            query = session.execute(
                "SELECT * FROM " + base_query + "WHERE " + sql_query_params + f' ORDER BY main.{sort_by} LIMIT {limit} OFFSET {offset}').all()
            return get_player_response_model_data(query, total, limit, offset)

    else:
        total = session.execute("SELECT COUNT(*) FROM " + base_query).first()[0]
        if desc == 1:
            query = session.execute(
                "SELECT * FROM " + base_query + f' ORDER BY main.{sort_by} DESC LIMIT {limit} OFFSET {offset}').all()
            return get_player_response_model_data(query, total, limit, offset)
        else:
            query = session.execute(
                "SELECT * FROM " + base_query + f' ORDER BY main.{sort_by} LIMIT {limit} OFFSET {offset}').all()
            return get_player_response_model_data(query, total, limit, offset)
