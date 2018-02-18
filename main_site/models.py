from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Province(models.Model):
    name = models.CharField(null=True, blank=True, max_length=42)

    # Return number of all valid votes in province.
    def get_valid_votes(self):
        communes = Commune.objects.filter(province=self)
        valid_votes = 0
        for commune in communes:
            valid_votes += commune.valid_votes
        return valid_votes

    # Returns a list with votes in this province for each candidate.
    # Votes are in order like candidates are saved in database.
    def get_votes_of_candidates(self):
        communes = Commune.objects.filter(province=self)
        candidates = Candidate.objects.all()
        sorted(candidates, key=lambda x: x.surname, reverse=False)
        votes_per_candidate = [0] * candidates.count()
        for i, candidate in enumerate(candidates):
            for commune in communes:
                votings = Voting.objects.filter(commune=commune, candidate=candidate)
                for voting in votings:
                    votes_per_candidate[i] += voting.votes

        return votes_per_candidate

    # Returns vote percentage for each candidate.
    def get_percentages(self):
        votes_per_candidate = self.get_votes_of_candidates()
        valid_votes = self.get_valid_votes()
        percentage_per_candidate = [0] * votes_per_candidate.__len__()
        if valid_votes != 0:
            for i, votes in enumerate(votes_per_candidate):
                percentage_per_candidate[i] = round(100 * votes_per_candidate[i] / valid_votes, 2)
        return percentage_per_candidate

    def __str__(self):
        return self.name.encode('utf-8')

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.my_natural_key


class Candidate(models.Model):
    name = models.CharField(max_length=42)
    surname = models.CharField(max_length=42)

    def __str__(self):
        return self.surname.upper().encode('utf-8') + " " + self.name.encode('utf-8')


def counter(clean):
    # Counts how many candidates is display inline in Commune
    counter.cnt += 1
    if clean:
        counter.cnt = 0
counter.cnt = 0


def sum_votes(v, clean):
    # Sums votes of displayed candidates
    if clean:
        sum_votes.votes = 0
    else:
        sum_votes.votes += v
sum_votes.votes = 0


class Voting(models.Model):
    candidate = models.ForeignKey('Candidate', null=True, blank=True, on_delete=models.CASCADE)
    commune = models.ForeignKey('Commune', null=True, blank=True, on_delete=models.CASCADE)
    votes = models.IntegerField(null=True, blank=True, default=0, verbose_name='Votes')

    def clean(self):
        candidates = Candidate.objects.all()
        counter(False)
        sum_votes(self.votes, False)
        # Check sum of votes only when clean checks last candidate
        if sum_votes.votes != self.commune.valid_votes \
                and counter.cnt % candidates.count() == 0:
            sum_votes(0, True)
            raise ValidationError('Sum of all votes do not sum to valid votes in commune')
        if counter.cnt % candidates.count() == 0:
            counter(True)
            sum_votes(0, True)

    def __str__(self):
        return self.candidate.surname.encode('utf-8') + " - " + self.commune.name.encode('utf-8')


class CommuneType(models.Model):
    name = models.CharField(max_length=42)

    # Return number of all valid votes in type.
    def get_valid_votes(self):
        communes = Commune.objects.filter(type=self)
        valid_votes = 0
        for commune in communes:
            valid_votes += commune.valid_votes
        return valid_votes

    # Returns a list with votes in this type of commune for each candidate.
    # Votes are in order like candidates are saved in database.
    def get_votes_of_candidates(self):
        communes = Commune.objects.filter(type=self)
        candidates = Candidate.objects.all()
        votes_per_candidate = [0] * candidates.count()
        for i, candidate in enumerate(candidates):
            for commune in communes:
                votings = Voting.objects.filter(commune=commune, candidate=candidate)
                for voting in votings:
                    votes_per_candidate[i] += voting.votes
        return votes_per_candidate

    # Returns vote percentage for each candidate.
    def get_percentages(self):
        votes_per_candidate = self.get_votes_of_candidates()
        valid_votes = self.get_valid_votes()
        percentage_per_candidate = [0] * votes_per_candidate.__len__()
        if valid_votes != 0:
            for i, votes in enumerate(votes_per_candidate):
                percentage_per_candidate[i] = round(100 * votes_per_candidate[i] / valid_votes, 2)
        return percentage_per_candidate

    def __str__(self):
        return self.name.encode('utf-8')


