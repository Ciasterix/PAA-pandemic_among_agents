import random

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from agent import PandemicAgent


class PandemicModel(Model):

    def __init__(
            self,
            num_agents,
            num_sick,
            width,
            height,
            prob_no_symptoms,
            prob_symptoms,
            prob_hospitalization,
            prob_death,
            sick_time,
            time_to_quarantine,
            hospitalization_limit,
            vaccination,
            vaccination_delay,
            vaccination_rate
    ):
        super().__init__()
        self.num_agents = num_agents
        self.num_sick = num_sick
        self.grid = SingleGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.hospitalization_limit = hospitalization_limit

        self.vaccination = vaccination
        self._vaccination = False
        self.vaccination_delay = vaccination_delay
        self.vaccination_rate = vaccination_rate

        #  Create agents
        for i in range(self.num_agents):
            a = PandemicAgent(
                name=i,
                model=self,
                prob_no_symptoms=prob_no_symptoms,
                prob_symptoms=prob_symptoms,
                prob_hospital=prob_hospitalization,
                prob_death=prob_death,
                sick_time=sick_time,
                time_to_quarantine=time_to_quarantine
            )
            # Force infection of first >>num_sick<< agents
            if i < self.num_sick:
                a.infect(force=True)
            self.schedule.add(a)
            self.__place_randomly_on_grid(a)

        self.data_collector = DataCollector(
            model_reporters={"Sick": self.count_sick})

    def __place_randomly_on_grid(self, agent):
        self.grid.position_agent(agent)

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()
        if self.is_vaccination_launched():
            self.vaccinate()

    def is_below_the_limit_of_hospitalized(self):
        return self.count_hospitalized(None) < self.hospitalization_limit

    def count_sick(self, _):
        sick_agents = [a.is_sick() for a in self.schedule.agents]
        return sum(sick_agents) / len(self.schedule.agents)

    def count_hospitalized(self, _):
        sick_agents = [a.is_hospitalized() for a in self.schedule.agents]
        return sum(sick_agents) / len(self.schedule.agents)

    def count_vaccinated(self):
        vaccinated_agents = [a.is_vaccinated() for a in self.schedule.agents]
        return sum(vaccinated_agents) / len(self.schedule.agents)

    def count_one_type_of_agents(self, agent_type):
        agents = [a.state == agent_type for a in self.schedule.agents]
        return sum(agents) / len(self.schedule.agents)

    def start_vaccination(self):
        if self.vaccination:
            self._vaccination = True

    def is_vaccination_launched(self):
        if self._vaccination:
            return True
        elif self.schedule.steps > self.vaccination_delay:
            self.start_vaccination()
            return True
        return False

    def vaccinate(self):
        not_sick_agents = [
            a for a in self.schedule.agents
            if a.can_be_vaccinated()]
        agents_to_vaccinate = random.sample(
            not_sick_agents, min(len(not_sick_agents), self.vaccination_rate))
        for agent in agents_to_vaccinate:
            agent.vaccinate()
