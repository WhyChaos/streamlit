import streamlit as st

st.write(
    """
    <div id="myDiv"></div>
    <script>
    document.addEventListener("mousemove", function(event) {
        var x = event.clientX;
        var y = event.clientY;
        var coords = "X coords: " + x + ", Y coords: " + y;
        document.getElementById("myDiv").innerHTML = coords;
        Streamlit.setComponentValue(coords);
    });
    </script>
    """
)


coords = st.empty()

if coords is not None:
    coords = coords.value
    st.text(coords)