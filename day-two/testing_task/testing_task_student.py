import csv
import random

# -------------------- START OF GIVEN SECTION --------------------
escape = "\033[]"[:-1] # This is a weird thing just because it was breaking my code editor to do simply.
colours = {
    "BLUE": escape+"1;94m",
    "PURPLE": escape+"1;95m",
    "WHITE": escape+"0m",
    "RED": escape+"1;91m"
}

def import_data(file_path):
    with open(file_path) as flanker_file:
        csv_reader = csv.reader(flanker_file)
        header_row = csv_reader.__next__()
        data = {header: [] for header in header_row}

        for row in csv_reader:
            for column_idx, element in enumerate(row):
                try:
                    formatted_element = float(element)
                except:
                    formatted_element = element
                data[header_row[column_idx]].append(formatted_element)
    return data

def mean(data_list):
    return sum(data_list)/len(data_list)

def find_indices(data_list, match):
    return [index for index, elem in enumerate(data_list) if elem == match]

def get_at_indices(data_list, indices_list):
    return [data_list[idx] for idx in indices_list]

def count_bins(bins, data_list):
    counts = [0]*len(bins)
    for value in data_list:
            for idx, bin in enumerate(bins):
                if idx == len(bins)-1 and value <= bin[1]:
                    counts[idx] += 1
                if value >= bin[0] and value < bin[1]:
                    counts[idx] += 1
                    break
    return counts

def plot_histogram(data_list_one, data_list_two = [0.0], bin_count=20, plot_max_width= 20, title = None):
    padding = 7
    if type(data_list_two) is not list:
        data_list_two = [data_list_two]
    max_value = max(data_list_one + data_list_two)
    min_value = min(data_list_one + data_list_two)

    # Organise bins
    bin_bounds = list(range(bin_count+1))
    spacing = ((max_value-min_value)/bin_count)
    offset = min_value
    bin_bounds = list(map(lambda value: (value*spacing)+offset, bin_bounds))
    bins = [[bin_bounds[idx], bin_bounds[idx+1]] for idx in range(len(bin_bounds)-1)]
    data_list_one_counts = count_bins(bins, data_list_one)
    data_list_two_counts = count_bins(bins, data_list_two)

    max_count = max(data_list_one_counts+data_list_two_counts)
    normalising_factor = (1/max_count)*plot_max_width
    if max_count > plot_max_width:
        normalised_data_list_one_counts = [(count*normalising_factor).__ceil__() for count in data_list_one_counts]
        normalised_data_list_two_counts = [(count*normalising_factor).__ceil__() for count in data_list_two_counts]
    else:
        normalised_data_list_one_counts = data_list_one_counts
        normalised_data_list_two_counts = data_list_two_counts
    
    if title: 
        print("_"*(2*padding+plot_max_width))
        print(title)

    print("_"*(2*padding+plot_max_width))

    for idx, bin in enumerate(bins):
        data_list_one_value = normalised_data_list_one_counts[idx]
        data_list_two_value = normalised_data_list_two_counts[idx]

        print(round(bin[0], 3), end=' ')
        print(" "*(padding-len(str(round(bins[idx][0], 3)))), end='')
        print("|", end='')
        
        overlap = min(data_list_one_value, data_list_two_value)
        
        # Print overlap first
        print(colours["PURPLE"]+"o"*overlap+colours["WHITE"], end='')
        print(colours["BLUE"]+"o"*max(data_list_one_value-overlap, 0)+colours["WHITE"], end='')
        print(colours["RED"]+"o"*max(data_list_two_value-overlap, 0)+colours["WHITE"])
    print(f"o represents {1/normalising_factor} units")
    print("-"*(2*padding+plot_max_width))

# -------------------- END OF GIVEN SECTION --------------------




