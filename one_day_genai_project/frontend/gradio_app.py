import requests
import gradio as gr

API_URL = 'http://localhost:8000'

def ask(question, role):
    r = requests.post(f'{API_URL}/ask', json={'question': question, 'user_role': role}, timeout=30)
    data = r.json()
    sql = data.get('sql_executed') or ''
    sources = '\n\n'.join([f"{s['source']} p{s['page']}: {s['text'][:350]}" for s in data.get('sources', [])])
    return data['answer'], data['route'], sql, sources

with gr.Blocks(title='Sales + Onboarding AI') as demo:
    gr.Markdown('# Sales + Onboarding AI Assistant')
    q = gr.Textbox(label='Question', value='Top 3 products by revenue last month')
    role = gr.Dropdown(['sales_rep', 'manager', 'admin'], value='sales_rep', label='Role')
    btn = gr.Button('Ask')
    answer = gr.Textbox(label='Answer')
    route = gr.Textbox(label='Route')
    sql = gr.Code(label='SQL', language='sql')
    sources = gr.Textbox(label='Sources')
    btn.click(ask, inputs=[q, role], outputs=[answer, route, sql, sources])

demo.launch(server_port=7860)
