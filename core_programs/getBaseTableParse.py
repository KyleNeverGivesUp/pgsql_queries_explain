import json

input_data = '''
[
    {
        "ID": "0",
        "Left": "cc",
        "Right": "cct2",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "comp_cast_type",
        "Left_Alias": "cc",
        "Right_Alias": "cct2",
        "Pred": "cc.status_id = cct2.id",
        "ProbeKeys": "cc.status_id",
        "BuildKeys": "cct2.id",
        "NumTuplesLeft": 135086,
        "NumTuplesRight": 4,
        "NumTuplesOutput": 761,
        "Projection": [
            "cc_status_id",
            "cc_subject_id",
            "cc_movie_id",
            "cct2_id",
            "cc_features",
            "cct2_features"
        ],
        "NumDimLeft": "4",
        "NumDimRight": "1",
        "NumDimOutput": "5",
        "Filter": [
            "(cct2.kind) = 'completeverified'"
        ]
    },
    {
        "ID": "1",
        "Left": "0",
        "Right": "cct1",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "comp_cast_type",
        "Left_Alias": "cc",
        "Right_Alias": "cct1",
        "Pred": "cct1.id = cc.subject_id",
        "ProbeKeys": "cc.subject_id",
        "BuildKeys": "cct1.id",
        "NumTuplesLeft": 761,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 4,
        "Projection": [
            "cc_subject_id",
            "cc_movie_id",
            "cct1_id",
            "cc_features",
            "cct1_features"
        ],
        "NumDimLeft": "4",
        "NumDimRight": "1",
        "NumDimOutput": "5",
        "Filter": [
            "(cct1.kind) = 'cast'"
        ]
    },
    {
        "ID": "2",
        "Left": "1",
        "Right": "ci",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "cast_info",
        "Left_Alias": "cc",
        "Right_Alias": "ci",
        "Pred": "ci.movie_id = cc.movie_id",
        "ProbeKeys": "cc.movie_id",
        "BuildKeys": "ci.movie_id",
        "NumTuplesLeft": 4,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 3,
        "Projection": [
            "ci_person_id",
            "ci_movie_id",
            "ci_role_id",
            "cc_movie_id",
            "ci_person_role_id",
            "cc_features",
            "ci_features"
        ],
        "NumDimLeft": "3",
        "NumDimRight": "7",
        "NumDimOutput": "10",
        "Filter": [
            "(ci.note) IN ('(voice)', '(voice) (uncredited)', '(voice: English version)')"
        ]
    },
    {
        "ID": "3",
        "Left": "2",
        "Right": "an",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "aka_name",
        "Left_Alias": "cc",
        "Right_Alias": "an",
        "Pred": "an.person_id = ci.person_id",
        "ProbeKeys": "cc.person_id",
        "BuildKeys": "an.person_id",
        "NumTuplesLeft": 3,
        "NumTuplesRight": 2,
        "NumTuplesOutput": 7,
        "Projection": [
            "an_person_id",
            "ci_person_id",
            "ci_movie_id",
            "ci_role_id",
            "cc_movie_id",
            "ci_person_role_id",
            "cc_features",
            "an_features"
        ],
        "NumDimLeft": "7",
        "NumDimRight": "1",
        "NumDimOutput": "8",
        "Filter": []
    },
    {
        "ID": "4",
        "Left": "3",
        "Right": "rt",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "role_type",
        "Left_Alias": "cc",
        "Right_Alias": "rt",
        "Pred": "rt.id = ci.role_id",
        "ProbeKeys": "cc.role_id",
        "BuildKeys": "rt.id",
        "NumTuplesLeft": 7,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "rt_id",
            "an_person_id",
            "ci_person_id",
            "ci_movie_id",
            "cc_movie_id",
            "ci_role_id",
            "ci_person_role_id",
            "cc_features",
            "rt_features"
        ],
        "NumDimLeft": "8",
        "NumDimRight": "2",
        "NumDimOutput": "10",
        "Filter": [
            "(rt.role) = 'actress'"
        ]
    },
    {
        "ID": "5",
        "Left": "4",
        "Right": "chn",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "char_name",
        "Left_Alias": "cc",
        "Right_Alias": "chn",
        "Pred": "chn.id = ci.person_role_id",
        "ProbeKeys": "cc.person_role_id",
        "BuildKeys": "chn.id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "an_person_id",
            "ci_person_id",
            "chn_id",
            "ci_movie_id",
            "cc_movie_id",
            "ci_person_role_id",
            "cc_features",
            "chn_features"
        ],
        "NumDimLeft": "7",
        "NumDimRight": "7",
        "NumDimOutput": "14",
        "Filter": [
            "(chn.name) = 'Queen'"
        ]
    },
    {
        "ID": "6",
        "Left": "5",
        "Right": "n",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "name",
        "Left_Alias": "cc",
        "Right_Alias": "n",
        "Pred": "n.id = an.person_id",
        "ProbeKeys": "cc.person_id",
        "BuildKeys": "n.id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "an_person_id",
            "ci_person_id",
            "ci_movie_id",
            "cc_movie_id",
            "n_id",
            "cc_features",
            "n_features"
        ],
        "NumDimLeft": "7",
        "NumDimRight": "9",
        "NumDimOutput": "16",
        "Filter": [
            "((n.name) LIKE '%An%') AND ((n.gender) = 'f')"
        ]
    },
    {
        "ID": "7",
        "Left": "6",
        "Right": "n",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "name",
        "Left_Alias": "cc",
        "Right_Alias": "n",
        "Pred": "ci.person_id = n.id",
        "ProbeKeys": "cc.person_id",
        "BuildKeys": "n.id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "an_person_id",
            "ci_person_id",
            "ci_movie_id",
            "cc_movie_id",
            "n_id",
            "cc_features",
            "n_features"
        ],
        "NumDimLeft": "7",
        "NumDimRight": "9",
        "NumDimOutput": "16",
        "Filter": [
            "((n.name) LIKE '%An%') AND ((n.gender) = 'f')"
        ]
    },
    {
        "ID": "8",
        "Left": "7",
        "Right": "mk",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "movie_keyword",
        "Left_Alias": "cc",
        "Right_Alias": "mk",
        "Pred": "mk.movie_id = ci.movie_id",
        "ProbeKeys": "cc.movie_id",
        "BuildKeys": "mk.movie_id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 47,
        "NumTuplesOutput": 5,
        "Projection": [
            "chn_name",
            "n_name",
            "an_person_id",
            "ci_person_id",
            "mk_movie_id",
            "mk_keyword_id",
            "ci_movie_id",
            "cc_movie_id",
            "n_id",
            "cc_features",
            "mk_features"
        ],
        "NumDimLeft": "11",
        "NumDimRight": "3",
        "NumDimOutput": "14",
        "Filter": []
    },
    {
        "ID": "9",
        "Left": "8",
        "Right": "k",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "keyword",
        "Left_Alias": "cc",
        "Right_Alias": "k",
        "Pred": "k.id = mk.keyword_id",
        "ProbeKeys": "cc.keyword_id",
        "BuildKeys": "k.id",
        "NumTuplesLeft": 5,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "an_person_id",
            "ci_person_id",
            "mk_movie_id",
            "mk_keyword_id",
            "ci_movie_id",
            "cc_movie_id",
            "n_id",
            "k_id",
            "cc_features",
            "k_features"
        ],
        "NumDimLeft": "11",
        "NumDimRight": "1",
        "NumDimOutput": "12",
        "Filter": [
            "(k.keyword) = 'computer-animation'"
        ]
    },
    {
        "ID": "10",
        "Left": "9",
        "Right": "mi",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "movie_info",
        "Left_Alias": "cc",
        "Right_Alias": "mi",
        "Pred": "mi.movie_id = mk.movie_id",
        "ProbeKeys": "cc.movie_id",
        "BuildKeys": "mi.movie_id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "mi_info_type_id",
            "an_person_id",
            "ci_person_id",
            "mk_movie_id",
            "mi_movie_id",
            "ci_movie_id",
            "cc_movie_id",
            "n_id",
            "cc_features",
            "mi_features"
        ],
        "NumDimLeft": "10",
        "NumDimRight": "5",
        "NumDimOutput": "15",
        "Filter": [
            "(mi.info IS NOT NULL) AND (((mi.info) LIKE 'Japan:%200%') OR ((mi.info) LIKE 'USA:%200%'))"
        ]
    },
    {
        "ID": "11",
        "Left": "10",
        "Right": "mi",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "movie_info",
        "Left_Alias": "cc",
        "Right_Alias": "mi",
        "Pred": "ci.movie_id = mi.movie_id",
        "ProbeKeys": "cc.movie_id",
        "BuildKeys": "mi.movie_id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "mi_info_type_id",
            "an_person_id",
            "ci_person_id",
            "mk_movie_id",
            "mi_movie_id",
            "ci_movie_id",
            "cc_movie_id",
            "n_id",
            "cc_features",
            "mi_features"
        ],
        "NumDimLeft": "10",
        "NumDimRight": "5",
        "NumDimOutput": "15",
        "Filter": [
            "(mi.info IS NOT NULL) AND (((mi.info) LIKE 'Japan:%200%') OR ((mi.info) LIKE 'USA:%200%'))"
        ]
    },
    {
        "ID": "12",
        "Left": "11",
        "Right": "pi",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "person_info",
        "Left_Alias": "cc",
        "Right_Alias": "pi",
        "Pred": "pi.person_id = an.person_id",
        "ProbeKeys": "cc.person_id",
        "BuildKeys": "pi.person_id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 26,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "mi_info_type_id",
            "an_person_id",
            "pi_info_type_id",
            "mk_movie_id",
            "pi_person_id",
            "mi_movie_id",
            "ci_movie_id",
            "cc_movie_id",
            "cc_features",
            "pi_features"
        ],
        "NumDimLeft": "14",
        "NumDimRight": "5",
        "NumDimOutput": "19",
        "Filter": []
    },
    {
        "ID": "13",
        "Left": "12",
        "Right": "pi",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "person_info",
        "Left_Alias": "cc",
        "Right_Alias": "pi",
        "Pred": "n.id = pi.person_id",
        "ProbeKeys": "cc.id",
        "BuildKeys": "pi.person_id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 26,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "mi_info_type_id",
            "an_person_id",
            "pi_info_type_id",
            "mk_movie_id",
            "pi_person_id",
            "mi_movie_id",
            "ci_movie_id",
            "cc_movie_id",
            "n_id",
            "cc_features",
            "pi_features"
        ],
        "NumDimLeft": "14",
        "NumDimRight": "5",
        "NumDimOutput": "19",
        "Filter": []
    },
    {
        "ID": "14",
        "Left": "13",
        "Right": "it3",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "info_type",
        "Left_Alias": "cc",
        "Right_Alias": "it3",
        "Pred": "it3.id = pi.info_type_id",
        "ProbeKeys": "cc.info_type_id",
        "BuildKeys": "it3.id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "mi_info_type_id",
            "pi_info_type_id",
            "mk_movie_id",
            "mi_movie_id",
            "ci_movie_id",
            "cc_movie_id",
            "it3_id",
            "cc_features",
            "it3_features"
        ],
        "NumDimLeft": "12",
        "NumDimRight": "2",
        "NumDimOutput": "14",
        "Filter": [
            "(it3.info) = 'trivia'"
        ]
    },
    {
        "ID": "15",
        "Left": "14",
        "Right": "it",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "info_type",
        "Left_Alias": "cc",
        "Right_Alias": "it",
        "Pred": "it.id = mi.info_type_id",
        "ProbeKeys": "cc.info_type_id",
        "BuildKeys": "it.id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "mi_info_type_id",
            "mk_movie_id",
            "it_id",
            "mi_movie_id",
            "ci_movie_id",
            "cc_movie_id",
            "cc_features",
            "it_features"
        ],
        "NumDimLeft": "9",
        "NumDimRight": "2",
        "NumDimOutput": "11",
        "Filter": [
            "(it.info) = 'release dates'"
        ]
    },
    {
        "ID": "16",
        "Left": "15",
        "Right": "t",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "title",
        "Left_Alias": "cc",
        "Right_Alias": "t",
        "Pred": "t.id = mk.movie_id",
        "ProbeKeys": "cc.movie_id",
        "BuildKeys": "t.id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "t_title",
            "t_id",
            "mk_movie_id",
            "mi_movie_id",
            "ci_movie_id",
            "cc_movie_id",
            "cc_features",
            "t_features"
        ],
        "NumDimLeft": "8",
        "NumDimRight": "12",
        "NumDimOutput": "20",
        "Filter": [
            "t.production_year BETWEEN 2000 AND 2010"
        ]
    },
    {
        "ID": "17",
        "Left": "16",
        "Right": "t",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "title",
        "Left_Alias": "cc",
        "Right_Alias": "t",
        "Pred": "mi.movie_id = t.id",
        "ProbeKeys": "cc.movie_id",
        "BuildKeys": "t.id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "t_title",
            "t_id",
            "mk_movie_id",
            "mi_movie_id",
            "ci_movie_id",
            "cc_movie_id",
            "cc_features",
            "t_features"
        ],
        "NumDimLeft": "8",
        "NumDimRight": "12",
        "NumDimOutput": "20",
        "Filter": [
            "t.production_year BETWEEN 2000 AND 2010"
        ]
    },
    {
        "ID": "18",
        "Left": "17",
        "Right": "mc",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "movie_companies",
        "Left_Alias": "cc",
        "Right_Alias": "mc",
        "Pred": "mc.movie_id = mk.movie_id",
        "ProbeKeys": "cc.movie_id",
        "BuildKeys": "mc.movie_id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 5,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "t_title",
            "mc_movie_id",
            "mk_movie_id",
            "mc_company_id",
            "cc_features",
            "mc_features"
        ],
        "NumDimLeft": "12",
        "NumDimRight": "5",
        "NumDimOutput": "17",
        "Filter": []
    },
    {
        "ID": "19",
        "Left": "18",
        "Right": "mc",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "movie_companies",
        "Left_Alias": "cc",
        "Right_Alias": "mc",
        "Pred": "t.id = mc.movie_id",
        "ProbeKeys": "cc.id",
        "BuildKeys": "mc.movie_id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 5,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "t_title",
            "mc_movie_id",
            "t_id",
            "mk_movie_id",
            "mc_company_id",
            "cc_features",
            "mc_features"
        ],
        "NumDimLeft": "12",
        "NumDimRight": "5",
        "NumDimOutput": "17",
        "Filter": []
    },
    {
        "ID": "20",
        "Left": "19",
        "Right": "cn",
        "Left_Table_Name": "complete_cast",
        "Right_Table_Name": "company_name",
        "Left_Alias": "cc",
        "Right_Alias": "cn",
        "Pred": "cn.id = mc.company_id",
        "ProbeKeys": "cc.company_id",
        "BuildKeys": "cn.id",
        "NumTuplesLeft": 1,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 1,
        "Projection": [
            "chn_name",
            "n_name",
            "t_title",
            "cn_id",
            "mc_company_id",
            "cc_features",
            "cn_features"
        ],
        "NumDimLeft": "8",
        "NumDimRight": "7",
        "NumDimOutput": "15",
        "Filter": [
            "(cn.country_code) = '[us]'"
        ]
    }
]
'''

