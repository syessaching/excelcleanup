import pandas as pd


def combineColumns():
    main_df = pd.read_excel('Copy_BYUHFirst-timeFreshmenCohortsforRetention.xlsx', sheet_name='Consolidated ', dtype={'Person ID':str})
    other_df = pd.read_excel('Copy_BYUHFirst-timeFreshmenCohortsforRetention.xlsx', sheet_name='Copy 2225 Cohort', dtype={'Person ID':str})
    other_df['Person ID'] = other_df['Person ID'].astype(str).str.zfill(9)
    other_df['ID'] = other_df['ID'].astype(str).str.zfill(7)  



    for col in main_df.columns:
        if col not in other_df.columns:
            other_df[col]=pd.NA

    other_df = other_df[main_df.columns]

    other_df.to_excel('FTFretention.xlsx', index=False)
# combineColumns()

def fillChurchHomeArea(row):
    home_area = row['Home Area']
    country = row ['Final Country']

    if home_area == 'Hawaii':
        return 'Hawaii'
    elif home_area in ['US Mainland', 'USA']:
        return 'US Continent'
    elif home_area=='Other International':
        return 'Other International'
    elif home_area == 'Pacific':
        if country in ['Guam', 'Northern Mariana Islands', 'Palau']:
            return 'Asia North'
        else:
            return 'Pacific'

    elif home_area == 'Asia':
        if country == 'Philippines':
            return 'Philippines'
        elif country in ['Japan', 'Korea', 'Republic of', 'Mongolia']:
            return 'Asia North'
        else: 
            return 'Asia'
        
    else:
        return 'Unknown'
    
def fillAgeGroup(row):
    age = int(row ['Short Age'])
    if pd.isna(age):
        return 'Age Unknown'
    age = int(age)

    if age < 18:
        return 'Under 18'
    elif 18 <= age <=19:
        return '18-19'
    elif 20 <= age <=21:
        return '20-21'
    elif 22 <= age <=24:
        return '22-24'
    elif 25 <= age <=29:
        return '25-29'
    elif age >29:
        return 'Over 29'
    else :
        return 'Age Unknown'
    

def checkCredit(row):
    try:
        credit = float(row['Take Prgrs'])
        if credit < 12:
            return 'Part-time'
        else:
            return 'Full-time'
    except:
        return 'Unknown'

def fillingValues():
    main_df = pd.read_excel('Copy_BYUHFirst-timeFreshmenCohortsforRetention.xlsx', sheet_name='Copy 2225 Cohort')
    df = pd.read_excel('FTFretention.xlsx', dtype={'Person ID': str})

    df['ID'] = df['ID'].astype(str)
    main_df['ID'] = main_df['ID'].astype(str)

    # Convert to numeric first, keep track of errors
    df['Birthdate_raw'] = pd.to_numeric(df['Birthdate'], errors='coerce')
    df['Census_raw'] = pd.to_numeric(df['Census Date'], errors='coerce')

    df['Birthdate'] = pd.to_datetime(df['Birthdate_raw'], unit='D', origin='1899-12-30', errors='coerce')
    df['Census Date'] = pd.to_datetime(df['Census_raw'], unit='D', origin='1899-12-30', errors='coerce')

    df['Cohort Year'] = df['Cohort Year'].fillna(2022)
    df['Retention Year'] = df['Retention Year'].fillna(2023)
    df['Cohort Acad Year'] = df['Cohort Acad Year'].fillna('2022-23')
    df['Degree seeking?'] = df['Degree seeking?'].fillna('Degree Seeking')

    df['1 year Outcome'] = df['ID'].map(main_df.set_index('ID')['1 Year Outcome'])
    df['Still Enrolled'] = (df['1 year Outcome'] == 'Still Enrolled').astype(int)
    df['Exclusion'] = (df['1 year Outcome'] == 'Exclusion').astype(int)
    df['Transfer'] = (df['1 year Outcome'] == 'Transfer').astype(int)
    df['No Outcome'] = df['1 year Outcome'].isna().astype(int)

    df['Final Country'] = df['Home Country'].fillna(df['Country'])
    df['Final Country'] = df['Final Country'].fillna(df['Home Area'])

    # Prevent apply errors by replacing missing strings with "Unknown"
    df['Home Area'] = df['Home Area'].fillna('Unknown')
    df['Final Country'] = df['Final Country'].fillna('Unknown')

    df['Church/Home Area'] = df.apply(fillChurchHomeArea, axis=1)

    df['Short Age'] = pd.to_numeric(df['Short Age'], errors='coerce')
    df['Age Group'] = df.apply(fillAgeGroup, axis=1)

    df['Take Prgrs'] = pd.to_numeric(df['Take Prgrs'], errors='coerce')
    df['Credit Load'] = df.apply(checkCredit, axis=1)
    df['ID#'] = pd.to_numeric(df['ID'], errors='coerce').fillna(0).astype(int)

    df.to_excel('FTFretention_filled.xlsx', index=False)

fillingValues()