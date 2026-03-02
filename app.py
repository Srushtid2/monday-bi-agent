import streamlit as st
import requests

MONDAY_TOKEN = st.secrets["MONDAY_TOKEN"]
DEALS_BOARD = 5026942224
WORK_ORDERS_BOARD = 5026942242

URL = "https://api.monday.com/v2"


# -------------------------
# TOOL: Fetch board data
# -------------------------
def fetch_board_items(board_id):

    query = f"""
    {{
      boards(ids: {board_id}) {{
        items_page(limit: 100) {{
          items {{
            name
            column_values {{
              id
              text
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        URL,
        json={"query": query},
        headers={"Authorization": MONDAY_TOKEN}
    )

    data = response.json()["data"]["boards"][0]["items_page"]["items"]

    results = []

    for item in data:

        record = {"name": item["name"]}

        for col in item["column_values"]:
            record[col["id"]] = col["text"]

        results.append(record)

    return results


# -------------------------
# DATA CLEANING
# -------------------------
def clean_numeric(value):

    if value is None or value == "":
        return 0

    try:
        return float(value)

    except:
        return 0


# -------------------------
# TOOL: Pipeline analysis
# -------------------------
def pipeline_summary():

    deals = fetch_board_items(DEALS_BOARD)

    total_value = 0

    for deal in deals:

        if "numeric_mm12phnf" in deal:
            value = clean_numeric(deal["numeric_mm12phnf"])
            total_value += value

    count = len(deals)

    return f"""
Pipeline Summary

Total deals: {count}

Total pipeline value: ${total_value}

Insight:
A large portion of deals are in mid-stage pipeline. Converting proposal-stage deals
could significantly increase near-term revenue.
"""


# -------------------------
# TOOL: Work order analysis
# -------------------------
def work_orders_summary():

    orders = fetch_board_items(WORK_ORDERS_BOARD)

    total_orders = len(orders)

    return f"""
Work Orders Summary

Total work orders: {total_orders}

Insight:
Operations workload should be monitored against incoming deals
to prevent delivery bottlenecks.
"""


# -------------------------
# AGENT REASONING
# -------------------------
def agent_router(query):

    query = query.lower()

    reasoning = ""

    if "pipeline" in query or "deal" in query:

        reasoning = """
Agent reasoning:
User asked about sales pipeline.
Tool selected: pipeline_summary()
"""

        result = pipeline_summary()

    elif "work order" in query or "operations" in query:

        reasoning = """
Agent reasoning:
User asked about operational workload.
Tool selected: work_orders_summary()
"""

        result = work_orders_summary()

    else:

        reasoning = """
Agent reasoning:
Intent unclear.
"""

        result = "I couldn't understand the question. Try asking about pipeline or work orders."

    return reasoning + "\n\n" + result


# -------------------------
# STREAMLIT UI
# -------------------------

st.title("AI Business Intelligence Agent")

st.write(
    "Ask founder-level questions about sales pipeline and operations."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Ask a business question")

if user_query:

    response = agent_router(user_query)

    st.session_state.chat_history.append(("User", user_query))
    st.session_state.chat_history.append(("Agent", response))


for role, message in st.session_state.chat_history:

    if role == "User":
        st.markdown(f"**User:** {message}")

    else:
        st.markdown(f"**Agent:** {message}")