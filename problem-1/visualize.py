import pandas as pd
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_pdf import PdfPages

def save_image(filename): 
    
    # PdfPages is a wrapper around pdf  
    # file so there is no clash and create 
    # files with no error. 
    p = PdfPages(filename) 
      
    # get_fignums Return list of existing  
    # figure numbers 
    fig_nums = plt.get_fignums()   
    figs = [plt.figure(n) for n in fig_nums] 
      
    # iterating over the numbers in list 
    for fig in figs:  
        
        # and saving the files 
        fig.savefig(p, format='pdf')  
      
    # close the object 
    p.close()

def prepare_dataframe(csv_path: str):
    dataframe = pd.read_csv(csv_path, header=0, names=['date', 'time_period', 'unemployment_rate'])
    dataframe['year'] = [int(time_period[:4]) for time_period in dataframe['time_period']]
    dataframe['month'] = [time_period[4:] for time_period in dataframe['time_period']]
    dataframe = dataframe.drop('date', axis=1)
    return dataframe

def problem_1a():
    poland_total = prepare_dataframe('dane/a/Poland-total.csv')
    poland_total_adjusted = prepare_dataframe('dane/a/Poland-seasonally-adjusted-total.csv')
    _, ax = plt.subplots()
    plt.plot(poland_total['time_period'], poland_total['unemployment_rate'], label ='z korekcją sezonowości')
    plt.plot(poland_total_adjusted['time_period'], poland_total_adjusted['unemployment_rate'], label ='bez korekcji sezonowości')

    ax.set_ylabel('Stopa bezrobocia')
    ax.set_xlabel('Rok')
    ax.legend()
    plt.title("Stopa bezrobocia w Polsce") 
    ax.grid(True)
    plt.xticks(poland_total.index, poland_total['year'], rotation=45)
    ax.margins(x=0)
    ax.set_xticks(ax.get_xticks()[::12])


    _, ax = plt.subplots()
    rate_difference = poland_total['unemployment_rate'] - poland_total_adjusted['unemployment_rate']
    rate_difference_by_month = {}
    for index, month in enumerate(poland_total_adjusted['month']):
        if month in rate_difference_by_month:
            rate_difference_by_month[month].append(rate_difference[index])
        else:
            rate_difference_by_month[month] = [rate_difference[index]]
    keys = []
    values = []
    for key, value in rate_difference_by_month.items():
        keys.append(key)
        values.append(value)
    ax.boxplot(values)
    ax.set_ylabel('Różnica w stopie bezrobocia')
    ax.set_xlabel('Miesiąc')
    ax.yaxis.grid(True)
    months_to_polish = {'Jan':'Styczeń', 'Feb':'Luty', 'Mar':'Marzec', 'Apr':'Kwiecień', 'May':'May', 'Jun':'Czerwiec', 'Jul':'Lipiec', 'Aug':'Sierpień', 'Sep':'Wrzesień', 'Oct':'Październik', 'Nov':'Listopad', 'Dec':'Grudzień'}
    plt.title("Stopa bezrobocia w Polsce")
    plt.xticks([x+1 for x in range(12)], [months_to_polish[key] for key in keys], rotation=45)
    ax.margins(x=0)

def get_min_year(data_frames):
    min_year_result = -1
    for data_frame in data_frames:
        min_year = min(data_frame['year'])
        if min_year > min_year_result:
            min_year_result = min_year
    return min_year_result

