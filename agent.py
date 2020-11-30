from enum import Enum

from mesa import Agent


class State(Enum):
    HEALTHY = 0
    NO_SYMPTOMS = 1
    SYMPTOMS = 2
    QUARANTINED = 3
    HOSPITALIZATION = 4
    RECOVERED = 5
    VACCINATED = 6
    DEAD = 7


class PandemicAgent(Agent):
    def __init__(
            self,
            name,
            model,
            prob_no_symptoms,
            prob_symptoms,
            prob_hospital,
            prob_death,
            sick_time,
            time_to_quarantine,
            time_before_death):
        super().__init__(name, model)

        self.prob_no_symptoms = prob_no_symptoms
        self.prob_symptoms = prob_symptoms
        self.prob_hospital = prob_hospital
        self.prob_death = prob_death
        self.sick_time = sick_time
        self.time_to_quarantine = time_to_quarantine
        self.time_before_death = time_before_death

        self.state = State.HEALTHY
        self.remaining_sick_time = 0
        self.countdown_to_quarantine = 0
        self.direction = self.random.choice(list(range(8)))

    def __move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False)

        if self.model.grid.is_cell_empty(possible_steps[self.direction]):
            self.model.grid.move_agent(self, possible_steps[self.direction])
        else:
            random_ids = self.random.sample(list(range(8)), k=8)
            for ri in random_ids:
                if self.model.grid.is_cell_empty(possible_steps[ri]):
                    self.direction = ri
                    self.model.grid.move_agent(self, possible_steps[ri])

    def step(self):
        if self.can_move():
            self.__move()
        if self.can_die():
            self.__see_whether_dies()
        if self.can_be_quarantined():
            self.__see_whether_goes_to_quarantine()
        if self.can_infect_others():
            neighbours = self.model.grid.get_neighbors(
                self.pos, moore=True, include_center=False)
            for n in neighbours:
                n.infect()
        if self.is_sick():
            self.__see_whether_sickness_ends()

    def __see_whether_sickness_ends(self):
        self.remaining_sick_time = max(self.remaining_sick_time - 1, 0)
        if self.remaining_sick_time == 0:
            self.state = State.RECOVERED

    def __see_whether_goes_to_quarantine(self):
        self.countdown_to_quarantine = max(self.countdown_to_quarantine - 1, 0)
        if self.state == State.SYMPTOMS:
            if self.countdown_to_quarantine == 0:
                self.state = State.QUARANTINED

    def __see_whether_dies(self):
        rand_val = self.model.random.uniform(0, 1)
        if rand_val < self.prob_death:
            self.state = State.DEAD

    def is_sick(self):
        return (self.state == State.NO_SYMPTOMS or
                self.state == State.SYMPTOMS or
                self.state == State.QUARANTINED or
                self.state == State.HOSPITALIZATION)

    def is_vaccinated(self):
        return self.state == State.VACCINATED

    def was_sick(self):
        return (self.state == State.RECOVERED or
                self.state == State.DEAD)

    def can_infect_others(self):
        return (self.state == State.NO_SYMPTOMS or
                self.state == State.SYMPTOMS)

    def can_be_infected(self):
        return (not self.is_sick() and
                not self.was_sick() and
                not self.is_vaccinated())

    def can_move(self):
        return not (self.state == State.QUARANTINED or
                    self.state == State.HOSPITALIZATION or
                    self.state == State.DEAD)

    def can_die(self):
        return ((self.state == State.SYMPTOMS or
                self.state == State.QUARANTINED or
                self.state == State.HOSPITALIZATION) and
                self.time_before_death == self.remaining_sick_time)

    def can_be_vaccinated(self):
        return (not self.is_sick() and
                not self.was_sick() and
                not self.state == State.VACCINATED)

    def is_hospitalized(self):
        return self.state == State.HOSPITALIZATION

    def can_be_quarantined(self):
        return self.state == State.SYMPTOMS

    def infect(self, force=False):
        if force:
            self.state = State.NO_SYMPTOMS
            self.remaining_sick_time = self.sick_time
        elif self.can_be_infected():
            rand_val = self.model.random.uniform(0, 1)
            if rand_val < self.prob_no_symptoms:
                self.state = State.NO_SYMPTOMS
            elif rand_val < self.prob_no_symptoms + self.prob_symptoms:
                self.state = State.SYMPTOMS
                self.countdown_to_quarantine = self.time_to_quarantine
            elif rand_val < (self.prob_no_symptoms + self.prob_symptoms
                             + self.prob_hospital):
                if self.model.is_below_the_limit_of_hospitalized():
                    self.state = State.HOSPITALIZATION
                else:
                    self.state = State.DEAD
            self.remaining_sick_time = self.sick_time

    def vaccinate(self):
        self.state = State.VACCINATED
