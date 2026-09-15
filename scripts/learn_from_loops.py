"""Refresh cross-loop evidence or route one new shot without making a paid call."""
import argparse
import json
from pathlib import Path
from amarillo.learning import recommend, save_learning


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path, default=Path('artifacts'))
    parser.add_argument('--route')
    parser.add_argument('--reference', action='store_true')
    parser.add_argument('--audio', action='store_true')
    args = parser.parse_args()
    data = save_learning(args.artifacts)
    if args.route:
        print(json.dumps(recommend(data['runs'], args.route, has_reference=args.reference,
                                   audio=args.audio), indent=2))
    else:
        print(f"Saved {len(data['runs'])} attempts and {len(data['routes'])} routes to {args.artifacts}/learning/")


if __name__ == '__main__':
    main()
