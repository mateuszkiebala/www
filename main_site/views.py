# encoding: utf-8
import json
from django.http import HttpResponse
from django.shortcuts import render
from .models import Province, Commune, CommuneType, Candidate, InhabitantsRange, Voting
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required


def fill_province_voting(prov_name):
    provinces = Province.objects.filter(name=prov_name)
    # There should be only one province of this name.
    if not provinces:
        return [0, 0]
    else:
        return provinces[0].get_percentages()


# Returns list with votes for each candidate.
def get_votes():
    candidates = Candidate.objects.all()
    votes = [0] * candidates.count()
    for i, candidate in enumerate(candidates):
        votings = Voting.objects.filter(candidate=candidate)
        for voting in votings:
            votes[i] += voting.votes
    return votes


# Returns number of distributed ballots in whole country.
def get_distributed_ballots():
    ballots = 0
    communes = Commune.objects.all()
    for commune in communes:
        ballots += commune.distributed_ballots
    return ballots


# Returns percentage of votes for candidate.
def get_percentages():
    candidates = Candidate.objects.all()
    votes = get_votes()
    all_valid_votes = get_valid_votes()
    percentage = [0] * candidates.count()
    for i, candidate in enumerate(candidates):
        percentage[i] = round(100 * votes[i] / all_valid_votes, 2)
    return percentage


# Returns number of entitled inhabitants in whole country.
def get_entitled_inhabitants():
    entitled = 0
    communes = Commune.objects.all()
    for commune in communes:
        entitled += commune.entitled_inhabitants
    return entitled


# Returns number of valid votes for whole country.
def get_valid_votes():
    valid = 0
    communes = Commune.objects.all()
    for commune in communes:
        valid += commune.valid_votes
    return valid


def get_all_votes():
    votes = 0
    communes = Commune.objects.all()
    for commune in communes:
        votes += commune.votes
    return votes


# Returns number of inhabitants
def get_all_inhabitants():
    inhabitants = 0
    communes = Commune.objects.all()
    for commune in communes:
        inhabitants += commune.inhabitants
    return inhabitants


def get_person_per_meter():
    inhabitants = get_all_inhabitants()
    field = 312685
    return round(inhabitants / field, 0)


def index(request):
    provinces = Province.objects.all()
    communes = Commune.objects.all()
    candidates = Candidate.objects.all()
    communes_types = CommuneType.objects.all()
    ranges = InhabitantsRange.objects.all()

    username = ''
    if request.user.is_authenticated():
        username = request.user.username

    return render(request, 'main_site/index.html',
                  {'provinces': provinces, 'communes': communes,
                   'candidates': candidates, 'commune_types': communes_types,
                   'inhabitants_ranges': ranges, 'username': username})


def create_json_for_commune(commune, votings):
    if commune.province is None:
        province_name = '-'
    else:
        province_name = commune.province.name
    # Candidates sorted by surname.
    new_votings_list = sorted(votings, key=lambda x: x.candidate.surname, reverse=False)
    my_json = JsonSerializer()
    my_json.commune = commune.name
    my_json.province_name = province_name
    my_json.inhabitants = commune.inhabitants
    my_json.entitled_inhabitants = commune.entitled_inhabitants
    my_json.distributed_ballots = commune.distributed_ballots
    my_json.votes = commune.votes
    my_json.valid_votes = commune.valid_votes
    my_json.candidate_0_votes = new_votings_list[0].votes
    my_json.candidate_1_votes = new_votings_list[1].votes
    return my_json.to_json()


def create_json_for_headers(title, candidates):
    sorted(candidates, key=lambda x: x.surname, reverse=False)
    my_json = JsonSerializer()
    my_json.commune = title
    my_json.province_name = 'Województwo'
    my_json.inhabitants = 'Mieszkańcy'
    my_json.entitled_inhabitants = 'Uprawnione osoby'
    my_json.distributed_ballots = 'Wydane karty'
    my_json.votes = 'Głosy'
    my_json.valid_votes = 'Ważne głosy'
    my_json.candidate_0 = candidates[0].name + " " + candidates[0].surname
    my_json.candidate_1 = candidates[1].name + " " + candidates[1].surname
    return my_json.to_json()


