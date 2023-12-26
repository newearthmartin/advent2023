import math
from functools import reduce
from collections import defaultdict

with (open('20.txt') as f):
    def parse(name):
        if '%' in name: return name[1:], '%'
        if '&' in name: return name[1:], '&'
        if name == 'broadcaster': return name, 'broadcaster'
        raise Exception(f'Unexpected name {name}')
    lines = (line.strip() for line in f.readlines())
    lines = (line.split(' -> ') for line in lines)
    lines = [(parse(name), out.split(', ')) for name, out in lines]
    types = {name: module_type for (name, module_type), _ in lines}
    out = {name: out for (name, _), out in lines}
    state = defaultdict(lambda: {})

    def set_state():
        state.clear()
        for name, outs in out.items():
            for m_out in outs:
                if types.get(m_out, None) == '&':
                    state[m_out][name] = False
    set_state()


def one_cycle(cycle=None, watch=None):
    rv1, rv2 = 1, 0
    signals = [('broadcaster', False, 'button')]
    while signals:
        if watch:
            watch_signals = [src for dest, signal, src in signals if src in watch and signal]
            for src in watch_signals:
                watch[src] = cycle
        new_signals = []
        for name, pulse, src_name in signals:
            m_type = types.get(name, None)
            if not m_type:
                continue
            if m_type == 'broadcaster':
                new_signals += [(m, False, name) for m in out[name]]
            elif m_type == '%':
                if pulse: continue
                is_on = state[name].get('on', False)
                is_on = not is_on
                state[name]['on'] = is_on
                new_signals += [(m, is_on, name) for m in out[name]]
            elif m_type == '&':
                state[name][src_name] = pulse
                new_pulse = not all(state[name].values())
                new_signals += [(m, new_pulse, name) for m in out[name]]
            else:
                raise Exception(f'Unexpected type {m_type}')
        signals = new_signals
        rv1 += sum(1 for _, pulse, _ in signals if not pulse)
        rv2 += sum(1 for _, pulse, _ in signals if pulse)
    return rv1, rv2


def part1():
    lo, hi = 0, 0
    for _ in range(1000):
        res = one_cycle()
        lo += res[0]
        hi += res[1]
    return lo * hi


def inward(name): return [n for n, outs in out.items() if name in outs]
def lcm(a, b): return abs(a*b) // math.gcd(a, b)
def lcm_multiple(numbers): return reduce(lcm, numbers)


def part2():
    watch = {name: None for name in inward('hj')}
    for i in range(10000):
        one_cycle(cycle=i + 1, watch=watch)
        if all(v is not None for v in watch.values()):
            break
    return lcm_multiple(watch.values())


print('Part 1:', part1())  # 836127690
set_state()
print('Part 2:', part2())