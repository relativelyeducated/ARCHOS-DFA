#!/usr/bin/env python3
"""
Constitutional Republic DFA (Decline-Failure-Autocracy) Cycle Analysis
Comparing historical republics to current US trajectory
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3

# ============================================================================
# DATASET 1: Historical Republics - Core Data
# ============================================================================

republics_data = {
    'Republic': [
        'Roman Republic',
        'Venetian Republic',
        'Florentine Republic',
        'Dutch Republic',
        'French First Republic',
        'French Third Republic',
        'French Fourth Republic',
        'Weimar Republic',
        'United States'
    ],
    'Start_Year': [509, 697, 1115, 1588, 1792, 1870, 1946, 1919, 1789],
    'End_Year': [-27, 1797, 1532, 1795, 1804, 1940, 1958, 1933, None],
    'Duration_Years': [482, 1100, 417, 207, 12, 70, 12, 14, 236],
    'Population_Peak_Millions': [4.0, 0.2, 0.1, 2.0, 28.0, 40.0, 42.0, 65.0, 334.0],
    'Government_Type': [
        'Mixed Republic',
        'Oligarchic Republic',
        'Mixed Republic',
        'Federal Republic',
        'Revolutionary Republic',
        'Parliamentary Republic',
        'Parliamentary Republic',
        'Parliamentary Republic',
        'Constitutional Federal Republic'
    ],
    'End_Type': [
        'Empire',
        'Dissolved/Conquered',
        'Hereditary Duchy',
        'Conquered/Reformed',
        'Empire',
        'Occupied/Authoritarian',
        'Constitutional Reform',
        'Totalitarian Dictatorship',
        'Active'
    ]
}

df_republics = pd.DataFrame(republics_data)

# Calculate current age for US
current_year = 2025
df_republics.loc[df_republics['Republic'] == 'United States', 'Duration_Years'] = current_year - 1789

# ============================================================================
# DATASET 2: DFA Cycle Stages by Republic
# ============================================================================

dfa_stages_data = {
    'Republic': [
        'Roman Republic', 'Roman Republic', 'Roman Republic', 'Roman Republic', 'Roman Republic',
        'Venetian Republic', 'Venetian Republic', 'Venetian Republic', 'Venetian Republic', 'Venetian Republic',
        'Weimar Republic', 'Weimar Republic', 'Weimar Republic', 'Weimar Republic', 'Weimar Republic',
        'French Third Republic', 'French Third Republic', 'French Third Republic', 'French Third Republic', 'French Third Republic',
        'United States', 'United States', 'United States', 'United States'
    ],
    'Stage': [
        'Stability', 'Inequality Growth', 'Institutional Erosion', 'Violence Normalization', 'Autocratic Transition',
        'Stability', 'Inequality Growth', 'Institutional Erosion', 'Violence Normalization', 'Autocratic Transition',
        'Stability', 'Inequality Growth', 'Institutional Erosion', 'Violence Normalization', 'Autocratic Transition',
        'Stability', 'Inequality Growth', 'Institutional Erosion', 'Violence Normalization', 'Autocratic Transition',
        'Stability', 'Inequality Growth', 'Institutional Erosion', 'Current Stage'
    ],
    'Stage_Number': [
        1, 2, 3, 4, 5,
        1, 2, 3, 4, 5,
        1, 2, 3, 4, 5,
        1, 2, 3, 4, 5,
        1, 2, 3, 3
    ],
    'Approximate_Year_Start': [
        -509, -133, -100, -88, -27,
        697, 1500, 1700, None, 1797,
        1919, 1923, 1929, 1932, 1933,
        1870, 1920, 1934, 1940, 1940,
        1789, 1970, 2000, 2020
    ],
    'Duration_Years': [
        376, 33, 12, 61, None,
        803, 200, 97, None, None,
        4, 6, 3, 1, None,
        50, 14, 6, 0, None,
        181, 30, 20, 5
    ],
    'Key_Indicators': [
        'Expansion, civic virtue, institutions strong',
        'Post-Punic War inequality, Gracchi reforms, land crisis',
        'Political violence, private armies, Marius/Sulla conflicts',
        'Civil wars, proscriptions, triumvirates',
        'Augustus becomes Emperor',
        'Trade dominance, stable oligarchy, Great Council functions',
        'Economic stagnation begins, hereditary rigidity increases',
        'Trade routes shift, Ottoman pressure, constitutional inflexibility',
        'External conquest imminent',
        'Napoleon forces dissolution May 12, 1797',
        'Post-WWI instability, Versailles resentment',
        'Hyperinflation: bread 1 mark → 100 billion marks',
        'Great Depression, 30% unemployment, extremism rises',
        'Street violence, SA/SS vs Communists, democracy breakdown',
        'Hitler appointed Chancellor Jan 30, Enabling Act March 1933',
        'Post Franco-Prussian War stability',
        'Economic strain, political instability, weak executives',
        'Constitutional crisis, rapid government turnover',
        'German invasion and occupation',
        'Vichy collaboration',
        'Founding through post-WWII prosperity',
        'Wage stagnation, inequality rise, dual-income necessity',
        'Polarization, norm erosion, inequality peak, perpetual wars',
        'Institutional stress, political violence increase'
    ]
}

df_dfa_stages = pd.DataFrame(dfa_stages_data)

# ============================================================================
# DATASET 3: Economic Indicators - Inequality & Labor
# ============================================================================

us_economic_data = {
    'Year': [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020],
    'Women_Labor_Force_Participation_Pct': [33.9, 37.7, 43.3, 51.5, 57.5, 59.9, 58.6, 57.4],
    'Dual_Income_Households_Pct': [None, None, 39, None, None, 57, 60, 62],
    'Real_Wage_Index_Male_1970_100': [None, None, 100, 98, 92, 95, 88, 90],
    'Gini_Coefficient': [0.386, 0.368, 0.394, 0.403, 0.428, 0.462, 0.469, 0.485],
    'Top_1_Pct_Income_Share': [10.0, 8.4, 8.0, 8.5, 13.9, 16.5, 18.3, 20.5],
    'House_Price_to_Income_Ratio': [1.8, 2.0, 2.2, 2.8, 3.2, 4.0, 4.5, 4.7],
    'Median_Household_Income_2020_Dollars': [None, 38000, 50000, 48500, 54600, 62500, 60000, 67500]
}

df_us_economic = pd.DataFrame(us_economic_data)

# ============================================================================
# DATASET 4: Constitutional Safeguards - Status
# ============================================================================

safeguards_data = {
    'Safeguard': [
        'No Standing Army',
        'No Foreign Entanglements',
        'Congress Declares War',
        'Electoral College Filter',
        'Senate Appointed by States',
        'Separation of Powers',
        'Checks and Balances',
        'Federalism (State Rights)',
        'Bill of Rights',
        'No Titles of Nobility',
        'Supermajority Requirements',
        'Impeachment Power',
        'Limited Federal Powers',
        'Protection Against Factions',
        'Judicial Review'
    ],
    'Founding_Intent': [
        'Citizen militia, prevent tyranny',
        'Avoid foreign wars and influence',
        'Prevent executive military adventurism',
        'Insulate from mob rule',
        'State sovereignty representation',
        'Prevent power concentration',
        'Ambition counteract ambition',
        'Dual sovereignty protection',
        'Protect minority rights',
        'Prevent aristocracy',
        'Protect against simple majority tyranny',
        'Remove corrupt executives',
        'Enumerated powers only',
        'Large republic prevents faction dominance',
        'Judicial check on legislature'
    ],
    'Historical_Lesson': [
        'Rome: Dictators with armies',
        'Rome/Venice: Imperial overreach',
        'Rome: Generals become emperors',
        'Athens: Mob rule, Socrates',
        'Venice: Oligarchy rigidity',
        'Rome: Power consolidation',
        'All: Single-branch dominance',
        'Rome: Centralization bred corruption',
        'Athens: Tyranny of majority',
        'Venice/Florence: Hereditary control',
        'Rome: Populist reforms',
        'Rome: No mechanism to remove dictator',
        'Rome: Imperial expansion unchecked',
        'All: Faction violence',
        'No classical equivalent'
    ],
    'Current_Status_2025': [
        'FAILED',
        'FAILED',
        'SIGNIFICANTLY ERODED',
        'ERODED',
        'FAILED (17th Amendment 1913)',
        'STRAINED',
        'WEAKENED',
        'ERODED',
        'HOLDING',
        'HOLDING',
        'HOLDING',
        'HOLDING BUT PARTISAN',
        'FAILED',
        'FAILED',
        'HOLDING BUT CONTESTED'
    ],
    'Erosion_Score_0_10': [10, 10, 7, 6, 10, 4, 5, 6, 2, 1, 2, 3, 8, 9, 3]
}

df_safeguards = pd.DataFrame(safeguards_data)

# Average erosion score
average_erosion = df_safeguards['Erosion_Score_0_10'].mean()

# ============================================================================
# DATASET 5: Warning Indicators - Multi-Republic Comparison
# ============================================================================

warning_indicators_data = {
    'Indicator': [
        'Income Inequality (Gini)',
        'Wealth Concentration (Top 1%)',
        'Political Polarization',
        'Political Violence',
        'Institutional Trust',
        'Foreign Military Bases',
        'Perpetual Wars',
        'Standing Army Size',
        'Debt to GDP Ratio',
        'Constitutional Crises',
        'Norm Violations',
        'Demagogue Appeal',
        'Media Fragmentation',
        'Civic Virtue Decline'
    ],
    'Roman_Republic_Late': [9, 10, 10, 10, 3, 8, 9, 8, 7, 9, 10, 10, 5, 9],
    'Weimar_Republic_Late': [7, 6, 10, 10, 2, 3, 7, 6, 10, 10, 9, 10, 8, 8],
    'Venetian_Republic_Late': [6, 8, 6, 4, 5, 5, 6, 5, 7, 8, 7, 5, 4, 7],
    'French_Third_Late': [6, 7, 9, 7, 4, 6, 8, 7, 8, 8, 7, 7, 6, 7],
    'United_States_2025': [9, 9, 9, 6, 4, 10, 9, 10, 9, 7, 8, 7, 9, 7]
}

df_warning_indicators = pd.DataFrame(warning_indicators_data)

# Calculate average scores
df_warning_indicators['Average_Failed_Republics'] = df_warning_indicators[
    ['Roman_Republic_Late', 'Weimar_Republic_Late', 'Venetian_Republic_Late', 'French_Third_Late']
].mean(axis=1)

# ============================================================================
# DATASET 6: US Timeline - Key Events
# ============================================================================

us_timeline_data = {
    'Year': [
        1789, 1860, 1913, 1917, 1929, 1941, 1950, 1963, 1968, 1970, 1971, 1973,
        1980, 1989, 2001, 2008, 2016, 2020, 2021, 2024
    ],
    'Event': [
        'Constitution Ratified',
        'Civil War Begins',
        '17th Amendment (Direct Senate Election)',
        'WWI Entry',
        'Great Depression Begins',
        'WWII Entry',
        'Korean War / Women 34% Labor Force',
        'JFK Assassination',
        'MLK/RFK Assassinations, Riots',
        'Nixon/Wage Stagnation Begins',
        'Nixon Shock (Gold Standard Ends)',
        'Roe v. Wade',
        'Reagan Revolution Begins',
        'Cold War Ends',
        '9/11 / Patriot Act / Forever Wars',
        'Financial Crisis / Great Recession',
        'Trump Election / Political Polarization Peak',
        'COVID-19 Pandemic',
        'Capitol Riot Jan 6',
        'Political Instability Continues'
    ],
    'DFA_Stage': [
        1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3
    ],
    'Institutional_Trust_Score': [
        9, 7, 8, 9, 7, 10, 9, 8, 6, 7, 6, 6, 7, 7, 6, 5, 4, 3, 3, 3
    ],
    'Political_Violence_Score': [
        1, 10, 2, 3, 3, 2, 1, 4, 7, 3, 2, 2, 2, 1, 4, 2, 4, 3, 8, 5
    ]
}

df_us_timeline = pd.DataFrame(us_timeline_data)

# ============================================================================
# DATASET 7: Founder Warnings - Prophecy Check
# ============================================================================

founder_warnings_data = {
    'Founder': [
        'George Washington',
        'George Washington',
        'James Madison',
        'James Madison',
        'James Madison',
        'Thomas Jefferson',
        'Benjamin Franklin',
        'John Adams',
        'Alexander Hamilton'
    ],
    'Warning': [
        'Beware political parties',
        'Avoid foreign entanglements',
        'Standing armies threaten liberty',
        'War is parent of armies, debts, inequality',
        'Inequality has malignant aspect',
        'Tree of liberty needs periodic refreshing',
        'A republic, if you can keep it',
        'Constitution only for moral people',
        'Your republic is a young maiden'
    ],
    'Year_Warned': [1796, 1796, 1795, 1795, 1792, 1787, 1787, 1798, 1802],
    'Current_Status_2025': [
        'HAPPENED - Two-party duopoly extreme',
        'HAPPENED - 800+ bases, perpetual wars',
        'HAPPENED - Largest military in history',
        'HAPPENED - $35T debt, forever wars, inequality peak',
        'HAPPENED - Gini 0.485, highest since Gilded Age',
        'UNCLEAR - No revolution yet',
        'QUESTIONED - Republic under strain',
        'DEBATED - Civic virtue decline observed',
        'ONGOING - Republic survival uncertain'
    ],
    'Prophecy_Accuracy_Score': [10, 10, 10, 10, 10, 5, 8, 7, 8]
}

df_founder_warnings = pd.DataFrame(founder_warnings_data)

# ============================================================================
# SAVE TO SQLite DATABASE
# ============================================================================

db_path = '/home/king/Aiscrub/data_lake/republic_dfa_analysis.db'
conn = sqlite3.connect(db_path)

# Save all dataframes to database
df_republics.to_sql('republics_core', conn, if_exists='replace', index=False)
df_dfa_stages.to_sql('dfa_cycle_stages', conn, if_exists='replace', index=False)
df_us_economic.to_sql('us_economic_indicators', conn, if_exists='replace', index=False)
df_safeguards.to_sql('constitutional_safeguards', conn, if_exists='replace', index=False)
df_warning_indicators.to_sql('warning_indicators', conn, if_exists='replace', index=False)
df_us_timeline.to_sql('us_timeline', conn, if_exists='replace', index=False)
df_founder_warnings.to_sql('founder_warnings', conn, if_exists='replace', index=False)

conn.close()

# ============================================================================
# SAVE TO CSV FILES
# ============================================================================

df_republics.to_csv('/home/king/Aiscrub/processed_files/republics_core.csv', index=False)
df_dfa_stages.to_csv('/home/king/Aiscrub/processed_files/dfa_cycle_stages.csv', index=False)
df_us_economic.to_csv('/home/king/Aiscrub/processed_files/us_economic_indicators.csv', index=False)
df_safeguards.to_csv('/home/king/Aiscrub/processed_files/constitutional_safeguards.csv', index=False)
df_warning_indicators.to_csv('/home/king/Aiscrub/processed_files/warning_indicators.csv', index=False)
df_us_timeline.to_csv('/home/king/Aiscrub/processed_files/us_timeline.csv', index=False)
df_founder_warnings.to_csv('/home/king/Aiscrub/processed_files/founder_warnings.csv', index=False)

# ============================================================================
# GENERATE SUMMARY REPORT
# ============================================================================

print("=" * 80)
print("CONSTITUTIONAL REPUBLIC DFA CYCLE ANALYSIS")
print("Dataset Generation Complete")
print("=" * 80)
print()

print("📊 DATASETS CREATED:")
print(f"  1. Republics Core Data: {len(df_republics)} republics")
print(f"  2. DFA Cycle Stages: {len(df_dfa_stages)} stage records")
print(f"  3. US Economic Indicators: {len(df_us_economic)} time periods")
print(f"  4. Constitutional Safeguards: {len(df_safeguards)} safeguards")
print(f"  5. Warning Indicators: {len(df_warning_indicators)} indicators")
print(f"  6. US Timeline Events: {len(df_us_timeline)} events")
print(f"  7. Founder Warnings: {len(df_founder_warnings)} prophecies")
print()

print("📈 KEY FINDINGS:")
print()

print("AVERAGE REPUBLIC LIFESPAN:")
failed_republics = df_republics[df_republics['End_Year'].notna() & (df_republics['Republic'] != 'United States')]
avg_lifespan = failed_republics['Duration_Years'].mean()
print(f"  Failed Republics Average: {avg_lifespan:.0f} years")
print(f"  US Current Age: {current_year - 1789} years")
print(f"  Comparison: US is {((current_year - 1789) / avg_lifespan * 100):.0f}% of average failed republic lifespan")
print()

print("CONSTITUTIONAL SAFEGUARD EROSION:")
print(f"  Average Erosion Score: {average_erosion:.1f}/10")
print(f"  Failed Safeguards: {len(df_safeguards[df_safeguards['Current_Status_2025'] == 'FAILED'])}/15")
print(f"  Holding Safeguards: {len(df_safeguards[df_safeguards['Current_Status_2025'] == 'HOLDING'])}/15")
print()

print("WARNING INDICATORS - US vs Historical Average:")
for idx, row in df_warning_indicators.iterrows():
    indicator = row['Indicator']
    us_score = row['United_States_2025']
    avg_failed = row['Average_Failed_Republics']
    diff = us_score - avg_failed
    status = "⚠️ HIGHER" if diff > 1 else "✓ LOWER" if diff < -1 else "≈ SIMILAR"
    print(f"  {indicator:30s}: {us_score}/10 vs {avg_failed:.1f}/10 [{status}]")
print()

print("FOUNDER PROPHECY ACCURACY:")
avg_prophecy = df_founder_warnings['Prophecy_Accuracy_Score'].mean()
print(f"  Average Accuracy: {avg_prophecy:.1f}/10")
print(f"  Warnings that came true: {len(df_founder_warnings[df_founder_warnings['Prophecy_Accuracy_Score'] >= 8])}/{len(df_founder_warnings)}")
print()

print("DFA CYCLE ASSESSMENT:")
print(f"  Current US Stage: Stage 3 (Institutional Erosion)")
print(f"  Time in Stage 3: ~20-25 years (2000-2025)")
print(f"  Historical Pattern: Stage 3 duration varies 6-97 years before Stage 4")
print()

print("=" * 80)
print("📁 FILES SAVED:")
print("  Database: /home/king/Aiscrub/data_lake/republic_dfa_analysis.db")
print("  CSV Files: /home/king/Aiscrub/processed_files/*.csv")
print("=" * 80)
