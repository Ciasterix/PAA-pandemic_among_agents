from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

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
            hospitalization_limit
    ):
        super().__init__()
        self.num_agents = num_agents
        self.num_sick = num_sick
        # TODO Change to mesa.space.SingleGrid
        # which strictly enforces one object per cell
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.hospitalization_limit = hospitalization_limit

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
            )
            # Force infection of first >>num_sick<< agents
            if i < self.num_sick:
                a.infect(force=True)
            self.schedule.add(a)
            self.__place_randomly_on_grid(a)

        self.data_collector = DataCollector(
            model_reporters={"Sick": self.compute_sick})

    # TODO Place only in unique cells
    def __place_randomly_on_grid(self, agent):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        self.grid.place_agent(agent, (x, y))

    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()

    def compute_sick(self, _):  # TODO check if parameter can be deleted
        sick_agents = [a.is_sick() for a in self.schedule.agents]
        return sum(sick_agents) / len(self.schedule.agents)