def problem_1b():
    countries = ['Poland', 'Czech Republik', 'France', 'Germany', 'Slovakia']
    countries_to_polish = {'Poland':'Polska', 'Czech Republik':'Czechy', 'France':'Francja', 'Germany':'Niemcy', 'Slovakia':'Słowacja'}
    countries_data_frames = []
    for country in countries:
        countries_data_frames.append(prepare_dataframe(f'dane/b/{country}-seasonally-adjusted-total.csv'))
    min_year = get_min_year(countries_data_frames)
    
    _, ax = plt.subplots()
    for index, country_data_frame in enumerate(countries_data_frames):
        country_data_frame = country_data_frame[country_data_frame['year'] >= min_year].reset_index()
        countries_data_frames[index] = country_data_frame
        plt.plot(country_data_frame['time_period'], country_data_frame['unemployment_rate'], label = countries_to_polish[countries[index]])

    ax.set_ylabel('Stopa bezrobocia')
    ax.set_xlabel('Rok')
    ax.legend()
    ax.grid(True)
    plt.xticks(countries_data_frames[0].index, countries_data_frames[0]['year'], rotation=45)
    plt.title("Stopa bezrobocia z korekcją sezonowości")
    ax.margins(x=0)
    ax.set_xticks(ax.get_xticks()[::12])

def problem_1c():
    min_year = 2010
    max_year = 2014

    poland_man_total = prepare_dataframe('dane/c/Poland-man-total.csv')
    poland_man_total = poland_man_total[poland_man_total['year'] >= min_year].reset_index()
    poland_man_total = poland_man_total[poland_man_total['year'] <= max_year].reset_index()

    poland_woman_total = prepare_dataframe('dane/c/Poland-woman-total.csv')
    poland_woman_total = poland_woman_total[poland_woman_total['year'] >= min_year].reset_index()
    poland_woman_total = poland_woman_total[poland_woman_total['year'] <= max_year].reset_index()

    _, ax = plt.subplots()
    plt.plot(poland_man_total['time_period'], poland_man_total['unemployment_rate'], label ='mężczyzna')
    plt.plot(poland_woman_total['time_period'], poland_woman_total['unemployment_rate'], label ='kobieta')

    ax.set_ylabel('Stopa bezrobocia')
    ax.set_xlabel('Rok')
    ax.legend()
    ax.grid(True)
    plt.xticks(poland_man_total.index, poland_man_total['year'], rotation=45)
    plt.title("Stopa bezrobocia w Polsce bez korekcji sezonowości")
    ax.margins(x=0)
    ax.set_xticks(ax.get_xticks()[::12])

    _, ax = plt.subplots()
    rate_difference = poland_woman_total['unemployment_rate'] - poland_man_total['unemployment_rate']
    rate_difference_by_month = {}
    for index, month in enumerate(poland_woman_total['month']):
        if month in rate_difference_by_month:
            rate_difference_by_month[month].append(rate_difference[index])
        else:
            rate_difference_by_month[month] = [rate_difference[index]]
    keys = []
    values = []
    for key, value in rate_difference_by_month.items():
        keys.append(key)
        values.append(value)
    ax.boxplot(values)
    ax.set_ylabel('Różnica w stopie bezrobocia')
    ax.set_xlabel('Miesiąc')
    plt.title("Różnica w stopie bezrobocia w Polsce bez korekcji sezonowości")
    ax.yaxis.grid(True)
    months_to_polish = {'Jan':'stń', 'Feb':'ly', 'Mar':'mrz', 'Apr':'kń', 'May':'mj', 'Jun':'czc', 'Jul':'lc', 'Aug':'sń', 'Sep':'wń', 'Oct':'pk', 'Nov':'ld', 'Dec':'gń'}
    months_to_polish = {'Jan':'Styczeń', 'Feb':'Luty', 'Mar':'Marzec', 'Apr':'Kwiecień', 'May':'May', 'Jun':'Czerwiec', 'Jul':'Lipiec', 'Aug':'Sierpień', 'Sep':'Wrzesień', 'Oct':'Październik', 'Nov':'Listopad', 'Dec':'Grudzień'}
    plt.xticks([x+1 for x in range(12)], [months_to_polish[key] for key in keys], rotation=45)
    ax.margins(x=0)

    interesting_months = ['Dec', 'Jan', 'Feb', 'Jun', 'Jul', 'Aug']
    # _, ax = plt.subplots()
    rate_difference = poland_woman_total['unemployment_rate'] - poland_man_total['unemployment_rate']
    rate_difference_by_month = {}
    for index, month in enumerate(poland_woman_total['month']):
        if month not in interesting_months:
            continue
        if month in rate_difference_by_month:
            rate_difference_by_month[month].append(rate_difference[index])
        else:
            rate_difference_by_month[month] = [rate_difference[index]]
    keys = []
    values = []
    for key, value in rate_difference_by_month.items():
        keys.append(key)
        values.append(value)
    # ax.boxplot(values)
    # ax.set_ylabel('Różnica w stopie bezrobocia')
    # ax.set_xlabel('Miesiąc')
    # ax.yaxis.grid(True)
    # plt.xticks([x+1 for x in range(6)], keys, rotation=90)
    # ax.margins(x=0)

    _, ax = plt.subplots()
    ax.boxplot([values[-1] + values[0] + values[1], values[2] + values[3] + values[4]])
    ax.set_ylabel('Różnica w stopie bezrobocia')
    ax.set_xlabel('Pora roku')
    ax.yaxis.grid(True)
    plt.xticks([x+1 for x in range(2)], ['Zima', 'Lato'], rotation=45)
    plt.title("Różnica w stopie bezrobocia w Polsce bez korekcji sezonowości")
    ax.margins(x=0)

