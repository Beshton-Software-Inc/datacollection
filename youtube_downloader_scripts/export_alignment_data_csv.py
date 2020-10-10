import csv, sys, os, getopt

def generate_alignment_data_csv(directory):
    csv_columns = ['Youtube Video ID', 'MFA Alignment Result', 'Language Code', 'Chunk Label', 'Chunk Text', 'Audio Link']
    csv_data = []
    for root, _, files in os.walk(directory):
        for name in files:
            if '.txt' not in name:
                continue
            root_split = root.split('/')
            yotube_video_id = root_split[3]
            mfa_alignment_result = root_split[1]
            language_code = root_split[2]
            chunk_label = name[0:len(name)-4]
            chunk_text = open(os.path.join(root, name)).read()
            csv_data.append({'Youtube Video ID': yotube_video_id, 
                            'MFA Alignment Result': mfa_alignment_result,
                            'Language Code': language_code, 
                            'Chunk Label': chunk_label, 
                            'Chunk Text': chunk_text })
    csv_file = 'alignment_output.csv'
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in csv_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")

if __name__ == "__main__":
    directory = None
    
    options, _ = getopt.getopt(sys.argv[1:], 'd:', ['directory='])
    for opt, arg in options:
        if opt in ('-d', '--directory'):
            directory = arg
    generate_alignment_data_csv(directory)