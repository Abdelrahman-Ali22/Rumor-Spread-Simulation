# Agent-Based Rumor Spread Simulation

## Project Overview

This project performs an agent-based simulation of rumor spreading inside a company. The main focus of the simulation is to show how a rumor can spread between employees through local interactions, probability based decisions and random contact patterns.

Employees are represented as individual agents located inside a circular company space. Each employee can be in one of three states: unaware, rumor spreader or resistant.

The project was completed as part of the Business Simulations assignment. The simulation includes animation, interactive sliders, a reset button, sensitivity analysis, and comparison between 5 and 10 simulation repetitions.

## Assignment Objective

The main objective of the assignment is to build a working agent-based model and explain how individual employee behavior can create a larger organizational pattern.

The required simulation includes:

- Employee agents
- Different employee states
- Local interaction between employees
- Probability-based rumor spreading
- Resistance and recovery behavior
- Animated visualization
- Interactive sliders
- Reset simulation option
- Sensitivity analysis
- Comparison between 5 and 10 repetitions
- Interpretation of model behavior and results

## Simulation Idea

The model simulates rumor spreading inside a company.

At the beginning of the simulation:

- Some employees are unaware of the rumor
- Some employees are already spreading the rumor
- Some employees are resistant to the rumor

During each simulation step, rumor spreaders can contact nearby unaware employees. A contacted employee may become a rumor spreader, become resistant, or remain unaware depending on probability rules.

The goal is to observe how the number of unaware, spreading, and resistant employees changes over time.

## Employee States

| State | Code | Color | Description |
|---|---:|---|---|
| Unaware | 0 | Blue | The employee has not heard the rumor or is not spreading it |
| Rumor Spreader | 1 | Red | The employee is actively spreading the rumor |
| Resistant | 2 | Green | The employee rejects the rumor or stopped spreading it |

## Technologies Used

The project was implemented in Python using the following libraries:

- numpy
- matplotlib
- random

Matplotlib is used for the animation, graphs, sliders, and buttons. NumPy is used for array operations and employee position calculations. The random library is used for random decisions in the simulation.

## Project Workflow

## 1. Import Libraries

The project starts by importing the required Python libraries:

```python
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import random
```

Matplotlib is also set to use the TkAgg backend so the animation opens in a separate window when running the code in PyCharm.

## 2. Define Basic Model Settings

The main simulation settings are defined at the beginning of the code:

| Parameter | Value | Description |
|---|---:|---|
| `num_agents` | 80 | Total number of employees |
| `steps` | 30 | Maximum number of simulation steps |
| `spread_prob` | 0.30 | Probability that an unaware employee becomes a rumor spreader |
| `resistant_prob` | 0.20 | Probability that an unaware employee rejects the rumor |
| `recovery_prob` | 0.08 | Probability that a rumor spreader becomes resistant |
| `spread_distance` | 0.25 | Maximum distance for rumor spreading |
| `max_contacts` | 5 | Maximum number of employees one spreader can contact in one step |

## 3. Create Employee States

The model uses three employee states:

```python
UNAWARE = 0
INFECTED = 1
RESISTANT = 2
```

These constants make the code easier to understand and help assign colors to employees in the visualization.

## 4. Reset and Initialize the Simulation

The reset function starts a new simulation.

It performs the following steps:

- Clears previous simulation history
- Creates 80 employees
- Sets all employees as unaware
- Randomly selects 5 employees as initial rumor spreaders
- Randomly selects 10 employees as initially resistant
- Places all employees randomly inside a circular company space

This allows each simulation run to start with different random positions and different initial employees.

## 5. Company Space

The company is represented as a circular space.

Employees are placed randomly inside the circle. The circle does not represent a real office layout, but it is used to show which employees are close enough to interact.

Employees who are closer than the spread distance can affect each other.

## 6. Rumor Spreading Logic

At each simulation step, the model checks every rumor spreader.

For each rumor spreader:

1. The model finds nearby unaware employees.
2. It randomly selects a limited number of contacts.
3. Each contacted employee is tested using probability rules.
4. The contacted employee may become a rumor spreader, become resistant, or stay unaware.
5. The rumor spreader may also recover and become resistant.

The main probability logic is:

```python
r = random.random()

if r < current_spread_prob:
    new_agents[j] = INFECTED

elif r < current_spread_prob + current_resistant_prob:
    new_agents[j] = RESISTANT
```

A current rumor spreader can also stop spreading:

```python
if random.random() < current_recovery_prob:
    new_agents[i] = RESISTANT
```

## 7. Visualization

The simulation window contains two main plots.

