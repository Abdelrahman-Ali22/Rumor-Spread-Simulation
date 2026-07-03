import matplotlib
matplotlib.use('TkAgg')  # makes the animation open in a separate PyCharm window

import numpy as np
import matplotlib.pyplot as plt
import random
from matplotlib.widgets import Slider, Button
from matplotlib.animation import FuncAnimation


# -----------------------------
# BASIC MODEL SETTINGS
# -----------------------------

num_agents = 80          # total number of employees
steps = 30               # number of simulation steps

spread_prob = 0.30       # chance that an unaware employee becomes a rumor spreader
resistant_prob = 0.20    # chance that an unaware employee rejects the rumor
recovery_prob = 0.08     # chance that a rumor spreader becomes resistant

spread_distance = 0.25   # distance needed for rumor spreading
max_contacts = 5         # maximum number of people one infected agent can contact in one step


# -----------------------------
# EMPLOYEE STATES
# -----------------------------

UNAWARE = 0              # employee has not heard the rumor
INFECTED = 1             # employee is spreading the rumor
RESISTANT = 2            # employee rejects/stops spreading the rumor


# -----------------------------
# GLOBAL VARIABLES
# -----------------------------

agents = None
x = None
y = None

history_unaware = []
history_infected = []
history_resistant = []

current_step = 0
animation = None


# -----------------------------
# RESET / CREATE SIMULATION
# -----------------------------

def reset_simulation(event=None):
    global agents, x, y
    global history_unaware, history_infected, history_resistant
    global current_step, animation

    current_step = 0

    history_unaware = []
    history_infected = []
    history_resistant = []

    agents = np.zeros(num_agents)

    # choose 5 initial rumor spreaders
    infected_people = random.sample(range(num_agents), 5)

    for i in infected_people:
        agents[i] = INFECTED

    # choose 10 initial resistant employees
    available_people = []

    for i in range(num_agents):
        if agents[i] != INFECTED:
            available_people.append(i)

    resistant_people = random.sample(available_people, 10)

    for i in resistant_people:
        agents[i] = RESISTANT

    # random positions inside a circle
    angles = np.random.rand(num_agents) * 2 * np.pi
    radius = np.sqrt(np.random.rand(num_agents))

    x = radius * np.cos(angles)
    y = radius * np.sin(angles)

    if animation is not None:
        animation.event_source.start()


# -----------------------------
# RESET WHEN SLIDER CHANGES
# -----------------------------

def slider_changed(value):
    reset_simulation()


# -----------------------------
# GET COLORS FOR EMPLOYEE STATES
# -----------------------------

def get_colors():
    colors = []

    for a in agents:

        if a == UNAWARE:
            colors.append("blue")

        elif a == INFECTED:
            colors.append("red")

        else:
            colors.append("green")

    return colors


# -----------------------------
# RUN ONE SIMULATION WITHOUT ANIMATION
# USED FOR SENSITIVITY ANALYSIS
# -----------------------------

def run_one_simulation(test_spread_prob, test_resistant_prob, test_recovery_prob, test_max_contacts):

    temp_agents = np.zeros(num_agents)

    # initial rumor spreaders
    infected_people = random.sample(range(num_agents), 5)

    for i in infected_people:
        temp_agents[i] = INFECTED

    # initial resistant employees
    available_people = []

    for i in range(num_agents):
        if temp_agents[i] != INFECTED:
            available_people.append(i)

    resistant_people = random.sample(available_people, 10)

    for i in resistant_people:
        temp_agents[i] = RESISTANT

    # random employee positions
    angles_temp = np.random.rand(num_agents) * 2 * np.pi
    radius_temp = np.sqrt(np.random.rand(num_agents))

    x_temp = radius_temp * np.cos(angles_temp)
    y_temp = radius_temp * np.sin(angles_temp)

    peak_infected = np.sum(temp_agents == INFECTED)
    rumor_duration = 0

    for step in range(steps):

        new_temp_agents = temp_agents.copy()

        # makes sure one unaware employee is affected only once in the same step
        affected_this_step = set()

        for i in range(num_agents):

            if temp_agents[i] == INFECTED:

                nearby_unaware = []

                for j in range(num_agents):

                    if temp_agents[j] == UNAWARE and j not in affected_this_step:

                        distance = np.sqrt(
                            (x_temp[i] - x_temp[j]) ** 2 +
                            (y_temp[i] - y_temp[j]) ** 2
                        )

                        if distance < spread_distance:
                            nearby_unaware.append(j)

                random.shuffle(nearby_unaware)

                selected_people = nearby_unaware[:test_max_contacts]

                for j in selected_people:

                    r = random.random()

                    if r < test_spread_prob:
                        new_temp_agents[j] = INFECTED

                    elif r < test_spread_prob + test_resistant_prob:
                        new_temp_agents[j] = RESISTANT

                    affected_this_step.add(j)

                # infected employee may recover and become resistant
                if random.random() < test_recovery_prob:
                    new_temp_agents[i] = RESISTANT

        temp_agents = new_temp_agents

        infected_count = np.sum(temp_agents == INFECTED)

        if infected_count > peak_infected:
            peak_infected = infected_count

        if infected_count > 0:
            rumor_duration = step + 1

        if infected_count == 0:
            break

    final_unaware = np.sum(temp_agents == UNAWARE)
    final_infected = np.sum(temp_agents == INFECTED)
    final_resistant = np.sum(temp_agents == RESISTANT)

    return final_unaware, final_infected, final_resistant, peak_infected, rumor_duration


