import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Load audit data
with open('/home/ubuntu/audit_intl_websites_geo.json', 'r') as f:
    data = json.load(f)

results = data['results']

# Define scoring weights per category
# Category 1: Technical Foundation (20 points)
#   - site_loads (5), https_enabled (5), viewport_meta (5), robots_txt_exists (5)
# Category 2: AI Discoverability (25 points)
#   - robots_ai_crawlers (8), llms_txt_exists (8), schema_jsonld (5), moving_company_schema (4)
# Category 3: Content Quality (20 points)
#   - meta_description (5), faq_section (5), blog_resources (5), service_area_pages (5)
# Category 4: Trust & Authority (20 points)
#   - about_team_page (5), reviews_testimonials (5), contact_info_visible (5), gbp_link (5)
# Category 5: Entity Authority (15 points)
#   - moving_company_schema (5), meta_description (5), about_team_page (5)
# Note: some fields contribute to multiple categories

def score_site(r):
    o = r['output']
    scores = {}
    
    # Technical Foundation (20 pts)
    tech = 0
    tech += 5 if o.get('site_loads') else 0
    tech += 5 if o.get('https_enabled') else 0
    tech += 5 if o.get('viewport_meta') else 0
    tech += 5 if o.get('robots_txt_exists') else 0
    scores['Technical Foundation'] = tech
    
    # AI Discoverability (25 pts)
    ai = 0
    ai += 8 if o.get('robots_ai_crawlers') else 0
    ai += 8 if o.get('llms_txt_exists') else 0
    ai += 5 if o.get('schema_jsonld') else 0
    ai += 4 if o.get('moving_company_schema') else 0
    scores['AI Discoverability'] = ai
    
    # Content Quality (20 pts)
    content = 0
    content += 5 if o.get('meta_description') else 0
    content += 5 if o.get('faq_section') else 0
    content += 5 if o.get('blog_resources') else 0
    content += 5 if o.get('service_area_pages') else 0
    scores['Content Quality'] = content
    
    # Trust & Authority (20 pts)
    trust = 0
    trust += 5 if o.get('about_team_page') else 0
    trust += 5 if o.get('reviews_testimonials') else 0
    trust += 5 if o.get('contact_info_visible') else 0
    trust += 5 if o.get('gbp_link') else 0
    scores['Trust & Authority'] = trust
    
    # Entity Authority (15 pts)
    entity = 0
    entity += 5 if o.get('moving_company_schema') else 0
    entity += 5 if o.get('meta_description') else 0
    entity += 5 if o.get('about_team_page') else 0
    scores['Entity Authority'] = entity
    
    total = sum(scores.values())
    scores['Total'] = total
    
    return scores

# Calculate scores
site_scores = {}
for r in results:
    domain = r['output']['domain']
    site_scores[domain] = score_site(r)

# Print scores
print("=" * 80)
print("INTERNATIONAL PORTFOLIO GEO SCORECARD")
print("=" * 80)
for domain, scores in sorted(site_scores.items(), key=lambda x: x[1]['Total'], reverse=True):
    total = scores['Total']
    grade = 'A' if total >= 80 else 'B' if total >= 65 else 'C' if total >= 50 else 'D' if total >= 35 else 'F'
    print(f"\n{domain}: {total}/100 ({grade})")
    for cat, val in scores.items():
        if cat != 'Total':
            max_pts = {'Technical Foundation': 20, 'AI Discoverability': 25, 'Content Quality': 20, 'Trust & Authority': 20, 'Entity Authority': 15}
            print(f"  {cat}: {val}/{max_pts[cat]}")

# Save scores to JSON for report
scores_export = {}
for domain, scores in site_scores.items():
    total = scores['Total']
    grade = 'A' if total >= 80 else 'B' if total >= 65 else 'C' if total >= 50 else 'D' if total >= 35 else 'F'
    scores_export[domain] = {**scores, 'Grade': grade}

with open('/home/ubuntu/intl_scores.json', 'w') as f:
    json.dump(scores_export, f, indent=2)

# --- VISUALIZATION 1: Overall Scorecard Bar Chart ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'

domains = sorted(site_scores.keys(), key=lambda x: site_scores[x]['Total'], reverse=True)
totals = [site_scores[d]['Total'] for d in domains]
short_domains = [d.replace('.com', '').replace('.net', '') for d in domains]
grades = []
for t in totals:
    grades.append('A' if t >= 80 else 'B' if t >= 65 else 'C' if t >= 50 else 'D' if t >= 35 else 'F')

colors = []
for t in totals:
    if t >= 80: colors.append('#2ecc71')
    elif t >= 65: colors.append('#27ae60')
    elif t >= 50: colors.append('#f39c12')
    elif t >= 35: colors.append('#e67e22')
    else: colors.append('#e74c3c')

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(range(len(domains)), totals, color=colors, height=0.6, edgecolor='white', linewidth=1.5)