| Plot | Description |
|---|---|
| Company space plot | Shows employees inside the circular company space |
| State over time graph | Shows how the number of unaware, rumor spreader, and resistant employees changes over time |

The colors are:

- Blue = unaware employees
- Red = rumor spreaders
- Green = resistant employees

## 8. Interactive Sliders

The simulation includes four sliders:

| Slider | Purpose |
|---|---|
| Rumor Probability | Controls how easily the rumor spreads |
| Resistance Probability | Controls how often employees reject the rumor |
| Recovery Probability | Controls how often rumor spreaders stop spreading |
| Max Contacts per Spreader | Controls how many employees one spreader can contact in one step |

Changing a slider restarts the simulation with the new parameter value.

## 9. Reset Button

The reset button restarts the simulation.

When the button is clicked:

- Employee states are reset
- New random employees are selected as initial spreaders and resistant employees
- New random positions are created
- The simulation starts again from step 0

## 10. Sensitivity Analysis

The project includes a sensitivity analysis function.

Sensitivity analysis means changing one input parameter and observing how the output changes.

In this project, the tested parameter is rumor probability.

The tested rumor probability values are:

```text
0.10, 0.20, 0.30, 0.40, 0.50
```

The analysis compares:

- 5 repetitions
- 10 repetitions

For each value, the model calculates average results for:

- Final rumor spreaders
- Peak rumor spreaders
- Rumor duration

## 11. Sensitivity Analysis Purpose

The purpose of the sensitivity analysis is to show how randomness affects the results.

Because this is an agent based model, one simulation run may not represent the general behavior. Random positions, random initial spreaders, random contacts, and random recovery decisions can all affect the final result.

Using more repetitions gives smoother and more reliable average results.

## 12. Main Results

The simulation shows that higher rumor probability usually increases the peak number of rumor spreaders.

This means that when employees are more likely to believe and spread the rumor, the rumor reaches more people at its highest point.

However, the final number of rumor spreaders does not always increase perfectly. This happens because the model includes randomness, resistance, and recovery.

Some employees may reject the rumor or stop spreading it, which can reduce the final number of active rumor spreaders.

## 13. Interpretation

The model demonstrates an important idea in agent-based modeling:

Small local decisions can create large global patterns.

Each employee follows simple rules, but the total company-level result can show different behaviors, such as:

- Fast rumor growth
- Slow rumor growth
- A peak followed by decline
- Rumor disappearance
- Growth of resistant employees

This shows how individual behavior can affect the whole organization.

## How to Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repository-name.git
```

## 2. Open the Project Folder

```bash
cd your-repository-name
```

## 3. Install the Required Libraries

```bash
pip install numpy matplotlib
```

## 4. Run the Python File

If your file is named `rumor_spread_simulation.py`, run:

```bash
python rumor_spread_simulation.py
```

If your file is still named `BS Project.py`, run:

```bash
python "BS Project.py"
```

## 5. Use the Simulation

After running the file, a simulation window will open.

You can:

- Watch the rumor spread animation
- Change the sliders
- Restart the simulation using the reset button
- Run sensitivity analysis using the sensitivity analysis button

## Repository Structure

```text
.
├── rumor_spread_simulation.py
├── Report.pdf
└── README.md
```

If the original Python file name is not changed, the structure may be:

```text
.
├── BS Project.py
├── Report.pdf
└── README.md
```

## Main Features

- Agent-based model
- Animated company space visualization
- Employee state graph over time
- Interactive sliders
- Reset button
- Sensitivity analysis button
- Comparison between 5 and 10 repetitions
- Probability-based behavior
- Distance-based interaction
- Clear visual states using colors

## Possible Future Improvements

Possible improvements for this project include:

- Add employee movement
- Create departments or groups
- Use a communication network instead of physical distance
- Give employees different trust levels
- Give employees different influence levels
- Test more parameters in sensitivity analysis
- Increase repetitions to 20 or 30
- Save sensitivity results automatically to a CSV file
- Add a graphical start menu
- Export final graphs automatically

## Conclusion

This project demonstrates a complete agent-based rumor spreading simulation using Python.

The simulation starts with individual employees and simple behavior rules. Through local interactions, the model creates a larger pattern showing how a rumor spreads, peaks, declines, or disappears inside a company.

The sensitivity analysis shows that increasing rumor probability usually increases the peak number of rumor spreaders. It also shows that 10 repetitions are usually more stable than 5 repetitions because they reduce the effect of randomness.

Overall, the project shows how agent based modeling can be used to understand organizational behavior and how small individual decisions can create important company-level outcomes.

