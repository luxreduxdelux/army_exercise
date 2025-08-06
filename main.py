class Unit:
    """
    Unit. Can train to increase its strength, or transform to upgrade to the next unit type tier.
    """
    DEFAULT_UNIT_AGE : int = 18

    def __init__(self, age: int, unit_type):
        """
        Create an Unit instance, with given age and unit type.
        """

        self.age       = age
        self.strength  = unit_type.STRENGTH_FORCE
        self.unit_type = unit_type

    def get_age(self) -> int:
        """
        Get the age of the unit.
        """

        return self.age

    def get_strength(self) -> int:
        """
        Get the strength of the unit.
        """

        return self.strength

    def train(self, army):
        """
        Train an unit to increase its strength. May or may not actually train the unit depending on
        if enough gold is actually available to train the unit.
        """

        if army.gold_count  >= self.unit_type.TRAIN_STRENGTH_COST:
            army.gold_count -= self.unit_type.TRAIN_STRENGTH_COST
            self.strength   += self.unit_type.TRAIN_STRENGTH_GAIN

    def transform(self, army):
        """
        Transform an unit to its next tier. May or may not actually transform the unit depending on its
        current tier and if enough gold is available to actually transform the unit.
        """

        if self.unit_type.TRANSFORM_COST is not None and self.unit_type.TRANSFORM_UNIT is not None:
            if army.gold_count  >= self.unit_type.TRANSFORM_COST:
                army.gold_count -= self.unit_type.TRANSFORM_COST
                self.unit_type   = self.unit_type.TRANSFORM_UNIT

class Knight:
    STRENGTH_FORCE      : int  = 20
    TRAIN_STRENGTH_GAIN : int  = 10
    TRAIN_STRENGTH_COST : int  = 30
    TRANSFORM_COST      : None = None
    TRANSFORM_UNIT      : None = None

class Archer:
    STRENGTH_FORCE      : int = 10
    TRAIN_STRENGTH_GAIN : int = 7
    TRAIN_STRENGTH_COST : int = 20
    TRANSFORM_COST      : int = 40
    TRANSFORM_UNIT      : any = Knight

class Pikeman:
    STRENGTH_FORCE      : int = 5
    TRAIN_STRENGTH_GAIN : int = 3
    TRAIN_STRENGTH_COST : int = 10
    TRANSFORM_COST      : int = 30
    TRANSFORM_UNIT      : any = Archer

#================================================================

class Battle:
    """
    A battle, which can store an enemy army which we fought and the result of the battle (victory, failure, tie).
    """

    RESULT_VICTORY : int = 0
    RESULT_FAILURE : int = 1
    RESULT_TIE     : int = 2

    def __init__(self, army, result: int):
        """
        Create a new Battle instance.
        """

        self.army   = army
        self.result = result

#================================================================

