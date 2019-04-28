from textwrap import dedent

INSTRUCTIONS = dedent("""
http://localhost:8080/multiply/3/5  => 15
http://localhost:8080/add/23/42  => 65
http://localhost:8080/subtract/23/42  => -19
http://localhost:8080/divide/22/11  => 2
""")

def add(one, two):
    return str(int(one) + int(two))

def subtract(one, two):
    return str(int(one) - int(two))

def divide(one, two):
    return str(int(one) / int(two))

def multiply(one, two):
    return str(int(one) * int(two))


def resolve_path(path):
    supported_operations = ["add", "multiply", "subtract", "divide"]

    try:
        _, operator, first, second = path.split("/")

        if operator.lower() not in supported_operations:
            raise KeyError

        args = [first, second]

        return operator, args
    except ValueError:
        return ValueError

def application(environ, start_response):
    operators = {
        'add': add,
        'divide': divide,
        'subtract': subtract,
        'multiply': multiply
    }

    status = "200 OK"

    if environ.get('REQUEST_METHOD') == "GET":
        body = INSTRUCTIONS

        try:
            func, args = resolve_path(environ.get('PATH_INFO'))
            body = operators[func](*args)
        except TypeError:
            # handling for favicon.ico
            pass
        except KeyError:
            # handling when operator is not add, subtract, multiple or divide
            body = "Unsupported operator, instructions below: {}".format(INSTRUCTIONS)

    elif environ.get('REQUEST_METHOD') == "POST":
        body = "Unsupported operation."
    else:
        body = "This is neither a GET request nor a POST request!"

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-length', str(len(body)))]
    start_response(status, response_headers)
    return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
