import streamlit as st

def main():
    st.title("红色问号按钮示例")
    
    st.write("点击下面的红色问号按钮查看更多信息：")
    st.markdown('123124<a href="#" style="color: red; font-size: 30px;">?</a>', unsafe_allow_html=True)

    # 可以在这里添加更多内容

if __name__ == "__main__":
    main()
