from pathlib import Path
import random
import sqlite3
from datetime import date, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
PDFS = DATA / 'pdfs'
DB = DATA / 'sales_onboarding.db'

PRODUCTS = [
    (1, 'Sales Starter', 'Subscription', 99),
    (2, 'Growth CRM', 'Subscription', 249),
    (3, 'Enterprise Enablement', 'Services', 1200),
    (4, 'Onboarding Accelerator', 'Services', 800),
    (5, 'Analytics Add-on', 'Subscription', 149),
]
REGIONS = [(1, 'North America'), (2, 'EMEA'), (3, 'APAC'), (4, 'LATAM')]
CUSTOMERS = [
    (1, 'Acme Corp', 1, 'Mid-market'), (2, 'Globex', 2, 'Enterprise'),
    (3, 'Initech', 1, 'SMB'), (4, 'Umbrella Retail', 3, 'Enterprise'),
    (5, 'Hooli', 4, 'Mid-market'), (6, 'Stark Industries', 1, 'Enterprise'),
]

def generate_db():
    DATA.mkdir(exist_ok=True)
    if DB.exists():
        DB.unlink()
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.executescript('''
    CREATE TABLE products(id INTEGER PRIMARY KEY, name TEXT, category TEXT, price REAL);
    CREATE TABLE regions(id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, region_id INTEGER, segment TEXT);
    CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, quantity INTEGER, created_at TEXT);
    CREATE TABLE onboarding_events(id INTEGER PRIMARY KEY, rep_name TEXT, event_type TEXT, completed_at TEXT);
    ''')
    cur.executemany('INSERT INTO products VALUES (?,?,?,?)', PRODUCTS)
    cur.executemany('INSERT INTO regions VALUES (?,?)', REGIONS)
    cur.executemany('INSERT INTO customers VALUES (?,?,?,?)', CUSTOMERS)
    start = date(2026, 1, 1)
    order_id = 1
    random.seed(7)
    for day in range(120):
        d = start + timedelta(days=day)
        for _ in range(random.randint(2, 7)):
            customer = random.choice(CUSTOMERS)[0]
            product = random.choice(PRODUCTS)[0]
            qty = random.randint(1, 12)
            cur.execute('INSERT INTO orders VALUES (?,?,?,?,?)', (order_id, customer, product, qty, d.isoformat()))
            order_id += 1
    events = [
        ('Maya', 'CRM bootcamp', '2026-01-05'), ('Maya', 'Mock discovery call', '2026-01-08'),
        ('Ethan', 'Security training', '2026-02-02'), ('Ava', 'Pricing certification', '2026-02-10'),
        ('Noah', 'Product demo certification', '2026-03-18'),
    ]
    cur.executemany('INSERT INTO onboarding_events(rep_name,event_type,completed_at) VALUES (?,?,?)', events)
    conn.commit()
    conn.close()
    print(f'Created {DB}')

def make_pdf(path: Path, title: str, sections: list[tuple[str, str]], table_data=None):
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles['Title']), Spacer(1, 12)]
    for heading, body in sections:
        story.append(Paragraph(heading, styles['Heading2']))
        story.append(Paragraph(body, styles['BodyText']))
        story.append(Spacer(1, 10))
    if table_data:
        tbl = Table(table_data, hAlign='LEFT')
        tbl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(tbl)
    doc = SimpleDocTemplate(str(path), pagesize=letter, rightMargin=48, leftMargin=48, topMargin=48, bottomMargin=48)
    doc.build(story)

def generate_pdfs():
    PDFS.mkdir(parents=True, exist_ok=True)
    make_pdf(
        PDFS / 'sales_playbook_2026.pdf',
        '2026 Sales Playbook',
        [
            ('Qualification Rules', 'A lead is qualified when budget, authority, need, and timeline are documented. Sales reps must record pain points, current tools, expected rollout date, and success metrics before moving an opportunity to proposal.'),
            ('Packages', 'Sales Starter includes core CRM workflows. Growth CRM adds pipeline analytics and forecasting. Enterprise Enablement includes implementation support, executive business reviews, security review assistance, and custom onboarding workshops.'),
            ('Discounting', 'Discounts over 15 percent require manager approval. Multi-year deals may receive services credits instead of subscription discounts.'),
            ('Refund Policy', 'Refund requests must be submitted within 30 days of invoice date. Services already delivered are non-refundable, but unused onboarding hours can be converted to enablement credits.'),
        ],
        [['Package', 'Best for', 'Implementation Support'], ['Sales Starter', 'SMB teams', 'Self-service'], ['Growth CRM', 'Scaling teams', 'Standard'], ['Enterprise Enablement', 'Large teams', 'Dedicated consultant']]
    )
    make_pdf(
        PDFS / 'new_hire_onboarding_guide.pdf',
        'Sales New Hire Onboarding Guide',
        [
            ('Week 1', 'Complete security training, CRM login setup, product overview, and shadow two discovery calls. New hires should learn the standard handoff from SDR to AE.'),
            ('Week 2', 'Practice discovery call scripts, learn objection handling, and complete the pricing certification. Managers review two mock calls and provide structured feedback.'),
            ('Week 3', 'Run a supervised product demo. Reps must explain setup requirements, onboarding timeline, data import process, and support escalation paths.'),
            ('Quality Bar', 'A new sales rep is considered ramp-ready when they pass product demo certification, pricing certification, and a manager-reviewed discovery call.'),
        ]
    )
    print(f'Created PDFs in {PDFS}')

if __name__ == '__main__':
    generate_db()
    generate_pdfs()