# -----------------------------
# SENSITIVITY ANALYSIS
# COMPARISON: 5 REPETITIONS VS 10 REPETITIONS
# -----------------------------

def run_sensitivity_analysis(event=None):

    # compare these two numbers of repetitions
    repetition_tests = [5, 10]

    # test only rumor probability to keep the code faster
    spread_values = [0.10, 0.20, 0.30, 0.40, 0.50]

    base_resistant = resistant_slider.val
    base_recovery = recovery_slider.val
    base_contacts = int(contacts_slider.val)

    all_results = {}

    for repetitions in repetition_tests:

        results_spread = []
        peak_spread = []
        duration_spread = []

        for value in spread_values:

            final_infected_results = []
            peak_results = []
            duration_results = []

            for r in range(repetitions):

                result = run_one_simulation(
                    value,
                    base_resistant,
                    base_recovery,
                    base_contacts
                )

                final_infected_results.append(result[1])
                peak_results.append(result[3])
                duration_results.append(result[4])

            results_spread.append(np.mean(final_infected_results))
            peak_spread.append(np.mean(peak_results))
            duration_spread.append(np.mean(duration_results))

        all_results[repetitions] = {
            "final": results_spread,
            "peak": peak_spread,
            "duration": duration_spread
        }

    # -----------------------------
    # PLOT COMPARISON
    # -----------------------------

    fig_compare, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Plot 1: final rumor spreaders
    axs[0].plot(
        spread_values,
        all_results[5]["final"],
        marker="o",
        label="5 repetitions"
    )

    axs[0].plot(
        spread_values,
        all_results[10]["final"],
        marker="o",
        label="10 repetitions"
    )

    axs[0].set_title("Final Rumor Spreaders")
    axs[0].set_xlabel("Rumor Probability")
    axs[0].set_ylabel("Average Final Spreaders")
    axs[0].legend()

    # Plot 2: peak rumor spreaders
    axs[1].plot(
        spread_values,
        all_results[5]["peak"],
        marker="o",
        label="5 repetitions"
    )

    axs[1].plot(
        spread_values,
        all_results[10]["peak"],
        marker="o",
        label="10 repetitions"
    )

    axs[1].set_title("Peak Rumor Spreaders")
    axs[1].set_xlabel("Rumor Probability")
    axs[1].set_ylabel("Average Peak Spreaders")
    axs[1].legend()

    # Plot 3: rumor duration
    axs[2].plot(
        spread_values,
        all_results[5]["duration"],
        marker="o",
        label="5 repetitions"
    )

    axs[2].plot(
        spread_values,
        all_results[10]["duration"],
        marker="o",
        label="10 repetitions"
    )

    axs[2].set_title("Rumor Duration")
    axs[2].set_xlabel("Rumor Probability")
    axs[2].set_ylabel("Average Duration")
    axs[2].legend()

    fig_compare.suptitle(
        "Sensitivity Analysis: Comparison Between 5 and 10 Repetitions",
        fontsize=14
    )

    plt.tight_layout()
    plt.show()

    # -----------------------------
    # PRINT RESULTS
    # -----------------------------

    print("\nSensitivity Analysis: Comparison Between 5 and 10 Repetitions")
    print("------------------------------------------------------------")

    print("\nTested rumor probability values:")
    print(spread_values)

    print("\nAverage final rumor spreaders:")
    print("5 repetitions: ", all_results[5]["final"])
    print("10 repetitions:", all_results[10]["final"])

    print("\nAverage peak rumor spreaders:")
    print("5 repetitions: ", all_results[5]["peak"])
    print("10 repetitions:", all_results[10]["peak"])

    print("\nAverage rumor duration:")
    print("5 repetitions: ", all_results[5]["duration"])
    print("10 repetitions:", all_results[10]["duration"])

    print("\nConclusion:")
    print("10 repetitions usually gives smoother and more stable results than 5 repetitions.")
    print("5 repetitions is faster, but it is more affected by randomness.")


# -----------------------------
# CREATE MAIN FIGURE
# -----------------------------

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

plt.subplots_adjust(bottom=0.38)


# -----------------------------
# CREATE SLIDERS
# -----------------------------

ax_spread = plt.axes([0.20, 0.26, 0.65, 0.03])

spread_slider = Slider(
    ax=ax_spread,
    label="Rumor Probability",
    valmin=0.0,
    valmax=1.0,
    valinit=spread_prob
)

ax_resistant = plt.axes([0.20, 0.20, 0.65, 0.03])

