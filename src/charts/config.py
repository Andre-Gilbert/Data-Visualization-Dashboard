# Style
CHART_HEIGHT = 560
TITLE_FONT_SIZE = 18
CHART_MARGIN = {'t': 70, 'b': 40, 'l': 80, 'r': 80}
SAP_FONT = "'72', '72full', Arial, Helvetica, sans-serif"
SAP_TEXT_COLOR = '#32363a'
SAP_LABEL_COLOR = '#6a6d70'
IBCS_HUE_1 = '#000000'
IBCS_HUE_2 = '#999999'
SAP_UI_CHART_PALETTE_SEMANTIC_NEUTRAL = '#848f94'
SAP_UI_POINT_CHART_NUMBER = '#0854A0'
SAP_UI_POINT_CHART_LABEL = '#6a6d70'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_1 = '#5899DA'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_2 = '#E8743B'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_3 = '#19A979'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_4 = '#ED4A7B'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_5 = '#945ECF'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_6 = '#13A4B4'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_7 = '#525DF4'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_8 = '#BF399E'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_9 = '#6C8893'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_10 = '#EE6868'
SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_11 = '#2F6497'

SAP_UI_CHART_PALETTE_QUALITATIVE_HUES = [
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_1,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_2,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_3,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_4,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_5,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_6,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_7,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_8,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_9,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_10,
    SAP_UI_CHART_PALETTE_QUALITATIVE_HUE_11,
]

DEVIATION_CAUSES = [
    'no deviation',
    'delivery deviation - too late',
    'damaged goods (obvious defects)',
    'over-delivery',
    'under-delivery',
    'damaged goods and over-delivery',
    'damaged goods and under-delivery',
    'damaged goods and under-delivery',
    'over-delivery&delivery deviation - too late',
    'damaged goods & over-delivery & deliv. dev. - too late',
    'under-delivery&delivery deviation - too late',
]

DEVIATION_CAUSE_COLORS = dict(zip(DEVIATION_CAUSES, SAP_UI_CHART_PALETTE_QUALITATIVE_HUES))

# Strings
SUBTITLE_ORDERED_SPEND = 'Ordered Spend | EUR'
SUBTITLE_NUMBER_OF_ORDERS = 'Number of Orders'
DISPLAY = 'Display'
ORDERED_SPEND = 'Ordered Spend'
NUMBER_OF_ORDERS = 'Number of Orders'
TEMPLATE = 'plotly_white'

# Empty Graphs
EMPTY_GRAPH = {
    'layout': {
        'xaxis': {
            'visible': False
        },
        'yaxis': {
            'visible': False
        },
        'annotations': [{
            'text': 'No matching data found',
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {
                'size': 28,
                'color': SAP_UI_POINT_CHART_NUMBER
            }
        }]
    }
}

EMPTY_GRAPH_IBCS = {
    'layout': {
        'xaxis': {
            'visible': False
        },
        'yaxis': {
            'visible': False
        },
        'annotations': [{
            'text': 'No matching data found',
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {
                'size': 28,
                'color': IBCS_HUE_1
            }
        }]
    }
}
