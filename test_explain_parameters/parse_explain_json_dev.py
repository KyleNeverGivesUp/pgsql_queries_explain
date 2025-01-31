
import json
import re
from pathlib import Path
from dataclasses import dataclass, field, asdict
import sys
from typing import Final

# Define class for join_info
@dataclass
class join_info_class:
     ID: str
     Left: str
     Right: str
     Left_Table_Name: str
     Right_Table_Name: str
     Left_Alias: str
     Right_Alias: str
     Pred: str
     ProbeKeys: str
     BuildKeys: str
     NumTuplesLeft: str
     NumTuplesRight: str
     NumTuplesOutput: str
     Projection: list
     NumDimLeft: str
     NumDimRight: str
     NumDimOutput: str

# Function to read and parse JSON from the file
def load_json_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove the first line and combine the rest
    json_lines = ''.join(lines[2:-2]).strip()
    json_cleaned = json_lines.replace('+', '').strip()
    #Convert to JSON
    data=json.loads(json_cleaned)
    return data

# Retrieve projection_cols from Json Node
def get_proj_cols(node):
    if "Output" in node:
        return node.get("Output")
    return None

# Filter out which tables are not register in the "tables", tables used to identify if the join order isn't correct retrieving from json node
def filter_alias_func(predicate, table_info):
    filter_alias = []
    alias_group = get_pred_alias(predicate)
    # print(table_info.values())
    for item in alias_group:
        if item not in table_info.keys():
            filter_alias.append(item)
    return filter_alias

# Retrieve table alias from predicate
def get_pred_alias(predicate):
    alias_group = []
    # print(table_info)
    for preds in predicate:
        for split_preds in preds.split("="):
            pred = split_preds.strip()
            pred_index = pred.index(".")
            pred_alias = pred[:pred_index]
            alias_group.append(pred_alias)
    return list(set(alias_group))

# Recursion for retrieve
def get_table_info(table_node,table_type):
        if "Relation Name" in table_node and table_node.get("Parent Relationship")==table_type:
            table_name = table_node.get("Relation Name")
            table_alias = table_node.get("Alias")
            return table_name.strip(), table_alias.strip()
        elif "Plans" in table_node:
            if len(table_node["Plans"]) == 1:
                for subnode in table_node["Plans"]:
                    return get_table_info(subnode,"Outer")
            else:
                for subnode in table_node["Plans"]:
                    return get_table_info(subnode,table_type)

def get_pred_cond(node,join_type):
    conds = []
    if node:
        if join_type is None:
            pred_cond_keys = ['Index Cond', 'Hash Cond', 'Join Filter', 'Merge Cond']
        else:
            pred_cond_keys = [join_type]

        # handle index cond is not in current level and dive into next level to recursive
        for key in pred_cond_keys:
            plans = node.get("Plans")
            if plans and isinstance(plans, list):
                if len(plans) >= 2:
                    # print(f"lens >=2 node is {node}")
                    plan1 = plans[1]
                    # print(f"for loop in plans len >=2")
                    if key in plan1 and plan1[key]:
                        # print(f"key is {key} in plans len >=2 for node[1]")
                        cond = plan1[key].replace("(", "").replace(")", "")
                        if cond:
                            # print("FOUND - plans len >=2 for plan1")
                            conds.append(cond)
                            # print(conds)
                            break
                    else:
                        # print(f"no key {key} in plans len >=2, dive into plan1")
                        sub_cond = get_pred_cond(plan1, key)
                        if sub_cond:
                            conds.extend(sub_cond)
                            break
                    plan0 = plans[0]
                    if key in plan0 and plan0[key]:
                        # print(f"for {key} loop in plans len >=2 for plan0")
                        cond = plan0[key].replace("(", "").replace(")", "")
                        if cond:
                            # print("FOUND - plans len >=2 for plan0")
                            conds.append(cond)
                            # print(conds)
                            break
                elif len(plans) ==1:
                    # print(f"lens ==1 node is {node}")
                    plan0 = plans[0]
                    # print(f"for {key} loop in plans len ==1 for plan0")
                    if key in plan0 and plan0[key]:
                        # print(f"finding {key} loop in plans len ==1")
                        cond = plan0[key].replace("(", "").replace(")", "")
                        if cond:
                            # print("FOUND - plans len ==1 for node[0]")
                            conds.append(cond)
                            # print(conds)
                            break
                    else:
                        # print(f"No {key} loop in plans len ==1, dive into sub_plans")
                        sub_plans0 = plan0.get("Plans")
                        if sub_plans0:
                            sub_cond = get_pred_cond(plan0, key)
                            if sub_cond:
                                conds.extend(sub_cond)
                                break
        for key in pred_cond_keys:
            if key in node:
                # print(f"finding {key} loop in node attribute")
                # print(pred_cond_keys)
                cond = node.get(key).replace("(", "").replace(")", "")
                if cond:
                    # print(f"FOUND {key} loop in node attribute")
                    conds.append(cond)
                    continue
        # print(conds)
        return conds

def filter_predicates_func(predicate, filter_alias, backup):
    predicate_new = []
    if not filter_alias:
        return predicate
    try:
        pattern = re.compile(r'\b(?:' + '|'.join(re.escape(alias) for alias in filter_alias) + r')\.', re.IGNORECASE)
    except re.error as e:
        return predicate

    backup.extend([item for item in predicate if pattern.search(item)])
    predicate_new.extend([item for item in predicate if not pattern.search(item)])
    return predicate_new