resistant_slider = Slider(
    ax=ax_resistant,
    label="Resistance Probability",
    valmin=0.0,
    valmax=1.0,
    valinit=resistant_prob
)

ax_recovery = plt.axes([0.20, 0.14, 0.65, 0.03])

recovery_slider = Slider(
    ax=ax_recovery,
    label="Recovery Probability",
    valmin=0.0,
    valmax=1.0,
    valinit=recovery_prob
)

ax_contacts = plt.axes([0.20, 0.08, 0.65, 0.03])

contacts_slider = Slider(
    ax=ax_contacts,
    label="Max Contacts per Spreader",
    valmin=1,
    valmax=15,
    valinit=max_contacts,
    valstep=1
)


# -----------------------------
# CREATE BUTTONS
# -----------------------------

ax_reset = plt.axes([0.25, 0.01, 0.20, 0.04])
reset_button = Button(ax_reset, "Reset Simulation")

ax_sensitivity = plt.axes([0.55, 0.01, 0.30, 0.04])
sensitivity_button = Button(ax_sensitivity, "Sensitivity Analysis")


# -----------------------------
# UPDATE FUNCTION FOR ANIMATION
# -----------------------------

def update(frame):
    global agents
    global current_step
    global animation

    ax1.clear()
    ax2.clear()

    current_step += 1

    # read current slider values
    current_spread_prob = spread_slider.val
    current_resistant_prob = resistant_slider.val
    current_recovery_prob = recovery_slider.val
    current_max_contacts = int(contacts_slider.val)

    # update model
    new_agents = agents.copy()

    affected_this_step = set()

    for i in range(num_agents):

        if agents[i] == INFECTED:

            nearby_unaware = []

            for j in range(num_agents):

                if agents[j] == UNAWARE and j not in affected_this_step:

                    distance = np.sqrt(
                        (x[i] - x[j]) ** 2 +
                        (y[i] - y[j]) ** 2
                    )

                    if distance < spread_distance:
                        nearby_unaware.append(j)

            random.shuffle(nearby_unaware)

            selected_people = nearby_unaware[:current_max_contacts]

            for j in selected_people:

                r = random.random()

                if r < current_spread_prob:
                    new_agents[j] = INFECTED

                elif r < current_spread_prob + current_resistant_prob:
                    new_agents[j] = RESISTANT

                affected_this_step.add(j)

            if random.random() < current_recovery_prob:
                new_agents[i] = RESISTANT

    agents = new_agents

    # count states
    unaware_count = np.sum(agents == UNAWARE)
    infected_count = np.sum(agents == INFECTED)
    resistant_count = np.sum(agents == RESISTANT)

    history_unaware.append(unaware_count)
    history_infected.append(infected_count)
    history_resistant.append(resistant_count)

    # -----------------------------
    # LEFT PLOT: COMPANY SPACE
    # -----------------------------

    circle = plt.Circle((0, 0), 1, fill=False, linestyle="--")
    ax1.add_patch(circle)

    ax1.scatter(x, y, c=get_colors(), s=60)

    ax1.set_title(f"Rumor Spread Simulation - Step {current_step}")
    ax1.set_xlim(-1.1, 1.1)
    ax1.set_ylim(-1.1, 1.1)
    ax1.set_aspect("equal")

    ax1.set_xlabel("Company Space X")
    ax1.set_ylabel("Company Space Y")

    # -----------------------------
    # RIGHT PLOT: STATES OVER TIME
    # -----------------------------

    ax2.plot(history_unaware, label="Unaware employees", color="blue")
    ax2.plot(history_infected, label="Rumor spreaders", color="red")
    ax2.plot(history_resistant, label="Resistant employees", color="green")

    ax2.set_title("Employee States Over Time")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Number of Employees")
    ax2.set_ylim(0, num_agents)
    ax2.legend()

    ax2.text(
        0.02,
        0.95,
        f"Rumor probability = {current_spread_prob:.2f}\n"
        f"Resistance probability = {current_resistant_prob:.2f}\n"
        f"Recovery probability = {current_recovery_prob:.2f}\n"
        f"Max contacts per spreader = {current_max_contacts}",
        transform=ax2.transAxes,
        verticalalignment="top"
    )

    # stop conditions
    if current_step >= steps:
        ax2.set_title("Employee States Over Time - Simulation Finished")
        animation.event_source.stop()

    if infected_count == 0:
        ax2.set_title("Employee States Over Time - Rumor Disappeared")
        animation.event_source.stop()


# -----------------------------
# CONNECT BUTTONS AND SLIDERS
# -----------------------------

reset_button.on_clicked(reset_simulation)
sensitivity_button.on_clicked(run_sensitivity_analysis)

spread_slider.on_changed(slider_changed)
resistant_slider.on_changed(slider_changed)
recovery_slider.on_changed(slider_changed)
contacts_slider.on_changed(slider_changed)


# -----------------------------
# START SIMULATION
# -----------------------------

reset_simulation()
    
animation = FuncAnimation(
    fig,
    update,
    interval=600,
    cache_frame_data=False
)

plt.show()