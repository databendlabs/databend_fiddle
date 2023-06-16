from databend import SessionContext
import streamlit as st
from urllib.parse import quote
from streamlit_ace import st_ace, KEYBINDINGS, THEMES

import streamlit.components.v1 as components


st.set_page_config(page_title = "databend", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items = None)

ctx = SessionContext()

def read_index_html(copy_text: int):
    with open("index.html") as f:
        return f.read().replace("copy_text", f"`{copy_text}`")

def main():
	c1, c2 = st.columns([4, 1])

	params = st.experimental_get_query_params()

	if "sql" not in st.session_state:
		st.session_state.sql = ""

	if params.get("sql"):
		st.session_state.sql  = " ".join(params["sql"])
	else:
		st.session_state.sql  = ""

	with c1:
		content = st_ace(
			placeholder = "Write your SQL here",
			language = "sql",
			value = st.session_state.sql ,
			theme = c2.selectbox("Theme", options=THEMES, index=22),
			keybinding = c2.selectbox("Keybinding", options=KEYBINDINGS, index=3),
			font_size=c2.slider("Font size", 5, 24, 14),
			min_lines=25,
			wrap = True,
			key="ace",
		)

		st.session_state.sql = content
		with c2:
			if st.button("Share") and st.session_state.sql != "":
				components.html(
					read_index_html(st.session_state.sql),
					height=0,
					width=0,
				)
			st.code('''
			Note:
			Share could only work after
			execution.
			''', language='python')

		if content:
			result = ""
			sql = ""
			for line in content.split("\n"):
				if line != "":
					sql += " " + line
					if line.strip().endswith(";"):
						query_result = ctx.sql(sql).collect()
						result += str(query_result) + "\n"
						sql = ""
			st.text(result)



if __name__ == "__main__":
	main()