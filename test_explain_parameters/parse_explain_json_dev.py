import json
import re


class join_info_class:
    def __init__(self, ID, Left, Right, Left_Alias, Right_Alias, Pred, ProbeKeys, BuildKeys, NumTuplesLeft, NumTuplesRight, NumTuplesOutput, Projection, NumDimLeft, NumDimRight, NumDimOutput ):
        self.id = ID
        self.left_table = Left
        self.right_table = Right
        self.pred_cond = Pred
        self.left_alias = Left_Alias
        self.right_alias = Right_Alias
        self.probe_keys = ProbeKeys
        self.build_keys = BuildKeys
        self.num_tuples_left = NumTuplesLeft
        self.num_tuples_right = NumTuplesRight
        self.num_tuples_output = NumTuplesOutput
        self.projection_cols = Projection
        self.num_dim_left = NumDimLeft
        self.num_dim_right = NumDimRight
        self.num_dim_output = NumDimOutput


    def to_dict(self):
        return {
            "ID": self.id,
            "Left": self.left_table,
            "Left_Alias": self.left_alias,
            "Right": self.right_table,
            "Right_Alias": self.right_alias,
            "Pred": self.pred_cond,
            "ProbeKeys": self.probe_keys,
            "BuildKeys": self.build_keys,
            "NumTuplesLeft": self.num_tuples_left,
            "NumTuplesRight": self.num_tuples_right,
            "NumTuplesOutput": self.num_tuples_output,
            "Projection": self.projection_cols,
            "NumDimLeft": self.num_dim_left,
            "NumDimRight": self.num_dim_right,
            "NumDimOutput": self.num_dim_output
        }

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

def get_proj_cols(node):
    if "Output" in node:
        return node.get("Output")
    return None

def filter_alias_func(predicate, table_info):
    filter_alias = []
    alias_group = get_pred_alias(predicate)
    # print(table_info.values())
    for item in alias_group:
        if item not in table_info.keys():
            filter_alias.append(item)
    return filter_alias

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

def get_table_info(table_node,table_type):
    parent_relationship = table_node.get("Parent Relationship")
    if parent_relationship == table_type:
        if "Relation Name" in table_node and table_node.get("Parent Relationship")==table_type:
            table_name = table_node.get("Relation Name")
            table_alias = table_node.get("Alias")
            table_rows = table_node.get("Actual Rows")
            table_output = table_node.get("Output")
            return table_name.strip(), table_alias.strip(), table_rows, len(table_output)
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
            left_table_name, left_table_alias, left_num_tuples, left_proj_cols = get_table_info(left_table_node, "Outer")
            right_table_name, right_table_alias, right_num_tuples, right_proj_cols = get_table_info(right_table_node,"Inner")
            table.update({left_table_alias: left_table_name})
            table.update({right_table_alias: right_table_name})
            predicate = get_pred_cond(node,None)
            # print("predicate:", predicate)
            filter_alias = filter_alias_func(predicate, table)
            # print("predicate:", predicate)
            predicate_filter = filter_predicates_func(predicate, filter_alias, backup)
            # print("predicate:", predicate)
            predicate_filter = restore_backup_pred(predicate_filter, backup, table)
            # print("predicate:", predicate)
            # print("predicate_filter:", predicate_filter)
            # print("backup:", backup)
            for pred in predicate_filter:
                print("predicate:", pred)
                # print(left_table_alias, right_table_alias)
                probKey, buildKey, = get_join_keys(left_table_alias, right_table_alias, pred)
                print("probKey", probKey)
                print("buildKey", buildKey)
                num_tuples_output = node.get("Actual Rows", 0)
                projection_cols = get_proj_cols(node)
                if left_table_node and right_table_node:
                    join_info = join_info_class(
                        ID=str(len(joins)),
                        Left=left_table_name,
                        Left_Alias=left_table_alias,
                        Right=right_table_name,
                        Right_Alias=right_table_alias,
                        Pred=pred,
                        ProbeKeys=probKey,
                        BuildKeys=buildKey,
                        NumTuplesLeft=left_num_tuples,
                        NumDimRight=right_num_tuples,
                        NumTuplesOutput=num_tuples_output,
                        Projection=projection_cols,
                        NumDimLeft=left_proj_cols,
                        NumTuplesRight=right_proj_cols,
                        NumDimOutput=left_proj_cols + right_proj_cols
                    )
                    joins.append(join_info)
            print("=============================")
if __name__ == "__main__":

    explain_json = load_json_from_file(
        '/Users/kyle/PycharmProjects/24SFSE100Kyle/test_explain_parameters/1a_explain_format_json.txt')


