from django.db import models


class PC(models.Model):
    # id = models.ForeignKey('State', models.DO_NOTHING, db_column='id')
    year = models.CharField(max_length=10, blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pc'


class PCBigTable(models.Model):
    # id = models.ForeignKey('States', models.DO_NOTHING, db_column='id')
    pc_name_url = models.TextField(blank=True, null=True)
    pc_name = models.CharField(max_length=100, blank=True, null=True)
    no = models.IntegerField()
    type = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    winning_candidate = models.CharField(max_length=100, blank=True, null=True)
    party_url = models.TextField(blank=True, null=True)
    party = models.CharField(max_length=100, blank=True, null=True)
    electors = models.CharField(max_length=100, blank=True, null=True)
    votes = models.CharField(max_length=100, blank=True, null=True)
    turnout_percent = models.CharField(max_length=100, blank=True, null=True)
    margin = models.CharField(max_length=100, blank=True, null=True)
    margin_percent = models.CharField(max_length=100, blank=True, null=True)
    acs_url = models.TextField(blank=True, null=True)
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pc_bigtable'
        unique_together = (('id', 'no', 'year'),)


class PCDetail(models.Model):
    # id = models.IntegerField()
    no = models.IntegerField()
    state = models.CharField(max_length=100, blank=True, null=True)
    acs = models.CharField(db_column='ACs', max_length=100, blank=True, null=True)  # Field name made lowercase.
    pc_type = models.CharField(max_length=100, blank=True, null=True)
    pc_seats = models.CharField(max_length=100, blank=True, null=True)
    poll_date = models.CharField(max_length=100, blank=True, null=True)
    counting_date = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField()
    result_date = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pc_details'
        unique_together = (('id', 'no', 'year'),)


class PCDetailAggregation(models.Model):
    # id = models.ForeignKey(PCBigTable, on_delete=models.DO_NOTHING, db_column='id')
    no = models.ForeignKey(PCBigTable, related_name='pc_detail_aggregations', on_delete=models.DO_NOTHING,
                           db_column='no')
    electors = models.CharField(max_length=100, blank=True, null=True)
    male_electors = models.CharField(max_length=100, blank=True, null=True)
    female_electors = models.CharField(max_length=100, blank=True, null=True)
    male_voters = models.CharField(max_length=100, blank=True, null=True)
    total_male_voters = models.CharField(max_length=100, blank=True, null=True)
    female_voters = models.CharField(max_length=100, blank=True, null=True)
    total_votes_polled = models.CharField(max_length=100, blank=True, null=True)
    booths = models.CharField(max_length=100, blank=True, null=True)
    total_valid_votes = models.CharField(max_length=100, blank=True, null=True)
    valid_votes = models.CharField(max_length=100, blank=True, null=True)
    service_voters = models.CharField(max_length=100, blank=True, null=True)
    margin = models.CharField(max_length=100, blank=True, null=True)
    nota_votes = models.CharField(max_length=100, blank=True, null=True)
    year = models.ForeignKey(PCBigTable, related_name='pc_detail_year_aggregations', on_delete=models.DO_NOTHING,
                             db_column='year')

    class Meta:
        managed = False
        db_table = 'pc_details_agg'
        unique_together = (('id', 'no', 'year'),)


class PCElectionVote(models.Model):
    # id = models.ForeignKey('States', models.DO_NOTHING, db_column='id')
    electors = models.CharField(max_length=50, blank=True, null=True)
    votes_polled = models.CharField(max_length=50, blank=True, null=True)
    turnout = models.CharField(max_length=50, blank=True, null=True)
    parliamentary_constituencies = models.CharField(max_length=10, blank=True, null=True)
    general = models.CharField(max_length=100, blank=True, null=True)
    bye_election_results = models.CharField(max_length=10, blank=True, null=True)
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pc_elec_votes'
        unique_together = (('id', 'year'),)


class PCPartyVote(models.Model):
    # id = models.ForeignKey('States', models.DO_NOTHING, db_column='id')
    party = models.CharField(max_length=100)
    seats = models.CharField(max_length=100, blank=True, null=True)
    votes = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pc_partyvotes'
        unique_together = (('id', 'party', 'year'),)


class YearToDistMapping(models.Model):
    year = models.IntegerField()
    state = models.CharField(max_length=100, blank=True, null=True)
    state_id = models.IntegerField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    district_id = models.IntegerField(primary_key=True)
    dist_fips = models.CharField(max_length=22, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'year_to_dist_mapping'


class State(models.Model):
    name = models.CharField(max_length=100)
    state_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'states'


class PDistrictRanking(models.Model):
    year = models.IntegerField()
    state_abbr = models.CharField(max_length=2, blank=True, null=True)
    district_fips = models.CharField(max_length=22, blank=True, null=True)
    total_county_votes = models.DecimalField(max_digits=32, decimal_places=5, blank=True,
                                             null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_state_votes = models.DecimalField(max_digits=54, decimal_places=5, blank=True,
                                            null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    percentage = models.DecimalField(max_digits=38, decimal_places=2, blank=True, null=True)
    ranking = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'p_district_rankings'


class InElectionMetadata(models.Model):
    year = models.IntegerField()
    race = models.CharField(max_length=9)
    election_type = models.CharField(max_length=7)
    race_abbr = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'in_election_metadata'
