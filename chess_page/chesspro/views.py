from .chess import Chess_Board, ChessException, ChessException_2, ChessException_5
from django.http import JsonResponse, HttpResponse
from .errors import *

possible_errors = {1: 'Zła pozycja figury szachowej.',
                   2: 'Zły kolor figury szachowej.',
                   3: 'Złe argumenty do tworzenia szachownicy',
                   4: 'Złe dane wejściowe. Podałeś źle pozycje figury./n Podaj "pawn/A2" np.',
                   5: 'Podałeś złą literową pozycję. Dostępne są litery od a-h.',
                   6: 'Podałeś złą numeryczną pozycję. Dostępne są cyfry od 1-8.',
                   7: 'Podałeś złą nazwę figry. Użyj np "pawn".',
                   8: 'Dana figura nie znajduje się na danym polu.',
                   9: 'Liczba argumentów jest nie wystarczająca, lub jest za duża.'
                   }


main_aplication = Chess_Board()

def main_view(request):
    return HttpResponse()

def test_json_view(request):
    return JsonResponse(data={}, status=200)


def list_moves(request, **kwargs) -> JsonResponse:
    figure = kwargs['figure']
    field = kwargs['field']
    try:
        data_to_back: tuple[str] = main_aplication.move_options(figure, field)
    except ChessException as err:
        if isinstance(err, ChessException_5) or isinstance(err, ChessException_6):
            return JsonResponse(data={'availableMoves': None, 'error': possible_errors[err.num], 'figure': None, 'currentField': None},
                                status=409)
        elif isinstance(err, ChessException_7):
            return JsonResponse(data={'availableMoves': None, 'error': possible_errors[err.num], 'figure': None, 'currentField': None},
                                status=404)
        else:
            return JsonResponse(data={'availableMoves': None, 'error': possible_errors[err.num], 'figure': None, 'currentField': None},
                                status=500)
    else:
        return JsonResponse(data={'availableMoves': data_to_back, 'error': None, 'figure': figure.lower(), 'currentField': field.lower()},
                            status=200)

def validate_moves(request, **kwargs) -> JsonResponse:
    figure = kwargs['figure']
    field1 = kwargs['field1']
    field2 = kwargs['field2']
    try:
        data_to_back: bool = main_aplication.validate_moves(figure, field1, field2)
    except ChessException as err:
        if err.destination:
            if isinstance(err, ChessException_5) or isinstance(err, ChessException_6):
                return JsonResponse(data={'move': None, 'error': 'Destination Field Error\n' + possible_errors[err.num], 'figure': None,  'currentField': None, 'destField': None},
                                    status=409)
            elif isinstance(err, ChessException_7):
                return JsonResponse(data={'move': None, 'error': possible_errors[7], 'figure': None, 'currentField': None, 'destField': None},
                                    status=404)
            else:
                JsonResponse(data={'move': None, 'error': possible_errors[err.num], 'figure': None, 'currentField': None, 'destField': None},
                             status=500)
        else:
            if isinstance(err, ChessException_5) or isinstance(err, ChessException_6):
                return JsonResponse(data={'move': None, 'error': possible_errors[err.num], 'figure': None,  'currentField': None, 'destField': None},
                                    status=409)
            elif isinstance(err, ChessException_7):
                return JsonResponse(data={'move': None, 'error': possible_errors[7], 'figure': None, 'currentField': None, 'destField': None},
                                    status=404)
            else:
                JsonResponse(data={'move': None, 'error': possible_errors[err.num], 'figure': None, 'currentField': None, 'destField': None},
                             status=500)
    else:
        if data_to_back == True:
            return JsonResponse(data={'move': 'valid', 'error': None, 'figure': figure.lower(), 'currentField': field1.lower(),
                                      'destField': field2.lower()}, status=200)
        else:
            return JsonResponse(data={'move': 'ivalid', 'error': 'Current move is not permitted.', 'figure': figure.lower(),
                                      'currentField': field1.lower(), 'destField': field2.lower()}, status=200)














