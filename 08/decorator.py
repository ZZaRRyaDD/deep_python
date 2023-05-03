import cProfile
import pstats


FUNC_EXECUTE = """
{func_name}:
\tncalls {ncalls}
\ttottime {tottime}
\tpercall_tottime {percall_tottime}
\tcumtime {cumtime}
\tpercall_cumtime {percall_cumtime}
\tfile_name {file_name}
"""


class ProfiledFunction:
    def __init__(self, func):
        self.func = func
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
        print(f"{self.func.__name__} runs")
        print("*" * 20)
        for number, run in enumerate(self.runs, 1):
            print(f"Run #{number}")
            print(f"Total time: {run.total_tt}", sep="")
            for method, profile in run.func_profiles.items():
                print(
                    FUNC_EXECUTE.format(
                        func_name=method,
                        ncalls=profile.ncalls,
                        tottime=profile.tottime,
                        percall_tottime=profile.percall_tottime,
                        cumtime=profile.cumtime,
                        percall_cumtime=profile.percall_cumtime,
                        file_name=profile.file_name,
                    ),
                    sep="",
                )
        print("*" * 20 + "\n\n")


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