class InhabitantsRange(models.Model):
    max_end = 1000000000000000
    begin = models.IntegerField(default=0, verbose_name='Begin')
    end = models.IntegerField(default=0, verbose_name='End')
    name = models.CharField(max_length=42, verbose_name='Name')

    # Returns valid votes for this range.
    def get_valid_votes(self):
        communes = Commune.objects.filter(inhabitants__gte=self.begin, inhabitants__lte=self.end)
        valid_votes = 0
        for commune in communes:
            valid_votes += commune.valid_votes
        return valid_votes

    # Returns a list with votes in this range of inhabitants for each candidate.
    # Votes are in order like candidates are saved in database.
    def get_votes_of_candidates(self):
        communes = Commune.objects.filter(inhabitants__gte=self.begin, inhabitants__lte=self.end)
        candidates = Candidate.objects.all()
        votes_per_candidate = [0] * candidates.count()
        for i, candidate in enumerate(candidates):
            for commune in communes:
                votings = Voting.objects.filter(commune=commune, candidate=candidate)
                for voting in votings:
                    votes_per_candidate[i] += voting.votes
        return votes_per_candidate

    # Returns vote percentage for each candidate.
    def get_percentages(self):
        votes_per_candidate = self.get_votes_of_candidates()
        valid_votes = self.get_valid_votes()
        percentage_per_candidate = [0] * votes_per_candidate.__len__()
        if valid_votes != 0:
            for i, votes in enumerate(votes_per_candidate):
                percentage_per_candidate[i] = round(100 * votes_per_candidate[i] / valid_votes, 2)
        return percentage_per_candidate

    def clean(self):
        if self.end == 0:
            self.end = self.max_end

    def __str__(self):
        return self.name.encode('utf-8')


class Commune(models.Model):
    name = models.CharField(null=True, blank=True, max_length=42)
    province = models.ForeignKey('Province', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Province')
    type = models.ForeignKey('CommuneType', null=True, blank=True, on_delete=models.CASCADE, verbose_name='Commune type')
    inhabitants = models.IntegerField(null=True, blank=True, default=0, verbose_name='Inhabitants')
    entitled_inhabitants = models.IntegerField(null=True, blank=True, default=0, verbose_name='Entitled inhabitants')
    distributed_ballots = models.IntegerField(null=True, blank=True, default=0, verbose_name='Distributed ballots')
    votes = models.IntegerField(null=True, blank=True, default=0, verbose_name='Votes')
    valid_votes = models.IntegerField(null=True, blank=True, default=0, verbose_name='Valid votes')
    last_mod_date = models.DateTimeField(null=True, auto_now=True)
    last_mod_user = models.CharField(default="admin", max_length=42)

    def __unicode__(self):
        return self.name

    def get_last_mod_date_str(self):
        if self.last_mod_date is None:
            return '2016-05-19 19:34'
        else:
            return self.last_mod_date.strftime('%Y-%m-%d %H:%M')

    def get_province_name(self):
        return self.province.name

    # Check whether the commune already exists in database.
    def commune_exists(self):
        return self.name != '' and Commune.objects.filter(name=self.name, province=self.province).exists()

    def is_valid_entitled(self):
        if self.entitled_inhabitants > self.inhabitants:
            return False
        else:
            return True

    def is_valid_distributed_ballots(self):
        if self.distributed_ballots > self.entitled_inhabitants:
            return False
        else:
            return True

    def is_valid_votes(self):
        if self.votes > self.distributed_ballots:
            return False
        else:
            return True

    def is_valid_valid_votes(self):
        if self.valid_votes > self.votes:
            return False
        else:
            return True

    def save(self, *attr, **kwargs):
        # Save only objects that haven't changed their votes value.
        if self.last_mod_date is None:
            self.last_mod_date = timezone.now()
        super(Commune, self).save(*attr, **kwargs)

    def clean(self):
        # We can create (add) one commune only once.
        if self._state.adding and self.commune_exists():
            raise ValidationError('This commune already exists. You can only edit it.')
        elif not self.is_valid_entitled():
            raise ValidationError({
                'entitled_inhabitants': 'There are more entitled inhabitants than all inhabitants'
                })
        elif not self.is_valid_distributed_ballots():
            raise ValidationError({
                'distributed_ballots': 'There are more distributed ballots than all entitled inhabitants'
                })
        elif not self.is_valid_votes():
            raise ValidationError({
                'votes': 'There are more votes than distributed ballots'
                })
        elif not self.is_valid_valid_votes():
            raise ValidationError({
                'valid_votes': 'There are more valid votes than all votes'
                })

    def __str__(self):
        return self.name.encode('utf-8')