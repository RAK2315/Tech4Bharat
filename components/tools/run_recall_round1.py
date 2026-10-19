"""Run each research phase in a fresh CPU process under the recorded caps."""
import argparse
import json
from pathlib import Path
import sys

import psutil

from component_inspector.research.ksdd2_round1 import write_json
from component_inspector.vision.resources import run_bounded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--weights', type=Path, required=True)
    parser.add_argument('--phases', nargs='+', default=['baseline', 'features', 'supervised', 'patchcore', 'coverage'])
    args = parser.parse_args()
    root = args.root.resolve()
    for phase in args.phases:
        if (root/f'{phase}-complete.json').exists():
            print(phase, 'already complete; using saved output', flush=True)
            continue
        command = [sys.executable, '-m', 'component_inspector.research.ksdd2_round1',
                   '--phase', phase, '--root', str(root), '--weights', str(args.weights.resolve())]
        cap = min(4*1024**3, int(.60*psutil.virtual_memory().available))
        print('START', phase, 'RSS cap', cap, flush=True)
        resource = run_bounded(command, root/f'{phase}-worker.log', max_rss_bytes=cap, max_seconds=1800)
        write_json(root/f'{phase}-resources.json', resource)
        print('END', phase, json.dumps(resource), flush=True)
        if resource['status'] != 'completed':
            raise SystemExit(1)


if __name__ == '__main__':
    main()
