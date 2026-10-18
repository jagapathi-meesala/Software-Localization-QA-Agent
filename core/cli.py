import argparse, json, sys
from pathlib import Path
from core.engine import compare_json, compare_csv, validate_json_file

def main():
    parser=argparse.ArgumentParser(description="Local deterministic software localization QA")
    sub=parser.add_subparsers(dest="command",required=True)
    v=sub.add_parser("validate"); v.add_argument("file"); v.add_argument("--locale",default="unknown"); v.add_argument("--output")
    c=sub.add_parser("compare"); c.add_argument("source_or_csv"); c.add_argument("target",nargs="?"); c.add_argument("--source-locale",default="source"); c.add_argument("--target-locale",default="target"); c.add_argument("--output")
    args=parser.parse_args()
    try:
        if args.command=="validate": report=validate_json_file(args.file,args.locale)
        elif args.target: report=compare_json(args.source_or_csv,args.target,args.source_locale,args.target_locale)
        else: report=compare_csv(args.source_or_csv,args.source_locale,args.target_locale)
        rendered=json.dumps(report,indent=2,ensure_ascii=False)+"\n"
        if args.output: Path(args.output).write_text(rendered,encoding="utf-8")
        print(rendered,end="")
        return 1 if report["summary"]["errors"] else 0
    except (OSError,ValueError,json.JSONDecodeError) as exc:
        print(json.dumps({"status":"input_error","error":str(exc)},indent=2),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main())
