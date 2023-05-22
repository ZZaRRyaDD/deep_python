import cProfile
import pstats


FUNC_EXECUTE = """\tncalls: {ncalls}
\ttottime: {tottime}
\tpercall_tottime: {percall_tottime}
\tcumtime: {cumtime}
\tpercall_cumtime: {percall_cumtime}
\tfile_name: {file_name}
"""


class ProfiledFunction:
    def __init__(self, func):
        self.func = func
        self.func_name = func.__name__
        self.runs = []

    def __call__(self, *args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = self.func(*args, **kwargs)
        pr.disable()
        ps = pstats.Stats(pr)
        self.runs.append(ps.get_stats_profile())
        return result

    def print_stat(self) -> None:
        print(f"Func {self.func.__name__}")
        total_tt = sum([run.total_tt for run in self.runs])
        print(f"Total time: {total_tt}")
        func_profiles = [run.func_profiles[self.func_name] for run in self.runs]
        tottime = sum([run.tottime for run in func_profiles])
        percall_tottime = sum([run.percall_tottime for run in func_profiles])
        cumtime = sum([run.cumtime for run in func_profiles])
        percall_cumtime = sum([run.percall_cumtime for run in func_profiles])
        file_name = list(set([run.file_name for run in func_profiles]))[0]
        print(
            FUNC_EXECUTE.format(
                func_name=self.func_name,
                ncalls=len(self.runs),
                tottime=tottime,
                percall_tottime=percall_tottime,
                cumtime=cumtime,
                percall_cumtime=percall_cumtime,
                file_name=file_name,
            ) + "\n",
        )


def profile_deco(func) -> ProfiledFunction:
    return ProfiledFunction(func)


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)


add.print_stat()
sub.print_stat()
