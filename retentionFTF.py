import pandas as pd


def combineColumns():
    main_df = pd.read_excel('Copy_BYUHFirst-timeFreshmenCohortsforRetention.xlsx', sheet_name='Consolidated ', dtype={'Person ID':str})
    other_df = pd.read_excel('Copy_BYUHFirst-timeFreshmenCohortsforRetention.xlsx', sheet_name='Copy 2225 Cohort', dtype={'Person ID':str})
    other_df['Person ID'] = other_df['Person ID'].astype(str).str.zfill(9)
    other_df['ID'] = other_df['ID'].astype(str).str.zfill(7)  # or however long they should be



    for col in main_df.columns:
        if col not in other_df.columns:
            other_df[col]=pd.NA

    other_df = other_df[main_df.columns]

    other_df.to_excel('FTFretention.xlsx', index=False)
# combineColumns()

def fillingValues():
    main_df = pd.read_excel('Copy_BYUHFirst-timeFreshmenCohortsforRetention.xlsx', sheet_name='Copy 2225 Cohort')
    df= pd.read_excel('FTFretention.xlsx', dtype={'Person ID': str})

    df['ID'] = df['ID'].astype(str)
    main_df['ID']=main_df['ID'].astype(str)


    df['Cohort Year']= df['Cohort Year'].fillna(2022)
    df['Retention Year'] = df['Retention Year'].fillna(2023)
    df['Cohort Acad Year'] = df['Cohort Acad Year'].fillna('2022-23')
    df['ID#'] = df['ID']
    
    df['1 year Outcome'] =df['ID'].map(main_df.set_index('ID')['1 Year Outcome'])


    df['Still Enrolled'] = (df['1 year Outcome']=='Still Enrolled' ).astype(int)
    df['Exclusion'] = (df['1 year Outcome']== 'Exclusion').astype(int)
    df['Transfer'] = (df['1 year Outcome']=='Transfer').astype(int)
    df['No Outcome']= df['1 year Outcome'].isna().astype(int)
    

    df.to_excel('FTFretention_filled.xlsx', index=False)

fillingValues()