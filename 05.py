import re

with open('05.txt') as f:
    seeds = [int(seed) for seed in re.findall(r'\d+', f.readline())]
    lines = [line.strip() for line in f.readlines() if line.strip()]

seed_to_soil = []
soil_to_fertilizer = []
fertilizer_to_water = []
water_to_light = []
light_to_temperature = []
temperature_to_humidity = []
humidity_to_location = []

all_maps = [
    seed_to_soil,
    soil_to_fertilizer,
    fertilizer_to_water,
    water_to_light,
    light_to_temperature,
    temperature_to_humidity,
    humidity_to_location
]

current = None
for line in lines:
    if line.startswith('seed-to-soil'): current = seed_to_soil
    elif line.startswith('soil-to-fertilizer'): current = soil_to_fertilizer
    elif line.startswith('fertilizer-to-water'): current = fertilizer_to_water
    elif line.startswith('water-to-light'): current = water_to_light
    elif line.startswith('light-to-temperature'): current = light_to_temperature
    elif line.startswith('temperature-to-humidity'): current = temperature_to_humidity
    elif line.startswith('humidity-to-location'): current = humidity_to_location
    else:
        line = [int(val) for val in line.split(' ')]
        current.append(line)


def part1():
    def get_val(mapping, i):
        for dest, source, length in mapping:
            if source <= i < source + length:
                return dest + (i - source)
        return i
    min_loc = None
    for seed in seeds:
        soil = get_val(seed_to_soil, seed)
        fertilizer = get_val(soil_to_fertilizer, soil)
        water = get_val(fertilizer_to_water, fertilizer)
        light = get_val(water_to_light, water)
        temperature = get_val(light_to_temperature, light)
        humidity = get_val(temperature_to_humidity, temperature)
        location = get_val(humidity_to_location, humidity)
        min_loc = min(location, min_loc) if min_loc is not None else location
    return min_loc


def part2():
    for map in all_maps:
        map.sort(key=lambda e: e[1])

    ranges = []
    for i in range(len(seeds) // 2):
        ranges.append((seeds[2 * i], seeds[2 * i + 1]))
    ranges.sort(key=lambda e: e[0])

    for map in all_maps:
        dest_ranges = []
        while ranges:
            new_ranges = []
            for range_start, range_len in ranges:
                found = False
                for dest, source, source_len in map:
                    range_end = range_start + range_len
                    source_end = source + source_len
                    if range_start >= source_end:
                        continue
                    if range_end <= source:
                        continue
                    if range_start < source:
                        new_ranges.append((range_start, source - range_start))
                        range_start = source
                        range_len = range_end - range_start
                    if range_end > source_end:
                        new_ranges.append((source_end, range_end - source_end))
                        range_len = source_end - range_start
                    dest_start = dest + (range_start - source)
                    dest_ranges.append((dest_start, range_len))
                    found = True
                    break
                if not found:
                    dest_ranges.append((range_start, range_len))
            ranges = new_ranges
        dest_ranges.sort(key=lambda e: e[0])
        ranges = dest_ranges
    return ranges[0][0]


print('Part 1:', part1())
print('Part 2:', part2())

