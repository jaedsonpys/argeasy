class InvalidArgumentUseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidFlagUseError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidActionError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
