"""Day 22: Wizard Simulator 20XX.

Solution finds the cheapest plan, but doesn't actually terminate in
reasonable time. It's again a basic depth first search, with some
constraints on which edges are available from each state node.
"""

from dataclasses import dataclass
import os
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Character:
    hp: int
    mana: int = 0
    dmg: int = 0


@dataclass(frozen=True)
class Spell:
    name: str
    duration: int
    cost: int
    armor: int = 0
    dmg: int = 0
    heal: int = 0
    recharge: int = 0


@dataclass
class State:
    pc: Character
    boss: Character
    effects: Dict[Spell, int]
    total_mana: int
    hard_mode: bool


SPELLS = (
    Spell(name="magic missile", duration=0, cost=53, dmg=4),
    Spell(name="drain", duration=0, cost=73, dmg=2, heal=2),
    Spell(name="shield", duration=6, cost=113, armor=7),
    Spell(name="poison", duration=6, cost=173, dmg=3),
    Spell(name="recharge", duration=5, cost=229, recharge=101),
)


def debug(str: str):
    if os.environ.get("DEBUG", None):
        print(str)


def read_data() -> str:
    day = os.path.basename(__file__).split(".")[0].split("_")[1]
    fname = os.path.join(os.path.dirname(__file__), "input", f"{day}.input")

    with open(fname, encoding="utf-8") as handle:
        return handle.read().strip()


def parse(data: str) -> Character:
    hp, dmg = [int(line.split(": ")[1]) for line in data.split("\n")]
    return Character(hp=hp, dmg=dmg)


def run_sim(pc: Character, boss: Character, spells: List[Spell]) -> State:
    next_state = State(pc=pc, boss=boss, effects={}, total_mana=0, hard_mode=False)
    for turn, spell in enumerate(spells):
        debug(
            f"Turn {turn}, pc_hp: {next_state.pc.hp} pc_mana: {next_state.pc.mana} boss_hp: {next_state.boss.hp}"
        )
        next_state = run_turn(next_state, spell)
    return next_state


def run_turn(state: State, spell: Spell) -> State:
    pc_hp = state.pc.hp
    pc_mana = state.pc.mana
    pc_armor = 0
    boss_hp = state.boss.hp
    total_mana = state.total_mana

    if state.hard_mode:
        pc_hp -= 1
        if pc_hp <= 0:
            return State(
                pc=Character(hp=pc_hp, mana=pc_mana),
                boss=Character(hp=boss_hp, dmg=state.boss.dmg),
                effects=state.effects,
                total_mana=total_mana,
                hard_mode=state.hard_mode,
            )

    # Apply effects
    current_effects: Dict[Spell, int] = {}
    for effect, duration in state.effects.items():
        debug(f"applying {effect.name}, {duration - 1} remaining")
        boss_hp -= effect.dmg
        pc_hp += effect.heal
        pc_mana += effect.recharge

        if duration - 1 > 0:
            current_effects[effect] = duration - 1

    if boss_hp <= 0:
        debug(f"boss died, {total_mana}")
        return State(
            pc=Character(hp=pc_hp, mana=pc_mana),
            boss=Character(hp=boss_hp, dmg=state.boss.dmg),
            effects=current_effects,
            total_mana=total_mana,
            hard_mode=state.hard_mode,
        )

    debug(f"casting {spell.name}")
    pc_mana -= spell.cost
    total_mana += spell.cost
    if not spell.duration:
        boss_hp -= spell.dmg
        pc_hp += spell.heal
    else:
        current_effects[spell] = spell.duration

    if boss_hp <= 0:
        debug(f"boss died, {total_mana}")
        return State(
            pc=Character(hp=pc_hp, mana=pc_mana),
            boss=Character(hp=boss_hp, dmg=state.boss.dmg),
            effects=current_effects,
            total_mana=total_mana,
            hard_mode=state.hard_mode,
        )

    debug("boss turn")

    # Apply effects
    next_effects = {}
    for effect, duration in current_effects.items():
        debug(f"applying {effect.name}, {duration - 1} remaining")
        boss_hp -= effect.dmg
        pc_hp += effect.heal
        pc_mana += effect.recharge
        pc_armor = max(pc_armor, effect.armor)

        if duration - 1 > 0:
            next_effects[effect] = duration - 1
    current_effects = next_effects

    if boss_hp <= 0:
        debug(f"boss died, {total_mana}")
        return State(
            pc=Character(hp=pc_hp, mana=pc_mana),
            boss=Character(hp=boss_hp, dmg=state.boss.dmg),
            effects=current_effects,
            total_mana=total_mana,
            hard_mode=state.hard_mode,
        )

    debug(f"attack for {max(state.boss.dmg - pc_armor, 1)} {state.boss.dmg} {pc_armor}")
    pc_hp -= max(state.boss.dmg - pc_armor, 1)

    return State(
        pc=Character(hp=pc_hp, mana=pc_mana),
        boss=Character(hp=boss_hp, dmg=state.boss.dmg),
        effects=current_effects,
        total_mana=total_mana,
        hard_mode=state.hard_mode,
    )


def part1(pc: Character, boss: Character, hard_mode: bool = False):
    search: List[Tuple[State, Spell]] = []
    init_state = State(pc=pc, boss=boss, effects={}, total_mana=0, hard_mode=hard_mode)

    cheapest: Optional[int] = None
    for spell in SPELLS:
        if spell.cost <= pc.mana:
            search.append((init_state, spell))

    while search:
        state, spell = search.pop()
        state = run_turn(state, spell)

        if cheapest and state.total_mana >= cheapest:
            continue

        if state.pc.hp <= 0:
            continue

        if state.boss.hp <= 0:
            if not cheapest or state.total_mana < cheapest:
                cheapest = state.total_mana
                print(f"cheapest {cheapest}")
            continue

        for spell in SPELLS:
            if state.effects.get(spell, 0) <= 1 and spell.cost <= state.pc.mana:
                search.append((state, spell))

    return cheapest


def test_run_sim():
    spells = {s.name: s for s in SPELLS}
    state = run_sim(
        pc=Character(hp=10, mana=250),
        boss=Character(hp=13, dmg=8),
        spells=[spells["poison"], spells["magic missile"]],
    )
    assert state.boss.hp == 0
    assert state.total_mana == 226


def test_run_sim_b():
    spells = {s.name: s for s in SPELLS}
    state = run_sim(
        pc=Character(hp=10, mana=250),
        boss=Character(hp=14, dmg=8),
        spells=[
            spells["recharge"],
            spells["shield"],
            spells["drain"],
            spells["poison"],
            spells["magic missile"],
        ],
    )
    assert state.boss.hp == -1
    assert state.total_mana == 641


def test_part1():
    assert (
        part1(
            pc=Character(hp=10, mana=250),
            boss=Character(hp=13, dmg=8),
        )
        == 226
    )


def test_part1_b():
    assert (
        part1(
            pc=Character(hp=10, mana=250),
            boss=Character(hp=14, dmg=8),
        )
        == 641
    )


if __name__ == "__main__":
    print(part1(Character(hp=50, mana=500), parse(read_data())))
    print(part1(Character(hp=50, mana=500), parse(read_data()), hard_mode=True))
