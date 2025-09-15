import requests
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

def map_alleles_to_AB(data):
    """
    Given a list of [allele, count] pairs, return a mapping where:
    - the allele with the highest count is mapped to 'A'
    - the allele with the lowest count is mapped to 'B'
    - all other alleles are ignored

    :param data: List of [allele (str), count (int)] pairs
    :return: Dictionary mapping alleles to 'A' or 'B'
    """
    if not data or len(data) < 2:
        raise ValueError("Data must contain at least two allele-count pairs.")

    # Find allele with max and min count
    max_item = max(data, key=lambda x: x[1])
    min_item = min(data, key=lambda x: x[1])

    # Build mapping
    mapping = {
        max_item[0] : 'A',
        min_item[0] : 'B'
    }

    return mapping
def map_to_AB(data):
    """
    Given a list of [allele, count] pairs, return a mapping where:
    - the allele with the highest count is mapped to 'A'
    - the allele with the lowest count is mapped to 'B'
    - all other alleles are ignored

    :param data: List of [allele (str), count (int)] pairs
    :return: Dictionary mapping alleles to 'A' or 'B'
    """
    if not data or len(data) < 2:
        raise ValueError("Data must contain at least two allele-count pairs.")

    # Find allele with max and min count
    max_item = max(data, key=lambda x: x[1])
    min_item = min(data, key=lambda x: x[1])

    # Build mapping
    mapping = {
        'A' : max_item[0],
        'B' : min_item[0],
    }

    return mapping
def replace_with_mapping(input_str, mappings):
        """
        Replace substrings in `input_str` based on `mappings` dict.
        Longer keys in `mappings` are matched before shorter ones.

        :param input_str: The original string to process
        :param mappings: A dictionary mapping substrings to replacement symbols
        :return: Transformed string with replacements
        """
        result = []
        i = 0
        sorted_keys = sorted(mappings.keys(), key=len, reverse=True)  # prioritize longer matches
        if isinstance(input_str, float):
            input_str = ""
        while i < len(input_str):
            matched = False
            for key in sorted_keys:
                if input_str.startswith(key, i):
                    result.append(mappings[key])
                    i += len(key)
                    matched = True
                    break
            if not matched:
                # If no match, just add the original character
                result.append(input_str[i])
                i += 1

        return ''.join(result)
# Using flask to make an api
# import necessary libraries and functions

dataset_mapping = {
    'gnomADe:ALL' : 'gnomADe: ALL',
    'gnomADe:asj' : 'gnomADe: Ashkenazi Jewish',
    'gnomADe:nfe' : 'gnomADe: Non-Finnish European',
    'gnomADe:mid' : 'gnomADe: Middle Eastern',
    'gnomADe:remaining' : 'gnomADe: Remaining',
    'gnomADe:afr' : 'gnomADe: African/African American',
    'gnomADe:fin' : 'gnomADe: Finnish',
    'gnomADe:eas' : 'gnomADe: East Asian',
    'gnomADe:sas' : 'gnomADe: South Asian',
    'gnomADe:amr' : 'gnomADe: Latino',
    'gnomADg:ALL' : 'gnomADg: ALL',
    'gnomADg:asj' : 'gnomADg: Ashkenazi Jewish',
    'gnomADg:nfe' : 'gnomADg: Non-Finnish European',
    'gnomADg:mid' : 'gnomADg: Middle Eastern',
    'gnomADg:remaining' : 'gnomADg: Remaining',
    'gnomADg:ami' : 'gnomADg: Amish',
    'gnomADg:afr' : 'gnomADg: African/African American',
    'gnomADg:fin' : 'gnomADg: Finnish',
    'gnomADg:eas' : 'gnomADg: East Asian',
    'gnomADg:sas' : 'gnomADg: South Asian',
    'gnomADg:amr' : 'gnomADg: Latino',
    'ALFA:SAMN10492702' : 'ALFA: South Asian',
    'ALFA:SAMN10492701' : 'ALFA: Other Asian',
    'ALFA:SAMN10492705' : 'ALFA: Total',
    'ALFA:SAMN10492703' : 'ALFA: African',
    'ALFA:SAMN10492697' : 'ALFA: East Asian',
    'ALFA:SAMN11605645' : 'ALFA: Other',
    'ALFA:SAMN10492696' : 'ALFA: African Others',
    'ALFA:SAMN10492704' : 'ALFA: Asian',
    'ALFA:SAMN10492698' : 'ALFA: African American',
    'ALFA:SAMN10492699' : 'ALFA: Latin American 1',
    'ALFA:SAMN10492700' : 'ALFA: Latin American 2',
    'ALFA:SAMN10492695' : 'ALFA: European',
    'GEM-J' : 'GEM-J',
    'TOPMed' : 'TOPMed',
    '1000GENOMES:phase_3:ACB' : '1000GENOMES: African-Caribbean',
    '1000GENOMES:phase_3:AFR' : '1000GENOMES: African',
    '1000GENOMES:phase_3:ALL' : '1000GENOMES: ALL',
    '1000GENOMES:phase_3:AMR' : '1000GENOMES: American',
    '1000GENOMES:phase_3:ASW' : '1000GENOMES: African-American SW',
    '1000GENOMES:phase_3:BEB' : '1000GENOMES: Bengali',
    '1000GENOMES:phase_3:CDX' : '1000GENOMES: Dai Chinese',
    '1000GENOMES:phase_3:CEU' : '1000GENOMES: CEPH',
    '1000GENOMES:phase_3:CHB' : '1000GENOMES: Han Chinese',
    '1000GENOMES:phase_3:CHS' : '1000GENOMES: Southern Han Chinese',
    '1000GENOMES:phase_3:CLM' : '1000GENOMES: Colombian',
    '1000GENOMES:phase_3:EAS' : '1000GENOMES: East Asian',
    '1000GENOMES:phase_3:ESN' : '1000GENOMES: Esan',
    '1000GENOMES:phase_3:EUR' : '1000GENOMES: European',
    '1000GENOMES:phase_3:FIN' : '1000GENOMES: Finnish',
    '1000GENOMES:phase_3:GBR' : '1000GENOMES: British',
    '1000GENOMES:phase_3:GIH' : '1000GENOMES: Gujarati',
    '1000GENOMES:phase_3:GWD' : '1000GENOMES: Gambian',
    '1000GENOMES:phase_3:IBS' : '1000GENOMES: Spanish',
    '1000GENOMES:phase_3:ITU' : '1000GENOMES: Indian',
    '1000GENOMES:phase_3:JPT' : '1000GENOMES: Japanese',
    '1000GENOMES:phase_3:KHV' : '1000GENOMES: Kinh Vietnamese',
    '1000GENOMES:phase_3:LWK' : '1000GENOMES: Luhya',
    '1000GENOMES:phase_3:MSL' : '1000GENOMES: Mende',
    '1000GENOMES:phase_3:MXL' : '1000GENOMES: Mexican-American',
    '1000GENOMES:phase_3:PEL' : '1000GENOMES: Peruvian',
    '1000GENOMES:phase_3:PJL' : '1000GENOMES: Punjabi',
    '1000GENOMES:phase_3:PUR' : '1000GENOMES: Puerto Rican',
    '1000GENOMES:phase_3:SAS' : '1000GENOMES: South Asian',
    '1000GENOMES:phase_3:STU' : '1000GENOMES: Sri Lankan',
    '1000GENOMES:phase_3:TSI' : '1000GENOMES: Tuscan',
    '1000GENOMES:phase_3:YRI' : '1000GENOMES: Yoruba',
    'GGVP:GWF' : 'GGVP: The Gambia - Fula',
    'GGVP:GWD' : 'GGVP: The Gambia - Mandinka',
    'GGVP:GWW' : 'GGVP: The Gambia - Wolof',
    'GGVP:GWJ' : 'GGVP: The Gambia - Jola',
    'GGVP:ALL' : 'GGVP: ALL',
}
# creating a Flask app
app = Flask(__name__)
CORS(app)
# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/', methods = ['GET'])
def home():
    if(request.method == 'GET'):

        data = {'search for a rsID' : 1}
        return jsonify({'data': data})

