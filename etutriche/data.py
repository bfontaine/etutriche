# -*- coding: UTF-8 -*-

import csv
import os.path
from glob import glob
from datetime import datetime
from collections import defaultdict

class Result:
    def __init__(self, exam, ts, username, score, answers):
        self.exam = exam
        self.ts = ts
        self.username = username
        self.score = score
        self.answers = answers

    @property
    def series(self):
        return Series(":".join((self.exam, self.username)), self.answers)


class Results:
    def __init__(self):
        # username -> exam -> result
        self._res = defaultdict(dict)

    def append(self, r):
        self._res[r.username][r.exam] = r

    def __len__(self):
        return sum((len(d) for d in self._res.values()))

    def __iter__(self):
        for user_exams in self._res.values():
            for r in user_exams.values():
                yield r

    def __repr__(self):
        return "{%s}" % repr(list(self))[1:-1]

    def all_exams(self):
        exams = set()
        for user_exams in self._res.values():
            exams.update(user_exams)

        return sorted(exams)

    def by_username(self, username):
        if username not in self._res:
            return []

        return sorted(self._res[username].items())

    def by_usernames(self, *usernames):
        exams = self.all_exams()
        d = {e: [] for e in exams}

        for username in usernames:
            user_exams = self._res[username]
            for e in d:
                d[e].append(user_exams.get(e))

        return d




class Series:
    def __init__(self, label, answers):
        self.label = label
        self.answers = answers

    def common_answers(self, other):
        n = 0
        for a, b in zip(self.answers, other.answers):
            if a == b:
                n += 1

        return n

    def similarity_score(self, other):
        l1 = len(self.answers)
        l2 = len(other.answers)

        # Dice-Sørensen
        return 2 * self.common_answers(other) / float(l1 + l2)

    def __eq__(self, other):
        return isinstance(other, Series) and self.label == other.label

    def __hash__(self):
        return hash(self.label)


def load_results(path="results"):
    paths = []
    if os.path.isdir(path):
        paths.extend(sorted(glob("%s/*.csv" % path)))
    else:
        paths.append(path)

    results = Results()

    for path in paths:
        name = os.path.splitext(os.path.basename(path))[0]
        usernames = set()

        with open(path, newline="") as f:
            reader = csv.reader(f)
            header = True
            for row in reader:
                if header:
                    header = False
                    continue
                ts_text, username, score = row[:3]
                # remove the last answer; the question is often something like
                # "did you find this exam difficult?"
                answers = row[5:-1]

                # e.g. 10/12/2016 11:32:18
                #      11/15/2016 15:19:59
                ts = datetime.strptime(ts_text, "%m/%d/%Y %H:%M:%S")
                username = username.strip().lower()
                score = float(score.split("/")[0])

                if username in usernames:
                    continue

                usernames.add(username)

                results.append(Result(name, ts, username, score, answers))

    return results


def make_series(results):
    answers = defaultdict(list)

    for r in results:
        answers[r.username].extend(r.answers)

    for label, answers in answers.items():
        yield Series(label, answers)


def load_series(path="results"):
    return make_series(load_results(path))


def compare_series(series, threshold=0.8):
    """
    O(n^2) comparison
    """
    pairs = set()

    series = list(series)
    for i, s1 in enumerate(series):
        for j, s2 in enumerate(series):
            if i >= j:
                continue

            score = s1.similarity_score(s2)

            if score >= threshold:
                p = (s1, s2, score) if s1.label <= s2.label else (s2, s1, score)
                pairs.add(p)

    return list(pairs)
