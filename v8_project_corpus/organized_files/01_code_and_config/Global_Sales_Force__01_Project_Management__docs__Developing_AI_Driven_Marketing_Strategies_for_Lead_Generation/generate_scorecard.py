import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Agg')

# Load audit data
with open('/home/ubuntu/audit_websites_geo.json', 'r') as f:
    data = json.load(f)

results = data['results']

# Define scoring criteria (each out of points shown)
# Total possible: 100 points
scoring = {
    'site_loads': 5,           # Site loads successfully
    'https_enabled': 5,        # HTTPS
    'mobile_responsive': 5,    # Mobile responsive
    'schema_markup_present': 15, # Schema markup (critical for GEO)
    'llms_txt_exists': 10,     # llms.txt file
    'robots_txt_ai_crawlers': 10, # AI crawler access
    'faq_content': 10,         # FAQ content
    'meta_description': 5,     # Meta description
    'blog_or_resources': 10,   # Blog/resources
    'reviews_displayed': 10,   # Reviews displayed
    'team_about_page': 5,      # Team/about page
    'service_area_pages': 5,   # Service area pages
    'gbp_link': 5,             # Google Business Profile link
}

def score_field(field_name, value):
    """Score a field based on its value"""
    max_points = scoring[field_name]
    val = value.upper().strip() if value else ''
    
    if val.startswith('YES'):
        return max_points
    elif val.startswith('PARTIAL'):
        return max_points * 0.5
    elif val.startswith('REDIRECT'):
        return max_points * 0.5
    elif val.startswith('ALLOWED'):
        return max_points
    elif val.startswith('NOT_MENTIONED'):
        # Not blocking = partial credit (they're not blocking but not explicitly allowing)
        return max_points * 0.7
    elif val.startswith('NO_ROBOTS_TXT'):
        return max_points * 0.3
    elif val.startswith('BLOCKED'):
        return 0
    elif val.startswith('NO'):
        return 0
    elif val.startswith('NONE'):
        return 0
    else:
        return 0

# Build scorecard
scorecard = []
for r in results:
    domain = r['output']['domain']
    scores = {}
    total = 0
    
    for field, max_pts in scoring.items():
        val = r['output'].get(field, '')
        pts = score_field(field, val)
        scores[field] = pts
        total += pts
    
    # Schema types bonus info
    schema_types = r['output'].get('schema_types_found', 'NONE')
    
    entry = {
        'domain': domain,
        'total_score': total,
        'grade': '',
        **scores,
        'schema_types': schema_types,
        'notes': r['output'].get('overall_notes', '')
    }
    scorecard.append(entry)

# Assign grades
for entry in scorecard:
    s = entry['total_score']
    if s >= 85:
        entry['grade'] = 'A'
    elif s >= 70:
        entry['grade'] = 'B'
    elif s >= 55:
        entry['grade'] = 'C'
    elif s >= 40:
        entry['grade'] = 'D'
    else:
        entry['grade'] = 'F'

# Sort by score descending
scorecard.sort(key=lambda x: x['total_score'], reverse=True)

# Save scorecard as JSON for the report
with open('/home/ubuntu/scorecard_data.json', 'w') as f:
    json.dump(scorecard, f, indent=2)

# Print summary
print("=" * 80)
print("GEO READINESS SCORECARD — GLOBAL SALES FORCE")
print("=" * 80)
for entry in scorecard:
    print(f"  {entry['grade']}  {entry['total_score']:5.1f}/100  {entry['domain']}")
print()

# Calculate category averages
categories = {
    'Technical Foundation': ['site_loads', 'https_enabled', 'mobile_responsive'],
    'AI Discoverability': ['schema_markup_present', 'llms_txt_exists', 'robots_txt_ai_crawlers'],
    'Content Quality': ['faq_content', 'meta_description', 'blog_or_resources'],
    'Trust & Authority': ['reviews_displayed', 'team_about_page', 'gbp_link'],
    'Local SEO': ['service_area_pages'],
}