@app.route('/search', methods = ['GET'])
def return_data():

    rsID = request.args.get('rsID')
    dataset = request.args.get('dataset') # dropdown list
    genotype = request.args.get('genotype')

        # Check if parameters are present
    if not rsID or not dataset or not genotype:
        return jsonify({'error': 'Missing rsID or genotype parameter'}), 400

    # request info: ensembl.rest
    server = "https://rest.ensembl.org"
    ext = "/variation/human/" + rsID + "?pops=1"
    r = requests.get(server + ext, headers={"Content-Type": "application/json"})

    if not r.ok:
        r.raise_for_status()
        sys.exit()

    decoded = r.json()

    print(decoded['var_class'])
    if decoded['var_class'] != 'SNP':
        return jsonify({'error': 'Entered rsID does not correspond to an SNP, it corresponds to an ' + decoded['var_class'] + '. Please enter a different rsID.'}), 400
    else:
        pop = decoded["populations"]
        freq = []  # population alleles and their frequency
        all_freq = []
        count = 0
        # print("dataset:", dataset)
        for dec in pop:
            if dec["population"] == str(dataset):
                if dec["allele"] in genotype:
                    freq.append([dec["allele"], dec["frequency"]])
                all_freq.append([dec["allele"], dec["frequency"]])
                count += 1

        if count == 0:
            return jsonify({'error': 'Chosen population: ' + dataset_mapping[dataset] + ' does not have data for ' + rsID + '. Please choose a different population.'}), 400

        print(all_freq)
        if genotype[0] != genotype[1]:
            if 0 < len(freq) < 2:
                if genotype[0] in freq:
                    gen = genotype[1]
                else:
                    gen = genotype[0]
                return jsonify({'error': 'Entered genotype contains an allele not present in the population: '+gen+'. Please enter a different genotype.'}), 400
        if len(freq) == 0:
            return jsonify({'error': 'Entered genotype may be flipped or contain alleles not present on the population, please enter a different genotype.'}), 400
        if len(all_freq) == 2 and len(freq) == 1:
            mapping = map_alleles_to_AB(all_freq)
            final_mapping = map_to_AB(all_freq)
        elif len(all_freq) > 2 and len(freq) == 1:
            new_freq = []
            new_freq.append(freq[0])
            if freq[0][1] > 0.5:
                all_freq.remove(freq[0])
                max_item = max(all_freq, key=lambda x: x[1])
                new_freq.append(max_item)
            else:
                all_freq.remove(freq[0])
                max_item = max(all_freq, key=lambda x: x[1])
                new_freq.append(max_item)
            # print(new_freq)
            mapping = map_alleles_to_AB(new_freq)
            final_mapping = map_to_AB(new_freq)
        else:
            mapping = map_alleles_to_AB(freq)
            final_mapping = map_to_AB(freq)
        genotype_converted = replace_with_mapping(genotype, mapping)

        return jsonify({'rsID' : rsID, 'Dataset': dataset_mapping[dataset],
                        'Major allele (A)' : final_mapping['A'],
                        'Minor allele (B)' : final_mapping['B'],
                        'Genotype in ATCG format' : genotype,
                       'Genotype in AB format' : genotype_converted
                        })
                   # 'var class' : var_class, 'patient genotype')


# driver function
if __name__ == '__main__':

    app.run(debug = True)
