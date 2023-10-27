import json
from datetime import datetime

KEY_WORD = '[Data]'
NEW_LINE = '\n'


def parse_snp_data(values: list) -> dict:
    return {
        'SNP Name': values[0],
        'Allele - Forward': f"{values[2]}/{values[3]}",
        'Allele - Top': f"{values[4]}/{values[5]}",
        'Allele - AB': f"{values[6]}/{values[7]}",
        'GC Score': float(values[8]),
        'X': float(values[9]),
        'Y': float(values[10])
    }


def read_data_from_file(input_file: str) -> str:
    with open(input_file, 'r') as file:
        data_with_header = file.read()
    return data_with_header


def write_data_to_json(output_file: str, data: list) -> None:
    json_data = {'Data': data}
    with open(output_file, 'w') as out_file:
        json.dump(json_data, out_file, indent=2)


def extract_data(data: str) -> str:
    lines = data.split(NEW_LINE)
    data_start_index = lines.index(KEY_WORD)
    data_lines = lines[data_start_index + 2:]
    return NEW_LINE.join(data_lines)


def group_data(data: str) -> list:
    samples = []
    data_lines = data.strip().split(NEW_LINE)

    sample_data = None
    sample_id = None

    for line in data_lines:
        values = line.split()
        new_sample_id = values[1]
        snp_data = parse_snp_data(values)

        if new_sample_id != sample_id:
            if sample_data is not None:
                samples.append(sample_data)
            sample_id = new_sample_id
            sample_data = {'Sample ID': str(sample_id), 'SNP Data': [snp_data]}
        else:
            sample_data['SNP Data'].append(snp_data)

    if sample_data is not None:
        samples.append(sample_data)

    return samples


def main(input_file: str, output_file: str) -> None:
    data = read_data_from_file(input_file)
    extracted_data = extract_data(data)
    grouped_data = group_data(extracted_data)
    write_data_to_json(output_file, grouped_data)


if __name__ == '__main__':
    start_time = datetime.now()
    input_file = 'LLP_Genomed_Ayr_OVNG50V02_20230213_FinalReport.txt'
    output_file = 'output.json'
    main(input_file, output_file)
    end_time = datetime.now()
    execution_time = end_time - start_time
    print(f"Data saved to '{output_file}'.")
    print(f"Execution time: {execution_time.total_seconds():.0f}s")