def problem_1d():
    min_year = 2010
    max_year = 2014

    poland_man_old = prepare_dataframe('dane/d/man_old.csv')
    poland_man_old = poland_man_old[poland_man_old['year'] >= min_year].reset_index()
    poland_man_old = poland_man_old[poland_man_old['year'] <= max_year].reset_index()

    poland_man_youth = prepare_dataframe('dane/d/man_youth.csv')
    poland_man_youth = poland_man_youth[poland_man_youth['year'] >= min_year].reset_index()
    poland_man_youth = poland_man_youth[poland_man_youth['year'] <= max_year].reset_index()

    poland_woman_old = prepare_dataframe('dane/d/woman_old.csv')
    poland_woman_old = poland_woman_old[poland_woman_old['year'] >= min_year].reset_index()
    poland_woman_old = poland_woman_old[poland_woman_old['year'] <= max_year].reset_index()

    poland_woman_youth = prepare_dataframe('dane/d/woman_youth.csv')
    poland_woman_youth = poland_woman_youth[poland_woman_youth['year'] >= min_year].reset_index()
    poland_woman_youth = poland_woman_youth[poland_woman_youth['year'] <= max_year].reset_index()

    _, ax = plt.subplots()
    plt.plot(poland_man_old['time_period'], poland_man_old['unemployment_rate'], label ='mężczyzna 25-74')
    plt.plot(poland_man_youth['time_period'], poland_man_youth['unemployment_rate'], label ='mężczyzna 15-24')

    plt.plot(poland_woman_old['time_period'], poland_woman_old['unemployment_rate'], label ='kobieta 25-74')
    plt.plot(poland_woman_youth['time_period'], poland_woman_youth['unemployment_rate'], label ='kobieta 15-24')

    ax.set_ylabel('Stopa bezrobocia')
    ax.set_xlabel('Rok')
    ax.legend(loc='upper left')
    ax.grid(True)
    plt.xticks(poland_man_old.index, poland_man_old['year'], rotation=45)
    plt.title("Stopa bezrobocia w Polsce bez korekcji sezonowości z podziałem na wiek")
    ax.margins(x=0)
    ax.set_xticks(ax.get_xticks()[::12])

def main():
    plt.rcParams["figure.figsize"] = [7.00, 3.50] 
    plt.rcParams["figure.autolayout"] = True
    problem_1a()
    problem_1b()
    problem_1c()
    problem_1d()
    save_image('results.pdf')

if __name__ == '__main__':
    main()