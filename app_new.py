# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go
# from pathlib import Path
# import folium
# from streamlit_folium import st_folium

# # Page config
# st.set_page_config(
#     page_title="TPS Transit Safety Intelligence",
#     page_icon="🚇",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS - TPS Branding
# st.markdown("""
# <style>
#     .main { background-color: #f5f7fa; }
#     h1 { color: #003366; font-family: 'Arial', sans-serif; font-weight: 700; }
#     h2 { color: #003366; font-family: 'Arial', sans-serif; }
#     h3 { color: #1a4d80; font-family: 'Arial', sans-serif; }
#     .stButton>button { 
#         background-color: #003366; 
#         color: white; 
#         border-radius: 5px;
#         font-weight: 600;
#     }
#     .stButton>button:hover { background-color: #004080; }
#     .metric-card {
#         background-color: white;
#         padding: 20px;
#         border-radius: 10px;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         text-align: center;
#     }
#     .metric-value {
#         font-size: 36px;
#         font-weight: bold;
#         color: #003366;
#     }
#     .metric-label {
#         font-size: 14px;
#         color: #666;
#         margin-top: 5px;
#     }
#     .insight-box {
#         background-color: #e6f2ff;
#         padding: 15px;
#         border-left: 4px solid #003366;
#         border-radius: 5px;
#         margin: 10px 0;
#     }
#     .risk-high { color: #d32f2f; font-weight: bold; }
#     .risk-medium { color: #f57c00; font-weight: bold; }
#     .risk-low { color: #388e3c; font-weight: bold; }
# </style>
# """, unsafe_allow_html=True)

# @st.cache_data
# def load_data():
#     # Try to detect the correct path structure
#     current_dir = Path.cwd()
    
#     # Check if we're in project root or in a subdirectory
#     if (current_dir / 'outputs').exists():
#         output_dir = current_dir / 'outputs'
#         data_dir = current_dir / 'data'
#     elif (current_dir.parent / 'outputs').exists():
#         output_dir = current_dir.parent / 'outputs'
#         data_dir = current_dir.parent / 'data'
#     else:
#         # Try relative path from where streamlit runs
#         output_dir = Path('outputs')
#         data_dir = Path('data')
    
#     data = {}
#     try:
#         # Load from data directory
#         data['stations'] = pd.read_csv(data_dir / '02_master_station_list.csv')
        
#         # Load from outputs directory
#         data['profiles'] = pd.read_csv(output_dir / '05_station_risk_profiles.csv')
#         data['danger_windows'] = pd.read_csv(output_dir / '06_station_danger_windows.csv')
#         data['fifa_stations'] = pd.read_csv(output_dir / '07_fifa_affected_stations.csv')
#         data['fifa_priority'] = pd.read_csv(output_dir / '07_fifa_priority_stations.csv')
        
#         # Try to load FIXED files first, fallback to original names
#         try:
#             data['activity'] = pd.read_csv(output_dir / '09_event_amplification_FIXED.csv')
#         except:
#             data['activity'] = pd.read_csv(output_dir / '09_event_amplification.csv')
        
#         try:
#             data['deployment'] = pd.read_csv(output_dir / '10_fifa_deployment_schedule_UPDATED.csv')
#         except:
#             data['deployment'] = pd.read_csv(output_dir / '10_fifa_deployment_schedule.csv')
        
#         try:
#             data['scenarios'] = pd.read_csv(output_dir / '10_deployment_scenarios_UPDATED.csv')
#         except:
#             data['scenarios'] = pd.read_csv(output_dir / '10_deployment_scenarios.csv')
        
#         # DYNAMIC: Calculate total crimes from station profiles
#         data['total_crimes'] = int(data['profiles']['total_crimes'].sum())
        
#     except Exception as e:
#         st.error(f"Error loading data: {e}")
#         st.error(f"Tried loading from: {output_dir.absolute()}")
#         st.info(f"Current directory: {current_dir.absolute()}")
#         st.info("Make sure you run the app from the project root: streamlit run app.py")
#         return None
    
#     return data

# data = load_data()

# if data is None:
#     st.error("Failed to load data files. Please ensure all analysis files are present.")
#     st.stop()

# # Sidebar Navigation
# st.sidebar.markdown("""
# <div style='text-align: center; padding: 20px 0; background-color: #003366; border-radius: 10px; margin-bottom: 20px;'>
#     <h2 style='color: white; margin: 0;'>🚔 TPS</h2>
#     <p style='color: #ccc; margin: 5px 0 0 0; font-size: 12px;'>Transit Safety</p>
# </div>
# """, unsafe_allow_html=True)

# st.sidebar.title("Navigation")

# page = st.sidebar.radio(
#     "Select View",
#     ["🏠 Executive Dashboard", "📊 Station Analysis", "🎯 FIFA 2026 Deployment", "📈 Data Explorer"]
# )

# # ============================================================================
# # PAGE 1: EXECUTIVE DASHBOARD
# # ============================================================================
# if page == "🏠 Executive Dashboard":
#     st.title("🚇 Transit Safety Intelligence Dashboard")
#     st.markdown("### Toronto Police Service - FIFA 2026 Readiness")
    
#     # Hero KPIs - FULLY DYNAMIC
#     col1, col2, col3, col4 = st.columns(4)
    
#     # DYNAMIC: Get actual crime count from data
#     total_crimes = data['total_crimes']
#     num_stations = len(data['profiles'])
    
#     with col1:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-value">{total_crimes:,}</div>
#             <div class="metric-label">Crimes Analyzed</div>
#             <div class="metric-label" style="font-size:11px">2018-2025</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-value">{num_stations}</div>
#             <div class="metric-label">Stations Monitored</div>
#             <div class="metric-label" style="font-size:11px">TTC + GO Transit</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">8</div>
#             <div class="metric-label">Years of Data</div>
#             <div class="metric-label" style="font-size:11px">Historical Patterns</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col4:
#         st.markdown("""
#         <div class="metric-card">
#             <div class="metric-value">6</div>
#             <div class="metric-label">FIFA Matches</div>
#             <div class="metric-label" style="font-size:11px">June-July 2026</div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Risk Map
#     st.subheader("🗺️ Station Risk Overview")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         # Create map
#         toronto_center = [43.6532, -79.3832]
        
#         # Check if we have valid coordinates
#         valid_coords = data['profiles'][(pd.notna(data['profiles']['latitude'])) & 
#                                         (pd.notna(data['profiles']['longitude']))]
        
#         if len(valid_coords) > 0:
#             m = folium.Map(location=toronto_center, zoom_start=11, tiles='CartoDB positron')
            
#             # Add stations
#             for _, row in valid_coords.iterrows():
#                 crimes_per_week = row['crimes_per_week']
                
#                 # Color by risk
#                 if crimes_per_week > 7:
#                     color = 'red'
#                     risk = 'CRITICAL'
#                 elif crimes_per_week > 3:
#                     color = 'orange'
#                     risk = 'HIGH'
#                 elif crimes_per_week > 1:
#                     color = 'yellow'
#                     risk = 'MEDIUM'
#                 else:
#                     color = 'green'
#                     risk = 'LOW'
                
#                 folium.CircleMarker(
#                     location=[row['latitude'], row['longitude']],
#                     radius=max(5, min(15, crimes_per_week)),
#                     popup=f"<b>{row['station_name']}</b><br>"
#                           f"Risk: {risk}<br>"
#                           f"Crimes/week: {crimes_per_week:.1f}<br>"
#                           f"Total: {row['total_crimes']:,}",
#                     color=color,
#                     fill=True,
#                     fillColor=color,
#                     fillOpacity=0.6
#                 ).add_to(m)
            
#             st_folium(m, width=700, height=500, returned_objects=[])
#         else:
#             # Fallback: scatter plot if no coordinates
#             st.warning("Map coordinates not available. Showing scatter plot instead.")
            
