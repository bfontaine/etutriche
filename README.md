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

## Data Format

The data format comes from the Google Form’s output of our online exams. Each
CSV has one header line then one line per student’s input; only the first input
is used. Each line has the following fields:

* Date of submission (`%m/%d/%Y %H:%M:%S`)
* Username (email address)
* Score (In the format `17 / 20` in our case)
* Last name (ignored)
* First name (ignored)

The `N` following fields are the student’s answers to the `N` questions. They
must be single- or multiple-choices questions; we don’t support answers typed
by the students.
