from dash.dependencies import Input, Output

from app import app


@app.callback(Output(component_id='page-header', component_property='children'),
              Input(component_id='page-switch', component_property='value'))
def update_page_header(page_id):
    if page_id == 'OS':
        return 'Ordered Spend'
    else:
        return 'Supplier Performance'
