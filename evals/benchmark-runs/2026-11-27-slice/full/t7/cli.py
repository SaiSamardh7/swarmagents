import argparse
import sys
from datetime import date
from core import add_task, complete_task, list_tasks, list_overdue


def _iso_date(s):
    try:
        return date.fromisoformat(s).isoformat()
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid date {s!r}, expected YYYY-MM-DD")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="taskman")
    parser.add_argument("--db", default="tasks.json")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add"); p_add.add_argument("title")
    p_add.add_argument("--due", type=_iso_date, default=None, metavar="YYYY-MM-DD")
    p_done = sub.add_parser("done"); p_done.add_argument("id", type=int)
    p_list = sub.add_parser("list")
    p_list.add_argument("--overdue", action="store_true", help="show only overdue tasks")
    args = parser.parse_args(argv)
    if args.cmd == "add":
        if args.due is None:
            print(add_task(args.db, args.title))
        else:
            print(add_task(args.db, args.title, due=args.due))
    elif args.cmd == "done":
        print("ok" if complete_task(args.db, args.id) else "not found")
    elif args.cmd == "list":
        tasks = list_overdue(args.db) if args.overdue else list_tasks(args.db)
        for t in tasks:
            mark = "x" if t["done"] else " "
            print(f'[{mark}] {t["id"]} {t["title"]}')

if __name__ == "__main__":
    main()
