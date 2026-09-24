"""Gate shot planning on an actual, recorded general-library review."""
import argparse
from amarillo.library import require_reference_review


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('review', help='Project reference-review.json')
    args = parser.parse_args()
    review = require_reference_review(args.review)
    print(f"General reference review passed: {len(review['references'])} videos from {review['library']}")


if __name__ == '__main__':
    main()
