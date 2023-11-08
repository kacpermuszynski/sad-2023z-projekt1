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
    plt.plot(poland_total['time_period'], poland_total['unemployment_rate'], label ='Poland not adjusted')
    plt.plot(poland_total_adjusted['time_period'], poland_total_adjusted['unemployment_rate'], label ='Poland adjusted')

    ax.set_ylabel('Unemployment rate')
    ax.set_xlabel('Year')
    ax.legend()
    ax.grid(True)
    plt.xticks(poland_total.index, poland_total['year'], rotation=90)
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
    ax.set_ylabel('Unemployment rate difference')
    ax.set_xlabel('Month')
    ax.yaxis.grid(True)
    plt.xticks([x+1 for x in range(12)], keys, rotation=90)
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
    countries_data_frames = []
    for country in countries:
        countries_data_frames.append(prepare_dataframe(f'dane/b/{country}-seasonally-adjusted-total.csv'))
    min_year = get_min_year(countries_data_frames)
    
    _, ax = plt.subplots()
    for index, country_data_frame in enumerate(countries_data_frames):
        country_data_frame = country_data_frame[country_data_frame['year'] >= min_year].reset_index()
        countries_data_frames[index] = country_data_frame
        plt.plot(country_data_frame['time_period'], country_data_frame['unemployment_rate'], label =f'{countries[index]} adjusted')

    ax.set_ylabel('Unemployment rate')
    ax.set_xlabel('Year')
    ax.legend()
    ax.grid(True)
    plt.xticks(countries_data_frames[0].index, countries_data_frames[0]['year'], rotation=90)
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
    plt.plot(poland_man_total['time_period'], poland_man_total['unemployment_rate'], label ='Poland man not adjusted')
    plt.plot(poland_woman_total['time_period'], poland_woman_total['unemployment_rate'], label ='Poland woman adjusted')

    ax.set_ylabel('Unemployment rate')
    ax.set_xlabel('Year')
    ax.legend()
    ax.grid(True)
    plt.xticks(poland_man_total.index, poland_man_total['year'], rotation=90)
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
    ax.set_ylabel('Unemployment rate difference')
    ax.set_xlabel('Month')
    ax.yaxis.grid(True)
    plt.xticks([x+1 for x in range(12)], keys, rotation=90)
    ax.margins(x=0)

    interesting_months = ['Dec', 'Jan', 'Feb', 'Jun', 'Jul', 'Aug']
    _, ax = plt.subplots()
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
    ax.boxplot(values)
    ax.set_ylabel('Unemployment rate difference')
    ax.set_xlabel('Month')
    ax.yaxis.grid(True)
    plt.xticks([x+1 for x in range(6)], keys, rotation=90)
    ax.margins(x=0)

    _, ax = plt.subplots()
    abc = values[-1] + values[0]
    print(abc)
    ax.boxplot([values[-1] + values[0] + values[1], values[2] + values[3] + values[4]])
    ax.set_ylabel('Unemployment rate difference')
    ax.set_xlabel('Season')
    ax.yaxis.grid(True)
    plt.xticks([x+1 for x in range(2)], ['Winter', 'Summer'])
    ax.margins(x=0)

def main():
    plt.rcParams["figure.figsize"] = [7.00, 3.50] 
    plt.rcParams["figure.autolayout"] = True
    problem_1a()
    problem_1b()
    problem_1c()
    save_image('results.pdf')

if __name__ == '__main__':
    main()