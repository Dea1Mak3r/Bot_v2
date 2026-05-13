import streamlit as st
import pandas as pd
import asyncio
import httpx
from config import settings
import altair as alt

# Настройки страницы
st.set_page_config(page_title="Stand Dashboard", layout="wide")
st.title("🚀 Мониторинг стендов: Lenta & Mars")

API_URL = settings.API_URL


# ФУНКЦИИ ДЛЯ РАБОТЫ С API
async def fetch_api(endpoint, method="GET"):
    try:
        async with httpx.AsyncClient() as client:
            if method == "POST":
                response = await client.post(f"{API_URL}/{endpoint}", timeout=300)
            else:
                response = await client.get(f"{API_URL}/{endpoint}", timeout=10)

            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Ошибка API ({response.status_code}): {response.text}")
    except Exception as e:
        st.error(f"Ошибка связи: {e}")
    return None


# УПРАВЛЕНИЕ (ВЕРХНЯЯ ПАНЕЛЬ)
st.subheader("🛠 Управление")
col_ctrl1, col_ctrl2 = st.columns([1, 3])

with col_ctrl1:
    mode = st.radio("Тип проверки:", ["Статус", "Версия"], horizontal=False)

with col_ctrl2:
    st.write(f"Выполнить запрос для **{mode}**:")
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        if st.button("🏢 Проверить Lenta", use_container_width=True):
            path = "status/lenta" if mode == "Статус" else "version/lenta"
            st.session_state.last_res = asyncio.run(fetch_api(path))
            st.session_state.last_type = mode

    with btn_col2:
        if st.button("🚀 Проверить Mars", use_container_width=True):
            path = "status/mars" if mode == "Статус" else "version/mars"
            st.session_state.last_res = asyncio.run(fetch_api(path))
            st.session_state.last_type = mode

# Вывод результата последней проверки
if 'last_res' in st.session_state and st.session_state.last_res:
    res = st.session_state.last_res
    st.info(f"**Результат ({st.session_state.last_type}):** {res}")

st.divider()

# АНАЛИТИКА И ГРАФИКИ

st.subheader("📈 Аналитика (последние 1000 проверок)")

# Загружаем данные для графиков
status_history = asyncio.run(fetch_api("history/status?limit=1000"))

if status_history:
    # 1. Загружаем данные
    df_status = pd.DataFrame(status_history)

    # 2. Исправляем время
    df_status['timestamp'] = pd.to_datetime(df_status['timestamp'])

    # 3. Создаем график
    if not df_status.empty:
        # Создаем базовый график
        base = alt.Chart(df_status).mark_line(
            interpolate='step-after',
            strokeWidth=3
        ).encode(
            x=alt.X('timestamp:T', title='Время (МСК)'),
            y=alt.Y('status_code:Q', title='HTTP Код', scale=alt.Scale(domain=[0, 600])),
            color=alt.Color('stand:N', scale=alt.Scale(
                domain=['LENTA', 'MARS'],
                range=['#0000FF', '#00FF00']
            ), legend=None),  # Легенда не нужна, так как есть заголовки строк
            tooltip=['timestamp:T', 'stand:N', 'status_code:Q', 'description:N']
        ).properties(
            width='container',
            height=200  # Высота каждого отдельного графика
        )

        # Разделяем на строки по полю 'stand'
        facet_chart = base.facet(
            row=alt.Row('stand:N', title='Стенд')
        ).configure_facet(
            spacing=20  # Расстояние между графиками Lenta и Mars
        ).interactive()

        st.altair_chart(facet_chart, use_container_width=True)
    else:
        st.warning("Данные для графиков отсутствуют.")
else:
    st.warning("База данных истории пока пуста")


st.divider()

# ТАБЛИЦЫ ДАННЫХ

st.subheader("📋 Логи системы")
expander = st.expander("Посмотреть подробные таблицы")
with expander:
    tab_s, tab_v = st.tabs(["История Статусов", "История Версий"])

    with tab_s:
        if status_history:
            st.dataframe(df_status, use_container_width=True)

    with tab_v:
        version_history = asyncio.run(fetch_api("history/version?limit=1000"))
        if version_history:
            st.dataframe(pd.DataFrame(version_history), use_container_width=True)