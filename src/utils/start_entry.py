from pathlib import Path
from datetime import datetime
from ..rules.rule_factory import RuleFactory
from ..action.action_factory import FileActionFactory, DirActionFactory
from ..entities.entry import Entry
from ..database.queries import db_call, get_selected_entry, get_file_types, change_entry_state, update_next_run, update_last_run
from .calculate_next_run import calculate_next_run

def start_entry(entry_id: int):
    try:
        entry_result = db_call(get_selected_entry, entry_id)

        if not entry_result.get("success"):
            raise Exception(f"Something went wrong while retrieving the entry:\n{entry_result.get("error")}")    

        # Either the entry is inactive or it's already running
        if entry_result.get("data")["state"] != 1:
            return
        
        next_run = datetime.strptime(entry_result.get("data")["next_run"], "%d.%m.%Y %H:%M:%S")
        if next_run > datetime.now():
            return
        
        file_type_result = db_call(get_file_types, entry_id)

        if not file_type_result.get("success"):
            raise Exception(f"Something went wrong while retrieving the file types:\n{file_type_result.get("error")}")

        file_types = [r[0] for r in file_type_result.get("data")]
        entry = Entry.from_row(entry_result.get("data"))

        rule = RuleFactory().create(entry, file_types)
        file_rule = rule.file_rule
        dir_rule = rule.dir_rule

        file_action = FileActionFactory().create(entry)
        dir_action = DirActionFactory().create(entry)

        db_call(change_entry_state, entry_id, 2)

        for item in Path(entry.originpath).iterdir():
            if file_rule and file_rule.match(item):
                file_action.execute(item)
            elif dir_rule and dir_rule.match(item):
                dir_action.execute(item)

        db_call(change_entry_state, entry_id, 1)
        db_call(update_last_run, entry_id)
        db_call(update_next_run, entry_id, calculate_next_run(entry.interval_type, entry.schedule_type, entry.schedule_value))
    except Exception as e:
        db_call(change_entry_state, entry_id, 1)