import streamlit as st

# 创建一个开关组件
switch_state = st.checkbox("切换状态")

# 检查开关状态，并进行相应操作
if switch_state:
    st.write("开关已打开")
else:
    st.write("开关已关闭")
