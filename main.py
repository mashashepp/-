import asyncio

from zapr import Zapros
from schemes import Team
from schemes import Match
from schemes import Player

import os
from dotenv import load_dotenv

teams = []
team_otv = dict()
match = []
players = []
team_by_id_player = dict()


async def load_data():
    global teams, team_otv, match, players, team_by_id_player
    load_dotenv()

    Zap = Zapros(os.getenv("BASE_URL"), os.getenv("AUTH_TOKEN"))

    json_get = Zap.teams_zapros()
    for elem in json_get:
        teams.append(Team(elem['id'], elem['name'], elem['players']))

    sem = asyncio.Semaphore(10)

    async def get_players():
        global players, team_by_id_player
        tasks = []
        for elem in teams:
            team_id = elem.get_id()
            for player_id in elem.get_people():
                team_by_id_player[player_id] = team_id

                async def _process_player_data(p_id):
                    async with sem:
                        try:
                            json_ans = await Zap.players_id_zapros(p_id)
                            players.append(
                                Player(json_ans['id'], json_ans['name'], json_ans['surname'], json_ans['number']))
                        except TypeError as e:
                            print(f'Ошибка: {e}')
                        except Exception as e:
                            print(f'ошибка для игрока {p_id}: {e}')

                tasks.append(_process_player_data(player_id))
        await asyncio.gather(*tasks)
        await Zap.close_session()

    await get_players()

    json_get_1 = Zap.matches_zapros()

    for elem in json_get_1:
        match.append(Match(elem['id'], elem['team1'], elem['team2'], elem['team1_score'], elem['team2_score']))
    for elem in teams:
        team_otv[elem.get_name()] = elem.get_id()


def get_stats(s: list):
    name_k = " ".join(s[1:])[1:-1]
    cnt_win = 0
    cnt_loss = 0
    gol_yes = 0
    gol_no = 0
    id_k = team_otv.get(name_k)
    if id_k is None:
        print('0 0 0')
        return

    for elem in match:
        if elem.get_team1() == id_k:
            gol = elem.get_team1_score() - elem.get_team2_score()
            if gol > 0:
                cnt_win += 1
            elif gol < 0:
                cnt_loss += 1
            gol_yes += elem.get_team1_score()
            gol_no += elem.get_team2_score()
        elif elem.get_team2() == id_k:
            gol = elem.get_team2_score() - elem.get_team1_score()
            if gol > 0:
                cnt_win += 1
            elif gol < 0:
                cnt_loss += 1
            gol_yes += elem.get_team2_score()
            gol_no += elem.get_team1_score()
    if (gol_yes - gol_no) > 0:
        print(cnt_win, cnt_loss, str('+') + str(gol_yes - gol_no))
    else:
        print(cnt_win, cnt_loss, gol_yes - gol_no)


def get_versus(s):
    p_id_1 = int(s[1])
    p_id_2 = int(s[2])
    p_name_1 = team_by_id_player.get(p_id_1)
    p_name_2 = team_by_id_player.get(p_id_2)
    ans = 0
    if p_name_1 is None or p_name_2 is None or p_name_1 == p_name_2:
        print(0)
        return
    for elem in match:
        if (elem.get_team1() == p_name_1 and elem.get_team2() == p_name_2) or (
                elem.get_team1() == p_name_2 and elem.get_team2() == p_name_1):
            ans += 1
    print(ans)


async def main():
    global teams, team_otv, match, players, team_by_id_player

    await load_data()

    players.sort()
    for elem in players:
        print(elem.full_name())

    while True:
        s = input()
        if len(s)==0:
            continue
        s = s.split()
        if len(s) == 0:
            continue
        if s[0] == 'stats?':
            get_stats(s)
        elif s[0] == 'versus?':
            get_versus(s)


if __name__ == "__main__":
    asyncio.run(main())