@api_view(['GET', ])
def get_communes(request):
    if request.method == 'GET':
        clicked = request.GET['clicked']
        result = []
        communes = Commune.objects.all()
        if Province.objects.filter(name=clicked).exists():
            for commune in communes:
                if commune.province is not None and clicked == commune.get_province_name():
                    candidates = Voting.objects.filter(commune=commune).order_by('candidate')
                    result.append(create_json_for_commune(commune, candidates))

        elif CommuneType.objects.filter(name=clicked).exists():
            for commune in communes:
                if commune.type is not None and clicked == commune.type.name:
                    candidates = Voting.objects.filter(commune=commune).order_by('candidate')
                    result.append(create_json_for_commune(commune, candidates))

        elif InhabitantsRange.objects.filter(name=clicked).exists():
            begin = 0
            end = 100000000000
            splitted = clicked.split()
            if len(splitted) == 2:
                if splitted[0] == "do":
                    end = splitted[1]
                elif splitted[0] == "powyzej":
                    begin = splitted[1]
            elif len(splitted) == 4:
                begin = splitted[1]
                end = splitted[3]

            communes = Commune.objects.filter(inhabitants__gte=begin, inhabitants__lte=end)
            for commune in communes:
                candidates = Voting.objects.filter(commune=commune).order_by('candidate')
                result.append(create_json_for_commune(commune, candidates))
        else:
            print("Error in clicked data")
            print(clicked)

        return Response(result)


@api_view(['GET', ])
def get_headers(request):
    if request.method == 'GET':
        clicked = request.GET['clicked']
        candidates = Candidate.objects.all().order_by('surname');
        result = []
        if Province.objects.filter(name=clicked).exists():
            result.append(create_json_for_headers('Gmina', candidates))
        elif CommuneType.objects.filter(name=clicked).exists():
            result.append(create_json_for_headers('Gmina', candidates))
        elif InhabitantsRange.objects.filter(name=clicked).exists():
            result.append(create_json_for_headers('Gmina', candidates))
        else:
            print("Error in clicked data")
            print(clicked)
        return Response(result)


def get_candidates(candidates_nicks):
    candidates = Candidate.objects.all()
    results = {}
    for i, candidate in enumerate(candidates):
        nick = candidate.name + " " + candidate.surname
        # Key: candidate number, Value: candidate object
        results[candidates_nicks[nick]] = candidate
    return results


@api_view(['GET', ])
def get_last_mod(request):
    if request.method == 'GET':
        commune_name = request.GET['commune']
        province_name = request.GET['province']
        provinces = Province.objects.filter(name=province_name)
        if len(provinces) != 1:
            return Response(status=501)
        communes = Commune.objects.filter(name=commune_name, province=provinces[0])
        if len(communes) != 1:
            return Response(status=501)
        date = communes[0].get_last_mod_date_str()
        my_json = JsonSerializer()
        my_json.user = communes[0].last_mod_user
        my_json.date = date
        return Response([my_json.to_json()])


@csrf_protect
@login_required()
@api_view(['POST', ])
def update_results(request):
    if request.method == 'POST':
        json_data = request.data
        # Data from site - json
        candidates_nicks = {json_data['candidate_0_name']: 'candidate_0', json_data['candidate_1_name']: 'candidate_1'}
        candidates = get_candidates(candidates_nicks)
        province_name = json_data['province_name']
        inhabitants = json_data['inhabitants']
        ent_inh = json_data['entitled_inhabitants']
        dis_ballots = json_data['distributed_ballots']
        votes = json_data['votes']
        valid_votes = json_data['valid_votes']
        candidate_0_votes = json_data['candidate_0_votes']
        candidate_1_votes = json_data['candidate_1_votes']

        provinces = Province.objects.filter(name=province_name)
        if len(provinces) != 1:
            return HttpResponse(status=500)

        province = provinces[0]
        if int(ent_inh) > int(inhabitants):
            return HttpResponse('Więcej uprawnionych osób niż wszystkich mieszkańców.', status=500)
        elif int(dis_ballots) > int(ent_inh):
            return HttpResponse('Więcej wydanych kart niż uprawnionych mieszkańców.', status=500)
        elif int(votes) > int(dis_ballots):
            return HttpResponse('Więcej oddanych głosów niż wydanych kart.', status=500)
        elif int(valid_votes) > int(votes):
            return HttpResponse('Więcej ważnych głosów niż oddanych głosów.', status=500)
        elif (int(candidate_0_votes) + int(candidate_1_votes)) != int(valid_votes):
            return HttpResponse('Suma głosów oddanych na kandydatów nie równa się ilości ważnych głosów.', status=500)

        commune_name = json_data['commune']
        if commune_name == '':
            return Response(status=500)

        communes_set = Commune.objects.filter(name=commune_name, province=province)
        if len(communes_set) != 1:
            return HttpResponse(status=500)
        Voting.objects.filter(commune=communes_set[0],
                              candidate=candidates['candidate_0']).update(votes=candidate_0_votes)
        Voting.objects.filter(commune=communes_set[0],
                              candidate=candidates['candidate_1']).update(votes=candidate_1_votes)
        communes_set.update(inhabitants=inhabitants, entitled_inhabitants=ent_inh, distributed_ballots=dis_ballots,
                            votes=votes, valid_votes=valid_votes, last_mod_user=request.user.username,
                            last_mod_date=timezone.now())

        return HttpResponse("Zmiany zostały wprowadzone.")


