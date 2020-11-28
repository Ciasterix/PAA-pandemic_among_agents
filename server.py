from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules.ChartVisualization import ChartModule

from agent import State
from model import PandemicModel


# TODO create element to show number of agent of each type
# class CustomTextElement(TextElement):
#     """
#     Display a text count of how many happy agents there are.
#     """
#
#     def __init__(self, data_collector_name='data_collector'):
#         pass
#
#     def render(self, model):
#         return "Happy agents: " + str(model.happy)


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.6,
                 "Layer": 1}

    # HTML color names: https://www.w3schools.com/colors/colors_names.asp
    if agent.state == State.HEALTHY:
        portrayal["Color"] = "Chartreuse"  # light green
    elif agent.state == State.NO_SYMPTOMS:
        portrayal["Color"] = "orange"
    elif agent.state == State.SYMPTOMS:
        portrayal["Color"] = "red"
    elif agent.state == State.QUARANTINED:
        portrayal["Color"] = "yellow"
    elif agent.state == State.HOSPITALIZATION:
        portrayal["Color"] = "purple"
    elif agent.state == State.RECOVERED:
        portrayal["Color"] = "cyan"
    elif agent.state == State.DEAD:
        portrayal["Color"] = "grey"
    elif agent.state == State.VACCINATED:
        portrayal["Color"] = "DarkGreen"

    return portrayal


model_params = {
    # "N": UserSettableParameter("checkbox", "Grass Enabled", True),
    "num_agents": UserSettableParameter(
        "slider", "Number of agents", 50, 1, 625
    ),
    "num_sick": UserSettableParameter(
        "slider", "Number of agents sick from the beginning", 1, 1, 625
    ),
    "width": UserSettableParameter("slider", "Grid Width", 25, 5, 25),
    "height": UserSettableParameter("slider", "Grid Height", 25, 5, 25),
    "sick_time": UserSettableParameter(
        "slider", "Sickness time", 20, 1, 50
    ),
    "time_to_quarantine": UserSettableParameter(
        "slider", "Time before someone is quarantined", 10, 0, 50
    ),
    "prob_no_symptoms": UserSettableParameter(
        "slider", "Probability of infection without symptoms", 0.1, 0.0, 1.0, 0.01
    ),
    "prob_symptoms": UserSettableParameter(
        "slider", "Probability of infection with symptoms", 0.1, 0.0, 1.0, 0.01
    ),
    "prob_hospitalization": UserSettableParameter(
        "slider", "Probability of hospitalization", 0.1, 0.0, 1.0, 0.01
    ),
    "prob_death": UserSettableParameter(
        "slider", "Probability of death", 0.1, 0.0, 1.0, 0.01
    ),
    "hospitalization_limit": UserSettableParameter(
        "slider", "Maximum number of hospitalizations", 5, 0, 100
    ),
    "vaccination": UserSettableParameter(
        "checkbox", "Vaccination Enabled", True
    ),
    "vaccination_delay": UserSettableParameter(
        "slider", "Delay of the Vaccine lunch", 200, 0, 1000
    ),
    "vaccination_rate": UserSettableParameter(
        "slider", "Rate of the vaccination", 10, 0, 100
    )

}

chart = ChartModule(
    [{"Label": "Sick", "Color": "Black"}],
    data_collector_name='data_collector')

grid = CanvasGrid(agent_portrayal, 25, 25, 500, 500)

server = ModularServer(
    PandemicModel, [grid, chart], "Pandemic Model", model_params)
