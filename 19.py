LETTERS = ['x', 'm', 'a', 's']

with open('19.txt') as f:
    lines = (line.strip() for line in f.readlines())
    workflows = []
    parts = []
    while True:
        line = next(lines)
        if not line: break
        workflows.append(line)
    while True:
        try:
            line = next(lines)
        except StopIteration:
            break
        if not line: break
        parts.append(line)

    def parse_rule(r):
        rule_parts = r.split(':')
        if len(rule_parts) == 1: return rule_parts
        part0 = rule_parts[0]
        comp = '>' if '>' in part0 else '<'
        p1, p2 = part0.split(comp)
        return [p1, comp, int(p2), rule_parts[1]]

    workflows = (line.replace('}', '').split('{') for line in workflows)
    workflows = ((name, rules.split(',')) for name, rules in workflows)
    workflows = {name: [parse_rule(rule) for rule in rules] for name, rules in workflows}

    parts = (part.replace('{', '').replace('}', '').split(',') for part in parts)
    parts = ((p.split('=') for p in part) for part in parts)
    parts = [{k: int(v) for k, v in part} for part in parts]


def apply_rule(rule, part):
    if len(rule) == 1: return rule[0]
    name, comp, value, result = rule
    part_val = part[name]
    success = part_val > value if comp == '>' else part_val < value
    return result if success else None


def apply_workflow(name, part):
    for rule in workflows[name]:
        result = apply_rule(rule, part)
        if result is not None:
            return result
    assert False, 'should not reach here'


def is_accepted(part):
    workflow = 'in'
    while True:
        result = apply_workflow(workflow, part)
        if result == 'A': return True
        if result == 'R': return False
        assert result is not None
        assert result != workflow
        workflow = result


def part1():
    accepted_parts = (part for part in parts if is_accepted(part))
    return sum(sum(p.values()) for p in accepted_parts)


def get_opposite(constraint):
    name, comp, value = constraint
    new_comp = '>' if comp == '<' else '<'
    return name, new_comp, value + (1 if new_comp == '<' else -1)


def contradicts(constraints, constraint):
    name, comp, value = constraint
    return any((comp == '<' and value <= v) or (comp == '>' and value >= v)
               for n, c, v in constraints
               if name == n and comp != c)


def add_constraint(constraints, constraint):
    if contradicts(constraints, constraint):
        return None
    rv = constraints.copy()
    name, comp, value = constraint
    for i in range(len(rv)):
        n, c, v = rv[i]
        if n == name and c == comp:
            rv[i] = (n, c, max(v, value) if comp == '>' else min(v, value))
            return rv
    rv.append(constraint)
    return rv


def get_new_constraints(rule, constraints):
    name, comp, value, _ = rule
    const_yes = (name, comp, value)
    const_no = get_opposite(const_yes)
    constraints_yes = add_constraint(constraints, const_yes)
    constraints_no = add_constraint(constraints, const_no)
    return constraints_yes, constraints_no


def get_range(constraints, letter):
    rmin = 1
    rmax = 4001
    for name, comp, value in constraints:
        if name != letter: continue
        if comp == '<': rmax = min(rmax, value)
        if comp == '>': rmin = max(rmin, value + 1)
    return (rmin, rmax) if rmin <= rmax else None


def get_accepted_paths():
    paths = [('in', [])]
    accepted = []
    while paths:
        new_paths = []
        for workflow, constraints in paths:
            for rule in workflows[workflow]:
                if rule == ['A']:
                    accepted.append(constraints)
                    break
                elif rule == ['R']:
                    break
                elif len(rule) == 1:
                    new_paths.append((rule[0], constraints))
                    break
                else:
                    dest_yes = rule[3]
                    constraints_yes, constraints_no = get_new_constraints(rule, constraints)
                    if dest_yes == 'A':
                        if constraints_yes is not None:
                            accepted.append(constraints_yes)
                    elif dest_yes == 'R':
                        pass
                    else:
                        if constraints_yes is not None:
                            new_paths.append((dest_yes, constraints_yes))
                    if constraints_no is not None:
                        constraints = constraints_no
                    else:
                        break
        paths = new_paths
    return accepted


def part2():
    accepted = get_accepted_paths()
    ranges = [tuple(get_range(path, letter) for letter in LETTERS) for path in accepted ]
    rv = 0
    for rng in ranges:
        val = 1
        for rng_min, rng_max in rng:
            val *= rng_max - rng_min
        rv += val
    return rv


print('Part 1:', part1())
print('Part 2:', part2())
