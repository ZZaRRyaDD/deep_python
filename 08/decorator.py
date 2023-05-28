import cProfile
import pstats


FUNC_EXECUTE = """\tncalls: {ncalls}
\ttottime: {tottime}
\tpercall_tottime: {percall_tottime}
\tcumtime: {cumtime}
\tpercall_cumtime: {percall_cumtime}
\tfile_name:lineno(function): {file_name}
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
        print(f"Func {self.func.__name__}")
        func_info = {
            "ncalls": 0,
            "tottime": 0.0,
            "percall_tottime": 0.0,
            "cumtime": 0.0,
            "percall_cumtime": 0.0,
        }
        functions = {}
        total_tt = sum(run.total_tt for run in self.runs)
        print(f"Total time: {total_tt}")
        for run in self.runs:
            for function_name in run.func_profiles:
                func_run = run.func_profiles[function_name]
                if func_run.file_name == "~" and func_run.line_number == 0:
                    key = "{" + function_name + "}"
                else:
                    key = f"{func_run.file_name}:{func_run.line_number}({function_name})"
                if key not in functions:
                    functions[key] = func_info.copy()
                functions[key]["ncalls"] += 1
                functions[key]["tottime"] += func_run.tottime
                functions[key]["percall_tottime"] += func_run.percall_tottime
                functions[key]["cumtime"] += func_run.cumtime
                functions[key]["percall_cumtime"] += func_run.percall_cumtime

        for name, info in functions.items():
            print(
                FUNC_EXECUTE.format(
                    ncalls=info["ncalls"],
                    tottime=info["tottime"],
                    percall_tottime=info["percall_tottime"],
                    cumtime=info["cumtime"],
                    percall_cumtime=info["percall_cumtime"],
                    file_name=name,
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