cat_max = {
    'Technical Foundation': 15,
    'AI Discoverability': 35,
    'Content Quality': 25,
    'Trust & Authority': 20,
    'Local SEO': 5,
}

# Average scores by category across all 14 sites
cat_avgs = {}
for cat, fields in categories.items():
    total = sum(sum(e[f] for f in fields) for e in scorecard) / len(scorecard)
    max_total = sum(scoring[f] for f in fields)
    cat_avgs[cat] = (total / max_total) * 100

print("\nCategory Averages (% of max):")
for cat, avg in cat_avgs.items():
    print(f"  {cat}: {avg:.1f}%")

# ============================================================
# VISUALIZATION 1: Overall Scorecard Bar Chart
# ============================================================
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(14, 8))

domains = [e['domain'] for e in scorecard]
scores = [e['total_score'] for e in scorecard]
grades = [e['grade'] for e in scorecard]

# Shorten domain names for display
short_domains = []
for d in domains:
    d_short = d.replace('.com', '').replace('.net', '').replace('www.', '')
    if len(d_short) > 25:
        d_short = d_short[:22] + '...'
    short_domains.append(d_short)

# Color by grade
colors = []
for g in grades:
    if g == 'A': colors.append('#2ecc71')
    elif g == 'B': colors.append('#3498db')
    elif g == 'C': colors.append('#f39c12')
    elif g == 'D': colors.append('#e67e22')
    else: colors.append('#e74c3c')

bars = ax.barh(range(len(domains)), scores, color=colors, edgecolor='white', height=0.7)

# Add score labels
for i, (score, grade) in enumerate(zip(scores, grades)):
    ax.text(score + 1, i, f'{score:.0f}/100 ({grade})', va='center', fontsize=10, fontweight='bold')

