# Theme configuration for the Hypixel Stats Dashboard

THEME = {
    # Background colors
    'bg_primary': '#0f0f1a',      # Main background (deep dark blue)
    'bg_secondary': '#1a1a2e',    # Cards background
    'bg_tertiary': '#16213e',     # Sidebar background
    'bg_hover': '#1f2b47',        # Hover state

    # Text colors
    'text_primary': '#ffffff',
    'text_secondary': '#a0aec0',
    'text_muted': '#718096',

    # Accent colors
    'accent_primary': '#6366f1',   # Indigo
    'accent_success': '#10b981',   # Green
    'accent_warning': '#f59e0b',   # Amber
    'accent_danger': '#ef4444',    # Red
    'accent_info': '#3b82f6',      # Blue

    # Border
    'border_color': '#2d3748',
    'border_radius': '12px',

    # Shadows
    'shadow_sm': '0 2px 4px rgba(0, 0, 0, 0.3)',
    'shadow_md': '0 4px 12px rgba(0, 0, 0, 0.4)',
    'shadow_lg': '0 8px 24px rgba(0, 0, 0, 0.5)',

    # Glassmorphism effect
    'glass_bg': 'rgba(26, 26, 46, 0.8)',
    'glass_border': 'rgba(255, 255, 255, 0.1)',
}

# Chart color palette
CHART_COLORS = [
    '#6366f1',  # Indigo
    '#10b981',  # Emerald
    '#f59e0b',  # Amber
    '#ef4444',  # Red
    '#3b82f6',  # Blue
    '#8b5cf6',  # Violet
    '#ec4899',  # Pink
    '#14b8a6',  # Teal
    '#f97316',  # Orange
    '#84cc16',  # Lime
]

# Chart layout configuration
CHART_LAYOUT = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {
        'color': THEME['text_primary'],
        'family': 'Inter, system-ui, sans-serif',
    },
    'xaxis': {
        'gridcolor': THEME['border_color'],
        'zerolinecolor': THEME['border_color'],
    },
    'yaxis': {
        'gridcolor': THEME['border_color'],
        'zerolinecolor': THEME['border_color'],
    },
    'legend': {
        'bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': THEME['text_secondary']},
    },
    'margin': {'l': 40, 'r': 20, 't': 60, 'b': 40},
}
