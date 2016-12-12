# -*- coding: UTF-8 -*-

import argparse

from etutriche import data

def main(args):
    print("Parameters: threshold=%g, max_score=%g" % (
        args.threshold, args.max_score))

    results = data.load_results(args.path)
    series = data.make_series(results)

    exams = results.all_exams()
    print("Exams: %s" % ", ".join(exams))
    print()

    pairs = data.compare_series(series, args.threshold)
    print("Found %d possible cheating instances:" % len(pairs))
    for s1, s2, _ in sorted(pairs, key=lambda p: p[2], reverse=True):
        header = "%s + %s: %d/%d answers in common" % (
            s1.label, s2.label, s1.common_answers(s2), len(s1.answers))
        printed_header = False

        pair_exams = results.by_usernames(s1.label, s2.label)

        # Let's dive in the details
        for name, (r1, r2) in sorted(pair_exams.items()):
            if r1 is None or r2 is None:
                continue  # one of them wasn't here

            if r1.score < args.min_score and r2.score < args.min_score:
                continue # too bad scores

            if r1.score >= args.max_score and r2.score >= args.max_score:
                continue # good scores

            sub_s1 = r1.series
            sub_s2 = r2.series

            sub_score = sub_s1.similarity_score(sub_s2)
            if sub_score < args.threshold:
                continue

            if not printed_header:
                print(header)
                printed_header = True

            print("  %s: %d/%d answers in common (scores: %g + %g)" % (
                name, sub_s1.common_answers(sub_s2), len(sub_s1.answers),
                r1.score, r2.score))

        if printed_header:
            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect cheating students")
    parser.add_argument("path", metavar="DIR", help="results directory")
    parser.add_argument("-t", "--threshold", type=float, default=0.8)
    parser.add_argument("--best-score", type=float, default=20.0)
    parser.add_argument("--max-score", type=float, default=17.0)
    parser.add_argument("--min-score", type=float, default=5.0)
    main(parser.parse_args())
