def structure_raw_data(lines2):
    structured_data = []
    for i in range(0, len(lines2), 5):
        country = lines2[i].replace('\xa0', ' ')
        territorial_approach = lines2[i + 1].replace('\xa0', ' ')
        consumption_approach = lines2[i + 2]
        consumption_approach_by_person = lines2[i + 3].replace('\xa0', ' ')
        structured_data.append([country, territorial_approach, consumption_approach, consumption_approach_by_person])
    return structured_data

def clean_and_structure_data(data_string):
    data_converted = []
    for row in data_string:
        new_row = []
        for item in row:
            cleaned_item = item.replace(" ", "").strip()
            if cleaned_item.replace(",", "").replace(".", "").isdigit():
                new_item = float(cleaned_item.replace(",", ".")) if ',' in cleaned_item or '.' in cleaned_item else int(cleaned_item)
            else:
                new_item = item.strip()
            new_row.append(new_item)
        data_converted.append(new_row)
    return data_converted
