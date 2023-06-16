import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, THEMES
from databend import SessionContext

ctx = SessionContext()

def main():
	c1, c2 = st.columns([4, 1])

	with c1:
		content = st_ace(
			placeholder = "Write your SQL here",
			language = "sql",
			theme = c2.selectbox("Theme", options=THEMES, index=28),
			keybinding = c2.selectbox("Keybinding", options=KEYBINDINGS, index=3),
			font_size=c2.slider("Font size", 5, 24, 14),
			min_lines=25,
			wrap = True,
			key="ace",
		)

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