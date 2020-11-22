from enum import Enum

from mesa import Agent


class SickType(Enum):
    HEALTHY = 0
    NO_SYMPTOMS = 1
    SYMPTOMS = 2
    HOSPITALIZATION = 3
    RECOVERED = 4
    DEAD = 5


class PandemicAgent(Agent):
    def __init__(self, name, model, prob_no_symptoms, prob_symptoms,
                 prob_hospital, prob_death, sick_time):
        super().__init__(name, model)
        self.name = name  # TODO Check if line can be deleted

        self.prob_no_symptoms = prob_no_symptoms
        self.prob_symptoms = prob_symptoms
        self.prob_hospital = prob_hospital
        self.prob_death = prob_death
        self.sick_time = sick_time

        self.sickness = SickType.HEALTHY
        self.remaining_sick_time = 0

    def __move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        self.__move()
        if self.is_sick():
            self.decrease_sick_time()
            neighbours = self.model.grid.get_neighbors(
                self.pos,
                moore=True,
                include_center=False
            )
            for n in neighbours:
                n.infect()

    def decrease_sick_time(self):  # TODO Find better name for this function
        self.remaining_sick_time = max(self.remaining_sick_time - 1, 0)
        if self.remaining_sick_time == 0:
            self.sickness = SickType.RECOVERED

    def is_sick(self):
        return (self.sickness == SickType.NO_SYMPTOMS or
                self.sickness == SickType.SYMPTOMS or
                self.sickness == SickType.HOSPITALIZATION)

    def was_sick(self):
        return (self.sickness == SickType.RECOVERED or
                self.sickness == SickType.DEAD)

    def infect(self, force=False):  # TODO Maybe there is a better name
        if force:
            self.sickness = SickType.NO_SYMPTOMS
            self.remaining_sick_time = self.sick_time
        elif not self.is_sick() and not self.was_sick():
            rand_val = self.model.random.uniform(0, 1)
            if rand_val < self.prob_no_symptoms:
                self.sickness = SickType.NO_SYMPTOMS
            elif rand_val < self.prob_no_symptoms + self.prob_symptoms:
                self.sickness = SickType.SYMPTOMS
            elif rand_val < (self.prob_no_symptoms +
                             self.prob_symptoms + self.prob_hospital):
                self.sickness = SickType.HOSPITALIZATION
            self.remaining_sick_time = self.sick_time
