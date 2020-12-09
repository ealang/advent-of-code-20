import re
from typing import NamedTuple, List, Iterable, Optional


INSTRUCTION_JMP = "jmp"
INSTRUCTION_NOP = "nop"
INSTRUCTION_ACC = "acc"


class Instruction(NamedTuple):
    op: str
    value: int


class CPUState(NamedTuple):
    acc: int = 0
    i: int = 0


class LoopEncountered(Exception):
    def __init__(self, last_state: CPUState):
        super().__init__()
        self.last_state = last_state


def parse_program(filename: str) -> List[Instruction]:
    def parseinst(line: str) -> Instruction:
        op, value = re.match(r"(\w+) ([+-]\d+)", line).groups()
        return Instruction(op, int(value))

    with open(filename) as fp:
        return list(map(parseinst, fp.readlines()))


def execute_instruction(state: CPUState, instruction: Instruction) -> CPUState:
    if instruction.op == INSTRUCTION_ACC:
        return state._replace(acc=state.acc + instruction.value, i=state.i + 1)
    if instruction.op == INSTRUCTION_JMP:
        return state._replace(i=state.i + instruction.value)
    return state._replace(i=state.i + 1)


def execute(program: List[Instruction], state: Optional[CPUState] = None) -> Iterable[CPUState]:
    """ Run to completion. """
    if state is None:
        state = CPUState(acc=0, i=0)
    while state.i < len(program):
        yield state
        instruction = program[state.i]
        state = execute_instruction(state, instruction)


def execute_with_loop_detection(program: List[Instruction], state: Optional[CPUState] = None) -> Iterable[CPUState]:
    """ Run with added loop detection. """
    last_state: Optional[CPUState] = None
    seen_instructions = set()
    for state in execute(program, state):
        if state.i in seen_instructions:
            raise LoopEncountered(last_state)
        seen_instructions.add(state.i)
        yield state
        last_state = state


def part1(program: List[Instruction]) -> Optional[int]:
    try:
        list(execute_with_loop_detection(program))
    except LoopEncountered as state:
        return state.last_state.acc
    return None


def part2(program: List[Instruction]) -> Optional[int]:
    """
    O(n) compute which instruction to change to avoid infinite loop.
    """

    # Compute which instructions are part of cycles
    def is_on_cycle_cache():
        i_to_group = {len(program): -1}
        group_to_is_cycle = {-1: False}
        cur_group = 0

        def is_on_cycle(i):
            if i not in i_to_group:
                nonlocal cur_group
                try:
                    found_cycle = False
                    for state in execute_with_loop_detection(program, state=CPUState(i=i)):
                        if state.i in i_to_group:
                            found_cycle = group_to_is_cycle[i_to_group[state.i]]
                            break
                        i_to_group[state.i] = cur_group
                    group_to_is_cycle[cur_group] = found_cycle
                except LoopEncountered:
                    group_to_is_cycle[cur_group] = True
                cur_group += 1

            return group_to_is_cycle[i_to_group[i]]

        return is_on_cycle

    is_on_cycle = is_on_cycle_cache()

    # Find index where we can jump to a non-cycle
    mod = None
    for state in execute(program):
        instruction = program[state.i]
        if instruction.op == INSTRUCTION_JMP:
            if not is_on_cycle(state.i + 1):
                mod = instruction._replace(op=INSTRUCTION_NOP)
                break
        elif instruction.op == INSTRUCTION_NOP:
            if not is_on_cycle(state.i + instruction.value):
                mod = instruction._replace(op=INSTRUCTION_JMP)
                break

    # Modify and run
    if mod is not None:
        modified_program = program[:]
        modified_program[state.i] = mod

        for state in execute(modified_program):
            pass

        return state.acc

    return None


program = parse_program("input.txt")
print(part1(program))
print(part2(program))
