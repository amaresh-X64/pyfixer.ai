import streamlit as st
from main import clean_response
from langgraph_flow import run_bug_buster
import io
import contextlib

st.set_page_config(page_title="PYfixer.ai", layout="wide")
st.title("🛠️ PYfixer.ai")

# --- Setup Session State ---
if "code" not in st.session_state:
    with open("examples/buggy_code_example.py") as f:
        st.session_state.code = f.read()

# Used to persist function definitions across exec calls
if "exec_globals" not in st.session_state:
    st.session_state.exec_globals = {}

# --- Code Editor ---
st.subheader("Edit your Python code below:")
code = st.text_area(
    "Python Code Editor",
    value=st.session_state.code,
    height=300,
    key="code_editor"
)

# --- Run Code Button and Output Block ---
if st.button("Run Code"):
    st.markdown("### 🏃 Output")
    try:
        with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(code, st.session_state.exec_globals)  # Use persistent globals
            output = buf.getvalue()
        if output.strip():
            st.code(output, language="text")
        else:
            st.success("Code executed successfully. (No output)")
    except Exception as e:
        st.error(f"Error during execution: {e}")

# --- Bug Detection and Fixing ---
if st.button("Detect & Fix Bugs"):
    with st.spinner("Running PYfixer.ai Agents..."):
        result = run_bug_buster(code)
        st.session_state.result = result

# --- Results Display ---
if "result" in st.session_state:
    result = st.session_state.result

    st.markdown("### 🕵️ Bug Detector Agent")
    st.info(clean_response(result["bug_info"]))

    st.markdown("### 🔍 Explainer Agent")
    st.success(clean_response(result["explanation"]))

    st.markdown("### 🔧 Fixer Agent")
    st.code(clean_response(result["fixed_code"]), language="python")

    st.markdown("### 🧪 Test Agent")
    st.warning(clean_response(result["test_result"]))

    if st.button("Replace Editor Code with Fixed Code"):
        st.session_state.code = clean_response(result["fixed_code"])
        st.rerun()

    if st.button("Compile & Run Code", key="compile_run"):
        st.markdown("### 🏃 Output")
        try:
            with io.StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                exec(st.session_state.code, st.session_state.exec_globals)
                output = buf.getvalue()
            if output.strip():
                st.code(output, language="text")
            else:
                st.success("Code executed successfully. (No output)")
        except Exception as e:
            st.error(f"Error during execution: {e}")
