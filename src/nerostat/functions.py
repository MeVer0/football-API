def get_player_response_model_data(table, total, limit, offset):
    """
    Функция для приведения данных из запроса SQL в формат валидируемый моделью
    Pydantic в которой мы возвращаем ответ конечному пользователю
    :param table: таблица которую мы получаем из запроса к базе данных об игроке/игроках
    :param total: параметр для вывода информации о пагинации - число строк в получаемой таблице
    :param limit: параметр для вывода информации о пагинации - число допустимых к выводу строк
    :param offset: параметр для вывода информации о пагинации - число пропущенных строк
    :return: формат данных который можно провалидировать моделью пайдантика, в которой
    мы возвращаем данные конечному пользователю
    """
    value_list = []
    for table_row in table:
        new_table_row = {"player": {"id_player": table_row[0],
                                    "nationality": table_row[1],
                                    "player_name": table_row[2],
                                    "player_image": table_row[3],
                                    "player_country": table_row[4],
                                    "player_country_flag": table_row[5],
                                    "shirt_number": table_row[6],
                                    "weight": table_row[7],
                                    "height": table_row[8],
                                    "birth": table_row[9],
                                    "age": table_row[10]
                                    },
                         "player_price": {
                             "player_price": table_row[11],
                             "info_update_date": table_row[12],
                             "currency": table_row[13]
                         },
                         "player_team": {
                             "id_team": table_row[14],
                             "team_name": table_row[15],
                             "team_image": table_row[16],
                             "team_country": table_row[17],
                             "team_country_flag": table_row[18]
                         },
                         "player_tournament": {
                             "id_tournament": table_row[19],
                             "tournament_name": table_row[20],
                             "tournament_image": table_row[21],
                             "tournament_country": table_row[22],
                             "tournament_country_flag": table_row[23]
                         },
                         "player_season": {
                             "id_season": table_row[24],
                             "is_current": table_row[25],
                             "period": table_row[26]
                         },
                         "player_stat": {
                             "_90s": table_row[27],
                             'rating': table_row[28],
                             'game_started': table_row[29],
                             'minutes': table_row[30],
                             'yellow_card': table_row[31],
                             'red_card': table_row[32],
                             'goals': table_row[33],
                             'assists': table_row[34],
                             'expected_goals': table_row[35],
                             'expected_non_penalty_goals': table_row[36],
                             'expected_assists': table_row[37],
                             'dribbles_pg_succ': table_row[39],
                             'dribbles_perc_succ': table_row[39],
                             'shots_pg': table_row[40],
                             'shots_in_target_pg': table_row[41],
                             'shots_acc_perc': table_row[42],
                             'passes_pg': table_row[43],
                             'passes_to_target_pg': table_row[44],
                             'passes_acc_perc': table_row[45],
                             'shot_creating_actions': table_row[46],
                             'goal_creating_actions': table_row[47],
                             'aerial_won_pg': table_row[48],
                             'aerial_won_perc': table_row[49],
                             'tackles_pg': table_row[50],
                             'interceptions_pg': table_row[51],
                             'blocked_shots_pg': table_row[52],
                         },

                         "player_positions": {
                             'GK': table_row[53],
                             'DL': table_row[54],
                             'DC': table_row[55],
                             'DR': table_row[56],
                             'DMC': table_row[57],
                             'ML': table_row[58],
                             'MC': table_row[59],
                             'MR': table_row[60],
                             'AML': table_row[61],
                             'AMC': table_row[62],
                             'AMR': table_row[63],
                             'FW': table_row[64],
                         },
                         }

        value_list.append(new_table_row)

    return {"players": value_list,
            "total": total,
            "limit": limit,
            "offset": offset
            }


def get_validate_query_string_params(params):
    """
    Функция для валидации параметров передаваемых в query_string. Она создает новых список из параметров в котором
     не будет специальных параметров и добавит приставку 'main.' в начале каждого параметра, т.к это необходимо для
    формирования конечного SQL запроса.
    :param params: список параметров передаваемых в query_string
    :return: список исключающий специальные параметры и с приставкой 'main.' для каждого параметра.
    """
    special_params = ("page", "sort_by", "desc")
    res = []
    for one_param in params:
        param_name, param_value = one_param
        if param_name not in special_params:
            res.append((f"main.{param_name}", param_value))
    return res


def get_equally_param(param):
    """
    :param param:  параметр вида: ("main.nationality", "1,2") или ("main.nationality",1")
    :return: ("main.nationality=1,2") => "nationality = 1 AND nationality = 2"
             ("main.nationality",1") => "main.nationality = 1
    """
    param_name, values = param
    query_list = [f"{param_name} = {v}" for v in values.split(',')]
    sql_query_string = ' OR '.join(query_list)
    return sql_query_string


def get_more_less_param(param):
    """
    :param param: параметр вида: "main.nationality_from=2" или "main.nationality_to=1" передаваемый в query_string
    :return: "main.nationality_from=2" => "main.nationality_from>=2"
    """
    param_name, value = param
    if '_from' in param_name:
        return f"{param_name.replace('_from', '')} >= {value}"
    elif '_to' in param_name:
        return f"{param_name.replace('_to', '')} <= {value}"
    return


def get_sql_query_by_params(params_list):
    """
    Функция для получения части SQL-запроса после 'WHERE'.
    :param params_list: список параметров из которых составляют SQL-запрос.
    Пример: [("main.nationality", "1,2"), ("main.weight_to", 100)]
    :return: Из примера: main.nationality = 1 AND main.nationality = 2 AND main.weight <= 100
    """
    sql_query_list = [get_more_less_param(param) if param[0].endswith('_to') or param[0].endswith('_from')
                        else get_equally_param(param) for param in params_list]
    sql_query = ' AND '.join(sql_query_list)
    return sql_query


def get_limit_and_offset(page):
    limit = page * 20
    offset = (page - 1) * 20
    return limit, offset