class Army:
    """
    An army.
    """

    DEFAULT_COIN_COUNT       : int = 1000
    BATTLE_VICTORY_GOLD_GAIN : int = 100
    BATTLE_FAILURE_UNIT_LOSS : int = 2
    BATTLE_TIE_UNIT_LOSS     : int = 1
    BATTLE_TIE_GOLD_LOSS     : int = 50

    def __init__(self, pike_count: int, archer_count: int, knight_count: int):
        """
        Create a new Army instance, adding the given Pikeman/Archer/Knight count to the instance automatically.
        """

        self.gold_count     = self.DEFAULT_COIN_COUNT
        self.unit_array     = []
        self.battle_history = []

        # add pikemen.
        for x in range(0, pike_count):
            self.unit_array.append(Unit(Unit.DEFAULT_UNIT_AGE, Pikeman))

        # add archer.
        for x in range(0, archer_count):
            self.unit_array.append(Unit(Unit.DEFAULT_UNIT_AGE, Archer))

        # add knight.
        for x in range(0, knight_count):
            self.unit_array.append(Unit(Unit.DEFAULT_UNIT_AGE, Knight))

    def battle_army(self, army):
        """
        Battle another army, adding it to both our army and their army's battle history.
        """

        # get our and their strength level.
        self_stength : int = self.get_army_strength()
        them_stength : int = army.get_army_strength()

        # victory condition: our strength is greater than their strength.
        if self_stength > them_stength:
            self.battle_victory(army)
            army.battle_failure(self)
        # failure condition: the inverse.
        elif self_stength < them_stength:
            self.battle_failure(army)
            army.battle_victory(self)
        # tie condition: same strength level!
        else:
            self.battle_tie(army)
            self.battle_tie(army)

    def battle_victory(self, army):
        """
        The outcome of a won battle; gain gold.
        """

        # gain gold!
        self.gold_count += self.BATTLE_VICTORY_GOLD_GAIN

        # add a victory to your battle history.
        self.battle_history.append(Battle(army, Battle.RESULT_VICTORY))

    def battle_failure(self, army):
        """
        The outcome of a lost battle; the strongest and second strongest unit in your army will lost.
        """

        # lose as many {BATTLE_TIE_UNIT_LOSS} unit in your army.
        for x in range(0, self.BATTLE_FAILURE_UNIT_LOSS):
            # get the strongest unit.
            strongest_unit = self.get_army_strongest()

            # if there even is one, remove it.
            if strongest_unit is not None:
                self.unit_array.remove(strongest_unit)

        # add a loss to your battle history.
        self.battle_history.append(Battle(army, Battle.RESULT_FAILURE))

    def battle_tie(self, army):
        """
        The outcome of a tie in battle; lose the strong unit in your army, and lose some gold.
        """

        # lose as many {BATTLE_TIE_UNIT_LOSS} unit in your army.
        for x in range(0, self.BATTLE_TIE_UNIT_LOSS):
            # get the strongest unit.
            strongest_unit = self.get_army_strongest()

            # if there even is one, remove it.
            if strongest_unit is not None:
                self.unit_array.remove(strongest_unit)

        # lose some gold, if we have enough to deduct.
        if self.gold_count  >= self.BATTLE_TIE_GOLD_LOSS:
            self.gold_count -= self.BATTLE_TIE_GOLD_LOSS

        # add a tie to your battle history.
        self.battle_history.append(Battle(army, Battle.RESULT_TIE))

    def get_army_strength(self) -> int:
        """
        Get the total strength of an army.
        """

        i: int = 0

        for unit in self.unit_array:
            i += unit.get_strength()

        return i

    def get_army_strongest(self):
        """
        Get the strongest unit of an army.
        """

        unit_point_max = 0
        unit_which     = None

        for unit in self.unit_array:
            # get the strength of the current unit.
            current_unit_strength = unit.get_strength()

            # if its strength is greater than the current maximum...
            if current_unit_strength >= unit_point_max:
                # set as return unit.
                unit_point_max = current_unit_strength
                unit_which     = unit

        return unit_which

class Chinese(Army):
    """
    Chinese army.
    """

    DEFAULT_PIKEMAN_COUNT = 2
    DEFAULT_ARCHER_COUNT  = 25
    DEFAULT_KNIGHT_COUNT  = 2

    def __init__(self):
        """
        Create a Chinese army instance.
        """

        super().__init__(
            self.DEFAULT_PIKEMAN_COUNT,
            self.DEFAULT_ARCHER_COUNT,
            self.DEFAULT_KNIGHT_COUNT
        )

class British(Army):
    """
    British army.
    """

    DEFAULT_PIKEMAN_COUNT = 10
    DEFAULT_ARCHER_COUNT  = 10
    DEFAULT_KNIGHT_COUNT  = 10

    def __init__(self):
        """
        Create a British army instance.
        """

        super().__init__(
            self.DEFAULT_PIKEMAN_COUNT,
            self.DEFAULT_ARCHER_COUNT,
            self.DEFAULT_KNIGHT_COUNT
        )

class Byzantine(Army):
    """
    Byzantine army.
    """

    DEFAULT_PIKEMAN_COUNT = 5
    DEFAULT_ARCHER_COUNT  = 8
    DEFAULT_KNIGHT_COUNT  = 15

    def __init__(self):
        """
        Create a Byzantine army instance.
        """

        super().__init__(
            self.DEFAULT_PIKEMAN_COUNT,
            self.DEFAULT_ARCHER_COUNT,
            self.DEFAULT_KNIGHT_COUNT
        )