import json
import os

from .structures import ForceGraphNode

def force_graph(results):
    _groups = []
    nodes = set()
    links = []

    for result in results:
        groups = [os.path.dirname(x) for x in result.paths]

        if groups[0] in _groups:
            group_left = _groups.index(groups[0])
        else:
            _groups.append(groups[0])
            group_left = len(groups) - 1
        
        if groups[1] in _groups:
            group_right = _groups.index(groups[1])
        else:
            _groups.append(groups[1])
            group_right = len(groups) - 1
        
        nodes |= {
            ForceGraphNode(id=result.paths[0], group=group_left),
            ForceGraphNode(id=result.paths[1], group=group_right),
        }

        if result.difference < 100:
            links.append({
                'source': result.paths[0],
                'target': result.paths[1],
                'value': result.difference
            })

    return json.dumps({
        'nodes': [
            {'id': x.id, 'group': x.group}
            for x in sorted(nodes)
        ],
        'links': links
    })

def raw(results):
    return sorted(results)

available_formatters = {
    'force-graph': force_graph,
    'raw': raw
}