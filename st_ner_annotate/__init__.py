import json
import streamlit as st
import streamlit.components.v1 as components


_component_func = components.declare_component(
    "st_ner_annotate", url="http://localhost:5000",
)

def st_ner_annotate(label, text, ents, key=None):
    """st_edit_named_entities.

    Parameters
    ----------
    text: str
        Text to render
    ents: object
        Entities found in text
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    object
        Entities that have been selected
    """
    component_value = _component_func(
        label=label, text=text, ents=ents, key=key, default=ents)

    return component_value

st.title("NER annotation tool")
uploaded_file = st.file_uploader("Selecione um JSON para realizar a marcação", type="json")
if 'files_annotated' not in st.session_state:
    st.session_state.files_annotated = 0

if uploaded_file is not None:
    if 'docs' not in st.session_state:
        st.session_state['docs'] = json.load(uploaded_file)
        json_string = json.dumps(st.session_state['docs'])
    docs = st.session_state['docs']
    entity_labels = ["CABECALHO", "COMECO DE RECORTE"]
    current_entity_type = st.selectbox("Mark for Entity Type", entity_labels)
    prev, _, download, _, next_ = st.columns([1, 4, 1, 4, 1])
    if next_.button('Next'):
        if st.session_state.files_annotated < len(docs) - 1:
            st.session_state.files_annotated += 1
    if prev.button('Previous'):
        if st.session_state.files_annotated > 0:
            st.session_state.files_annotated -= 1
    
    text = docs[st.session_state.files_annotated]['text']
    entities = docs[st.session_state.files_annotated]['entities']
    entities = st_ner_annotate(current_entity_type, text, entities, key=42)
    st.session_state['docs'][st.session_state.files_annotated]['entities'] = entities
    json_string = json.dumps(st.session_state['docs'])
    download.download_button(
        label="Baixar",
        data=json_string,
        file_name='marcacao.json',
        mime='application/json'
    )
