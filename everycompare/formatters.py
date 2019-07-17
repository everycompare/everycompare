import csv
import io
import json
import os

def force_graph(results):
    _dirs = set()
    nodes = set()
    links = []

    for result in results:
        _dirs |= {os.path.dirname(x) for x in result.paths}
        nodes |= set(result.paths)

        if result.difference < 100:
            links.append({
                'source': result.paths[0],
                'target': result.paths[1],
                'value': result.difference
            })

    _dirs = sorted(_dirs)

    return json.dumps({
        'nodes': [
            {'id': x, 'group': _dirs.index(os.path.dirname(x))}
            for x in sorted(nodes)
        ],
        'links': links
    })

def raw(results):
    return sorted(results)

def csv_writer(results):
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(('difference', 'file 1', 'file 2', 'comparison method'))

    [writer.writerow((x.difference, x.paths[0], x.paths[1], x.method)) for x in sorted(results)]

    return out.getvalue()

available_formatters = {
    'force-graph': force_graph,
    'raw': raw,
    'csv': csv_writer
}