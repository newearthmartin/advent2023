from functools import reduce

LETTERS = ['x', 'm', 'a', 's']

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


def split_range(rng1, rng2):
    """ splits rng1 only"""
    min1, max1 = rng1
    min2, max2 = rng2
    if rng1 == rng2: return [rng1]
    if max1 <= min2 or max2 <= min1: return [rng1]
    rv = []
    if min1 < min2 < max1:
        rv.append((min1, min2))
        min1 = min2
    if max2 < max1:
        rv.append((min1, max2))
        min1 = max2
    rv.append((min1, max1))
    return rv


def split_ranges(ranges1, ranges2):
    rv1 = []
    rv2 = []
    for i, (range1, range2) in enumerate(zip(ranges1, ranges2)):
        split1 = split_range(range1, range2)
        split2 = split_range(range2, range1)
        if len(split1) == 1 and len(split2) == 1: continue
        if len(split1) > 1: rv1 += ranges_from_split(ranges1, split1, i)
        if len(split2) > 1: rv2 += ranges_from_split(ranges2, split2, i)
        break
    return rv1, rv2


def ranges_from_split(ranges, split, letter):
    for rng in split:
        new_ranges = list(ranges)
        new_ranges[letter] = rng
        yield tuple(new_ranges)


def is_included(ranges1, ranges2):
    return all(ranges1[k][0] <= ranges2[k][0] and ranges1[k][1] >= ranges2[k][1] for k in range(len(ranges1)))


def consolidate(to_add):
    print('Consolidating constraints: ', end='')
    while True:
        changes = False
        to_add_list = list(to_add)
        for i in range(len(to_add_list)):
            ranges_1 = to_add_list[i]
            for j in range(i + 1, len(to_add_list)):
                ranges_2 = to_add_list[j]
                diffs = [k for k, v in enumerate(ranges_1) if ranges_2[k] != v]
                if len(diffs) == 1:
                    d = diffs[0]
                    new_rng = list(ranges_1)
                    if ranges_1[d][1] == ranges_2[d][0]:
                        new_rng[d] = ranges_1[d][0], ranges_2[d][1]
                    elif ranges_2[d][1] == ranges_1[d][0]:
                        new_rng[d] = ranges_2[d][0], ranges_1[d][1]
                    else:
                        continue
                    new_rng = tuple(new_rng)
                    changes = True
                    break
            if changes:
                break
        if changes:
            to_add.remove(ranges_1)
            to_add.remove(ranges_2)
            to_add.add(new_rng)
        else:
            break
    print(len(to_add))


def count_possibilities(accepted):
    added = set()
    to_add = set(tuple(get_range(constraints, letter) for letter in LETTERS) for constraints in accepted)
    consolidate(to_add)

    # for l in range(len(LETTERS)):
    #     print('Changing letter', LETTERS[l])
    #     while True:
    #         to_process = to_add.copy()
    #         remove_ranges = set()
    #         add_ranges = set()
    #         while to_process:
    #             ranges1 = to_process.pop()
    #             for ranges2 in to_add:
    #                 range1 = ranges1[l]
    #                 range2 = ranges2[l]
    #                 if range1 == range2: continue
    #                 split2 = split_range(range2, range1)
    #                 if len(split2) == 1: continue
    #                 remove_ranges.add(ranges2)
    #                 add_ranges.update(ranges_from_split(ranges2, split2, l))
    #         for rngs in remove_ranges:
    #             to_process.discard(rngs)
    #             to_add.discard(rngs)
    #         for rngs in add_ranges:
    #             to_add.add(rngs)
    #         if not remove_ranges or add_ranges:
    #             break

    i = 0
    while to_add:
        if i % 1000 == 0:
            print(i, len(to_add), len(added))
        i += 1
        ranges_add = to_add.pop()
        split = False
        for ranges_added in added:
            split_add, split_added = split_ranges(ranges_add, ranges_added)
            if not split_add and not split_added: continue
            if split_add:
                to_add.update(split_add)
            if split_added:
                added.discard(ranges_added)
                to_add.update(split_added)
            split = True
            break
        if not split:
            added.add(ranges_add)
    print()
    rv = 0
    for constraints in added:
        val = reduce(lambda x, y: (y[1] - y[0]) * x, constraints, 1)
        print(constraints, val)
        rv += val
    return rv


def get_accepted_paths():
    print('Calculating accepted paths: ', end='')
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
    print(len(accepted))
    return accepted


def part2():
    accepted = get_accepted_paths()
    return count_possibilities(accepted)


# print('Part 1:', part1())
print('Part 2:', part2())
