import argparse
from core import add_task, complete_task, list_tasks

def main(argv=None):
    parser = argparse.ArgumentParser(prog="taskman")
    parser.add_argument("--db", default="tasks.json")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add"); p_add.add_argument("title")
    p_done = sub.add_parser("done"); p_done.add_argument("id", type=int)
    sub.add_parser("list")
    args = parser.parse_args(argv)
    if args.cmd == "add":
        print(add_task(args.db, args.title))
    elif args.cmd == "done":
        print("ok" if complete_task(args.db, args.id) else "not found")
    elif args.cmd == "list":
        for t in list_tasks(args.db):
            mark = "x" if t["done"] else " "
            print(f'[{mark}] {t["id"]} {t["title"]}')

if __name__ == "__main__":
    main()
