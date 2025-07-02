import streamlit as st
import numpy as np
import requests
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import scipy.ndimage
import os

st.set_page_config(page_title="Reconnaissance MNIST", layout="wide")

st.title("Reconnaissance de chiffres manuscrits (MNIST)")
st.markdown("""
Bienvenue sur l'application de reconnaissance de chiffres manuscrits !

**Comment ça marche ?**
1. Dessinez un chiffre (0 à 9) dans la zone de dessin à gauche, en utilisant toute la surface et un trait bien visible.
2. Cliquez sur **Prédire** pour obtenir la reconnaissance automatique.
3. Le modèle vous affiche le chiffre prédit, le top-3 des probabilités, et un graphique de confiance.

*Conseil :* Pour de meilleurs résultats, dessinez un chiffre bien centré, épais, et sans lever la souris/stylet.
""")

# Layout principal : 2 colonnes
col1, col2 = st.columns([1,2])

with col1:
    st.subheader("Zone de dessin")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 1)",
        stroke_width=10,
        stroke_color="#000000",
        background_color="#FFFFFF",
        width=280,
        height=280,
        drawing_mode="freedraw",
        key="canvas" if 'clear_canvas' not in st.session_state or not st.session_state['clear_canvas'] else str(np.random.rand()),
    )
    clear_canvas = st.button("Effacer")
    if clear_canvas:
        st.session_state['clear_canvas'] = True
    else:
        st.session_state['clear_canvas'] = False

with col2:
    st.subheader("Prédiction du chiffre")
    if canvas_result.image_data is not None:
        img_draw = Image.fromarray((255 - canvas_result.image_data[:, :, 0]).astype(np.uint8))
        img_draw_resized = img_draw.resize((28, 28)).convert("L")
        st.image(img_draw_resized, caption="Image envoyée au modèle (28x28)", width=140)
        img_np_draw = np.array(img_draw_resized) / 255.0
        img_list_draw = img_np_draw.flatten().tolist()
        if st.button("Prédire", use_container_width=True):
            with st.spinner("Le modèle réfléchit..."):
                # url = "http://127.0.0.1:8000/api/v1/predict"
                API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
                url = f"{API_URL}/api/v1/predict"
                data = {"image": img_list_draw}
                try:
                    response = requests.post(url, json=data, timeout=5)
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ Chiffre prédit : {result['prediction']}")
                        st.markdown("**Top-3 des probabilités :**")
                        probs = np.array(result['probs'])
                        top3 = probs.argsort()[-3:][::-1]
                        st.table({"Chiffre": [str(idx) for idx in top3], "Probabilité (%)": [f"{probs[idx]*100:.1f}" for idx in top3]})
                        st.markdown("**Confiance du modèle :**")
                        st.bar_chart(result['probs'])
                    else:
                        st.error(f"❌ Erreur API : {response.status_code}. Vérifiez que l'API FastAPI est bien lancée.")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Impossible de contacter l'API. Vérifiez que le serveur FastAPI fonctionne (lancez-le avec : `uvicorn src.app.api:app --reload`).")
                except requests.exceptions.Timeout:
                    st.error("⏱️ L'API met trop de temps à répondre. Vérifiez sa disponibilité.")
                except Exception as e:
                    st.error(f"Erreur lors de l'appel à l'API : {e}")
    else:
        st.info("Commencez par dessiner un chiffre dans la zone à gauche.") 