from multiprocessing import get_context
from subprocess import run, PIPE
from sys import argv, exit
from pprint import pprint
from re import search, compile


# there's some encoding bug in finger(1)
translation_table = {
    b"\xc4M-^E": "ę",
    b"\xc4M-^Y": "ę",
    b"\xc5M-^[": "ś",
    b"\xc5M-^A": "Ł",
    b"\xc5M-^B": "ł",
    b"\xc5M-^D": "ń",
    b"\xc5M-^G": "?",
    b"\xc5M-^Z": "Ś",
    b"\xc5M-^D": "ń",
}


class Command:
    def __init__(self, source: str = ''):
        self._source = source
        for k, v in self._patterns.items():
            setattr(self, k, compile(v))

    @property
    def _patterns(self) -> str:
        members = self.__class__.__dict__
        members = filter(lambda m: not m.startswith('_'), members)
        return {p: getattr(self, p) for p in members}


    def __call__(self, *args) -> dict:
        exe = self.__class__.__name__.lower()
        proc = run([exe, *args], stdout=PIPE, stderr=PIPE)
        out, err = proc.stdout, proc.stderr

        if proc.returncode or not out or err:
            print(err.decode())
            return dict()

        def find(pattern):
            try:
                return pattern.search(self._source).group(1).strip()
            except AttributeError:
                return ""

        for from_, to in translation_table.items():
            out = out.replace(from_, to.encode())

        self._source = out.decode()
        return {k: find(v) for k, v in self._patterns.items()}


class Finger(Command):
    login      = "Login: (.*)\t"
    name       = "Name: (.*)\n"
    directory  = "Directory: (.*)\t"
    shell      = "Shell: (.*)\n"
    last_login = "(?:On|Last login) (.*)\n"
    idle       = "(.*) idle\n"


def main():
    if len(argv) != 4:
        print(__file__, "<pattern>", "<start index>", "<end index>")
        exit(1)

    with get_context('spawn').Pool(processes=4) as pool:
        finger = Finger()

        start, end = int(argv[2]), int(argv[3])
        usernames = (argv[1].format(i=i) for i in range(start, end))
        result = pool.map(finger, usernames)
        pprint(result)


if __name__ == '__main__':
    main()
