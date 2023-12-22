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


def one_cycle():
    rv1, rv2 = 1, 0
    signals = [('broadcaster', False, 'button')]
    has_rx = False
    while signals:
        hjs = [(s[2], s[1]) for s in signals if s[0] == 'hj' and s[1] is True]
        if hjs:
            print(hjs)
        # print([f'{src} --{"H" if pulse else "L"}--> {name} ' for name, pulse, src in signals])
        if any(name == 'rx' and not pulse for name, pulse, _ in signals): has_rx = True
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
    return rv1, rv2, has_rx


def part1():
    lo, hi = 0, 0
    for _ in range(1000):
        res = one_cycle()
        lo += res[0]
        hi += res[1]
    return lo * hi


def part2():
    i = 0
    while True:
        if i % 10000 == 0: print(i)
        i += 1
        res = one_cycle()
        if res[2]:
            print('Found!')
            return res[2]


print('Part 1:', part1())  # 836127690
set_state()
print('Part 2:', part2())