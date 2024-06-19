from vi import Agent, Simulation
from vi.config import Config
import random



class Rabbit(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def update(self):
        # Probability of reproduction
        if random.random() < 0.001:
            self.reproduce()


class Fox(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.energy = 100  # Initial energy level

        

    def update(self):
        rabbit = (
            self.in_proximity_accuracy()
            .without_distance()
            .filter_kind(Rabbit) 
            .first()
        )
        
        # Killing the rabbit
        if rabbit is not None:
            rabbit.kill()
            self.reproduce()
            self.energy += 20  # Gain energy after eating


        
        # Chance to die if energy is too low
        if self.energy <= 0:
            self.kill()

        
        # Energy consumption over time
        self.energy -= 0.3


class FoxesRabbits(Simulation):
    def __init__(self):
        super().__init__(Config(radius=120))
        self.time_step = 0
    def before_update(self):
        super().before_update()
        
        # Count rabbits and foxes
        rabbit_count = 0
        fox_count = 0
        
        for agent in self._agents:
            if isinstance(agent, Rabbit):
                rabbit_count += 1
            elif isinstance(agent, Fox):
                fox_count += 1
        
        # Print counts every 100 time steps
        if self.time_step % 100 == 0:
            print(f"Time step: {self.time_step}")
            print(f"Rabbit count: {rabbit_count}")
            print(f"Fox count: {fox_count}")
            print("--------------------")
        
        self.time_step += 1

    def after_update(self):
        super().after_update()

# Batch spawning agents
simulation = FoxesRabbits()
simulation.batch_spawn_agents(
    10,
    Rabbit,
    images=["/Users/miloszjatelnicki/Desktop/CS/images/white.png"],
)

simulation.batch_spawn_agents(
    1,
    Fox,
    images=["/Users/miloszjatelnicki/Desktop/CS/images/red.png"],
)

# Running the simulation
simulation.run()