if __name__ == "__main__":

    data = json.loads(input_data)

    # Initialize dictionaries
    alias_to_table = {}
    projections_mapping = {}
    filter_clauses = {}

    # Extract data from JSON
    for item in data:
        alias_to_table[item["Left_Alias"]] = item["Left_Table_Name"]
        alias_to_table[item["Right_Alias"]] = item["Right_Table_Name"]

        # Store the filter clause for alias
        filter_clauses[item["Left_Alias"]] = item.get("Filter", [])
        filter_clauses[item["Right_Alias"]] = item.get("Filter", [])

        # Process Projection columns
        for projection in item["Projection"]:
            if projection.split("_")[1] != "features":
                alias = projection.split("_")[0]  # Extract alias from column name
                if alias not in projections_mapping:
                    projections_mapping[alias] = set()
                projections_mapping[alias].add(projection)

    # Sort alias-to-table mapping by table name
    sorted_alias_to_table = dict(sorted(alias_to_table.items(), key=lambda x: x[1]))

    # Generate output cpp code
    output_code = []
    for alias, table in sorted_alias_to_table.items():
        # Extract projections for the alias
        projections = sorted(projections_mapping.get(alias, []))
        projections_with_features = [f"{'_'.join(col.split('_')[1:])} as {col}" for col in projections] + [
            f"{alias}_features"]
        projections_with_features_noas = [f"{col}" for col in projections] + [f"{alias}_features"]

        # Get the filter clause from input data
        filter_conditions = filter_clauses.get(alias, [])
        filter_clause = f'.filter({" AND ".join(filter_conditions)})' if filter_conditions else ""

        # Construct lines
        lines = [
            f"auto {alias}_a = PlanBuilder(planNodeIdGenerator, pool_.get())",
            f"    .values({{tableName2RowVector[\"{table}\"]}})"
        ]

        # when filter_clause != ""
        if filter_clause:
            lines.append(f"    {filter_clause}")

        # project info comes from projections_with_features
        proj_list = ",".join(f'"{proj}"' for proj in projections_with_features)
        # generate .project(...)
        lines.append(f'    .project({{{proj_list}}});')
        proj_list_noas = ",".join(f'"{proj}"' for proj in projections_with_features_noas)
        lines.append(f'tabel2Columns["{alias}"] = {{{proj_list_noas}}};')
        lines.append(f"sources[\"{alias}\"] = {alias}_a;")

        # concatenate
        code = "\n".join(lines)
        output_code.append(code.strip())

    # Print the generated cpp code
    print("\n\n".join(output_code))
