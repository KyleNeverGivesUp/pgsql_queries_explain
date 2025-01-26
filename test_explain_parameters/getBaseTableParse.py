import json
from collections import defaultdict

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
        "ProbeKeys": "status_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 135086,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 24592,
        "Projection": [
            "cc_subject_id",
            "cc_movie_id",
            "cct2_id",
            "cc_status_id"
        ],
        "NumDimLeft": "4",
        "NumDimRight": "1",
        "NumDimOutput": "5"
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
        "ProbeKeys": "subject_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 24592,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 17879,
        "Projection": [
            "cc_subject_id",
            "cc_movie_id",
            "cct1_id"
        ],
        "NumDimLeft": "4",
        "NumDimRight": "1",
        "NumDimOutput": "5"
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
        "ProbeKeys": "movie_id",
        "BuildKeys": "movie_id",
        "NumTuplesLeft": 17879,
        "NumTuplesRight": 0,
        "NumTuplesOutput": 7127,
        "Projection": [
            "cc_movie_id",
            "ci_person_role_id",
            "ci_movie_id",
            "ci_person_id",
            "ci_role_id"
        ],
        "NumDimLeft": "3",
        "NumDimRight": "7",
        "NumDimOutput": "10"
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
        "ProbeKeys": "person_id",
        "BuildKeys": "person_id",
        "NumTuplesLeft": 7127,
        "NumTuplesRight": 2,
        "NumTuplesOutput": 15410,
        "Projection": [
            "cc_movie_id",
            "an_person_id",
            "ci_person_role_id",
            "ci_movie_id",
            "ci_person_id",
            "ci_role_id"
        ],
        "NumDimLeft": "7",
        "NumDimRight": "1",
        "NumDimOutput": "8"
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
        "ProbeKeys": "role_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 15410,
        "NumTuplesRight": 0,
        "NumTuplesOutput": 2729,
        "Projection": [
            "cc_movie_id",
            "an_person_id",
            "ci_person_role_id",
            "ci_movie_id",
            "ci_person_id",
            "rt_id",
            "ci_role_id"
        ],
        "NumDimLeft": "8",
        "NumDimRight": "2",
        "NumDimOutput": "10"
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
        "ProbeKeys": "person_role_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 2729,
        "NumTuplesRight": 0,
        "NumTuplesOutput": 17,
        "Projection": [
            "cc_movie_id",
            "chn_id",
            "an_person_id",
            "ci_person_role_id",
            "ci_movie_id",
            "ci_person_id",
            "chn_name"
        ],
        "NumDimLeft": "7",
        "NumDimRight": "7",
        "NumDimOutput": "14"
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
        "ProbeKeys": "person_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 17,
        "NumTuplesRight": 0,
        "NumTuplesOutput": 8,
        "Projection": [
            "cc_movie_id",
            "n_name",
            "an_person_id",
            "ci_movie_id",
            "ci_person_id",
            "n_id",
            "chn_name"
        ],
        "NumDimLeft": "7",
        "NumDimRight": "9",
        "NumDimOutput": "16"
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
        "ProbeKeys": "person_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 17,
        "NumTuplesRight": 0,
        "NumTuplesOutput": 8,
        "Projection": [
            "cc_movie_id",
            "n_name",
            "an_person_id",
            "ci_movie_id",
            "ci_person_id",
            "n_id",
            "chn_name"
        ],
        "NumDimLeft": "7",
        "NumDimRight": "9",
        "NumDimOutput": "16"
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
        "ProbeKeys": "movie_id",
        "BuildKeys": "movie_id",
        "NumTuplesLeft": 8,
        "NumTuplesRight": 112,
        "NumTuplesOutput": 894,
        "Projection": [
            "mk_keyword_id",
            "cc_movie_id",
            "n_name",
            "an_person_id",
            "ci_movie_id",
            "ci_person_id",
            "n_id",
            "mk_movie_id",
            "chn_name"
        ],
        "NumDimLeft": "11",
        "NumDimRight": "3",
        "NumDimOutput": "14"
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
        "ProbeKeys": "keyword_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 894,
        "NumTuplesRight": 0,
        "NumTuplesOutput": 8,
        "Projection": [
            "mk_keyword_id",
            "cc_movie_id",
            "n_name",
            "an_person_id",
            "k_id",
            "ci_movie_id",
            "ci_person_id",
            "n_id",
            "mk_movie_id",
            "chn_name"
        ],
        "NumDimLeft": "11",
        "NumDimRight": "1",
        "NumDimOutput": "12"
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
        "ProbeKeys": "movie_id",
        "BuildKeys": "movie_id",
        "NumTuplesLeft": 8,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 6,
        "Projection": [
            "mi_movie_id",
            "cc_movie_id",
            "n_name",
            "an_person_id",
            "ci_movie_id",
            "ci_person_id",
            "mi_info_type_id",
            "n_id",
            "mk_movie_id",
            "chn_name"
        ],
        "NumDimLeft": "10",
        "NumDimRight": "5",
        "NumDimOutput": "15"
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
        "ProbeKeys": "movie_id",
        "BuildKeys": "movie_id",
        "NumTuplesLeft": 8,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 6,
        "Projection": [
            "mi_movie_id",
            "cc_movie_id",
            "n_name",
            "an_person_id",
            "ci_movie_id",
            "ci_person_id",
            "mi_info_type_id",
            "n_id",
            "mk_movie_id",
            "chn_name"
        ],
        "NumDimLeft": "10",
        "NumDimRight": "5",
        "NumDimOutput": "15"
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
        "ProbeKeys": "person_id",
        "BuildKeys": "person_id",
        "NumTuplesLeft": 6,
        "NumTuplesRight": 163,
        "NumTuplesOutput": 978,
        "Projection": [
            "mi_movie_id",
            "pi_info_type_id",
            "cc_movie_id",
            "an_person_id",
            "chn_name",
            "ci_movie_id",
            "mi_info_type_id",
            "mk_movie_id",
            "n_name",
            "pi_person_id"
        ],
        "NumDimLeft": "14",
        "NumDimRight": "5",
        "NumDimOutput": "19"
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
        "ProbeKeys": "id",
        "BuildKeys": "person_id",
        "NumTuplesLeft": 6,
        "NumTuplesRight": 163,
        "NumTuplesOutput": 978,
        "Projection": [
            "mi_movie_id",
            "pi_info_type_id",
            "cc_movie_id",
            "an_person_id",
            "chn_name",
            "ci_movie_id",
            "mi_info_type_id",
            "mk_movie_id",
            "n_id",
            "n_name",
            "pi_person_id"
        ],
        "NumDimLeft": "14",
        "NumDimRight": "5",
        "NumDimOutput": "19"
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
        "ProbeKeys": "info_type_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 978,
        "NumTuplesRight": 0,
        "NumTuplesOutput": 324,
        "Projection": [
            "it3_id",
            "mi_movie_id",
            "pi_info_type_id",
            "cc_movie_id",
            "chn_name",
            "ci_movie_id",
            "mi_info_type_id",
            "mk_movie_id",
            "n_name"
        ],
        "NumDimLeft": "12",
        "NumDimRight": "2",
        "NumDimOutput": "14"
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
        "ProbeKeys": "info_type_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 324,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 324,
        "Projection": [
            "mi_movie_id",
            "cc_movie_id",
            "it_id",
            "chn_name",
            "ci_movie_id",
            "mi_info_type_id",
            "mk_movie_id",
            "n_name"
        ],
        "NumDimLeft": "9",
        "NumDimRight": "2",
        "NumDimOutput": "11"
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
        "ProbeKeys": "movie_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 324,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 324,
        "Projection": [
            "mi_movie_id",
            "cc_movie_id",
            "t_title",
            "chn_name",
            "ci_movie_id",
            "t_id",
            "mk_movie_id",
            "n_name"
        ],
        "NumDimLeft": "8",
        "NumDimRight": "12",
        "NumDimOutput": "20"
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
        "ProbeKeys": "movie_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 324,
        "NumTuplesRight": 1,
        "NumTuplesOutput": 324,
        "Projection": [
            "mi_movie_id",
            "cc_movie_id",
            "t_title",
            "chn_name",
            "ci_movie_id",
            "t_id",
            "mk_movie_id",
            "n_name"
        ],
        "NumDimLeft": "8",
        "NumDimRight": "12",
        "NumDimOutput": "20"
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
        "ProbeKeys": "movie_id",
        "BuildKeys": "movie_id",
        "NumTuplesLeft": 324,
        "NumTuplesRight": 22,
        "NumTuplesOutput": 7128,
        "Projection": [
            "mc_movie_id",
            "t_title",
            "chn_name",
            "mc_company_id",
            "mk_movie_id",
            "n_name"
        ],
        "NumDimLeft": "12",
        "NumDimRight": "5",
        "NumDimOutput": "17"
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
        "ProbeKeys": "id",
        "BuildKeys": "movie_id",
        "NumTuplesLeft": 324,
        "NumTuplesRight": 22,
        "NumTuplesOutput": 7128,
        "Projection": [
            "mc_movie_id",
            "t_title",
            "chn_name",
            "mc_company_id",
            "t_id",
            "mk_movie_id",
            "n_name"
        ],
        "NumDimLeft": "12",
        "NumDimRight": "5",
        "NumDimOutput": "17"
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
        "ProbeKeys": "company_id",
        "BuildKeys": "id",
        "NumTuplesLeft": 7128,
        "NumTuplesRight": 0,
        "NumTuplesOutput": 1620,
        "Projection": [
            "cn_id",
            "t_title",
            "chn_name",
            "mc_company_id",
            "n_name"
        ],
        "NumDimLeft": "8",
        "NumDimRight": "7",
        "NumDimOutput": "15"
    }
]
'''


if __name__ == "__main__":

    data = json.loads(input_data)

    # initiate dics
    alias_to_table = {}
    projections_mapping = {}

    # traverse alias and table_name
    for item in data:
        alias_to_table[item["Left_Alias"]] = item["Left_Table_Name"]
        alias_to_table[item["Right_Alias"]] = item["Right_Table_Name"]

        # traverse Projection cols
        for projection in item["Projection"]:
            alias = projection.split("_")[0]  # pick up alias
            if alias not in projections_mapping:
                projections_mapping[alias] = set()
            projections_mapping[alias].add(projection)

    # sort alias_to_table
    sorted_alias_to_table = dict(sorted(alias_to_table.items(), key=lambda x: x[1]))

    output_code = []
    for alias, table in sorted_alias_to_table.items():
        # Add alias_features
        projections = sorted(projections_mapping.get(alias, []))
        projections_with_features = [f"{'_'.join(col.split('_')[1:])} as {col}" for col in projections] + [f"{alias}_features"]
        projections_with_features_noas = [f"{col}" for col in projections] + [f"{alias}_features"]


        # Generate cpp code
        code = f"""
        auto {alias}_a = PlanBuilder(planNodeIdGenerator, pool_.get())
                        .values({{tableName2RowVector["{table}"]}})
                        .project({{{','.join(f'"{proj}"' for proj in projections_with_features)}}});
        tabel2Columns["{alias}"] = {{{','.join(f'"{proj}"' for proj in projections_with_features_noas)}}};
        sources["{alias}"] = {alias}_a;
        """
        output_code.append(code.strip())

    print("\n\n".join(output_code))