#     explain_json = {
#    "Plans":[
#       {
#          "level":"a",
#          "Node Type":"Aggregate",
#          "Strategy":"Plain",
#          "Partial Mode":"Partial",
#          "Parent Relationship":"Outer",
#          "Actual Rows":1,
#          "Output":[
#             "PARTIAL min((mc.note)::text)",
#             "PARTIAL min((t.title)::text)",
#             "PARTIAL min(t.production_year)"
#          ],
#          "Plans":[
#             {
#                "level":"b",
#                "Node Type":"Nested Loop",
#                "Parent Relationship":"Outer",
#                "Output":[
#                   "mc.note",
#                   "t.title",
#                   "t.production_year"
#                ],
#                "Join Filter":"(mc.movie_id = t.id)",
#                "Plans":[
#                   {
#                      "level":"c",
#                      "Node Type":"Nested Loop",
#                      "Parent Relationship":"Outer",
#                      "Join Type":"Inner",
#                      "Actual Rows":49,
#                      "Output":[
#                         "mi_idx.movie_id",
#                         "mc.note",
#                         "mc.company_type_id",
#                         "mc.movie_id"
#                      ],
#                      "Plans":[
#                         {
#                            "level":"d",
#                            "Node Type":"Hash Join",
#                            "Parent Relationship":"Outer",
#                            "Output":[
#                               "mi_idx.movie_id"
#                            ],
#                            "Hash Cond":"(mi_idx.info_type_id = it.id)",
#                            "Actual Rows":83,
#                            "Plans":[
#                               {
#                                  "level":"e",
#                                  "Node Type":"Seq Scan",
#                                  "Parent Relationship":"Outer",
#                                  "Relation Name":"movie_info_idx",
#                                  "Schema":"public",
#                                  "Actual Rows":460012,
#                                  "Alias":"mi_idx",
#                                  "Output":[
#                                     "mi_idx.id",
#                                     "mi_idx.movie_id",
#                                     "mi_idx.info_type_id",
#                                     "mi_idx.info",
#                                     "mi_idx.note"
#                                  ]
#                               },
#                               {
#                                  "Node Type":"Hash",
#                                  "Parent Relationship":"Inner",
#                                  "Output":[
#                                     "it.id"
#                                  ],
#                                  "Plans":[
#                                     {
#                                        "Node Type":"Seq Scan",
#                                        "Parent Relationship":"Outer",
#                                        "Relation Name":"info_type",
#                                        "Actual Rows":1,
#                                        "Schema":"public",
#                                        "level":"e",
#                                        "Alias":"it",
#                                        "Output":[
#                                           "it.id"
#                                        ]
#                                     }
#                                  ]
#                               }
#                            ]
#                         },
#                         {
#                            "Node Type":"Index Scan",
#                            "Parent Relationship":"Inner",
#                            "Index Name":"movie_id_movie_companies",
#                            "Relation Name":"movie_companies",
#                            "Actual Rows":1,
#                            "Alias":"mc",
#                            "Output":[
#                               "mc.id",
#                               "mc.movie_id",
#                               "mc.company_id",
#                               "mc.company_type_id",
#                               "mc.note"
#                            ],
#                            "Index Cond":"(mc.movie_id = mi_idx.movie_id)"
#                         }
#                      ]
#                   },
#                   {
#                      "Node Type":"Memoize",
#                      "Parent Relationship":"Inner",
#                      "Output":[
#                         "ct.id"
#                      ],
#                      "Cache Key":"mc.company_type_id",
#                      "Cache Mode":"logical",
#                      "Plans":[
#                         {
#                            "Node Type":"Index Scan",
#                            "Parent Relationship":"Outer",
#                            "Index Name":"company_type_pkey",
#                            "Relation Name":"company_type",
#                            "Actual Rows":1,
#                            "Alias":"ct",
#                            "Output":[
#                               "ct.id"
#                            ],
#                            "Index Cond":"(ct.id = mc.company_type_id)"
#                         }
#                      ]
#                   }
#                ]
#             },
#             {
#                "Node Type":"Index Scan",
#                "Parent Relationship":"Inner",
#                "Index Name":"title_pkey",
#                "Relation Name":"title",
#                "Alias":"t",
#                "Actual Rows":1,
#                "Output":[
#                   "t.id",
#                   "t.title",
#                   "t.imdb_index",
#                   "t.kind_id",
#                   "t.production_year",
#                   "t.imdb_id",
#                   "t.phonetic_code",
#                   "t.episode_of_id",
#                   "t.season_nr",
#                   "t.episode_nr",
#                   "t.series_years",
#                   "t.md5sum"
#                ],
#                "Index Cond":"(t.id = mi_idx.movie_id)"
#             }
#          ]
#       }
#    ]
# }

    res = []
    backup = []
    table = {}
    main_func(explain_json, res, backup,0, table)
    # print(res)
    # for join_info in res:
    #     print(join_info.to_dict())
    joins_dict = [join.to_dict() for join in res]
    print(json.dumps(joins_dict, indent=4))

    # print(explain_json.get("Plans")[1])
    # print("Join Execution Details:")
    # print(f"Totally {len(results)} times join:")
    # for idx, join in enumerate(results):
    #     print(f"{join.to_dict()}")