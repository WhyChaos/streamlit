import streamlit as st

def main():
    st.title("Streamlit Popup Alert Example")

    st.write("Click the buttons below to trigger different types of popup alerts:")

    # 弹出警告
    if st.button("Show Warning"):
        st.warning("This is a warning message!")

    # 弹出错误
    if st.button("Show Error"):
        st.error("This is an error message!")

    # 弹出信息
    if st.button("Show Info"):
        st.info("This is an informational message!")

    # 弹出成功
    if st.button("Show Success"):
        st.success("This is a success message!")

if __name__ == "__main__":
    main()
