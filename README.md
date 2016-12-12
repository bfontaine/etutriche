# Etutriche

**Etutriche** is a quick experiment to automatically detect cheating students.
It reads exams' responses from a bunch of CSVs (one per exam) and tries to
find pairs of students with very similar answering patterns.

## Usage

    python etutriche.py [options] <path>

`path` should be a path for either a directory of `.csv`s or one `.csv`.

Supported options (see `--help` for more info):

* `--threshold`: set a custom threshold for the Sørensen-Dice score.
* `--max-score`: students with a score higher or equal to this value are
  excluded; we assume that high scores equal good students equal no cheating.
  The downside of this is that it can lead to false negatives; but we try to
  avoid false positives.
