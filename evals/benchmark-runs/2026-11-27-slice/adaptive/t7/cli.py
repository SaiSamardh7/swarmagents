import argparse
from datetime import date
from core import add_task, complete_task, list_tasks, list_overdue

def main(argv=None):
    parser = argparse.ArgumentParser(prog="taskman")
    parser.add_argument("--db", default="tasks.json")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_add = sub.add_parser("add"); p_add.add_argument("title"); p_add.add_argument("--due", metavar="YYYY-MM-DD")
    p_done = sub.add_parser("done"); p_done.add_argument("id", type=int)
    p_list = sub.add_parser("list"); p_list.add_argument("--overdue", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "add":
        if args.due:
            try:
                date.fromisoformat(args.due)
            except ValueError:
                parser.error("--due must be YYYY-MM-DD")
        print(add_task(args.db, args.title, due=args.due))
    elif args.cmd == "done":
        print("ok" if complete_task(args.db, args.id) else "not found")
    elif args.cmd == "list":
        for t in (list_overdue(args.db) if args.overdue else list_tasks(args.db)):
            mark = "x" if t["done"] else " "
            print(f'[{mark}] {t["id"]} {t["title"]}')

if __name__ == "__main__":
    main()
