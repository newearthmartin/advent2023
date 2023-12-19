with (open('19.txt') as f):
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


print('Part 1:', part1())
