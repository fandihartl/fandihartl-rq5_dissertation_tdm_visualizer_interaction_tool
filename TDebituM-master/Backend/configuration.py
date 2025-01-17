import os

#dash-auth user and passwords pairs. Need to save them in a save place.
#USER1 = os.getenv("USER1")
#PW1 = os.getenv("PW1")

#VALID_USERNAME_PASSWORD_PAIRS = {USER1: PW1}

# Select Backend connection
DATABASE = "Neo4j Aura"     # cloud service 
#DATABASE = "local DBMS"     # local neo4j DBMS 

if DATABASE == "local DBMS":
    NEO4J_SCHEME = "bolt"
    NEO4J_HOST = "localhost"
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME_LOCAL")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD_LOCAL")

elif DATABASE == "Neo4j Aura":
    NEO4J_SCHEME = os.getenv("NEO4J_SCHEME")
    NEO4J_HOST = os.getenv("NEO4J_HOST")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


# BubbleChart Parties
PARTIES = ['PUR', 'SAL', 'VER', 'MA', 'ME', 'EE', 'SE']

SANKEY_COLORS = {
    "ME": "rgba(255, 99, 71, 0.4)",
    "EE": "rgba(31, 119, 180, 0.4)",
    "SE": "rgba(255,182,193, 0.4)",
    "MA": "rgba(186,85,211, 0.4)",
    "SAL": "rgba(102, 0, 255, 0.4)",
    "PUR": "rgba(0, 153, 51, 0.4)",
    "SUP": "rgba(255, 51, 204, 0.4)",
    "Supplier": "rgba(204, 153, 0, 0.4)",
    "Purchasing Department": "rgba(153, 102, 0.4)",
    "Assembly": "rgba(204, 153, 0, 0.4)",
    "Testing": "rgba(0, 204, 102, 0.4)",
    "all": "rgba(204, 153, 0, 0.4)",
    "CUS": "rgba(204, 153, 0, 0.4)",
    "VER": "rgba(51, 102, 153, 0.4)"
}

TD_TYPES = ['Manufacturing TD', 'Test TD', 'Infrastructure TD', 'Requirements TD', 'Industrial Engineering TD',
            'Maintenance TD', 'Variants TD', 'Documentation TD', 'Process TD', 'Defect TD', 'Design TD', 'Architectural TD']
TD_TYPES_COLORS = {
    'Manufacturing TD': 'Coral', 
    'Test TD': 'rgba(255,0,0,0.9)',
    'Infrastructure TD': 'BlueViolet',
    'Requirements TD': 'Crimson',
    'Industrial Engineering TD': 'Cyan',
    'Maintenance TD': 'DarkOliveGreen',
    'Variants TD': 'DarkOrange',
    'Documentation TD': 'DeepSkyBlue',
    'Process TD': 'Gold',
    'Defect TD': 'IndianRed',
    'Design TD': 'PaleGreen',
    'Architectural TD': 'Pink'
} #REVIEW: improve palette

TITLE_STYLE = {
    "position": "fixed",
    "padding": "0rem 1rem",
    "top": 0,
    "left": 0,
    "width": "100vw",
    "height" : "4rem",
    "background-color": "rgb(191, 191, 191)",
}

SIDEBAR_STYLE = {
    "margin-top": "4rem",
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "1rem 1rem",
    "background-color": "rgb(217, 217, 217)",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "14rem",
    "margin-right": "25rem",
    "margin-top": "4rem",
    "padding": "2rem 1rem",
}

CONTROLS_STYLE = {
    "width": "25rem", "position": "fixed",
    "top": "9.5rem",
    "right": 10
}