for i, (bar, total, grade) in enumerate(zip(bars, totals, grades)):
    ax.text(total + 1.5, bar.get_y() + bar.get_height()/2, f'{total}/100 ({grade})', 
            va='center', fontsize=13, fontweight='bold', color='#2c3e50')

ax.set_yticks(range(len(domains)))
ax.set_yticklabels(short_domains, fontsize=12, fontweight='bold')
ax.set_xlim(0, 110)
ax.set_xlabel('GEO Readiness Score', fontsize=12, fontweight='bold')
ax.set_title('International Portfolio — GEO Readiness Scorecard', fontsize=16, fontweight='bold', pad=15)
ax.invert_yaxis()

# Add threshold lines
ax.axvline(x=80, color='#2ecc71', linestyle='--', alpha=0.5, linewidth=1)
ax.axvline(x=50, color='#f39c12', linestyle='--', alpha=0.5, linewidth=1)
ax.text(81, len(domains)-0.3, 'A threshold', fontsize=8, color='#2ecc71', alpha=0.7)
ax.text(51, len(domains)-0.3, 'C threshold', fontsize=8, color='#f39c12', alpha=0.7)

plt.tight_layout()
plt.savefig('/home/ubuntu/intl_scorecard_overall.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("\nSaved: intl_scorecard_overall.png")

# --- VISUALIZATION 2: Category Heatmap ---
categories = ['Technical Foundation', 'AI Discoverability', 'Content Quality', 'Trust & Authority', 'Entity Authority']
max_pts = [20, 25, 20, 20, 15]

fig, ax = plt.subplots(figsize=(12, 5))

# Create percentage matrix
matrix = []
for d in domains:
    row = []
    for cat, mx in zip(categories, max_pts):
        pct = (site_scores[d][cat] / mx) * 100
        row.append(pct)
    matrix.append(row)

matrix = np.array(matrix)

# Custom colormap
from matplotlib.colors import LinearSegmentedColormap
colors_map = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71']
cmap = LinearSegmentedColormap.from_list('custom', colors_map, N=256)

im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=0, vmax=100)

ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, fontsize=10, fontweight='bold', rotation=15, ha='right')
ax.set_yticks(range(len(domains)))
ax.set_yticklabels(short_domains, fontsize=11, fontweight='bold')

# Add text annotations
for i in range(len(domains)):
    for j in range(len(categories)):
        val = matrix[i][j]
        raw = site_scores[domains[i]][categories[j]]
        mx = max_pts[j]
        text_color = 'white' if val < 40 else 'black'
        ax.text(j, i, f'{raw}/{mx}\n({val:.0f}%)', ha='center', va='center', 
                fontsize=9, fontweight='bold', color=text_color)

ax.set_title('International Portfolio — Category Breakdown Heatmap', fontsize=14, fontweight='bold', pad=15)
cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('Score %', fontsize=10)

plt.tight_layout()
plt.savefig('/home/ubuntu/intl_scorecard_heatmap.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: intl_scorecard_heatmap.png")

# --- VISUALIZATION 3: Category Averages ---
fig, ax = plt.subplots(figsize=(10, 5))

cat_avgs = []
for cat, mx in zip(categories, max_pts):
    avg = np.mean([site_scores[d][cat] for d in domains])
    avg_pct = (avg / mx) * 100
    cat_avgs.append(avg_pct)

bar_colors = []
for pct in cat_avgs:
    if pct >= 80: bar_colors.append('#2ecc71')
    elif pct >= 60: bar_colors.append('#27ae60')
    elif pct >= 40: bar_colors.append('#f39c12')
    else: bar_colors.append('#e74c3c')

bars = ax.bar(range(len(categories)), cat_avgs, color=bar_colors, width=0.6, edgecolor='white', linewidth=1.5)

for bar, pct in zip(bars, cat_avgs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{pct:.0f}%', 
            ha='center', fontsize=13, fontweight='bold', color='#2c3e50')

ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, fontsize=10, fontweight='bold', rotation=15, ha='right')
ax.set_ylim(0, 110)
ax.set_ylabel('Average Score %', fontsize=12, fontweight='bold')
ax.set_title('International Portfolio — Average Category Scores', fontsize=14, fontweight='bold', pad=15)

ax.axhline(y=80, color='#2ecc71', linestyle='--', alpha=0.4, linewidth=1)
ax.axhline(y=50, color='#f39c12', linestyle='--', alpha=0.4, linewidth=1)

plt.tight_layout()
plt.savefig('/home/ubuntu/intl_scorecard_categories.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("Saved: intl_scorecard_categories.png")

# Print portfolio average
avg_total = np.mean([site_scores[d]['Total'] for d in domains])
print(f"\nPortfolio Average: {avg_total:.0f}/100")
