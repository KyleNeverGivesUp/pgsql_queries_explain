import json

# Load the JSON formatted execution plan
execution_plan_json = '''
{
    "Plan": {
        "Node Type": "Aggregate",
        "Plans": [
            {
                "Node Type": "Gather",
                "Plans": [
                    {
                        "Node Type": "Aggregate",
                        "Plans": [
                            {
                                "Node Type": "Nested Loop",
                                "Join Type": "Inner",
                                "Join Filter": "(mc.movie_id = t.id)",
                                "Plans": [
                                    {
                                        "Node Type": "Nested Loop",
                                        "Join Type": "Inner",
                                        "Plans": [
                                            {
                                                "Node Type": "Nested Loop",
                                                "Join Type": "Inner",
                                                "Plans": [
                                                    {
                                                        "Node Type": "Hash Join",
                                                        "Join Type": "Inner",
                                                        "Hash Cond": "(mi_idx.info_type_id = it.id)",
                                                        "Plans": [
                                                            {
                                                                "Node Type": "Seq Scan",
                                                                "Relation Name": "movie_info_idx"
                                                            },
                                                            {
                                                                "Node Type": "Seq Scan",
                                                                "Relation Name": "info_type"
                                                            }
                                                        ]
                                                    },
                                                    {
                                                        "Node Type": "Index Scan",
                                                        "Relation Name": "movie_companies",
                                                        "Index Cond": "(movie_id = mi_idx.movie_id)"
                                                    }
                                                ]
                                            },
                                            {
                                                "Node Type": "Memoize",
                                                "Plans": [
                                                    {
                                                        "Node Type": "Index Scan",
                                                        "Relation Name": "company_type",
                                                        "Index Cond": "(id = mc.company_type_id)"
                                                    }
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "Node Type": "Index Scan",
                                        "Relation Name": "title",
                                        "Index Cond": "(id = mi_idx.movie_id)"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
'''

# Recursive function to parse JOIN information
def parse_plan(plan, results, step=1):
    if "Node Type" in plan:
        if "Join Type" in plan:  # Identify JOIN nodes
            join_info = {
                "Step": step,  # Record the step number
                "Join Type": plan["Join Type"],  # Type of the join (e.g., Inner, Hash)
                "Left": get_relation_name(plan["Plans"][0]),  # Extract the left input relation
                "Right": get_relation_name(plan["Plans"][1]),  # Extract the right input relation
                "Condition": plan.get("Hash Cond") or plan.get("Join Filter") or plan.get("Index Cond")  # Extract join condition
            }
            results.append(join_info)  # Add the join information to results
            step += 1  # Increment the step count

    # If the plan has sub-nodes (Plans), process them recursively
    if "Plans" in plan:
        for sub_plan in plan["Plans"]:
            step = parse_plan(sub_plan, results, step)  # Recursively parse child plans
    return step  # Return the current step count

# Function to extract relation or node name
def get_relation_name(plan):
    if "Relation Name" in plan:  # Use "Relation Name" if available
        return plan["Relation Name"]
    elif "Node Type" in plan:  # Fallback to "Node Type" if no relation name
        return plan["Node Type"]
    return "unknown"  # Default to "unknown" if neither is available

# Main function
results = []  # List to store parsed join information
parse_plan(json.loads(execution_plan_json)["Plan"], results)  # Parse the plan recursively

# Output the parsed JOIN information in JSON format
print(json.dumps(results, indent=2))

