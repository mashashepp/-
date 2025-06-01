class Team:
    def __init__(self, id: int, name: str, people: list[int]):
        self.__id = id
        self.__name = name
        self.__people = people

    def get_people(self) -> list[int]:
        return self.__people

    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

class Match:
    def __init__(self, id: int, team1: int, team2: int, team1_score: int, team2_score: int):
        self.__id = id
        self.__team1 = team1
        self.__team2 = team2
        self.__team1_score = team1_score
        self.__team2_score = team2_score

    def get_team1(self) -> int:
        return self.__team1

    def get_team2(self) -> int:
        return self.__team2

    def get_team1_score(self) -> int:
        return self.__team1_score

    def get_team2_score(self) -> int:
        return self.__team2_score


class Player:
    def __init__(self, id_player: int, name: str, surname: str, number: int):
        self.__id = id_player
        self.__name = name
        self.__surname = surname
        self.__number = number

    def get_id(self) -> int:
        return self.__id

    def full_name(self) -> str:
      return f"{self.__name} {self.__surname}".strip()

    def __lt__(self, other) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        if self.full_name() == other.full_name():
            return self.__id < other.__id
        return self.full_name() < other.full_name()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.__id == other.__id

    def __hash__(self) -> int:
        return hash(self.__id)
