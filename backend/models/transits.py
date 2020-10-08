


def parse_json(data):
    changes = []
    route_id = data['routes'][0]['id']
    sections = data['routes'][0]['sections']
    for section in sections:
        section_info = {}
        section_info['transport_mode'] = section['transport']['mode']
        section_info['transportation type'] = section['type']
        if 'name' in section['transport'] and 'headsign' in section['transport']:
            section_info[section_info['transport_mode'] + ' name'] = section['transport']['name']
            section_info['head sign'] = section['transport']['headsign']
        if 'time' in section['departure']:
            section_info['departure time'] = section['departure']['time']
        if 'name' in section['departure']['place']:
            section_info['departure name'] = section['departure']['place']['name']
        section_info['departure type'] = section['departure']['place']['type']
        section_info['departure location'] = section['departure']['place']['location']
        if 'time' in section['arrival']:
            section_info['arrival time'] = section['arrival']['time']
        if 'name' in section['arrival']['place']:
            section_info['arrival name'] = section['arrival']['place']['name']
        section_info['arrival type'] = section['arrival']['place']['type']
        section_info['arrival location'] = section['arrival']['place']['location']
        if 'agency' in section:
            section_info['agency id'] = section['agency']['id']
            section_info['agency name'] = section['agency']['name']
            section_info['agency website'] = section['agency']['website']
        changes.append(section_info)
        
    return changes
