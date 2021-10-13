import sys

class O:
    pass

o = O()

with open("bugsinpy_id.info", "rt") as f:
    while True:
        l = f.readline()
        if not l:
            break
        split = l.split("=")
        setattr(o, split[0].lower(), split.pop().strip("\n "))
ids = list()
with open(o.work_dir.split("_BugsInPy")[0] + f"_BugsInPy/projects/{o.project_name}/bugs/{o.bug_id}/run_test.sh") as f:
    while True:
        l = f.readline()
        if not l:
            break
        ids.append(l.split(" ", 1).pop())
sys.stdout.write(" ".join(ids).replace("\n", " "))
