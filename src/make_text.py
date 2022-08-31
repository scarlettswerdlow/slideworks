import yaml
import openai
from datetime import datetime
import os.path
import pickle

################################################################################
#                                                                              #
#                                    Functions                                 #
#                                                                              #
################################################################################

def read_yaml(file_path):

    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def get_response(prompt):

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ) 
    
    rv = response['choices'][0]['text'].strip()

    return rv

def get_company_name(product_description):

  prompt = 'Write a name for a startup company that is the Uber of ' + product_description + '.'

  company_name = get_response(prompt)

  return company_name

def get_company_tagline(company_name):

    prompt = 'Write a tagline for a company named ' + company_name + '.'

    company_tagline = get_response(prompt)
    
    return company_tagline 

def get_problem_statement(product_description):

    prompt = 'Describe in bullet points of 5-10 words the problem with ' + product_description + ' today'

    problem_statement = get_response(prompt)

    return problem_statement

def get_solution_description(company_name, product_description):

    prompt = 'In one sentence, how does the company ' + company_name + ' solve the problem of ' + product_description + '?'

    solution_description = get_response(prompt)

    return solution_description

def get_market_size(product_description):

    prompt = 'What is the market size today for the ' + product_description + ' industry?'

    market_size = get_response(prompt)

    return market_size

def get_business_model(company_name, product_description):

    prompt = 'Describe how ' + company_name + ' will generate revenue and make a profit doing ' + product_description + '.'

    business_model = get_response(prompt)

    return business_model

def get_competitors(company_name, product_description):

    prompt = 'List the top 5 competitors to ' + company_name +  'in the ' + product_description + ' industry.'

    competitors = get_response(prompt)

    return competitors

def get_text(product_description):
    
    company_name = get_company_name(product_description)
    company_tagline = get_company_tagline(company_name)
    problem_statement = get_problem_statement(product_description)
    solution_description = get_solution_description(company_name, product_description)
    market_size = get_market_size(product_description)
    business_model = get_business_model(company_name, product_description)
    competitors = get_competitors(company_name, product_description)

    rv = {
        'product_description': product_description,
        'timestamp': datetime.now().strftime('%Y%m%d%H%M%S'),
        'results': {
            'company_name': company_name,
            'company_tagline': company_tagline,
            'problem_statement': problem_statement,
            'solution_description': solution_description,
            'market_size': market_size,
            'business_model': business_model,
            'competitors': competitors
        }
    }

    return rv

def main(config_fp, product_description):

    config = read_yaml(config_fp)
    openai.api_key = config['OPENAI']['SECRET_KEY']

    pitch_text = get_text(product_description)

    print(pitch_text)

    save_fn = pitch_text['timestamp'] + '_' + product_description + '.pickle'
    save_fp = os.path.join('../results/', save_fn)
    with open(save_fp, 'wb') as handle:
        pickle.dump(pitch_text, handle, protocol=pickle.HIGHEST_PROTOCOL)

################################################################################
#                                                                              #
#                                       Main                                   #
#                                                                              #
################################################################################

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description = 'GeneratePitchDeckText')
    parser.add_argument('--config', required = True, help = 'Path to config file')
    parser.add_argument('--product', required = True, help = 'Product description')
    args = parser.parse_args()

    main(
        config_fp = args.config, 
        product_description = args.product
    )