from mitmproxy import http
from mitmproxy import ctx
import configparser
import json

# main method used by mitmproxy
def response(flow):
    log_to_file = 0 # log flag

    config = configparser.ConfigParser() # initialize config parser
    config.read('./mitm-config.ini') # read ini config

    t_float_var = config.getfloat('target', 't_float_var') # get as float
    t_string_var = config.get('target', 't_string_var') # get as string
    
    try:
        txt_response = flow.response.get_text() # response casted to text
        mod_response = json.loads(txt_response) # load txt response as JSON. now we can modify its contents

        api_method = flow.request.path.split('/')[3].split('?')[0] # get method from URL E.g.: /this_is_going_to_be_pulled?id=42069
        pretty_host = flow.request.pretty_host # pull host from request. E.g.: api.example.com

        if log_to_file == 1:
            with open('./mitm-response.json', 'a') as file:
                file.write(f"HOST: {flow.request.pretty_host}\n")
                file.write(f"API METHOD: {api_method}\n")
                file.write(f"REQUEST PATH: {flow.request.path}\n")
                file.write(txt_response)
                file.write("\n\n\n\n")

        if pretty_host == "api.example.com":
            if api_method == "api_method_1":
                mod_response["some_node"] = t_string_var
                mod_response["some_node"]["one_more_thing"] = t_float_var

            if api_method == "api_method_2":
                mod_response["some_node"]["some_other_thing"] = t_float_var + 420.69
                mod_response["some_node"][0]["another_pretty_thing"] = t_string_var

        # Find something in request
        # E.g.: /api_method_2?id=42069&product_id=42069
        if flow.request.query.get('product_id') == "42069":
            ctx.log.info("Caught requesting product ID 42069") # output to event log
            mod_response["data"]["some_node"]["another_thing"] = modifyResponse(mod_response["data"]["some_node"]["another_thing"], t_float_var)

        # Check if there is a key in array (sorry, I'm from PHP)
        # E.g.: mod_response["data"]["search"]
        if "search" in mod_response["data"]:
            ctx.log.info("CAUGHT SEARCH REQUEST!!!!")
            for single_product in mod_response["data"]["search"]["products"]:
                if single_product["item"]["id"] == "42069":
                    single_product["current_thing"] = modifyResponse(single_product["current_thing"], t_float_var)

        flow.response.text = json.dumps(mod_response) # after we modified everything we wanted - pass modified response back to user
    except:
        ctx.log.info("NOTHING")

def modifyResponse(someNode, tFloatVar):
    someNode["current_thing"] = tFloatVar
    someNode["default_thing"] = "false"
    someNode["formatted_comparison_price"] = "$" + str(tFloatVar)
    someNode["formatted_comparison_price_type"] = str(tFloatVar)

    return someNode