@api_view(['GET', ])
def get_row(request):
    if request.method == 'GET':
        commune_name = request.GET['commune_name']
        province_name = request.GET['province_name']
        provinces = Province.objects.filter(name=province_name)
        if len(provinces) != 1:
            return Response(status=501)
        communes = Commune.objects.filter(name=commune_name, province=provinces[0])
        if len(communes) != 1:
            return Response(status=501)

        votings = Voting.objects.filter(commune=communes[0])
        return Response([create_json_for_commune(communes[0], votings)])


@api_view(['GET', ])
def get_province_table(request):
    if request.method == 'GET':
        provinces = Province.objects.all()
        table_rows = []
        for province in provinces:
            row = JsonSerializer()
            row.province_name = province.name
            row.valid_votes = province.get_valid_votes()
            row.candidate_0_votes = province.get_votes_of_candidates()[0]
            row.candidate_0_per = province.get_percentages()[0]
            row.candidate_1_votes = province.get_votes_of_candidates()[1]
            row.candidate_1_per = province.get_percentages()[1]
            table_rows.append(row.to_json())
        return Response(table_rows)


@api_view(['GET', ])
def get_commune_types_table(request):
    if request.method == 'GET':
        commune_types = CommuneType.objects.all()
        table_rows = []
        for type in commune_types:
            row = JsonSerializer()
            row.type_name = type.name
            row.valid_votes = type.get_valid_votes()
            row.candidate_0_votes = type.get_votes_of_candidates()[0]
            row.candidate_0_per = type.get_percentages()[0]
            row.candidate_1_votes = type.get_votes_of_candidates()[1]
            row.candidate_1_per = type.get_percentages()[1]
            table_rows.append(row.to_json())
        return Response(table_rows)


@api_view(['GET', ])
def get_ranges_table(request):
    if request.method == 'GET':
        ranges = InhabitantsRange.objects.all()
        table_rows = []
        for r in ranges:
            row = JsonSerializer()
            row.range_name = r.name
            row.valid_votes = r.get_valid_votes()
            row.candidate_0_votes = r.get_votes_of_candidates()[0]
            row.candidate_0_per = r.get_percentages()[0]
            row.candidate_1_votes = r.get_votes_of_candidates()[1]
            row.candidate_1_per = r.get_percentages()[1]
            table_rows.append(row.to_json())
        return Response(table_rows)


@api_view(['GET', ])
def get_general_data(request):
    if request.method == 'GET':
        data = JsonSerializer()
        data.votes = get_all_votes()
        data.cand_votes = get_votes()
        data.cand_per = get_percentages()
        data.inhabitants = get_all_inhabitants()
        data.population = get_person_per_meter()
        data.entitled_inhabitants = get_entitled_inhabitants()
        data.distributed_ballots = get_distributed_ballots()
        data.valid_votes = get_valid_votes()
        return Response([data.to_json()])


@api_view(['GET', ])
def get_map_data(request):
    if request.method == 'GET':
        array = []
        provinces = Province.objects.all()
        for province in provinces:
            data_0 = JsonSerializer()
            data_0.name = province.name + "_0"
            data_0.value = fill_province_voting(province.name)[0]

            data_1 = JsonSerializer()
            data_1.name = province.name + "_1"
            data_1.value = fill_province_voting(province.name)[1]
            array.append([data_0.to_json(), data_1.to_json()])
        return Response(array)


class JsonSerializer:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