#             fig = px.scatter(
#                 data['profiles'].head(30),
#                 x='distance_to_scotiabank',
#                 y='crimes_per_week',
#                 size='total_crimes',
#                 color='risk_category',
#                 hover_name='station_name',
#                 labels={
#                     'distance_to_scotiabank': 'Distance to Downtown (km)',
#                     'crimes_per_week': 'Crimes per Week'
#                 },
#                 color_discrete_map={
#                     'CRITICAL': '#d32f2f',
#                     'HIGH': '#f57c00',
#                     'MEDIUM': '#fdd835',
#                     'LOW': '#388e3c'
#                 }
#             )
#             fig.update_layout(height=500)
#             st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         st.markdown("**Risk Classification**")
        
#         critical = len(data['profiles'][data['profiles']['crimes_per_week'] > 7])
#         high = len(data['profiles'][(data['profiles']['crimes_per_week'] > 3) & (data['profiles']['crimes_per_week'] <= 7)])
#         medium = len(data['profiles'][(data['profiles']['crimes_per_week'] > 1) & (data['profiles']['crimes_per_week'] <= 3)])
#         low = len(data['profiles'][data['profiles']['crimes_per_week'] <= 1])
        
#         st.metric("🔴 Critical (>7/wk)", critical)
#         st.metric("🟠 High (3-7/wk)", high)
#         st.metric("🟡 Medium (1-3/wk)", medium)
#         st.metric("🟢 Low (<1/wk)", low)
        
#         st.markdown("---")
#         st.markdown("**Legend**")
#         st.markdown("• Circle size = Crime frequency")
#         st.markdown("• Color = Risk level")
    
#     st.markdown("---")
    
#     # Top 10 Highest Risk Stations
#     st.subheader("⚠️ Top 10 Highest-Risk Stations")
    
#     top_10 = data['profiles'].nlargest(10, 'crimes_per_week')
    
#     fig = px.bar(
#         top_10,
#         x='crimes_per_week',
#         y='station_name',
#         orientation='h',
#         color='crimes_per_week',
#         color_continuous_scale=['#388e3c', '#f57c00', '#d32f2f'],
#         labels={'crimes_per_week': 'Crimes per Week', 'station_name': 'Station'}
#     )
#     fig.update_layout(
#         height=400,
#         showlegend=False,
#         yaxis={'categoryorder': 'total ascending'}
#     )
#     st.plotly_chart(fig, use_container_width=True)
    
#     # Key Insights - DYNAMIC
#     st.markdown("---")
#     st.subheader("💡 Key Insights")
    
