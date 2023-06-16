import streamlit as st
from streamlit_ace import st_ace, KEYBINDINGS, THEMES
from databend import SessionContext

ctx = SessionContext()

def main():
	c1, c2 = st.columns([3, 1])
	c2.subheader("Parameters")

	with c1:
		content = st_ace(
			placeholder = "Write your SQL here",
			language = "sql",
			theme=c2.selectbox("Theme", options=THEMES, index=35),
			keybinding=c2.selectbox("Keybinding mode", options=KEYBINDINGS, index=3),
			font_size = 14,
			min_lines=25,
			key="ace",
		)

		if content:
			st.subheader("Query Result")
			result = ""
			for line in content.split("\n"):
				if line != "":
					result += str(ctx.sql(line).collect()) + "\n"
			st.text(result)


if __name__ == "__main__":
	main()