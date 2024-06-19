from enum import Enum, auto
import pygame as pg
from pygame.math import Vector2
from vi import Agent, Simulation
from vi.config import Config, dataclass, deserialize


@deserialize
@dataclass
class FlockingConfig(Config):
    # You can change these for different starting weights
    alignment_weight: float = 0.5
    cohesion_weight: float = 0.5
    separation_weight: float = 0.5

    # These should be left as is.
    delta_time: float = 0.5                                   # To learn more https://gafferongames.com/post/integration_basics/ 
    mass: int = 20                                            

    def weights(self) -> tuple[float, float, float]:
        return (self.alignment_weight, self.cohesion_weight, self.separation_weight)


class Bird(Agent):
    config: FlockingConfig

    def change_position(self):
        self.there_is_no_escape()
        proximity = list(self.in_proximity_accuracy().without_distance())
        if len(proximity) > 0:
            # Calculate alignment
            agent_vectors = sum((agent.move.normalize() for agent in proximity), Vector2(0, 0))
            average_vector = agent_vectors / len(proximity)
            alignment = average_vector - self.move

            # Calculate separation with a gentler approach
            separation_vector = Vector2(0, 0)
            for agent in proximity:
                distance = self.pos.distance_to(agent.pos)
                if distance < 50:  # Soft threshold for applying separation
                    # Apply a linear force inversely proportional to the distance
                    force_magnitude = 1 / max(distance, 1)  # Avoid division by zero and overly strong forces
                    separation_vector += (self.pos - agent.pos).normalize() * force_magnitude

            separation = separation_vector / len(proximity) if proximity else Vector2(0, 0)

            # Calculate cohesion
            xn = sum((agent.pos for agent in proximity), Vector2(0, 0))
            xn_average = xn / len(proximity)
            cohesion = xn_average - self.pos - self.move

            # Compute total force
            weights = self.config.weights()
            f_total = (alignment * weights[0] + separation * weights[2] + cohesion * weights[1]) / self.config.mass
            self.move += f_total
            self.pos += self.move * self.config.delta_time
        else:
            self.pos += self.move




        #END CODE -----------------


class Selection(Enum):
    ALIGNMENT = auto()
    COHESION = auto()
    SEPARATION = auto()


class FlockingLive(Simulation):
    selection: Selection = Selection.ALIGNMENT
    config: FlockingConfig

    def handle_event(self, by: float):
        if self.selection == Selection.ALIGNMENT:
            self.config.alignment_weight += by
        elif self.selection == Selection.COHESION:
            self.config.cohesion_weight += by
        elif self.selection == Selection.SEPARATION:
            self.config.separation_weight += by

    def before_update(self):
        super().before_update()

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.handle_event(by=0.1)
                elif event.key == pg.K_DOWN:
                    self.handle_event(by=-0.1)
                elif event.key == pg.K_1:
                    self.selection = Selection.ALIGNMENT
                elif event.key == pg.K_2:
                    self.selection = Selection.COHESION
                elif event.key == pg.K_3:
                    self.selection = Selection.SEPARATION

        a, c, s = self.config.weights()
        print(f"A: {a:.1f} - C: {c:.1f} - S: {s:.1f}")


(
    FlockingLive(
        FlockingConfig(
            image_rotation=True,
            movement_speed=1,
            radius=50,
            seed=1,
        )
    )
    .batch_spawn_agents(50, Bird, images=["/Users/olinekone/Downloads/Assignment_0/images/bird.png"])
    .run()
)
