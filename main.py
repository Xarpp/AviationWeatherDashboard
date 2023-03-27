import streamlit as st
import functions as f
import pandas as pd

st.set_page_config(page_title="Анализ погоды аэропортов", layout="wide",
                   initial_sidebar_state="expanded")

with open("style.css") as style:
    st.markdown(f'<style>{style.read()}</style>', unsafe_allow_html=True)


def create_graphs(code, time_range):
    if code != '':
        soup = f.get_doc_XML(code, time_range)
        df = pd.DataFrame({
            'Date': f.get_times(soup),
            'Temperature': f.get_temps(soup)
        })
        st.sidebar.line_chart(df)


def get_data_to_chart(soup):
    return pd.DataFrame({
        'Date': f.get_times(soup),
        'Temperature': f.get_temps(soup)
    })


def main():
    # sidebar
    try:
        st.title("Анализ погоды аэропортов")
        with st.sidebar:
            st.title("Параметры")
            airport_code = st.text_input("Введите код аэропорта:", max_chars=4)
            time_range = st.selectbox(label="Введите временной интервал", options=[3, 6, 12, 24, 48])
            st.button("Построить график")

        soup = f.get_doc_XML(airport_code, time_range)
        if f.check_error(soup):
            # Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Скорость ветра", str(f.get_avg_wind_speed(soup)) + " км/ч")
            col2.metric("Температура", str(f.get_avg_temp(soup)) + " °C")
            col3.metric("Давление", str(f.get_avg_pressure(soup)) + " мм.рт.ст.")

            # Chart
            st.markdown("### График температуры")
            df = get_data_to_chart(soup)
            df['Temperature'] = df['Temperature'].astype(float)
            df = df.set_index('Date')
            st.line_chart(df, width=1024, height=500)
        else:
            st.write("## Введите корректные данные...")
    except Exception as ex:
        print(ex)
        st.write("## Введите корректные данные...")


if __name__ == '__main__':
    main()