#     # Calculate dynamic statistics
#     top_10_crimes = top_10['total_crimes'].sum()
#     top_10_pct = (top_10_crimes / total_crimes) * 100
    
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.markdown(f"""
#         <div class="insight-box">
#         <b>📍 Crime Concentration</b><br>
#         Top 10 stations ({(10/num_stations)*100:.0f}% of network) account for {top_10_pct:.0f}% of all transit crime.
#         Focused deployment at these stations = maximum impact.
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown("""
#         <div class="insight-box">
#         <b>🌙 Late Night Pattern</b><br>
#         Peak crime occurs during late night hours (22:00-02:00).
#         Deploy maximum resources during this window.
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown("""
#         <div class="insight-box">
#         <b>📅 Event Amplification</b><br>
#         Major events (sports games) amplify crime by 2.61x.
#         Event-day surge staffing critical for FIFA 2026.
#         </div>
#         """, unsafe_allow_html=True)
        
#         st.markdown(f"""
#         <div class="insight-box">
#         <b>⚽ FIFA 2026 Readiness</b><br>
#         {len(data['fifa_priority'])} high-priority stations identified.
#         Deployment plan ready for 6 matches (Jun-Jul 2026).
#         </div>
#         """, unsafe_allow_html=True)

# # ============================================================================
# # PAGE 2: STATION ANALYSIS
# # ============================================================================
# elif page == "📊 Station Analysis":
#     st.title("📊 Station Deep Dive Analysis")
    
#     # Station selector
#     selected_station = st.selectbox(
#         "Select Station",
#         sorted(data['profiles']['station_name'].unique())
#     )
    
#     # Get station data
#     station_data = data['profiles'][data['profiles']['station_name'] == selected_station].iloc[0]
    
#     # Station header
#     col1, col2, col3, col4 = st.columns(4)
    
#     with col1:
#         risk_cat = station_data['risk_category']
#         risk_color = {'CRITICAL': 'red', 'Critical': 'red', 'HIGH': 'orange', 'High': 'orange', 
#                       'MEDIUM': 'yellow', 'Medium': 'yellow', 'LOW': 'green', 'Low': 'green'}.get(risk_cat, 'gray')
#         st.markdown(f"### {selected_station}")
#         st.markdown(f"<span style='color:{risk_color};font-weight:bold;font-size:20px'>● {risk_cat.upper()} RISK</span>", unsafe_allow_html=True)
    
#     with col2:
#         st.metric("Total Crimes", f"{int(station_data['total_crimes']):,}")
#         st.caption("2018-2025")
    
#     with col3:
#         st.metric("Crimes per Week", f"{station_data['crimes_per_week']:.1f}")
#         st.caption("Average rate")
    
#     with col4:
#         st.metric("Late Night %", f"{station_data['late_night_pct']:.1f}%")
#         st.caption("10pm-2am")
    
#     st.markdown("---")
    
#     # Charts
#     col1, col2 = st.columns(2)
    
#     with col1:
#         st.subheader("Weekend vs Weekday")
        
#         weekend_data = pd.DataFrame({
#             'Period': ['Weekday', 'Weekend'],
#             'Crimes per Day': [station_data['weekday_crimes_per_day'], station_data['weekend_crimes_per_day']]
#         })
        
#         fig = px.bar(
#             weekend_data,
#             x='Period',
#             y='Crimes per Day',
#             color='Period',
#             color_discrete_map={'Weekday': '#1f77b4', 'Weekend': '#ff7f0e'}
#         )
#         fig.update_layout(height=300, showlegend=False)
#         st.plotly_chart(fig, use_container_width=True)
        
#         multiplier = station_data['weekend_multiplier']
#         if multiplier > 1.2:
#             st.warning(f"⚠️ Weekend crimes are {multiplier:.2f}x higher - surge deployment needed")
#         else:
#             st.info(f"Weekend effect is modest ({multiplier:.2f}x)")
    
#     with col2:
#         st.subheader("Proximity to Venues")
        
#         venue_data = pd.DataFrame({
#             'Venue': ['BMO Field', 'Scotiabank Arena', 'Rogers Centre'],
#             'Distance (km)': [
#                 station_data['distance_to_bmo'],
#                 station_data['distance_to_scotiabank'],
#                 station_data['distance_to_rogers']
#             ]
#         })
        
#         fig = px.bar(
#             venue_data,
#             x='Venue',
#             y='Distance (km)',
#             color='Distance (km)',
#             color_continuous_scale='RdYlGn_r'
#         )
#         fig.update_layout(height=300, showlegend=False)
#         st.plotly_chart(fig, use_container_width=True)
        
#         if station_data['distance_to_bmo'] < 3:
#             st.success("✓ Within FIFA critical corridor (<3km from BMO)")
#         elif station_data['distance_to_scotiabank'] < 2:
#             st.success("✓ Near downtown event venues")
    
#     # Danger window
#     if selected_station in data['danger_windows']['station'].values:
#         danger_data = data['danger_windows'][data['danger_windows']['station'] == selected_station].iloc[0]
        
#         st.markdown("---")
#         st.subheader("⏰ Danger Window")
        
#         danger_start = int(danger_data['danger_start'])
#         danger_end = int(danger_data['danger_end'])
#         danger_pct = danger_data['danger_pct']
        
#         st.markdown(f"""
#         <div class="insight-box">
#         <b>Peak Crime Window: {danger_start:02d}:00 - {danger_end:02d}:00</b><br>
#         This 3-hour window accounts for <b>{danger_pct:.0f}%</b> of all crimes at this station.<br>
#         <b>Recommendation:</b> Deploy officers during this window for maximum impact.
#         </div>
#         """, unsafe_allow_html=True)

# # ============================================================================
# # PAGE 3: FIFA 2026 DEPLOYMENT
# # ============================================================================
# elif page == "🎯 FIFA 2026 Deployment":
#     st.title("⚽ FIFA 2026 Deployment Strategy")
#     st.markdown("### 6 Matches at BMO Field (June-July 2026)")
    
#     # UPDATED FIFA MATCH SCHEDULE
#     matches = [
#         "Match 1: Jun 12 (Friday 15:00)",
#         "Match 2: Jun 17 (Wednesday 19:00)",
#         "Match 3: Jun 20 (Saturday 16:00)",
#         "Match 4: Jun 23 (Tuesday 19:00)",
#         "Match 5: Jun 26 (Friday 15:00)",
#         "Match 6: Jul 2 (Thursday 19:00)"
#     ]
    
#     selected_match = st.selectbox("Select Match", matches, key='match_selector')
#     match_id = int(selected_match.split(':')[0].split()[-1])
    
#     # Match details
#     match_deploy = data['deployment'][data['deployment']['match_id'] == match_id].copy()
    
#     if len(match_deploy) > 0:
#         match_info = match_deploy.iloc[0]
        
#         # Calculate critical window based on kickoff time
#         kickoff_time = match_info['kickoff'] if 'kickoff' in match_info else '18:00'
#         kickoff_hour = int(kickoff_time.split(':')[0])
#         critical_start = kickoff_hour + 2  # 2 hours after match starts
#         critical_end = min(23, kickoff_hour + 6)  # 6 hours after kickoff
#         critical_window = f"{critical_start:02d}:00-{critical_end:02d}:00"
        
#         # Get risk level
#         risk = match_info['risk_level'] if 'risk_level' in match_info else 'MEDIUM'
        
#         # Get match-specific multiplier
#         risk_multipliers = {'HIGH': 1.3, 'MEDIUM-HIGH': 1.15, 'MEDIUM': 1.0}
#         match_multiplier = risk_multipliers.get(risk, 1.0)
        
#         # Calculate expected crimes per station (for visualization)
#         if 'amplification' in match_deploy.columns:
#             match_deploy['expected_crimes'] = (match_deploy['amplification'] * match_multiplier * 0.5).round(1)
#         else:
#             match_deploy['expected_crimes'] = match_deploy['officers'] * 1.5
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             st.metric("Total Officers", int(match_deploy['officers'].sum()))
        
#         with col2:
#             st.metric("Stations Covered", len(match_deploy))
        
#         with col3:
#             risk_color = {'HIGH': 'red', 'MEDIUM-HIGH': 'orange', 'MEDIUM': 'yellow'}.get(risk, 'green')
#             st.markdown(f"**Risk Level**")
#             st.markdown(f"<span style='color:{risk_color};font-weight:bold;font-size:18px'>{risk}</span>", unsafe_allow_html=True)
        
#         with col4:
#             st.metric("Critical Window", critical_window)
        
#         st.markdown("---")
        
#         # Deployment heatmap - NOW SHOWING AMPLIFICATION + EXPECTED CRIMES
#         st.subheader("📋 Station-by-Station Deployment")
        
#         # Sort by expected crimes (shows which stations are truly high-risk)
#         match_deploy_sorted = match_deploy.sort_values('expected_crimes', ascending=True)
        
#         # Create dual-axis visualization
#         fig = go.Figure()
        
#         # Bar 1: Officers deployed
#         fig.add_trace(go.Bar(
#             x=match_deploy_sorted['officers'],
#             y=match_deploy_sorted['station'],
#             orientation='h',
#             name='Officers',
#             marker=dict(color='#003366'),
#             text=match_deploy_sorted['officers'],
#             textposition='auto',
#         ))
        
#         # Bar 2: Expected crimes (semi-transparent)
#         if 'expected_crimes' in match_deploy_sorted.columns:
#             fig.add_trace(go.Bar(
#                 x=match_deploy_sorted['expected_crimes'],
#                 y=match_deploy_sorted['station'],
#                 orientation='h',
#                 name='Expected Crimes',
#                 marker=dict(
#                     color=match_deploy_sorted['expected_crimes'],
#                     colorscale='Reds',
#                     opacity=0.5,
#                     showscale=True,
#                     colorbar=dict(title="Expected<br>Crimes", x=1.15)
#                 ),
#                 text=match_deploy_sorted['expected_crimes'],
#                 textposition='auto',
#             ))
        
#         fig.update_layout(
#             height=450,
#             xaxis_title="Officers Deployed / Expected Crimes",
#             yaxis_title="Station",
#             barmode='overlay',
#             showlegend=True,
#             legend=dict(x=0.7, y=0.99),
#             hovermode='y unified'
#         )
        
#         st.plotly_chart(fig, use_container_width=True, key=f'deploy_chart_{match_id}')
        
#         # Key insight box
#         if 'amplification' in match_deploy.columns:
#             max_risk_station = match_deploy_sorted.iloc[-1]
#             min_risk_station = match_deploy_sorted.iloc[0]
            
#             st.markdown(f"""
#             <div class="insight-box">
#             <b>📊 Risk Analysis for This Match:</b><br>
#             • Highest Risk: <b>{max_risk_station['station']}</b> ({max_risk_station['amplification']:.2f}x amplification, {max_risk_station['expected_crimes']:.1f} expected crimes)<br>
#             • Lowest Risk: <b>{min_risk_station['station']}</b> ({min_risk_station['amplification']:.2f}x amplification, {min_risk_station['expected_crimes']:.1f} expected crimes)<br>
#             • Match Multiplier: <b>{match_multiplier}x</b> ({risk} risk level)
#             </div>
#             """, unsafe_allow_html=True)
        
#         # Deployment table - Enhanced with amplification data
#         st.subheader("📊 Detailed Deployment Schedule")
        
#         # Build display columns
#         display_cols = ['station', 'officers']
#         col_names = ['Station', 'Officers']
        
#         if 'amplification' in match_deploy.columns:
#             display_cols.append('amplification')
#             col_names.append('Amplification')
        
#         if 'expected_crimes' in match_deploy.columns:
#             display_cols.append('expected_crimes')
#             col_names.append('Expected Crimes')
        
#         display_cols.append('risk_level')
#         col_names.append('Risk Level')
        
#         display_df = match_deploy[display_cols].copy()
#         display_df.columns = col_names
        
#         # Sort by expected crimes descending
#         if 'Expected Crimes' in display_df.columns:
#             display_df = display_df.sort_values('Expected Crimes', ascending=False)
        
#         # Format numbers
#         if 'Amplification' in display_df.columns:
#             display_df['Amplification'] = display_df['Amplification'].apply(lambda x: f"{x:.2f}x")
#         if 'Expected Crimes' in display_df.columns:
#             display_df['Expected Crimes'] = display_df['Expected Crimes'].apply(lambda x: f"{x:.1f}")
        
#         st.dataframe(
#             display_df,
#             use_container_width=True,
#             hide_index=True,
#             key=f'deploy_table_{match_id}'
#         )
    
#     # Scenarios comparison - FULLY DYNAMIC
#     st.markdown("---")
#     st.subheader("🎯 Deployment Scenarios")
    
#     # Calculate scenario statistics from actual deployment data
#     if len(data['deployment']) > 0:
#         # Get unique match types and their officer counts
#         match_risk_summary = data['deployment'].groupby('risk_level')['officers'].sum().reset_index()
#         match_counts = data['deployment'].groupby('risk_level')['match_id'].nunique().reset_index()
#         match_risk_summary = match_risk_summary.merge(match_counts, on='risk_level')
#         match_risk_summary.columns = ['risk_level', 'total_officers', 'num_matches']
        
#         # Calculate average officers per match type
#         match_risk_summary['avg_per_match'] = (match_risk_summary['total_officers'] / 
#                                                 match_risk_summary['num_matches']).round(0).astype(int)
        
#         # Get HIGH risk as baseline (most common)
#         if 'HIGH' in match_risk_summary['risk_level'].values:
#             baseline_officers = int(match_risk_summary[match_risk_summary['risk_level'] == 'HIGH']['avg_per_match'].iloc[0])
#         else:
#             # Fallback to overall average
#             baseline_officers = int(data['deployment'].groupby('match_id')['officers'].sum().mean())
        
#         # Calculate scenarios as percentages of baseline
#         conservative_officers = int(baseline_officers * 0.75)  # 75% of baseline
#         balanced_officers = baseline_officers  # 100% (actual HIGH risk deployment)
#         aggressive_officers = int(baseline_officers * 1.15)  # 115% of baseline
        
#         # Calculate total shifts for 6 matches (assuming all HIGH risk for comparison)
#         num_matches = 6
#         conservative_total = conservative_officers * num_matches
#         balanced_total = balanced_officers * num_matches
#         aggressive_total = aggressive_officers * num_matches
        
#         # Get average amplification from deployment data
#         if 'amplification' in data['deployment'].columns:
#             avg_amplification = data['deployment']['amplification'].mean()
#             conservative_amp = avg_amplification * 0.80
#             balanced_amp = avg_amplification
#             aggressive_amp = avg_amplification * 1.20
#         else:
#             avg_amplification = 1.6
#             conservative_amp = 1.3
#             balanced_amp = 1.6
#             aggressive_amp = 1.9
        
#         # Calculate actual total deployment
#         actual_total = data['deployment'].groupby('match_id')['officers'].sum().sum()
        
#     else:
#         # Final fallback if no deployment data at all
#         baseline_officers = 28
#         conservative_officers = 21
#         balanced_officers = 28
#         aggressive_officers = 32
#         conservative_amp = 1.3
#         balanced_amp = 1.6
#         aggressive_amp = 1.9
#         conservative_total = 126
#         balanced_total = 168
#         aggressive_total = 192
#         actual_total = 165
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">Conservative</div>
#             <div class="metric-value">{conservative_officers}</div>
#             <div class="metric-label">officers/match ({conservative_amp:.2f}x)</div>
#             <div class="metric-label" style="margin-top:10px">~70% coverage</div>
#             <div class="metric-label" style="font-size:10px; margin-top:5px; color:#666;">
#             Total: {conservative_total} shifts
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col2:
#         st.markdown(f"""
#         <div class="metric-card" style="border: 3px solid #003366;">
#             <div class="metric-label">⭐ Balanced (Recommended)</div>
#             <div class="metric-value">{balanced_officers}</div>
#             <div class="metric-label">officers/match ({balanced_amp:.2f}x)</div>
#             <div class="metric-label" style="margin-top:10px">~85% coverage</div>
#             <div class="metric-label" style="font-size:10px; margin-top:5px; color:#003366;">
#             <b>Actual Total: {actual_total} shifts</b>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     with col3:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-label">Aggressive</div>
#             <div class="metric-value">{aggressive_officers}</div>
#             <div class="metric-label">officers/match ({aggressive_amp:.2f}x)</div>
#             <div class="metric-label" style="margin-top:10px">~95% coverage</div>
#             <div class="metric-label" style="font-size:10px; margin-top:5px; color:#666;">
#             Total: {aggressive_total} shifts
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
    
#     # Add explanation below scenarios
#     st.markdown(f"""
#     <div class="insight-box" style="margin-top:20px;">
#     <b>Scenario Comparison:</b><br>
#     • <b>Conservative</b>: Deploy fewer officers ({conservative_officers}/match), rely more on organic patrol coverage. Lower cost but higher risk.<br>
#     • <b>Balanced (Current Plan)</b>: Deploy {balanced_officers}/match at HIGH-risk matches, {balanced_officers-1}/match at MEDIUM-HIGH. 
#       Based on {balanced_amp:.2f}x average amplification across priority stations.<br>
#     • <b>Aggressive</b>: Maximum coverage ({aggressive_officers}/match), higher cost but lowest risk exposure. Suitable if Match 1 reveals higher-than-expected crime rates.<br><br>
#     <b>Recommendation:</b> Start with Balanced deployment ({actual_total} total shifts). After Match 1, measure actual crime rates and officer capacity, 
#     then adjust Matches 2-6 allocation accordingly. Adaptive learning eliminates the need to guess scenarios upfront.
#     </div>
#     """, unsafe_allow_html=True)
    
#     # Adaptive learning
#     st.markdown("---")
#     st.subheader("🔄 Adaptive Learning Strategy")
    
#     st.markdown("""
#     <div class="insight-box">
#     <b>Match 1 (June 12): TEST PHASE</b><br>
#     → Deploy baseline officers at 10 priority stations<br>
#     → <b>MEASURE</b> actual crimes at each station during deployment<br>
#     → <b>COMPARE</b> predicted vs actual amplification ratios<br>
#     → <b>IDENTIFY</b> over/under-resourced stations
#     </div>
    
#     <div class="insight-box">
#     <b>Matches 2-3: ADJUSTMENT PHASE</b><br>
#     → Reallocate based on Match 1 actuals<br>
#     → Shift officers from quiet stations to busy ones<br>
#     → Continue measuring and refining predictions
#     </div>
    
#     <div class="insight-box">
#     <b>Matches 4-6: OPTIMIZED PHASE</b><br>
#     → Deploy based on 3-match empirical average<br>
#     → Final refined strategy with validated multipliers<br>
#     → Maximum deployment efficiency achieved
#     </div>
#     """, unsafe_allow_html=True)

# # ============================================================================
# # PAGE 4: DATA EXPLORER
# # ============================================================================
# elif page == "📈 Data Explorer":
#     st.title("📈 Data Explorer")
    
#     # Dataset selector
#     dataset = st.selectbox(
#         "Select Dataset",
#         [
#             "Station Risk Profiles",
#             "FIFA Affected Stations",
#             "Event Amplification Analysis",
#             "Deployment Schedule"
#         ]
#     )
    
#     if dataset == "Station Risk Profiles":
#         st.subheader(f"Station Risk Profiles ({len(data['profiles'])} Stations)")
        
#         # Filters
#         col1, col2 = st.columns(2)
        
#         with col1:
#             risk_filter = st.multiselect(
#                 "Filter by Risk Category",
#                 options=data['profiles']['risk_category'].unique(),
#                 default=data['profiles']['risk_category'].unique()
#             )
        
#         with col2:
#             min_crimes = st.slider(
#                 "Minimum Total Crimes",
#                 0,
#                 int(data['profiles']['total_crimes'].max()),
#                 0
#             )
        
#         filtered_df = data['profiles'][
#             (data['profiles']['risk_category'].isin(risk_filter)) &
#             (data['profiles']['total_crimes'] >= min_crimes)
#         ]
        
#         st.dataframe(
#             filtered_df,
#             use_container_width=True,
#             hide_index=True
#         )
        
#         # Download button
#         csv = filtered_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             "📥 Download CSV",
#             csv,
#             "station_risk_profiles.csv",
#             "text/csv"
#         )
    
#     elif dataset == "FIFA Affected Stations":
#         st.subheader(f"FIFA Affected Stations ({len(data['fifa_priority'])} Priority Stations)")
        
#         st.dataframe(
#             data['fifa_priority'],
#             use_container_width=True,
#             hide_index=True
#         )
        
#         csv = data['fifa_priority'].to_csv(index=False).encode('utf-8')
#         st.download_button(
#             "📥 Download CSV",
#             csv,
#             "fifa_priority_stations.csv",
#             "text/csv"
#         )
    
#     elif dataset == "Event Amplification Analysis":
#         st.subheader("Event Amplification Analysis (CORRECTED)")
        
#         st.markdown("""
#         **CRITICAL UPDATE:** This uses corrected event amplification (2.61x average).
        
#         **Old Method (WRONG):** Compared ALL Fri/Sat vs Mon-Thu (1.08x - diluted signal)
        
#         **New Method (CORRECT):** Identified anomalous high-crime days during sports seasons (2.61x)
        
#         **Methodology:** 
#         - Identified days with crime >1.5 SD above day-of-week baseline
#         - Filtered to Leafs (Oct-May) and Jays (Apr-Oct) seasons
#         - Compared these 156 likely event days vs all other days
        
#         **Result:** Events amplify crime by 2.61x (not 1.08x)
#         """)
        
#         st.dataframe(
#             data['activity'],
#             use_container_width=True,
#             hide_index=True
#         )
        
#         csv = data['activity'].to_csv(index=False).encode('utf-8')
#         st.download_button(
#             "📥 Download CSV",
#             csv,
#             "event_amplification_FIXED.csv",
#             "text/csv"
#         )
    
#     elif dataset == "Deployment Schedule":
#         st.subheader("FIFA 2026 Deployment Schedule (UPDATED)")
        
#         st.markdown("""
#         **Schedule Updated:** Official FIFA 2026 Toronto match dates and times.
        
#         **Total Deployment:** 111 officer-shifts across 6 matches
        
#         **Risk Distribution:**
#         - HIGH (1.3x): 3 matches (Fri/Sat afternoon)
#         - MEDIUM-HIGH (1.15x): 3 matches (Weekday evening)
#         """)
        
#         st.dataframe(
#             data['deployment'],
#             use_container_width=True,
#             hide_index=True
#         )
        
#         csv = data['deployment'].to_csv(index=False).encode('utf-8')
#         st.download_button(
#             "📥 Download CSV",
#             csv,
#             "fifa_deployment_schedule.csv",
#             "text/csv"
#         )

# # Footer
# st.markdown("---")
# st.markdown(f"""
# <div style='text-align: center; color: #666; font-size: 12px;'>
#     <b>Toronto Police Service - Transit Safety Intelligence Dashboard</b><br>
#     Data Analysis Period: 2018-2025 ({data['total_crimes']:,} crimes) | FIFA 2026 Readiness Assessment<br>
#     Developed for TPS Strategic Planning & FIFA World Cup 2026
# </div>
# """, unsafe_allow_html=True)





import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import folium
from streamlit_folium import st_folium

# Page config
st.set_page_config(
    page_title="TPS Transit Safety Intelligence",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - TPS Branding
st.markdown("""
<style>
    .main { background-color: #f5f7fa; }
    h1 { color: #003366; font-family: 'Arial', sans-serif; font-weight: 700; }
    h2 { color: #003366; font-family: 'Arial', sans-serif; }
    h3 { color: #1a4d80; font-family: 'Arial', sans-serif; }
    .stButton>button { 
        background-color: #003366; 
        color: white; 
        border-radius: 5px;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #004080; }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 36px;
        font-weight: bold;
        color: #003366;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
        margin-top: 5px;
    }
    .insight-box {
        background-color: #e6f2ff;
        padding: 15px;
        border-left: 4px solid #003366;
        border-radius: 5px;
        margin: 10px 0;
    }
    .risk-high { color: #d32f2f; font-weight: bold; }
    .risk-medium { color: #f57c00; font-weight: bold; }
    .risk-low { color: #388e3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Streamlit Cloud path detection
    current_dir = Path.cwd()
    
    # Check multiple possible locations
    possible_output_dirs = [
        current_dir / 'outputs',
        current_dir.parent / 'outputs',
        Path('outputs'),
        Path('.') / 'outputs'
    ]
    
    output_dir = None
    for dir_path in possible_output_dirs:
        if dir_path.exists():
            output_dir = dir_path
            break
    
    if output_dir is None:
        st.error("❌ Cannot find 'outputs' directory. Please ensure all CSV files are uploaded to Streamlit Cloud.")
        st.info("Expected files in 'outputs/' folder:\n" +
                "- 05_station_risk_profiles.csv\n" +
                "- 06_station_danger_windows.csv\n" +
                "- 07_fifa_affected_stations.csv\n" +
                "- 07_fifa_priority_stations.csv\n" +
                "- 09_event_amplification_FIXED.csv\n" +
                "- 10_fifa_deployment_schedule_UPDATED.csv")
        return None
    
    data = {}
    try:
        # Load from outputs directory ONLY (no data directory needed)
        data['profiles'] = pd.read_csv(output_dir / '05_station_risk_profiles.csv')
        data['danger_windows'] = pd.read_csv(output_dir / '06_station_danger_windows.csv')
        data['fifa_stations'] = pd.read_csv(output_dir / '07_fifa_affected_stations.csv')
        data['fifa_priority'] = pd.read_csv(output_dir / '07_fifa_priority_stations.csv')
        
        # Try to load FIXED files first, fallback to original names
        try:
            data['activity'] = pd.read_csv(output_dir / '09_event_amplification_FIXED.csv')
        except:
            data['activity'] = pd.read_csv(output_dir / '09_event_amplification.csv')
        
        try:
            data['deployment'] = pd.read_csv(output_dir / '10_fifa_deployment_schedule_UPDATED.csv')
        except:
            data['deployment'] = pd.read_csv(output_dir / '10_fifa_deployment_schedule.csv')
        
        try:
            data['scenarios'] = pd.read_csv(output_dir / '10_deployment_scenarios_UPDATED.csv')
        except:
            data['scenarios'] = pd.read_csv(output_dir / '10_deployment_scenarios.csv')
        
        # DYNAMIC: Calculate total crimes from station profiles
        data['total_crimes'] = int(data['profiles']['total_crimes'].sum())
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.error(f"Tried loading from: {output_dir.absolute()}")
        st.info(f"Current directory: {current_dir.absolute()}")
        st.info("Make sure you run the app from the project root: streamlit run app.py")
        return None
    
    return data

data = load_data()

if data is None:
    st.error("Failed to load data files. Please ensure all analysis files are present.")
    st.stop()

# Sidebar Navigation
st.sidebar.markdown("""
<div style='text-align: center; padding: 20px 0; background-color: #003366; border-radius: 10px; margin-bottom: 20px;'>
    <h2 style='color: white; margin: 0;'>🚔 TPS</h2>
    <p style='color: #ccc; margin: 5px 0 0 0; font-size: 12px;'>Transit Safety</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select View",
    ["🏠 Executive Dashboard", "📊 Station Analysis", "🎯 FIFA 2026 Deployment", "📈 Data Explorer"]
)

# ============================================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ============================================================================
if page == "🏠 Executive Dashboard":
    st.title("🚇 Transit Safety Intelligence Dashboard")
    st.markdown("### Toronto Police Service - FIFA 2026 Readiness")
    
    # Hero KPIs - FULLY DYNAMIC
    col1, col2, col3, col4 = st.columns(4)
    
    # DYNAMIC: Get actual crime count from data
    total_crimes = data['total_crimes']
    num_stations = len(data['profiles'])
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_crimes:,}</div>
            <div class="metric-label">Crimes Analyzed</div>
            <div class="metric-label" style="font-size:11px">2018-2025</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{num_stations}</div>
            <div class="metric-label">Stations Monitored</div>
            <div class="metric-label" style="font-size:11px">TTC + GO Transit</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">8</div>
            <div class="metric-label">Years of Data</div>
            <div class="metric-label" style="font-size:11px">Historical Patterns</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">6</div>
            <div class="metric-label">FIFA Matches</div>
            <div class="metric-label" style="font-size:11px">June-July 2026</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Risk Map
    st.subheader("🗺️ Station Risk Overview")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create map
        toronto_center = [43.6532, -79.3832]
        
        # Check if we have valid coordinates
        valid_coords = data['profiles'][(pd.notna(data['profiles']['latitude'])) & 
                                        (pd.notna(data['profiles']['longitude']))]
        
        if len(valid_coords) > 0:
            m = folium.Map(location=toronto_center, zoom_start=11, tiles='CartoDB positron')
            
            # Add stations
            for _, row in valid_coords.iterrows():
                crimes_per_week = row['crimes_per_week']
                
                # Color by risk
                if crimes_per_week > 7:
                    color = 'red'
                    risk = 'CRITICAL'
                elif crimes_per_week > 3:
                    color = 'orange'
                    risk = 'HIGH'
                elif crimes_per_week > 1:
                    color = 'yellow'
                    risk = 'MEDIUM'
                else:
                    color = 'green'
                    risk = 'LOW'
                
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=max(5, min(15, crimes_per_week)),
                    popup=f"<b>{row['station_name']}</b><br>"
                          f"Risk: {risk}<br>"
                          f"Crimes/week: {crimes_per_week:.1f}<br>"
                          f"Total: {row['total_crimes']:,}",
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.6
                ).add_to(m)
            
            st_folium(m, width=700, height=500, returned_objects=[])
        else:
            # Fallback: scatter plot if no coordinates
            st.warning("Map coordinates not available. Showing scatter plot instead.")
            
            fig = px.scatter(
                data['profiles'].head(30),
                x='distance_to_scotiabank',
                y='crimes_per_week',
                size='total_crimes',
                color='risk_category',
                hover_name='station_name',
                labels={
                    'distance_to_scotiabank': 'Distance to Downtown (km)',
                    'crimes_per_week': 'Crimes per Week'
                },
                color_discrete_map={
                    'CRITICAL': '#d32f2f',
                    'HIGH': '#f57c00',
                    'MEDIUM': '#fdd835',
                    'LOW': '#388e3c'
                }
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Risk Classification**")
        
        critical = len(data['profiles'][data['profiles']['crimes_per_week'] > 7])
        high = len(data['profiles'][(data['profiles']['crimes_per_week'] > 3) & (data['profiles']['crimes_per_week'] <= 7)])
        medium = len(data['profiles'][(data['profiles']['crimes_per_week'] > 1) & (data['profiles']['crimes_per_week'] <= 3)])
        low = len(data['profiles'][data['profiles']['crimes_per_week'] <= 1])
        
        st.metric("🔴 Critical (>7/wk)", critical)
        st.metric("🟠 High (3-7/wk)", high)
        st.metric("🟡 Medium (1-3/wk)", medium)
        st.metric("🟢 Low (<1/wk)", low)
        
        st.markdown("---")
        st.markdown("**Legend**")
        st.markdown("• Circle size = Crime frequency")
        st.markdown("• Color = Risk level")
    
    st.markdown("---")
    
    # Top 10 Highest Risk Stations
    st.subheader("⚠️ Top 10 Highest-Risk Stations")
    
    top_10 = data['profiles'].nlargest(10, 'crimes_per_week')
    
    fig = px.bar(
        top_10,
        x='crimes_per_week',
        y='station_name',
        orientation='h',
        color='crimes_per_week',
        color_continuous_scale=['#388e3c', '#f57c00', '#d32f2f'],
        labels={'crimes_per_week': 'Crimes per Week', 'station_name': 'Station'}
    )
    fig.update_layout(
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Key Insights - DYNAMIC
    st.markdown("---")
    st.subheader("💡 Key Insights")
    
    # Calculate dynamic statistics
    top_10_crimes = top_10['total_crimes'].sum()
    top_10_pct = (top_10_crimes / total_crimes) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
        <b>📍 Crime Concentration</b><br>
        Top 10 stations ({(10/num_stations)*100:.0f}% of network) account for {top_10_pct:.0f}% of all transit crime.
        Focused deployment at these stations = maximum impact.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
        <b>🌙 Late Night Pattern</b><br>
        Peak crime occurs during late night hours (22:00-02:00).
        Deploy maximum resources during this window.
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="insight-box">
        <b>📅 Event Amplification</b><br>
        Major events (sports games) amplify crime by 2.61x.
        Event-day surge staffing critical for FIFA 2026.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="insight-box">
        <b>⚽ FIFA 2026 Readiness</b><br>
        {len(data['fifa_priority'])} high-priority stations identified.
        Deployment plan ready for 6 matches (Jun-Jul 2026).
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE 2: STATION ANALYSIS
# ============================================================================
elif page == "📊 Station Analysis":
    st.title("📊 Station Deep Dive Analysis")
    
    # Station selector
    selected_station = st.selectbox(
        "Select Station",
        sorted(data['profiles']['station_name'].unique())
    )
    
    # Get station data
    station_data = data['profiles'][data['profiles']['station_name'] == selected_station].iloc[0]
    
    # Station header
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        risk_cat = station_data['risk_category']
        risk_color = {'CRITICAL': 'red', 'Critical': 'red', 'HIGH': 'orange', 'High': 'orange', 
                      'MEDIUM': 'yellow', 'Medium': 'yellow', 'LOW': 'green', 'Low': 'green'}.get(risk_cat, 'gray')
        st.markdown(f"### {selected_station}")
        st.markdown(f"<span style='color:{risk_color};font-weight:bold;font-size:20px'>● {risk_cat.upper()} RISK</span>", unsafe_allow_html=True)
    
    with col2:
        st.metric("Total Crimes", f"{int(station_data['total_crimes']):,}")
        st.caption("2018-2025")
    
    with col3:
        st.metric("Crimes per Week", f"{station_data['crimes_per_week']:.1f}")
        st.caption("Average rate")
    
    with col4:
        st.metric("Late Night %", f"{station_data['late_night_pct']:.1f}%")
        st.caption("10pm-2am")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Weekend vs Weekday")
        
        weekend_data = pd.DataFrame({
            'Period': ['Weekday', 'Weekend'],
            'Crimes per Day': [station_data['weekday_crimes_per_day'], station_data['weekend_crimes_per_day']]
        })
        
        fig = px.bar(
            weekend_data,
            x='Period',
            y='Crimes per Day',
            color='Period',
            color_discrete_map={'Weekday': '#1f77b4', 'Weekend': '#ff7f0e'}
        )
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        multiplier = station_data['weekend_multiplier']
        if multiplier > 1.2:
            st.warning(f"⚠️ Weekend crimes are {multiplier:.2f}x higher - surge deployment needed")
        else:
            st.info(f"Weekend effect is modest ({multiplier:.2f}x)")
    
    with col2:
        st.subheader("Proximity to Venues")
        
        venue_data = pd.DataFrame({
            'Venue': ['BMO Field', 'Scotiabank Arena', 'Rogers Centre'],
            'Distance (km)': [
                station_data['distance_to_bmo'],
                station_data['distance_to_scotiabank'],
                station_data['distance_to_rogers']
            ]
        })
        
        fig = px.bar(
            venue_data,
            x='Venue',
            y='Distance (km)',
            color='Distance (km)',
            color_continuous_scale='RdYlGn_r'
        )
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        if station_data['distance_to_bmo'] < 3:
            st.success("✓ Within FIFA critical corridor (<3km from BMO)")
        elif station_data['distance_to_scotiabank'] < 2:
            st.success("✓ Near downtown event venues")
    
    # Danger window
    if selected_station in data['danger_windows']['station'].values:
        danger_data = data['danger_windows'][data['danger_windows']['station'] == selected_station].iloc[0]
        
        st.markdown("---")
        st.subheader("⏰ Danger Window")
        
        danger_start = int(danger_data['danger_start'])
        danger_end = int(danger_data['danger_end'])
        danger_pct = danger_data['danger_pct']
        
        st.markdown(f"""
        <div class="insight-box">
        <b>Peak Crime Window: {danger_start:02d}:00 - {danger_end:02d}:00</b><br>
        This 3-hour window accounts for <b>{danger_pct:.0f}%</b> of all crimes at this station.<br>
        <b>Recommendation:</b> Deploy officers during this window for maximum impact.
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE 3: FIFA 2026 DEPLOYMENT
# ============================================================================
elif page == "🎯 FIFA 2026 Deployment":
    st.title("⚽ FIFA 2026 Deployment Strategy")
    st.markdown("### 6 Matches at BMO Field (June-July 2026)")
    
    # UPDATED FIFA MATCH SCHEDULE
    matches = [
        "Match 1: Jun 12 (Friday 15:00)",
        "Match 2: Jun 17 (Wednesday 19:00)",
        "Match 3: Jun 20 (Saturday 16:00)",
        "Match 4: Jun 23 (Tuesday 19:00)",
        "Match 5: Jun 26 (Friday 15:00)",
        "Match 6: Jul 2 (Thursday 19:00)"
    ]
    
    selected_match = st.selectbox("Select Match", matches, key='match_selector')
    match_id = int(selected_match.split(':')[0].split()[-1])
    
    # Match details
    match_deploy = data['deployment'][data['deployment']['match_id'] == match_id].copy()
    
    if len(match_deploy) > 0:
        match_info = match_deploy.iloc[0]
        
        # Calculate critical window based on kickoff time
        kickoff_time = match_info['kickoff'] if 'kickoff' in match_info else '18:00'
        kickoff_hour = int(kickoff_time.split(':')[0])
        critical_start = kickoff_hour + 2  # 2 hours after match starts
        critical_end = min(23, kickoff_hour + 6)  # 6 hours after kickoff
        critical_window = f"{critical_start:02d}:00-{critical_end:02d}:00"
        
        # Get risk level
        risk = match_info['risk_level'] if 'risk_level' in match_info else 'MEDIUM'
        
        # Get match-specific multiplier
        risk_multipliers = {'HIGH': 1.3, 'MEDIUM-HIGH': 1.15, 'MEDIUM': 1.0}
        match_multiplier = risk_multipliers.get(risk, 1.0)
        
        # Calculate expected crimes per station (for visualization)
        if 'amplification' in match_deploy.columns:
            match_deploy['expected_crimes'] = (match_deploy['amplification'] * match_multiplier * 0.5).round(1)
        else:
            match_deploy['expected_crimes'] = match_deploy['officers'] * 1.5
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Officers", int(match_deploy['officers'].sum()))
        
        with col2:
            st.metric("Stations Covered", len(match_deploy))
        
        with col3:
            risk_color = {'HIGH': 'red', 'MEDIUM-HIGH': 'orange', 'MEDIUM': 'yellow'}.get(risk, 'green')
            st.markdown(f"**Risk Level**")
            st.markdown(f"<span style='color:{risk_color};font-weight:bold;font-size:18px'>{risk}</span>", unsafe_allow_html=True)
        
        with col4:
            st.metric("Critical Window", critical_window)
        
        st.markdown("---")
        
        # Deployment heatmap - NOW SHOWING AMPLIFICATION + EXPECTED CRIMES
        st.subheader("📋 Station-by-Station Deployment")
        
        # Sort by expected crimes (shows which stations are truly high-risk)
        match_deploy_sorted = match_deploy.sort_values('expected_crimes', ascending=True)
        
        # Create dual-axis visualization
        fig = go.Figure()
        
        # Bar 1: Officers deployed
        fig.add_trace(go.Bar(
            x=match_deploy_sorted['officers'],
            y=match_deploy_sorted['station'],
            orientation='h',
            name='Officers',
            marker=dict(color='#003366'),
            text=match_deploy_sorted['officers'],
            textposition='auto',
        ))
        
        # Bar 2: Expected crimes (semi-transparent)
        if 'expected_crimes' in match_deploy_sorted.columns:
            fig.add_trace(go.Bar(
                x=match_deploy_sorted['expected_crimes'],
                y=match_deploy_sorted['station'],
                orientation='h',
                name='Expected Crimes',
                marker=dict(
                    color=match_deploy_sorted['expected_crimes'],
                    colorscale='Reds',
                    opacity=0.5,
                    showscale=True,
                    colorbar=dict(title="Expected<br>Crimes", x=1.15)
                ),
                text=match_deploy_sorted['expected_crimes'],
                textposition='auto',
            ))
        
        fig.update_layout(
            height=450,
            xaxis_title="Officers Deployed / Expected Crimes",
            yaxis_title="Station",
            barmode='overlay',
            showlegend=True,
            legend=dict(x=0.7, y=0.99),
            hovermode='y unified'
        )
        
        st.plotly_chart(fig, use_container_width=True, key=f'deploy_chart_{match_id}')
        
        # Key insight box
        if 'amplification' in match_deploy.columns:
            max_risk_station = match_deploy_sorted.iloc[-1]
            min_risk_station = match_deploy_sorted.iloc[0]
            
            st.markdown(f"""
            <div class="insight-box">
            <b>📊 Risk Analysis for This Match:</b><br>
            • Highest Risk: <b>{max_risk_station['station']}</b> ({max_risk_station['amplification']:.2f}x amplification, {max_risk_station['expected_crimes']:.1f} expected crimes)<br>
            • Lowest Risk: <b>{min_risk_station['station']}</b> ({min_risk_station['amplification']:.2f}x amplification, {min_risk_station['expected_crimes']:.1f} expected crimes)<br>
            • Match Multiplier: <b>{match_multiplier}x</b> ({risk} risk level)
            </div>
            """, unsafe_allow_html=True)
        
        # Deployment table - Enhanced with amplification data
        st.subheader("📊 Detailed Deployment Schedule")
        
        # Build display columns
        display_cols = ['station', 'officers']
        col_names = ['Station', 'Officers']
        
        if 'amplification' in match_deploy.columns:
            display_cols.append('amplification')
            col_names.append('Amplification')
        
        if 'expected_crimes' in match_deploy.columns:
            display_cols.append('expected_crimes')
            col_names.append('Expected Crimes')
        
        display_cols.append('risk_level')
        col_names.append('Risk Level')
        
        display_df = match_deploy[display_cols].copy()
        display_df.columns = col_names
        
        # Sort by expected crimes descending
        if 'Expected Crimes' in display_df.columns:
            display_df = display_df.sort_values('Expected Crimes', ascending=False)
        
        # Format numbers
        if 'Amplification' in display_df.columns:
            display_df['Amplification'] = display_df['Amplification'].apply(lambda x: f"{x:.2f}x")
        if 'Expected Crimes' in display_df.columns:
            display_df['Expected Crimes'] = display_df['Expected Crimes'].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            key=f'deploy_table_{match_id}'
        )
    
    # Scenarios comparison - FULLY DYNAMIC
    st.markdown("---")
    st.subheader("🎯 Deployment Scenarios")
    
    # Calculate scenario statistics from actual deployment data
    if len(data['deployment']) > 0:
        # Get unique match types and their officer counts
        match_risk_summary = data['deployment'].groupby('risk_level')['officers'].sum().reset_index()
        match_counts = data['deployment'].groupby('risk_level')['match_id'].nunique().reset_index()
        match_risk_summary = match_risk_summary.merge(match_counts, on='risk_level')
        match_risk_summary.columns = ['risk_level', 'total_officers', 'num_matches']
        
        # Calculate average officers per match type
        match_risk_summary['avg_per_match'] = (match_risk_summary['total_officers'] / 
                                                match_risk_summary['num_matches']).round(0).astype(int)
        
        # Get HIGH risk as baseline (most common)
        if 'HIGH' in match_risk_summary['risk_level'].values:
            baseline_officers = int(match_risk_summary[match_risk_summary['risk_level'] == 'HIGH']['avg_per_match'].iloc[0])
        else:
            # Fallback to overall average
            baseline_officers = int(data['deployment'].groupby('match_id')['officers'].sum().mean())
        
        # Calculate scenarios as percentages of baseline
        conservative_officers = int(baseline_officers * 0.75)  # 75% of baseline
        balanced_officers = baseline_officers  # 100% (actual HIGH risk deployment)
        aggressive_officers = int(baseline_officers * 1.15)  # 115% of baseline
        
        # Calculate total shifts for 6 matches (assuming all HIGH risk for comparison)
        num_matches = 6
        conservative_total = conservative_officers * num_matches
        balanced_total = balanced_officers * num_matches
        aggressive_total = aggressive_officers * num_matches
        
        # Get average amplification from deployment data
        if 'amplification' in data['deployment'].columns:
            avg_amplification = data['deployment']['amplification'].mean()
            conservative_amp = avg_amplification * 0.80
            balanced_amp = avg_amplification
            aggressive_amp = avg_amplification * 1.20
        else:
            avg_amplification = 1.6
            conservative_amp = 1.3
            balanced_amp = 1.6
            aggressive_amp = 1.9
        
        # Calculate actual total deployment
        actual_total = data['deployment'].groupby('match_id')['officers'].sum().sum()
        
    else:
        # Final fallback if no deployment data at all
        baseline_officers = 28
        conservative_officers = 21
        balanced_officers = 28
        aggressive_officers = 32
        conservative_amp = 1.3
        balanced_amp = 1.6
        aggressive_amp = 1.9
        conservative_total = 126
        balanced_total = 168
        aggressive_total = 192
        actual_total = 165
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Conservative</div>
            <div class="metric-value">{conservative_officers}</div>
            <div class="metric-label">officers/match ({conservative_amp:.2f}x)</div>
            <div class="metric-label" style="margin-top:10px">~70% coverage</div>
            <div class="metric-label" style="font-size:10px; margin-top:5px; color:#666;">
            Total: {conservative_total} shifts
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border: 3px solid #003366;">
            <div class="metric-label">⭐ Balanced (Recommended)</div>
            <div class="metric-value">{balanced_officers}</div>
            <div class="metric-label">officers/match ({balanced_amp:.2f}x)</div>
            <div class="metric-label" style="margin-top:10px">~85% coverage</div>
            <div class="metric-label" style="font-size:10px; margin-top:5px; color:#003366;">
            <b>Actual Total: {actual_total} shifts</b>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Aggressive</div>
            <div class="metric-value">{aggressive_officers}</div>
            <div class="metric-label">officers/match ({aggressive_amp:.2f}x)</div>
            <div class="metric-label" style="margin-top:10px">~95% coverage</div>
            <div class="metric-label" style="font-size:10px; margin-top:5px; color:#666;">
            Total: {aggressive_total} shifts
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add explanation below scenarios
    st.markdown(f"""
    <div class="insight-box" style="margin-top:20px;">
    <b>Scenario Comparison:</b><br>
    • <b>Conservative</b>: Deploy fewer officers ({conservative_officers}/match), rely more on organic patrol coverage. Lower cost but higher risk.<br>
    • <b>Balanced (Current Plan)</b>: Deploy {balanced_officers}/match at HIGH-risk matches, {balanced_officers-1}/match at MEDIUM-HIGH. 
      Based on {balanced_amp:.2f}x average amplification across priority stations.<br>
    • <b>Aggressive</b>: Maximum coverage ({aggressive_officers}/match), higher cost but lowest risk exposure. Suitable if Match 1 reveals higher-than-expected crime rates.<br><br>
    <b>Recommendation:</b> Start with Balanced deployment ({actual_total} total shifts). After Match 1, measure actual crime rates and officer capacity, 
    then adjust Matches 2-6 allocation accordingly. Adaptive learning eliminates the need to guess scenarios upfront.
    </div>
    """, unsafe_allow_html=True)
    
    # Adaptive learning
    st.markdown("---")
    st.subheader("🔄 Adaptive Learning Strategy")
    
    st.markdown("""
    <div class="insight-box">
    <b>Match 1 (June 12): TEST PHASE</b><br>
    → Deploy baseline officers at 10 priority stations<br>
    → <b>MEASURE</b> actual crimes at each station during deployment<br>
    → <b>COMPARE</b> predicted vs actual amplification ratios<br>
    → <b>IDENTIFY</b> over/under-resourced stations
    </div>
    
    <div class="insight-box">
    <b>Matches 2-3: ADJUSTMENT PHASE</b><br>
    → Reallocate based on Match 1 actuals<br>
    → Shift officers from quiet stations to busy ones<br>
    → Continue measuring and refining predictions
    </div>
    
    <div class="insight-box">
    <b>Matches 4-6: OPTIMIZED PHASE</b><br>
    → Deploy based on 3-match empirical average<br>
    → Final refined strategy with validated multipliers<br>
    → Maximum deployment efficiency achieved
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PAGE 4: DATA EXPLORER
# ============================================================================
elif page == "📈 Data Explorer":
    st.title("📈 Data Explorer")
    
    # Dataset selector
    dataset = st.selectbox(
        "Select Dataset",
        [
            "Station Risk Profiles",
            "FIFA Affected Stations",
            "Event Amplification Analysis",
            "Deployment Schedule"
        ]
    )
    
    if dataset == "Station Risk Profiles":
        st.subheader(f"Station Risk Profiles ({len(data['profiles'])} Stations)")
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            risk_filter = st.multiselect(
                "Filter by Risk Category",
                options=data['profiles']['risk_category'].unique(),
                default=data['profiles']['risk_category'].unique()
            )
        
        with col2:
            min_crimes = st.slider(
                "Minimum Total Crimes",
                0,
                int(data['profiles']['total_crimes'].max()),
                0
            )
        
        filtered_df = data['profiles'][
            (data['profiles']['risk_category'].isin(risk_filter)) &
            (data['profiles']['total_crimes'] >= min_crimes)
        ]
        
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            "station_risk_profiles.csv",
            "text/csv"
        )
    
    elif dataset == "FIFA Affected Stations":
        st.subheader(f"FIFA Affected Stations ({len(data['fifa_priority'])} Priority Stations)")
        
        st.dataframe(
            data['fifa_priority'],
            use_container_width=True,
            hide_index=True
        )
        
        csv = data['fifa_priority'].to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            "fifa_priority_stations.csv",
            "text/csv"
        )
    
    elif dataset == "Event Amplification Analysis":
        st.subheader("Event Amplification Analysis (CORRECTED)")
        
        st.markdown("""
        **CRITICAL UPDATE:** This uses corrected event amplification (2.61x average).
        
        **Old Method (WRONG):** Compared ALL Fri/Sat vs Mon-Thu (1.08x - diluted signal)
        
        **New Method (CORRECT):** Identified anomalous high-crime days during sports seasons (2.61x)
        
        **Methodology:** 
        - Identified days with crime >1.5 SD above day-of-week baseline
        - Filtered to Leafs (Oct-May) and Jays (Apr-Oct) seasons
        - Compared these 156 likely event days vs all other days
        
        **Result:** Events amplify crime by 2.61x (not 1.08x)
        """)
        
        st.dataframe(
            data['activity'],
            use_container_width=True,
            hide_index=True
        )
        
        csv = data['activity'].to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            "event_amplification_FIXED.csv",
            "text/csv"
        )
    
    elif dataset == "Deployment Schedule":
        st.subheader("FIFA 2026 Deployment Schedule (UPDATED)")
        
        st.markdown("""
        **Schedule Updated:** Official FIFA 2026 Toronto match dates and times.
        
        **Total Deployment:** 111 officer-shifts across 6 matches
        
        **Risk Distribution:**
        - HIGH (1.3x): 3 matches (Fri/Sat afternoon)
        - MEDIUM-HIGH (1.15x): 3 matches (Weekday evening)
        """)
        
        st.dataframe(
            data['deployment'],
            use_container_width=True,
            hide_index=True
        )
        
        csv = data['deployment'].to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download CSV",
            csv,
            "fifa_deployment_schedule.csv",
            "text/csv"
        )

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <b>Toronto Police Service - Transit Safety Intelligence Dashboard</b><br>
    Data Analysis Period: 2018-2025 ({data['total_crimes']:,} crimes) | FIFA 2026 Readiness Assessment<br>
    Developed for TPS Strategic Planning & FIFA World Cup 2026
</div>
""", unsafe_allow_html=True)