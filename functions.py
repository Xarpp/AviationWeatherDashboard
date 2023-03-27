import requests
from bs4 import BeautifulSoup
import datetime
from statistics import mean


def check_error(soup):
    return soup.find("errors").text == "" and int(soup.find("data").attrs["num_results"]) != 0


def get_times(soup):
    time_mass = []
    if check_error(soup):
        obs_time = soup.find_all("observation_time")
        for time in reversed(obs_time):
            time_mass.append(datetime.datetime.strptime(time.text, '%Y-%m-%dT%H:%M:%SZ').strftime("%d.%m-%H:%M"))
        return time_mass
    else:
        print("Invalid arguments in URL")
        return -2


def get_temps(soup):
    temp_mass = []
    if check_error(soup):
        temp_c = soup.find_all("temp_c")
        for temp in temp_c:
            temp_mass.append(float(temp.text))
        return temp_mass
    else:
        print("Invalid arguments in URL")
        return -2


def get_avg_wind_speed(soup):
    wind_speed_mass = []
    if check_error(soup):
        wind_speed = soup.find_all("wind_speed_kt")
        for wind in wind_speed:
            wind_speed_mass.append(float(wind.text))
        return round(mean(wind_speed_mass) * 1.852, 1)
    else:
        print("Invalid arguments in URL")
        return -2


def get_avg_temp(soup):
    return round(mean(get_temps(soup)), 1)


def get_avg_pressure(soup):
    pressure_mass = []
    if check_error(soup):
        pressure_rt = soup.find_all("altim_in_hg")
        for rt in pressure_rt:
            pressure_mass.append(float(rt.text))
        return round(mean(pressure_mass), 1)
    else:
        print("Invalid arguments in URL")
        return -2


def get_doc_XML(code, time_range):
    try:
        url = f"https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&" \
              f"requestType=retrieve&format=xml&stationString={code}&hoursBeforeNow={time_range}"
        url_data = requests.get(url).text
        soup = BeautifulSoup(url_data, features="xml")
        return soup
    except Exception as ex:
        print(ex)
        return -1


if __name__ == '__main__':
    url = get_doc_XML('uuee', 24)
    # print(check_error(url))
    # print(get_times(url))
    # print(get_temps(url))
    # print(get_avg_temp(url))
    print(get_avg_pressure(url))