ax.set_yticks(range(len(domains)))
ax.set_yticklabels(short_domains, fontsize=9)
ax.set_xlabel('GEO Readiness Score (out of 100)', fontsize=12)
ax.set_title('GEO Readiness Scorecard — Global Sales Force (14 Brands)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlim(0, 110)
ax.invert_yaxis()

# Add grade legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2ecc71', label='A (85-100)'),
    Patch(facecolor='#3498db', label='B (70-84)'),
    Patch(facecolor='#f39c12', label='C (55-69)'),
    Patch(facecolor='#e67e22', label='D (40-54)'),
    Patch(facecolor='#e74c3c', label='F (0-39)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)

plt.tight_layout()
plt.savefig('/home/ubuntu/scorecard_overall.png', dpi=150, bbox_inches='tight')
plt.close()
print("\nSaved: scorecard_overall.png")

# ============================================================
# VISUALIZATION 2: Category Breakdown Heatmap
# ============================================================
fig, ax = plt.subplots(figsize=(16, 10))

# Build matrix: rows = domains, cols = scoring fields
field_labels = {
    'site_loads': 'Site\nLoads',
    'https_enabled': 'HTTPS',
    'mobile_responsive': 'Mobile',
    'schema_markup_present': 'Schema\nMarkup',
    'llms_txt_exists': 'llms.txt',
    'robots_txt_ai_crawlers': 'AI\nCrawlers',
    'faq_content': 'FAQ\nContent',
    'meta_description': 'Meta\nDesc',
    'blog_or_resources': 'Blog',
    'reviews_displayed': 'Reviews',
    'team_about_page': 'Team/\nAbout',
    'service_area_pages': 'Service\nAreas',
    'gbp_link': 'GBP\nLink',
}

fields = list(scoring.keys())
matrix = []
for e in scorecard:
    row = []
    for f in fields:
        max_pts = scoring[f]
        pct = (e[f] / max_pts * 100) if max_pts > 0 else 0
        row.append(pct)
    matrix.append(row)

matrix = np.array(matrix)

# Custom colormap: red -> yellow -> green
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('rg', ['#e74c3c', '#f39c12', '#2ecc71'])

im = ax.imshow(matrix, cmap=cmap, aspect='auto', vmin=0, vmax=100)

ax.set_xticks(range(len(fields)))
ax.set_xticklabels([field_labels[f] for f in fields], fontsize=9, ha='center')
ax.set_yticks(range(len(scorecard)))
ax.set_yticklabels([e['domain'] for e in scorecard], fontsize=9)

# Add text annotations
for i in range(len(scorecard)):
    for j in range(len(fields)):
        val = matrix[i, j]
        symbol = '●' if val == 100 else ('◐' if val > 0 else '✗')
        color = 'white' if val < 50 else 'black'
        ax.text(j, i, symbol, ha='center', va='center', fontsize=12, color=color, fontweight='bold')

ax.set_title('GEO Readiness Heatmap — Feature by Feature', fontsize=14, fontweight='bold', pad=15)

# Category brackets at top
cat_positions = {
    'Technical\nFoundation': (0, 2),
    'AI\nDiscoverability': (3, 5),
    'Content\nQuality': (6, 8),
    'Trust &\nAuthority': (9, 11),
    'Local\nSEO': (12, 12),
}

# Add colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.6, pad=0.02)
cbar.set_label('Score %', fontsize=10)

# Legend
ax.text(0, len(scorecard) + 0.8, '● = Full Score    ◐ = Partial    ✗ = Missing', 
        fontsize=10, ha='left', style='italic')

plt.tight_layout()
plt.savefig('/home/ubuntu/scorecard_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: scorecard_heatmap.png")

# ============================================================
# VISUALIZATION 3: Category Averages Radar/Bar
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))

cats = list(cat_avgs.keys())
avgs = [cat_avgs[c] for c in cats]

bar_colors = ['#3498db', '#e74c3c', '#f39c12', '#2ecc71', '#9b59b6']
bars = ax.barh(cats, avgs, color=bar_colors, edgecolor='white', height=0.6)

for i, (avg, cat) in enumerate(zip(avgs, cats)):
    ax.text(avg + 1, i, f'{avg:.0f}%', va='center', fontsize=11, fontweight='bold')

ax.set_xlim(0, 110)
ax.set_xlabel('Average Score Across All 14 Brands (%)', fontsize=11)
ax.set_title('GEO Category Performance — Portfolio Average', fontsize=14, fontweight='bold', pad=15)
ax.invert_yaxis()

# Add benchmark line at 70%
ax.axvline(x=70, color='red', linestyle='--', alpha=0.5, label='Target: 70%')
ax.legend(fontsize=10)

plt.tight_layout()
plt.savefig('/home/ubuntu/scorecard_categories.png', dpi=150, bbox_inches='tight')
plt.close()
print("Saved: scorecard_categories.png")

# ============================================================
# Print detailed data for report
# ============================================================
print("\n" + "=" * 80)
print("DETAILED SCORING")
print("=" * 80)
for e in scorecard:
    print(f"\n{e['domain']} — {e['total_score']:.0f}/100 (Grade: {e['grade']})")
    print(f"  Schema Types: {e['schema_types']}")
    for f in fields:
        max_pts = scoring[f]
        pts = e[f]
        status = '✓' if pts == max_pts else ('~' if pts > 0 else '✗')
        print(f"  {status} {field_labels[f].replace(chr(10), ' ')}: {pts:.0f}/{max_pts}")

# Count critical gaps
print("\n" + "=" * 80)
print("CRITICAL GAPS SUMMARY")
print("=" * 80)
gap_counts = {}
for f in fields:
    count = sum(1 for e in scorecard if e[f] == 0)
    if count > 0:
        gap_counts[f] = count

for f, count in sorted(gap_counts.items(), key=lambda x: -x[1]):
    print(f"  {field_labels[f].replace(chr(10), ' ')}: {count}/14 sites MISSING")

print("\nDone!")
