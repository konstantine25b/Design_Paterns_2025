from __future__ import annotations

from .creature import Creature


def render_world(predator: Creature, prey: Creature, width: int = 50) -> str:
    a = predator.position
    b = prey.position
    left = min(a, b)
    right = max(a, b)
    span = right - left
    if span <= 0:
        return "X"
    if span >= width:
        pa = 0 if a == left else width - 1
        pb = 0 if b == left else width - 1
    else:
        pa = a - left
        pb = b - left
    line = ["." for _ in range(width if span >= width else span + 1)]
    line[pa] = "A"
    line[pb] = "B"
    return "".join(line)


def describe_creature(c: Creature) -> str:
    parts = [
        f"pos={c.position}",
        f"legs={c.legs_count}",
        f"wings={c.wings_count}",
        f"claws={c.claws.name}",
        f"teeth={c.teeth_sharpness}",
        f"base={c.base_power}",
        f"stam={c.stamina}",
        f"hp={c.health}",
    ]
    return " ".join(parts)