def restore_backup_pred(predicate, backup_pred, table):
    if backup:
        new_predicate = predicate.copy()
        pattern = re.compile(r"([a-z]+)\.")
        move_to_pred = [pred for pred in backup_pred if all(alias in table for alias in pattern.findall(pred))]
        new_predicate.extend(move_to_pred)
        new_backup = [pred for pred in backup_pred if not all(alias in table for alias in pattern.findall(pred))]
        backup_pred.clear()
        backup_pred.extend(new_backup)
        return new_predicate
    else:
        return predicate.copy()

def get_join_keys(left_table_alias, right_table_alias, pred):
    left_join_key = ""
    right_join_key = ""
    # print(left_table_alias, right_table_alias)
    pattern = re.compile("\.")
    pred_dict = { i:j for i, j in [pattern.split(item.strip()) for item in pred.split("=")] }
    if left_table_alias in pred_dict:
        left_join_key = pred_dict[left_table_alias]
        pred_dict[left_table_alias] = pred_dict[left_table_alias]+"(taken)"
        # print("left_join_key",left_join_key)
    if right_table_alias in pred_dict:
        right_join_key = pred_dict[right_table_alias]
        pred_dict[right_table_alias] = pred_dict[right_table_alias] + "(taken)"
        # print("right_join_key", right_join_key)
    # handle occurrence of conflict  between pred and parent relationship
    if not left_join_key:
        for key in pred_dict.keys():
            if pred_dict[key][-7:] != "(taken)":
                # print(pred_dict[key])
                left_join_key = pred_dict[key]
                pred_dict[key] = pred_dict[key] + "(taken)"
    # print("left_join_key", left_join_key)
    # print("right_join_key", right_join_key)
    return left_join_key, right_join_key

def main_func(node, joins, backup, join_id_counter, table):
    # join_node_types = ["Hash Join", "Nested Loop", "Merge Join", "Memoize"]
    for key, value in node.items():
        if isinstance(value, dict):
            main_func(value, joins, backup, join_id_counter, table)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    main_func(item, joins, backup, join_id_counter, table)

    if node.get("Plans"):
        plans = node.get("Plans")
        if len(plans) >= 2:# and plans[0].get("Node Type") in join_node_types:
            # Determine which node is left table(prob table), outer is the left table, inner is right table
            if plans[0].get("Parent Relationship") == "Outer":
                left_table_node = plans[0]
                right_table_node = plans[1]
            else:
                left_table_node = plans[1]
                right_table_node = plans[0]
            left_num_tuples = left_table_node.get("Actual Rows")
            left_proj_cols = len(left_table_node.get("Output"))
            right_num_tuples = right_table_node.get("Actual Rows")
            right_proj_cols = len(right_table_node.get("Output"))
            left_table_name, left_table_alias = get_table_info(left_table_node, "Outer")
            right_table_name, right_table_alias = get_table_info(right_table_node,"Inner")
            table.update({left_table_alias: left_table_name})
            table.update({right_table_alias: right_table_name})
            predicate = get_pred_cond(node,None)
            filter_alias = filter_alias_func(predicate, table)
            predicate_filter = filter_predicates_func(predicate, filter_alias, backup)
            predicate_filter = restore_backup_pred(predicate_filter, backup, table)
            for pred in predicate_filter:
                # print("predicate:", pred)
                probKey, buildKey, = get_join_keys(left_table_alias, right_table_alias, pred)
                # print("probKey", probKey)
                # print("buildKey", buildKey)
                num_tuples_output = node.get("Actual Rows", 0)
                projection_cols = get_proj_cols(node)
                # Update for adding pred cols to projection
                projection_cols.extend(item.strip() for item in pred.split("="))
                projection_cols = list(set(col.replace(".","_") for col in projection_cols))
                if left_table_node and right_table_node:
                    join_info = join_info_class(
                        ID  = str(len(joins)),
                        Left = str(len(joins)-1) if len(joins) != 0 else left_table_alias,
                        Right = right_table_alias,
                        Left_Table_Name = left_table_name,
                        Left_Alias = left_table_alias,
                        Right_Table_Name = right_table_name,
                        Right_Alias = right_table_alias,
                        Pred = pred,
                        ProbeKeys = probKey,
                        BuildKeys = buildKey,
                        NumTuplesLeft = left_num_tuples,
                        NumTuplesRight = right_num_tuples,
                        NumTuplesOutput = num_tuples_output,
                        Projection = projection_cols,
                        NumDimLeft = str(left_proj_cols),
                        NumDimRight = str(right_proj_cols),
                        NumDimOutput = str(left_proj_cols + right_proj_cols)
                    )
                    joins.append(join_info)

if __name__ == "__main__":

    args = sys.argv
    # file_name = args[0]
    script_dir = Path(__file__).parent
    file_name = "29a_explain_verbose_analyze_format_json.txt"
    file_path = script_dir / file_name
    res = []
    backup = []
    table = {}
    try:
        explain_json = load_json_from_file(file_path)
    except FileNotFoundError:
        print("File not found")
    else:
        main_func(explain_json[0], res, backup, 0, table)

    print(f"Totally {len(res)} times join:")
    joins_dict = [asdict(join) for join in res]
    print(json.dumps(joins_dict, indent=4))