from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules.ChartVisualization import ChartModule
from mesa.visualization.modules import TextElement

from model import PandemicModel
from agent import SickType


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
                 "r": 0.5}

    # HTML color names: https://www.w3schools.com/colors/colors_names.asp
    if agent.sickness == SickType.HEALTHY:
        portrayal["Color"] = "Chartreuse"  # green
        portrayal["Layer"] = 1
    if agent.sickness == SickType.NO_SYMPTOMS:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 0
    elif agent.sickness == SickType.SYMPTOMS:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
    elif agent.sickness == SickType.HOSPITALIZATION:
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 1
    elif agent.sickness == SickType.RECOVERED:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
    elif agent.sickness == SickType.DEAD:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
    return portrayal


model_params = {
    # "N": UserSettableParameter("checkbox", "Grass Enabled", True),
    "num_agents": UserSettableParameter(
        "slider", "Number of agents", 20, 1, 625
    ),
    "num_sick": UserSettableParameter(
            "slider", "Number of agents SIck from the beginning", 1, 1, 625
    ),
    "width": UserSettableParameter("slider", "Grid Width", 25, 5, 25),
    "height": UserSettableParameter("slider", "Grid Height", 25, 5, 25),

    "sick_time": UserSettableParameter(
        "slider", "Sickness time", 20, 1, 100
    ),
    "prob_no_symptoms": UserSettableParameter(
        "slider", "Probability of sickness without symptoms", 0.1, 0.1, 1.0, 0.1
    ),
    "prob_symptoms": UserSettableParameter(
        "slider", "Probability of sickness with symptoms", 0.1, 0.1, 1.0, 0.1
    ),
    "prob_hospitalization": UserSettableParameter(
        "slider", "Probability of hospitalization", 0.1, 0.1, 1.0, 0.1
    ),
    "prob_death": UserSettableParameter(
        "slider", "Probability of death", 0.1, 0.1, 1.0, 0.1
    ),
    "hospitalization_limit": UserSettableParameter(
        "slider", "Maximum number of hospitalizations", 50, 10, 300
    )
}

chart = ChartModule(
    [{"Label": "Sick", "Color": "Black"}],
    data_collector_name='data_collector')

grid = CanvasGrid(agent_portrayal, 25, 25, 500, 500)

server = ModularServer(
    PandemicModel, [grid, chart], "Pandemic Model", model_params)
