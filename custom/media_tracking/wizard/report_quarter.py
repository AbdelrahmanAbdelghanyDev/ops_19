import threading
from odoo import models, fields, api, _
from odoo.exceptions import  UserError, ValidationError
import time

# date_from_helper = None
# date_to_helper = None
# date_domain = []


class QuarterReportMonth(models.Model):
    _name = 'quarter.report.month'
    _rec_name = 'name'
    _description = 'Quarter Report Months'

    name = fields.Char(string='Name')
    code = fields.Integer(string="Code")


class WizardQuarterDate(models.TransientModel):
    _name = 'a.wizard.quarter.date'

    quarter_id = fields.Many2one(comodel_name="a.wizard.quarter")
    date = fields.Date(string="Date", required=True)


class WizardQuarterTotalSampleDate(models.TransientModel):
    _name = 'a.wizard.quarter.total.sample.date'

    quarter_id = fields.Many2one(comodel_name="a.wizard.quarter.total.sample")
    date = fields.Date(string="Date", required=True)


class WizardQuarter(models.TransientModel):
    _name = 'a.wizard.quarter'
    _description = 'Rating By Program (Quarter) Wizard'

    date_from = fields.Date('From')
    date_to = fields.Date('To')
    type = fields.Selection([('region', 'Region'), ('age', 'Age'), ('sec', 'SEC'), ('gender', 'Gender')], string='Type')
    region = fields.Many2many('region.data', 'rel_region_data', string='Region')
    age = fields.Many2many('age.data', 'rel_age_data', string='Age')
    sec = fields.Many2many('sec.data', 'rel_sec_data', string='SEC')
    gender = fields.Many2many('gender.data', 'rel_gender_data', string='Gender')
    # specific_dates = fields.Boolean(string="Specific Dates")
    dates_ids = fields.One2many(comodel_name="a.wizard.quarter.date", inverse_name="quarter_id", string="Dates")
    month_ids = fields.Many2many(comodel_name="quarter.report.month", string="Months")
    date_format = fields.Selection(string="Date Format",
                                   selection=[('from_to', 'From/To'), ('days', 'Days'), ('months', 'Months')],
                                   default='from_to', required=True)
    total_sample = fields.Integer(string="Total Sample")
    wizard_date = fields.Char(string="Wizard Date")

    @api.onchange('age')
    def onchange_age(self):
        if not self.age:
            return {'domain': {'age': []}}
        else:
            age_list = []
            for rec in self.age:
                age_list.append(rec._origin.id)
            if self.env.ref('media_tracking.age_all').id in age_list:
                return {'domain': {'age': [('id', '=', False)]}}

    @api.onchange('sec')
    def onchange_sec(self):
        if not self.sec:
            return {'domain': {'sec': []}}
        else:
            sec_list = []
            for rec in self.sec:
                sec_list.append(rec._origin.id)
            if self.env.ref('media_tracking.sec_all').id in sec_list:
                return {'domain': {'sec': [('id', '=', False)]}}

    @api.onchange('gender')
    def onchange_gender(self):
        if not self.gender:
            return {'domain': {'gender': []}}
        else:
            gender_list = []
            for rec in self.gender:
                gender_list.append(rec._origin.id)
            if self.env.ref('media_tracking.gender_all').id in gender_list:
                return {'domain': {'gender': [('id', '=', False)]}}

    @api.onchange('region')
    def onchange_region(self):
        if not self.region:
            return {'domain': {'region': []}}
        else:
            region_list = []
            for rec in self.region:
                region_list.append(rec._origin.id)
            if self.env.ref('media_tracking.region_all').id in region_list:
                return {'domain': {'region': [('id', '=', False)]}}

    def create_total_report(self, total_records):

        # with api.Environment.manage():
        # new_cr = self.pool.cursor()
        # self = self.with_env(self.env(cr=new_cr))
        self._cr.execute('DELETE FROM a_full')
        query = '''
                SELECT period,media_channel_id,programs_id,sum(base) as sum,Count(*),AVG(base) as avg,
                AVG(base_male) as base_male,AVG(base_female) as base_female,
                AVG(base_cairo) as base_cairo,AVG(base_alex) as base_alex,
                AVG(base_delta) as base_delta,AVG(base_ue) as base_ue,
                AVG(base_c_r) as base_canal_red_sea,
                AVG(base_2) as base_2,
                AVG(base_3) as base_3,
                AVG(base_4) as base_4,
                AVG(base_5) as base_5,
                AVG(base_6) as base_6,
                AVG(base_7) as base_7,
                AVG(base_8) as base_8,
                AVG(base_9) as base_9,
                AVG(base_10) as base_10,
                AVG("base_A") as base_a,
                AVG("base_B") as base_b,
                AVG("base_C1") as base_c1,
                AVG("base_C2") as base_c2,
                AVG("base_DE") as base_de
                FROM a_quarter 
                GROUP BY period,media_channel_id,programs_id
                ORDER BY programs_id;
                '''
            # query = '''
            # select period,c.channel_id as channel_id,programs_id,sum(base),Count(*)
            # from a_quarter q join a_channels c on (q.channel_id=c.id)
            # Group By period,c.channel_id,programs_id;
            # '''
        self._cr.execute(query)
        result = self._cr.dictfetchall()
        for rec in result:
            program_line = self.env['a.program.line'].search([('media_channel_id', '=', rec['media_channel_id']),
                                                              ('program_id', '=', rec['programs_id']),
                                                              ('period', '=', rec['period'])], limit=1)
            if not program_line:
                continue
            else:
                if rec['media_channel_id']:
                    query = '''
                            SELECT programs_id,media_channel_id,name
                            FROM a_data_processing WHERE programs_id = %s AND media_channel_id = %s
                            GROUP BY programs_id, media_channel_id, name; 
                            ''' % (rec['programs_id'], rec['media_channel_id'])
                else:
                    query = '''
                            SELECT programs_id,media_channel_id,name
                            FROM a_data_processing WHERE programs_id = %s
                            GROUP BY programs_id, media_channel_id, name; 
                            ''' % (rec['programs_id'])

                self._cr.execute(query)
                number_of_watchers = len(self._cr.dictfetchall())

                self.env['a.full'].create({'programs_id': rec['programs_id'],
                                           'time_from': program_line.date_from_id.id,
                                           'time_to': program_line.date_to_id.id,
                                           'header_from': program_line.header,
                                           'header_to': program_line.header,
                                           'media_channel_id': rec['media_channel_id'],
                                           'total_rate': rec['sum'],
                                           'avg_rate': rec['avg'],
                                           'reach': (number_of_watchers / total_records) * 100
                                           if total_records != 0 else 0,
                                           'base': rec['avg'],
                                           'base_male': rec['base_male'],
                                           'base_female': rec['base_female'],
                                           'base_cairo': rec['base_cairo'],
                                           'base_alex': rec['base_alex'],
                                           'base_delta': rec['base_delta'],
                                           'base_ue': rec['base_ue'],
                                           'base_canal_red_sea': rec['base_canal_red_sea'],
                                           'base_2': rec['base_2'],
                                           'base_3': rec['base_3'],
                                           'base_4': rec['base_4'],
                                           'base_5': rec['base_5'],
                                           'base_6': rec['base_6'],
                                           'base_7': rec['base_7'],
                                           'base_8': rec['base_8'],
                                           'base_9': rec['base_9'],
                                           'base_10': rec['base_10'],
                                           'base_a': rec['base_a'],
                                           'base_b': rec['base_b'],
                                           'base_c1': rec['base_c1'],
                                           'base_c2': rec['base_c2'],
                                           'base_de': rec['base_de'],
                                           })
        self._cr.commit()

    @staticmethod
    def split_channel_lines(channel_lines, wanted_group_no=1):
        length = len(channel_lines)
        return [channel_lines[i * length // wanted_group_no: (i + 1) * length // wanted_group_no]
                for i in range(wanted_group_no)]

    def _thread_quarter_report(self, lines_groups, data_processing_base, number_of_quest_per_day):
        for group in lines_groups:
            query_str = '''channel_lines IN %s''' % str(tuple(group)) if len(group) > 1 else \
                '''channel_lines = %s''' % str(group[0])
            self._cr.execute(
                '''
                SELECT period,time_from,time_to,media_channel_id,programs_id,header,name,date
                FROM a_data_processing
                WHERE ''' + query_str + ''' AND id IN %s''' % str(tuple(data_processing_base.ids)))

            result = self._cr.dictfetchall()
            if result:
                data_processing = result[-1]
                self._cr.execute('''SELECT COUNT(*) as BaseCount,
                                    count(case when week_day IS TRUE then 1 else null end) as WeekdayCount,
                                    count(case when gender = 'male' then 1 else null end) as BaseMaleCount,
                                    count(case when gender = 'male' and week_day IS TRUE then 1 else null end) as WeekdayMaleCount,
                                    count(case when gender = 'female' then 1 else null end) as BaseFemaleCount,
                                    count(case when gender = 'female' and week_day IS TRUE then 1 else null end) as WeekdayFemaleCount,
                                    count(case when region = '1' then 1 else null end) as BaseCairoCount,
                                    count(case when region = '1' and week_day IS TRUE then 1 else null end) as WeekdayCairoCount,
                                    count(case when region = '2' then 1 else null end) as BaseAlexCount,
                                    count(case when region = '2' and week_day IS TRUE then 1 else null end) as WeekdayAlexCount,
                                    count(case when region = '3' then 1 else null end) as BaseDeltaCount,
                                    count(case when region = '3' and week_day IS TRUE then 1 else null end) as WeekdayDeltaCount,
                                    count(case when region = '4' then 1 else null end) as BaseUECount,
                                    count(case when region = '4' and week_day IS TRUE then 1 else null end) as WeekdayUECount,
                                    count(case when region = '5' then 1 else null end) as BaseCRCount,
                                    count(case when region = '5' and week_day IS TRUE then 1 else null end) as WeekdayCRCount,
                                    count(case when age_range = '1' then 1 else null end) as BaseAge1Count,
                                    count(case when age_range = '1' and week_day IS TRUE then 1 else null end) as WeekdayAge1Count,
                                    count(case when age_range = '2' then 1 else null end) as BaseAge2Count,
                                    count(case when age_range = '2' and week_day IS TRUE then 1 else null end) as WeekdayAge2Count,
                                    count(case when age_range = '3' then 1 else null end) as BaseAge3Count,
                                    count(case when age_range = '3' and week_day IS TRUE then 1 else null end) as WeekdayAge3Count,
                                    count(case when age_range = '4' then 1 else null end) as BaseAge4Count,
                                    count(case when age_range = '4' and week_day IS TRUE then 1 else null end) as WeekdayAge4Count,
                                    count(case when age_range = '5' then 1 else null end) as BaseAge5Count,
                                    count(case when age_range = '5' and week_day IS TRUE then 1 else null end) as WeekdayAge5Count,
                                    count(case when age_range = '6' then 1 else null end) as BaseAge6Count,
                                    count(case when age_range = '6' and week_day IS TRUE then 1 else null end) as WeekdayAge6Count,
                                    count(case when age_range = '7' then 1 else null end) as BaseAge7Count,
                                    count(case when age_range = '7' and week_day IS TRUE then 1 else null end) as WeekdayAge7Count,
                                    count(case when age_range = '8' then 1 else null end) as BaseAge8Count,
                                    count(case when age_range = '8' and week_day IS TRUE then 1 else null end) as WeekdayAge8Count,
                                    count(case when age_range = '9' then 1 else null end) as BaseAge9Count,
                                    count(case when age_range = '9' and week_day IS TRUE then 1 else null end) as WeekdayAge9Count,
                                    count(case when sec = 'A' then 1 else null end) as BaseACount,
                                    count(case when sec = 'A' and week_day IS TRUE then 1 else null end) as WeekdayACount,
                                    count(case when sec = 'B' then 1 else null end) as BaseBCount,
                                    count(case when sec = 'B' and week_day IS TRUE then 1 else null end) as WeekdayBCount,
                                    count(case when sec = 'C1' then 1 else null end) as BaseC1Count,
                                    count(case when sec = 'C1' and week_day IS TRUE then 1 else null end) as WeekdayC1Count,
                                    count(case when sec = 'C2' then 1 else null end) as BaseC2Count,
                                    count(case when sec = 'C2' and week_day IS TRUE then 1 else null end) as WeekdayC2Count,
                                    count(case when sec = 'DE' then 1 else null end) as BaseDECount,
                                    count(case when sec = 'DE' and week_day IS TRUE then 1 else null end) as WeekdayDECount
                                    from a_data_processing
                                    where id IN %s and ''' % str(
                    tuple(data_processing_base.ids)) + query_str)
                counters = self._cr.dictfetchall()
                base_counter = counters[0].get('basecount')
                wd_counter = counters[0].get('weekdaycount')
                we_counter = base_counter - wd_counter

                base_counter_male = counters[0].get('basemalecount')
                wd_counter_male = counters[0].get('weekdaymalecount')
                we_counter_male = base_counter_male - wd_counter_male

                base_counter_female = counters[0].get('basefemalecount')
                wd_counter_female = counters[0].get('weekdayfemalecount')
                we_counter_female = base_counter_female - wd_counter_female

                base_counter_cairo = counters[0].get('basecairocount')
                wd_counter_cairo = counters[0].get('weekdaycairocount')
                we_counter_cairo = base_counter_cairo - wd_counter_cairo

                base_counter_alex = counters[0].get('basealexcount')
                wd_counter_alex = counters[0].get('weekdayalexcount')
                we_counter_alex = base_counter_alex - wd_counter_alex

                base_counter_delta = counters[0].get('basedeltacount')
                wd_counter_delta = counters[0].get('weekdaydeltacount')
                we_counter_delta = base_counter_delta - wd_counter_delta

                base_counter_ue = counters[0].get('baseuecount')
                wd_counter_ue = counters[0].get('weekdayuecount')
                we_counter_ue = base_counter_ue - wd_counter_ue

                base_counter_c_r = counters[0].get('basecrcount')
                wd_counter_c_r = counters[0].get('weekdaycrcount')
                we_counter_c_r = base_counter_c_r - wd_counter_c_r

                base_counter_2 = counters[0].get('baseage1count')
                wd_counter_2 = counters[0].get('weekdayage1count')
                we_counter_2 = base_counter_2 - wd_counter_2

                base_counter_3 = counters[0].get('baseage2count')
                wd_counter_3 = counters[0].get('weekdayage2count')
                we_counter_3 = base_counter_3 - wd_counter_3

                base_counter_4 = counters[0].get('baseage3count')
                wd_counter_4 = counters[0].get('weekdayage3count')
                we_counter_4 = base_counter_4 - wd_counter_4

                base_counter_5 = counters[0].get('baseage4count')
                wd_counter_5 = counters[0].get('weekdayage4count')
                we_counter_5 = base_counter_5 - wd_counter_5

                base_counter_6 = counters[0].get('baseage5count')
                wd_counter_6 = counters[0].get('weekdayage5count')
                we_counter_6 = base_counter_6 - wd_counter_6

                base_counter_7 = counters[0].get('baseage6count')
                wd_counter_7 = counters[0].get('weekdayage6count')
                we_counter_7 = base_counter_7 - wd_counter_7

                base_counter_8 = counters[0].get('baseage7count')
                wd_counter_8 = counters[0].get('weekdayage7count')
                we_counter_8 = base_counter_8 - wd_counter_8

                base_counter_9 = counters[0].get('baseage8count')
                wd_counter_9 = counters[0].get('weekdayage8count')
                we_counter_9 = base_counter_9 - wd_counter_9

                base_counter_10 = counters[0].get('baseage9count')
                wd_counter_10 = counters[0].get('weekdayage9count')
                we_counter_10 = base_counter_10 - wd_counter_10

                base_counter_A = counters[0].get('baseacount')
                wd_counter_A = counters[0].get('weekdayacount')
                we_counter_A = base_counter_A - wd_counter_A

                base_counter_B = counters[0].get('basebcount')
                wd_counter_B = counters[0].get('weekdaybcount')
                we_counter_B = base_counter_B - wd_counter_B

                base_counter_C1 = counters[0].get('basec1count')
                wd_counter_C1 = counters[0].get('weekdayc1count')
                we_counter_C1 = base_counter_C1 - wd_counter_C1

                base_counter_C2 = counters[0].get('basec2count')
                wd_counter_C2 = counters[0].get('weekdayc2count')
                we_counter_C2 = base_counter_C2 - wd_counter_C2

                base_counter_DE = counters[0].get('basedecount')
                wd_counter_DE = counters[0].get('weekdaydecount')
                we_counter_DE = base_counter_DE - wd_counter_DE

                dates_of_program = set(data_processing_base.filtered(
                    lambda d: d.programs_id.id == data_processing['programs_id']).mapped('date'))
                no_of_ques = 0
                for date in dates_of_program:
                    no_of_ques += next((item for item in number_of_quest_per_day if item["call_date"] == date)
                                       , {'count': 0})['count']
                quarter_vals = {'period': data_processing['period'],
                                'time_from': data_processing['time_from'],
                                'time_to': data_processing['time_to'],
                                'duration': str(self.env['a.time_from'].browse(data_processing['time_from']).name) + '-' +
                                str(self.env['a.time_from'].browse(data_processing['time_to']).name),
                                # 'channel_id': data_processing['channel_id'],
                                'media_channel_id': data_processing['media_channel_id'],
                                'programs_id': data_processing['programs_id'],
                                'base': base_counter / no_of_ques * 100 if no_of_ques != 0 else 0,
                                # 'channel_lines': line.id,
                                'header': data_processing['header'],
                                'name': data_processing['name'] if data_processing['name']
                                else False,
                                'week_day': wd_counter / no_of_ques * 100 if no_of_ques != 0 else 0,
                                'week_end': we_counter / no_of_ques * 100 if no_of_ques != 0 else 0,
                                }

                if self.gender.ids != []:
                    ######## Male ##############
                    if 1 in self.gender.ids or 3 in self.gender.ids:
                        quarter_vals.update(
                            {'base_male': base_counter_male / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_male': wd_counter_male / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_male': we_counter_male / no_of_ques * 100 if no_of_ques != 0 else 0
                             })
                    ######## Female ##############
                    if 2 in self.gender.ids or 3 in self.gender.ids:
                        quarter_vals.update(
                            {'base_female': base_counter_female / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_female': wd_counter_female / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_female': we_counter_female / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                if self.region.ids != []:
                    ######## Cairo ##############
                    if 1 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_cairo': base_counter_cairo / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_cairo': wd_counter_cairo / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_cairo': we_counter_cairo / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######## Alex ##############
                    if 2 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_alex': base_counter_alex / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_alex': wd_counter_alex / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_alex': we_counter_alex / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######## Delta ##############
                    if 3 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_delta': base_counter_delta / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_delta': wd_counter_delta / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_delta': we_counter_delta / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######## UE ##############
                    if 4 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_ue': base_counter_ue / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_ue': wd_counter_ue / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_ue': we_counter_ue / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######## CR ##############
                    if 5 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_c_r': base_counter_c_r / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_c_r': wd_counter_c_r / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_c_r': we_counter_c_r / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                if self.age.ids != []:
                    ######### 15 - 19 ##############
                    if 1 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_2': base_counter_2 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_2': wd_counter_2 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_2': we_counter_2 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### 20 - 24 ##############
                    if 2 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_3': base_counter_3 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_3': wd_counter_3 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_3': we_counter_3 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### 25 - 29 ##############
                    if 3 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_4': base_counter_4 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_4': wd_counter_4 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_4': we_counter_4 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### 30 - 34 ##############
                    if 4 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_5': base_counter_5 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_5': wd_counter_5 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_5': we_counter_5 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### 35 - 39 ##############
                    if 5 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_6': base_counter_6 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_6': wd_counter_6 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_6': we_counter_6 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### 40 - 44 ##############
                    if 6 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_7': base_counter_7 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_7': wd_counter_7 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_7': we_counter_7 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### 45 - 49 ##############
                    if 7 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_8': base_counter_8 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_8': wd_counter_8 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_8': we_counter_8 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### 50 - 59 ##############
                    if 8 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_9': base_counter_9 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_9': wd_counter_9 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_9': we_counter_9 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### More Than 59 ##############
                    if 9 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_10': base_counter_10 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_10': wd_counter_10 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_10': we_counter_10 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                if self.sec.ids != []:
                    ######### A ##############
                    if 1 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_A': base_counter_A / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_A': wd_counter_A / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_A': we_counter_A / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### B ##############
                    if 2 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_B': base_counter_B / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_B': wd_counter_B / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_B': we_counter_B / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### C1 ##############
                    if 3 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_C1': base_counter_C1 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_C1': wd_counter_C1 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_C1': we_counter_C1 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                    ######### C2 ##############
                    if 4 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_C2': base_counter_C2 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_C2': wd_counter_C2 / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_C2': we_counter_C2 / no_of_ques * 100 if no_of_ques != 0 else 0
                             })
                    ######### DE ##############
                    if 5 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_DE': base_counter_DE / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_day_DE': wd_counter_DE / no_of_ques * 100 if no_of_ques != 0 else 0,
                             'week_end_DE': we_counter_DE / no_of_ques * 100 if no_of_ques != 0 else 0
                             })

                self.env['a.quarter'].create(quarter_vals)

    def thread_quarter_report(self, lines_groups, data_processing_base, total_record_data_processing):

        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            self._thread_quarter_report(lines_groups, data_processing_base, total_record_data_processing)
            new_cr.commit()
            new_cr.close()
        return{}

    def get_report_name(self):
        if self.date_from and self.date_to:
            return _("Rating By Program (Quarter) From %s To %s") % (self.date_from, self.date_to)
        elif self.month_ids:
            months = ''
            for month in self.month_ids:
                months += str(month.name) + ','
            return _("Rating By Program (Quarter) for months %s") % (months)
        elif self.dates_ids:
            dates = ''
            for date in self.dates_ids:
                dates += str(date.date) + ','
            return _("Rating By Program (Quarter) for dates %s") % (dates)
        else:
            return ''
        
    def get_data_processing_base(self, date_domain, filtered):
        gender_domain = []
        region_domain = []
        age_domain = []
        sec_domain = []
        if filtered:
            ######## Male ##############
            if 1 in self.gender.ids or 3 in self.gender.ids:
                if gender_domain:
                    gender_domain = ['|', ('gender', '=', 'male')] + gender_domain
                else:
                    gender_domain += [('gender', '=', 'male')]

            ######## Female ##############
            if 2 in self.gender.ids or 3 in self.gender.ids:
                if gender_domain:
                    gender_domain = ['|', ('gender', '=', 'female')] + gender_domain
                else:
                    gender_domain += [('gender', '=', 'female')]

            ######## Cairo ##############
            if 1 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 1)] + region_domain
                else:
                    region_domain += [('region', '=', 1)]

            ######## Alex ##############
            if 2 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 2)] + region_domain
                else:
                    region_domain += [('region', '=', 2)]

            ######## Delta ##############
            if 3 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 3)] + region_domain
                else:
                    region_domain += [('region', '=', 3)]

            ######## UE ##############
            if 4 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 4)] + region_domain
                else:
                    region_domain += [('region', '=', 4)]

            ######## CR ##############
            if 5 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 5)] + region_domain
                else:
                    region_domain += [('region', '=', 5)]

            ######### 15 - 19 ##############
            if 1 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 1)] + age_domain
                else:
                    age_domain += [('age_range', '=', 1)]

            ######### 20 - 24 ##############
            if 2 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 2)] + age_domain
                else:
                    age_domain += [('age_range', '=', 2)]

            ######### 25 - 29 ##############
            if 3 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 3)] + age_domain
                else:
                    age_domain += [('age_range', '=', 3)]

            ######### 30 - 34 ##############
            if 4 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 4)] + age_domain
                else:
                    age_domain += [('age_range', '=', 4)]

            ######### 35 - 39 ##############
            if 5 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 5)] + age_domain
                else:
                    age_domain += [('age_range', '=', 5)]

            ######### 40 - 44 ##############
            if 6 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 6)] + age_domain
                else:
                    age_domain += [('age_range', '=', 6)]

            ######### 45 - 49 ##############
            if 7 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 7)] + age_domain
                else:
                    age_domain += [('age_range', '=', 7)]

            ######### 50 - 59 ##############
            if 8 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 8)] + age_domain
                else:
                    age_domain += [('age_range', '=', 8)]

            ######### More Than 59 ##############
            if 9 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 9)] + age_domain
                else:
                    age_domain += [('age_range', '=', 9)]


            ######### A ##############
            if 1 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'A')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'A')]

            ######### B ##############
            if 2 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'B')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'B')]

            ######### C1 ##############
            if 3 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'C1')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'C1')]

            ######### C2 ##############
            if 4 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'C2')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'C2')]

            ######### DE ##############
            if 5 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'DE')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'DE')]
            filtered_domain = ['&'] + gender_domain + ['&'] + region_domain + ['&'] + age_domain +\
                              ['&'] + sec_domain
            # print(filtered_domain)
            return self.env['a.data.processing'].search(filtered_domain + date_domain +
                                                        [('channel_lines', '!=', False),
                                                        ('stage_id', '=', 'approved')])
        else:
            return self.env['a.data.processing'].search(date_domain + [('channel_lines', '!=', False),
                                                                       ('stage_id', '=', 'approved')])

    def get_total_sample_count(self, date_domain, filtered):
        gender_domain = []
        region_domain = []
        age_domain = []
        sec_domain = []
        if filtered:
            ######## Male ##############
            if 1 in self.gender.ids or 3 in self.gender.ids:
                if gender_domain:
                    gender_domain = ['|', ('s4', '=', 'male')] + gender_domain
                else:
                    gender_domain += [('s4', '=', 'male')]

            ######## Female ##############
            if 2 in self.gender.ids or 3 in self.gender.ids:
                if gender_domain:
                    gender_domain = ['|', ('s4', '=', 'female')] + gender_domain
                else:
                    gender_domain += [('s4', '=', 'female')]

            ######## Cairo ##############
            if 1 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 1)] + region_domain
                else:
                    region_domain += [('sec6', '=', 1)]

            ######## Alex ##############
            if 2 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 2)] + region_domain
                else:
                    region_domain += [('sec6', '=', 2)]

            ######## Delta ##############
            if 3 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 3)] + region_domain
                else:
                    region_domain += [('sec6', '=', 3)]

            ######## UE ##############
            if 4 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 4)] + region_domain
                else:
                    region_domain += [('sec6', '=', 4)]

            ######## CR ##############
            if 5 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 5)] + region_domain
                else:
                    region_domain += [('sec6', '=', 5)]

            ######### 15 - 19 ##############
            if 1 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 2)] + age_domain
                else:
                    age_domain += [('s3', '=', 2)]

            ######### 20 - 24 ##############
            if 2 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 3)] + age_domain
                else:
                    age_domain += [('s3', '=', 3)]

            ######### 25 - 29 ##############
            if 3 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 4)] + age_domain
                else:
                    age_domain += [('s3', '=', 4)]

            ######### 30 - 34 ##############
            if 4 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 5)] + age_domain
                else:
                    age_domain += [('s3', '=', 5)]

            ######### 35 - 39 ##############
            if 5 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 6)] + age_domain
                else:
                    age_domain += [('s3', '=', 6)]

            ######### 40 - 44 ##############
            if 6 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 7)] + age_domain
                else:
                    age_domain += [('s3', '=', 7)]

            ######### 45 - 49 ##############
            if 7 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 8)] + age_domain
                else:
                    age_domain += [('s3', '=', 8)]

            ######### 50 - 59 ##############
            if 8 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 9)] + age_domain
                else:
                    age_domain += [('s3', '=', 9)]

            ######### More Than 59 ##############
            if 9 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 10)] + age_domain
                else:
                    age_domain += [('s3', '=', 10)]


            ######### A ##############
            if 1 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'A')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'A')]

            ######### B ##############
            if 2 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'B')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'B')]

            ######### C1 ##############
            if 3 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'C1')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'C1')]

            ######### C2 ##############
            if 4 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'C2')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'C2')]

            ######### DE ##############
            if 5 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'DE')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'DE')]
            filtered_domain = ['&'] + gender_domain + region_domain + ['&'] + age_domain + sec_domain
            # print(filtered_domain)
            return self.env['a.questionnaire'].search_count(filtered_domain + date_domain +
                                                            [('stage_id', '=', 'approved')])
        else:
            return self.env['a.questionnaire'].search_count(date_domain + [('stage_id', '=', 'approved')])

    def generate_quarter_report(self):
        date_domain = []
        if self.date_format == 'from_to':
            date_domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to)]
        elif self.date_format == 'days':
            date_domain.append(('date', 'in', self.dates_ids.mapped('date')))
        else:
            date_domain.append(('month', 'in', self.month_ids.mapped('code')))

        filtered = self.env.context.get('filtered', False)

        self.total_sample = self.get_total_sample_count(date_domain, filtered)

        self.wizard_date = self.get_report_name()

        data_processing_base = self.get_data_processing_base(date_domain, filtered)
        questionnaire_ids = data_processing_base.mapped('name').mapped('id')

        if data_processing_base and data_processing_base.ids:

            samples_per_day = ''' 
            select count(*),call_date from a_questionnaire where id IN %s Group By call_date
            ''' % str(
                tuple(questionnaire_ids))
            self._cr.execute(samples_per_day)
            number_of_quest_per_day = self._cr.dictfetchall()
            self._cr.execute('DELETE FROM a_quarter')

        if data_processing_base:
            # print(data_processing_base)
            channel_lines = data_processing_base.mapped('channel_lines').mapped('id')
            query = '''
                    SELECT period,program,time_from,time_to,header,
                    array_agg(id) as ids
                    FROM a_channel_lines 
                    WHERE id IN %s
                    GROUP BY period,program,time_from,time_to,header
                    ''' % str(tuple(channel_lines))

            self._cr.execute(query)
            groups = self._cr.dictfetchall()
            groups_ids = []
            for group in groups:
                groups_ids.append(group['ids'])
            line_groups = self.split_channel_lines(groups_ids, 10)
            for line_group in line_groups:
                self._thread_quarter_report(line_group, data_processing_base, number_of_quest_per_day)

            total_records = self.get_total_sample()
            self.create_total_report(total_records)
            return {
                'name': self.get_report_name(),
                'view_mode': 'tree,pivot',
                'res_model': 'a.quarter',
                'view_ids': [(self.env.ref('media_tracking.quarter_list').id, 'list'),
                             (self.env.ref('media_tracking.quarter_view_pivot').id, 'pivot')],
                'target': 'current',
                'type': 'ir.actions.act_window', }
        else:
            raise UserError(
                _("No Records")
            )

        # ===============================================================================================
        # query = '''
        # SELECT period,programs_id,duration,time_from,time_to,media_channel_id,header,
        # name,count(*) as count, sum(base) as base,sum(week_day) as week_day, sum(week_end) as week_end,
        # array_agg(id) as ids
        # FROM a_quarter
        # GROUP BY period,programs_id,duration,time_from,time_to,media_channel_id,header,name
        # '''
        #
        # self._cr.execute(query)
        # groups = self._cr.dictfetchall()
        # for group in groups:
        #     print(group['ids'])
        #     if group['count'] > 1:
        #         self.env['a.quarter'].create({'period': group['period'],
        #                                       'time_from': group['time_from'],
        #                                       'time_to': group['time_to'],
        #                                       # 'channel_id': data_processing['channel_id'],
        #                                       'media_channel_id': group['media_channel_id'],
        #                                       'programs_id': group['programs_id'],
        #                                       'base': group['base'],
        #                                       # 'channel_lines': line.id,
        #                                       'header': group['header'],
        #                                       'name': group['name'],
        #                                       'week_day': group['week_day'],
        #                                       'week_end': group['week_end'],
        #                                       })
        #         self._cr.execute('DELETE FROM a_quarter WHERE id IN %s' % str(tuple(group['ids'])))
        #     else:
        #         continue

        # quarter_obj = self.env['a.quarter']
        # quarter_groups = quarter_obj.read_group([], ['period', 'programs_id', 'duration', 'time_from',
        #                                              'time_to', 'media_channel_id', 'header', 'name'],
        #                                         ['period', 'programs_id', 'duration'], lazy=False)
        # for group in quarter_groups:
        #     if group['__count'] > 1:
        #         quarter_lines = self.env['a.quarter'].search(group['__domain'])

        # ===============================================================================

    def get_total_sample(self) -> int:
        if self.env['a.wizard.quarter'].search([]):
            total_sample = self.env['a.wizard.quarter'].search([])[-1].total_sample
        else:
            return 0
        return total_sample

    def get_wizard_date(self):
        if self.env['a.wizard.quarter'].search([]):
            wizard_date = self.env['a.wizard.quarter'].search([])[-1].wizard_date
        else:
            return 'x'
        return wizard_date


class WizardQuarterTotalSample(models.TransientModel):
    _name = 'a.wizard.quarter.total.sample'
    _description = 'Rating By Program (Quarter) Wizard (total sample)'

    date_from = fields.Date('From')
    date_to = fields.Date('To')
    type = fields.Selection([('region', 'Region'), ('age', 'Age'), ('sec', 'SEC'), ('gender', 'Gender')], string='Type')
    region = fields.Many2many('region.data', 'rel_region_data_total_sample', string='Region')
    age = fields.Many2many('age.data', 'rel_age_data_total_sample', string='Age')
    sec = fields.Many2many('sec.data', 'rel_sec_data_total_sample', string='SEC')
    gender = fields.Many2many('gender.data', 'rel_gender_data_total_sample', string='Gender')
    dates_ids = fields.One2many(comodel_name="a.wizard.quarter.total.sample.date",
                                inverse_name="quarter_id", string="Dates")
    month_ids = fields.Many2many(comodel_name="quarter.report.month", string="Months")
    date_format = fields.Selection(string="Date Format",
                                   selection=[('from_to', 'From/To'), ('days', 'Days'), ('months', 'Months')],
                                   default='from_to', required=True)
    total_sample = fields.Integer(string="Total Sample")
    wizard_date = fields.Char(string="Wizard Date")

    @api.onchange('age')
    def onchange_age(self):
        if not self.age:
            return {'domain': {'age': []}}
        else:
            age_list = []
            for rec in self.age:
                age_list.append(rec._origin.id)
            if self.env.ref('media_tracking.age_all').id in age_list:
                return {'domain': {'age': [('id', '=', False)]}}

    @api.onchange('sec')
    def onchange_sec(self):
        if not self.sec:
            return {'domain': {'sec': []}}
        else:
            sec_list = []
            for rec in self.sec:
                sec_list.append(rec._origin.id)
            if self.env.ref('media_tracking.sec_all').id in sec_list:
                return {'domain': {'sec': [('id', '=', False)]}}

    @api.onchange('gender')
    def onchange_gender(self):
        if not self.gender:
            return {'domain': {'gender': []}}
        else:
            gender_list = []
            for rec in self.gender:
                gender_list.append(rec._origin.id)
            if self.env.ref('media_tracking.gender_all').id in gender_list:
                return {'domain': {'gender': [('id', '=', False)]}}

    @api.onchange('region')
    def onchange_region(self):
        if not self.region:
            return {'domain': {'region': []}}
        else:
            region_list = []
            for rec in self.region:
                region_list.append(rec._origin.id)
            if self.env.ref('media_tracking.region_all').id in region_list:
                return {'domain': {'region': [('id', '=', False)]}}

    def create_total_report(self, total_records):

        # with api.Environment.manage():
        # new_cr = self.pool.cursor()
        # self = self.with_env(self.env(cr=new_cr))
        self._cr.execute('DELETE FROM a_full_total_sample')
        query = '''
                SELECT period,media_channel_id,programs_id,sum(base) as sum,Count(*),AVG(base) as avg,
                AVG(base_male) as base_male,AVG(base_female) as base_female,
                AVG(base_cairo) as base_cairo,AVG(base_alex) as base_alex,
                AVG(base_delta) as base_delta,AVG(base_ue) as base_ue,
                AVG(base_c_r) as base_canal_red_sea,
                AVG(base_2) as base_2,
                AVG(base_3) as base_3,
                AVG(base_4) as base_4,
                AVG(base_5) as base_5,
                AVG(base_6) as base_6,
                AVG(base_7) as base_7,
                AVG(base_8) as base_8,
                AVG(base_9) as base_9,
                AVG(base_10) as base_10,
                AVG("base_A") as base_a,
                AVG("base_B") as base_b,
                AVG("base_C1") as base_c1,
                AVG("base_C2") as base_c2,
                AVG("base_DE") as base_de
                FROM a_quarter_total_sample
                GROUP BY period,media_channel_id,programs_id
                ORDER BY programs_id;
                '''
        self._cr.execute(query)
        result = self._cr.dictfetchall()
        for rec in result:
            program_line = self.env['a.program.line'].search([('media_channel_id', '=', rec['media_channel_id']),
                                                              ('program_id', '=', rec['programs_id']),
                                                              ('period', '=', rec['period'])], limit=1)
            if not program_line:
                continue
            else:
                if rec['media_channel_id']:
                    query = '''
                            SELECT programs_id,media_channel_id,name
                            FROM a_data_processing WHERE programs_id = %s AND media_channel_id = %s
                            GROUP BY programs_id, media_channel_id, name; 
                            ''' % (rec['programs_id'], rec['media_channel_id'])
                else:
                    query = '''
                            SELECT programs_id,media_channel_id,name
                            FROM a_data_processing WHERE programs_id = %s
                            GROUP BY programs_id, media_channel_id, name; 
                            ''' % (rec['programs_id'])

                self._cr.execute(query)
                number_of_watchers = len(self._cr.dictfetchall())

                self.env['a.full.total.sample'].create({'programs_id': rec['programs_id'],
                                                        'time_from': program_line.date_from_id.id,
                                                        'time_to': program_line.date_to_id.id,
                                                        'header_from': program_line.header,
                                                        'header_to': program_line.header,
                                                        'media_channel_id': rec['media_channel_id'],
                                                        'total_rate': rec['sum'],
                                                        'avg_rate': rec['avg'],
                                                        'reach': (number_of_watchers / total_records) * 100
                                                        if total_records != 0 else 0,
                                                        'base': rec['avg'],
                                                        'base_male': rec['base_male'],
                                                        'base_female': rec['base_female'],
                                                        'base_cairo': rec['base_cairo'],
                                                        'base_alex': rec['base_alex'],
                                                        'base_delta': rec['base_delta'],
                                                        'base_ue': rec['base_ue'],
                                                        'base_canal_red_sea': rec['base_canal_red_sea'],
                                                        'base_2': rec['base_2'],
                                                        'base_3': rec['base_3'],
                                                        'base_4': rec['base_4'],
                                                        'base_5': rec['base_5'],
                                                        'base_6': rec['base_6'],
                                                        'base_7': rec['base_7'],
                                                        'base_8': rec['base_8'],
                                                        'base_9': rec['base_9'],
                                                        'base_10': rec['base_10'],
                                                        'base_a': rec['base_a'],
                                                        'base_b': rec['base_b'],
                                                        'base_c1': rec['base_c1'],
                                                        'base_c2': rec['base_c2'],
                                                        'base_de': rec['base_de'],
                                                        })
        self._cr.commit()

    @staticmethod
    def split_channel_lines(channel_lines, wanted_group_no=1):
        length = len(channel_lines)
        return [channel_lines[i * length // wanted_group_no: (i + 1) * length // wanted_group_no]
                for i in range(wanted_group_no)]

    def _thread_quarter_report(self, lines_groups, data_processing_base, number_of_total_quest):
        for group in lines_groups:
            query_str = '''channel_lines IN %s''' % str(tuple(group)) if len(group) > 1 else \
                '''channel_lines = %s''' % str(group[0])
            self._cr.execute(
                '''
                SELECT period,time_from,time_to,media_channel_id,programs_id,header,name,date
                FROM a_data_processing
                WHERE ''' + query_str + ''' AND id IN %s''' % str(tuple(data_processing_base.ids)))

            result = self._cr.dictfetchall()
            if result:
                data_processing = result[-1]
                self._cr.execute('''SELECT COUNT(*) as BaseCount,
                                    count(case when week_day IS TRUE then 1 else null end) as WeekdayCount,
                                    count(case when gender = 'male' then 1 else null end) as BaseMaleCount,
                                    count(case when gender = 'male' and week_day IS TRUE then 1 else null end) as WeekdayMaleCount,
                                    count(case when gender = 'female' then 1 else null end) as BaseFemaleCount,
                                    count(case when gender = 'female' and week_day IS TRUE then 1 else null end) as WeekdayFemaleCount,
                                    count(case when region = '1' then 1 else null end) as BaseCairoCount,
                                    count(case when region = '1' and week_day IS TRUE then 1 else null end) as WeekdayCairoCount,
                                    count(case when region = '2' then 1 else null end) as BaseAlexCount,
                                    count(case when region = '2' and week_day IS TRUE then 1 else null end) as WeekdayAlexCount,
                                    count(case when region = '3' then 1 else null end) as BaseDeltaCount,
                                    count(case when region = '3' and week_day IS TRUE then 1 else null end) as WeekdayDeltaCount,
                                    count(case when region = '4' then 1 else null end) as BaseUECount,
                                    count(case when region = '4' and week_day IS TRUE then 1 else null end) as WeekdayUECount,
                                    count(case when region = '5' then 1 else null end) as BaseCRCount,
                                    count(case when region = '5' and week_day IS TRUE then 1 else null end) as WeekdayCRCount,
                                    count(case when age_range = '1' then 1 else null end) as BaseAge1Count,
                                    count(case when age_range = '1' and week_day IS TRUE then 1 else null end) as WeekdayAge1Count,
                                    count(case when age_range = '2' then 1 else null end) as BaseAge2Count,
                                    count(case when age_range = '2' and week_day IS TRUE then 1 else null end) as WeekdayAge2Count,
                                    count(case when age_range = '3' then 1 else null end) as BaseAge3Count,
                                    count(case when age_range = '3' and week_day IS TRUE then 1 else null end) as WeekdayAge3Count,
                                    count(case when age_range = '4' then 1 else null end) as BaseAge4Count,
                                    count(case when age_range = '4' and week_day IS TRUE then 1 else null end) as WeekdayAge4Count,
                                    count(case when age_range = '5' then 1 else null end) as BaseAge5Count,
                                    count(case when age_range = '5' and week_day IS TRUE then 1 else null end) as WeekdayAge5Count,
                                    count(case when age_range = '6' then 1 else null end) as BaseAge6Count,
                                    count(case when age_range = '6' and week_day IS TRUE then 1 else null end) as WeekdayAge6Count,
                                    count(case when age_range = '7' then 1 else null end) as BaseAge7Count,
                                    count(case when age_range = '7' and week_day IS TRUE then 1 else null end) as WeekdayAge7Count,
                                    count(case when age_range = '8' then 1 else null end) as BaseAge8Count,
                                    count(case when age_range = '8' and week_day IS TRUE then 1 else null end) as WeekdayAge8Count,
                                    count(case when age_range = '9' then 1 else null end) as BaseAge9Count,
                                    count(case when age_range = '9' and week_day IS TRUE then 1 else null end) as WeekdayAge9Count,
                                    count(case when sec = 'A' then 1 else null end) as BaseACount,
                                    count(case when sec = 'A' and week_day IS TRUE then 1 else null end) as WeekdayACount,
                                    count(case when sec = 'B' then 1 else null end) as BaseBCount,
                                    count(case when sec = 'B' and week_day IS TRUE then 1 else null end) as WeekdayBCount,
                                    count(case when sec = 'C1' then 1 else null end) as BaseC1Count,
                                    count(case when sec = 'C1' and week_day IS TRUE then 1 else null end) as WeekdayC1Count,
                                    count(case when sec = 'C2' then 1 else null end) as BaseC2Count,
                                    count(case when sec = 'C2' and week_day IS TRUE then 1 else null end) as WeekdayC2Count,
                                    count(case when sec = 'DE' then 1 else null end) as BaseDECount,
                                    count(case when sec = 'DE' and week_day IS TRUE then 1 else null end) as WeekdayDECount
                                    from a_data_processing
                                    where id IN %s and ''' % str(
                    tuple(data_processing_base.ids)) + query_str)
                counters = self._cr.dictfetchall()
                base_counter = counters[0].get('basecount')
                wd_counter = counters[0].get('weekdaycount')
                we_counter = base_counter - wd_counter

                base_counter_male = counters[0].get('basemalecount')
                wd_counter_male = counters[0].get('weekdaymalecount')
                we_counter_male = base_counter_male - wd_counter_male

                base_counter_female = counters[0].get('basefemalecount')
                wd_counter_female = counters[0].get('weekdayfemalecount')
                we_counter_female = base_counter_female - wd_counter_female

                base_counter_cairo = counters[0].get('basecairocount')
                wd_counter_cairo = counters[0].get('weekdaycairocount')
                we_counter_cairo = base_counter_cairo - wd_counter_cairo

                base_counter_alex = counters[0].get('basealexcount')
                wd_counter_alex = counters[0].get('weekdayalexcount')
                we_counter_alex = base_counter_alex - wd_counter_alex

                base_counter_delta = counters[0].get('basedeltacount')
                wd_counter_delta = counters[0].get('weekdaydeltacount')
                we_counter_delta = base_counter_delta - wd_counter_delta

                base_counter_ue = counters[0].get('baseuecount')
                wd_counter_ue = counters[0].get('weekdayuecount')
                we_counter_ue = base_counter_ue - wd_counter_ue

                base_counter_c_r = counters[0].get('basecrcount')
                wd_counter_c_r = counters[0].get('weekdaycrcount')
                we_counter_c_r = base_counter_c_r - wd_counter_c_r

                base_counter_2 = counters[0].get('baseage1count')
                wd_counter_2 = counters[0].get('weekdayage1count')
                we_counter_2 = base_counter_2 - wd_counter_2

                base_counter_3 = counters[0].get('baseage2count')
                wd_counter_3 = counters[0].get('weekdayage2count')
                we_counter_3 = base_counter_3 - wd_counter_3

                base_counter_4 = counters[0].get('baseage3count')
                wd_counter_4 = counters[0].get('weekdayage3count')
                we_counter_4 = base_counter_4 - wd_counter_4

                base_counter_5 = counters[0].get('baseage4count')
                wd_counter_5 = counters[0].get('weekdayage4count')
                we_counter_5 = base_counter_5 - wd_counter_5

                base_counter_6 = counters[0].get('baseage5count')
                wd_counter_6 = counters[0].get('weekdayage5count')
                we_counter_6 = base_counter_6 - wd_counter_6

                base_counter_7 = counters[0].get('baseage6count')
                wd_counter_7 = counters[0].get('weekdayage6count')
                we_counter_7 = base_counter_7 - wd_counter_7

                base_counter_8 = counters[0].get('baseage7count')
                wd_counter_8 = counters[0].get('weekdayage7count')
                we_counter_8 = base_counter_8 - wd_counter_8

                base_counter_9 = counters[0].get('baseage8count')
                wd_counter_9 = counters[0].get('weekdayage8count')
                we_counter_9 = base_counter_9 - wd_counter_9

                base_counter_10 = counters[0].get('baseage9count')
                wd_counter_10 = counters[0].get('weekdayage9count')
                we_counter_10 = base_counter_10 - wd_counter_10

                base_counter_A = counters[0].get('baseacount')
                wd_counter_A = counters[0].get('weekdayacount')
                we_counter_A = base_counter_A - wd_counter_A

                base_counter_B = counters[0].get('basebcount')
                wd_counter_B = counters[0].get('weekdaybcount')
                we_counter_B = base_counter_B - wd_counter_B

                base_counter_C1 = counters[0].get('basec1count')
                wd_counter_C1 = counters[0].get('weekdayc1count')
                we_counter_C1 = base_counter_C1 - wd_counter_C1

                base_counter_C2 = counters[0].get('basec2count')
                wd_counter_C2 = counters[0].get('weekdayc2count')
                we_counter_C2 = base_counter_C2 - wd_counter_C2

                base_counter_DE = counters[0].get('basedecount')
                wd_counter_DE = counters[0].get('weekdaydecount')
                we_counter_DE = base_counter_DE - wd_counter_DE

                # dates_of_program = set(data_processing_base.filtered(
                #     lambda d: d.programs_id.id == data_processing['programs_id']).mapped('date'))
                # no_of_ques = 0
                # for date in dates_of_program:
                #     no_of_ques += next((item for item in number_of_quest_per_day if item["call_date"] == date)
                #                        , {'count': 0})['count']

                quarter_vals = {'period': data_processing['period'],
                                'time_from': data_processing['time_from'],
                                'time_to': data_processing['time_to'],
                                'duration': str(
                                    self.env['a.time_from'].browse(data_processing['time_from']).name) + '-' +
                                            str(self.env['a.time_from'].browse(data_processing['time_to']).name),
                                'media_channel_id': data_processing['media_channel_id'],
                                'programs_id': data_processing['programs_id'],
                                'base': base_counter / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                                # 'channel_lines': line.id,
                                'header': data_processing['header'],
                                'name': data_processing['name'] if data_processing['name']
                                else False,
                                'week_day': wd_counter / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                                'week_end': we_counter / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                                }

                if self.gender.ids != []:
                    ######## Male ##############
                    if 1 in self.gender.ids or 3 in self.gender.ids:
                        quarter_vals.update(
                            {'base_male': base_counter_male / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_male': wd_counter_male / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_male': we_counter_male / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })
                    ######## Female ##############
                    if 2 in self.gender.ids or 3 in self.gender.ids:
                        quarter_vals.update(
                            {'base_female': base_counter_female / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_female': wd_counter_female / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_female': we_counter_female / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                if self.region.ids != []:
                    ######## Cairo ##############
                    if 1 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_cairo': base_counter_cairo / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_cairo': wd_counter_cairo / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_cairo': we_counter_cairo / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######## Alex ##############
                    if 2 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_alex': base_counter_alex / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_alex': wd_counter_alex / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_alex': we_counter_alex / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######## Delta ##############
                    if 3 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_delta': base_counter_delta / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_delta': wd_counter_delta / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_delta': we_counter_delta / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######## UE ##############
                    if 4 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_ue': base_counter_ue / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_ue': wd_counter_ue / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_ue': we_counter_ue / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######## CR ##############
                    if 5 in self.region.ids or 6 in self.region.ids:
                        quarter_vals.update(
                            {'base_c_r': base_counter_c_r / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_c_r': wd_counter_c_r / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_c_r': we_counter_c_r / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                if self.age.ids != []:
                    ######### 15 - 19 ##############
                    if 1 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_2': base_counter_2 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_2': wd_counter_2 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_2': we_counter_2 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### 20 - 24 ##############
                    if 2 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_3': base_counter_3 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_3': wd_counter_3 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_3': we_counter_3 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### 25 - 29 ##############
                    if 3 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_4': base_counter_4 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_4': wd_counter_4 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_4': we_counter_4 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### 30 - 34 ##############
                    if 4 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_5': base_counter_5 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_5': wd_counter_5 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_5': we_counter_5 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### 35 - 39 ##############
                    if 5 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_6': base_counter_6 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_6': wd_counter_6 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_6': we_counter_6 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### 40 - 44 ##############
                    if 6 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_7': base_counter_7 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_7': wd_counter_7 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_7': we_counter_7 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### 45 - 49 ##############
                    if 7 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_8': base_counter_8 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_8': wd_counter_8 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_8': we_counter_8 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### 50 - 59 ##############
                    if 8 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_9': base_counter_9 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_9': wd_counter_9 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_9': we_counter_9 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### More Than 59 ##############
                    if 9 in self.age.ids or 10 in self.age.ids:
                        quarter_vals.update(
                            {'base_10': base_counter_10 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_10': wd_counter_10 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_10': we_counter_10 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                if self.sec.ids != []:
                    ######### A ##############
                    if 1 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_A': base_counter_A / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_A': wd_counter_A / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_A': we_counter_A / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### B ##############
                    if 2 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_B': base_counter_B / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_B': wd_counter_B / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_B': we_counter_B / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### C1 ##############
                    if 3 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_C1': base_counter_C1 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_C1': wd_counter_C1 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_C1': we_counter_C1 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                    ######### C2 ##############
                    if 4 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_C2': base_counter_C2 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_C2': wd_counter_C2 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_C2': we_counter_C2 / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })
                    ######### DE ##############
                    if 5 in self.sec.ids or 6 in self.sec.ids:
                        quarter_vals.update(
                            {'base_DE': base_counter_DE / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_day_DE': wd_counter_DE / number_of_total_quest * 100 if number_of_total_quest != 0 else 0,
                             'week_end_DE': we_counter_DE / number_of_total_quest * 100 if number_of_total_quest != 0 else 0
                             })

                self.env['a.quarter.total.sample'].create(quarter_vals)

    def thread_quarter_report(self, lines_groups, data_processing_base, total_record_data_processing):

        with api.Environment.manage():
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            self._thread_quarter_report(lines_groups, data_processing_base, total_record_data_processing)
            new_cr.commit()
            new_cr.close()
        return {}

    def get_report_name(self):
        if self.date_from and self.date_to:
            return _("Rating By Program (Quarter) From %s To %s") % (self.date_from, self.date_to)
        elif self.month_ids:
            months = ''
            for month in self.month_ids:
                months += str(month.name) + ','
            return _("Rating By Program (Quarter) for months %s") % (months)
        elif self.dates_ids:
            dates = ''
            for date in self.dates_ids:
                dates += str(date.date) + ','
            return _("Rating By Program (Quarter) for dates %s") % (dates)
        else:
            return ''

    def get_data_processing_base(self, date_domain, filtered):
        gender_domain = []
        region_domain = []
        age_domain = []
        sec_domain = []
        if filtered:
            ######## Male ##############
            if 1 in self.gender.ids or 3 in self.gender.ids:
                if gender_domain:
                    gender_domain = ['|', ('gender', '=', 'male')] + gender_domain
                else:
                    gender_domain += [('gender', '=', 'male')]

            ######## Female ##############
            if 2 in self.gender.ids or 3 in self.gender.ids:
                if gender_domain:
                    gender_domain = ['|', ('gender', '=', 'female')] + gender_domain
                else:
                    gender_domain += [('gender', '=', 'female')]

            ######## Cairo ##############
            if 1 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 1)] + region_domain
                else:
                    region_domain += [('region', '=', 1)]

            ######## Alex ##############
            if 2 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 2)] + region_domain
                else:
                    region_domain += [('region', '=', 2)]

            ######## Delta ##############
            if 3 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 3)] + region_domain
                else:
                    region_domain += [('region', '=', 3)]

            ######## UE ##############
            if 4 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 4)] + region_domain
                else:
                    region_domain += [('region', '=', 4)]

            ######## CR ##############
            if 5 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('region', '=', 5)] + region_domain
                else:
                    region_domain += [('region', '=', 5)]

            ######### 15 - 19 ##############
            if 1 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 1)] + age_domain
                else:
                    age_domain += [('age_range', '=', 1)]

            ######### 20 - 24 ##############
            if 2 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 2)] + age_domain
                else:
                    age_domain += [('age_range', '=', 2)]

            ######### 25 - 29 ##############
            if 3 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 3)] + age_domain
                else:
                    age_domain += [('age_range', '=', 3)]

            ######### 30 - 34 ##############
            if 4 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 4)] + age_domain
                else:
                    age_domain += [('age_range', '=', 4)]

            ######### 35 - 39 ##############
            if 5 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 5)] + age_domain
                else:
                    age_domain += [('age_range', '=', 5)]

            ######### 40 - 44 ##############
            if 6 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 6)] + age_domain
                else:
                    age_domain += [('age_range', '=', 6)]

            ######### 45 - 49 ##############
            if 7 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 7)] + age_domain
                else:
                    age_domain += [('age_range', '=', 7)]

            ######### 50 - 59 ##############
            if 8 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 8)] + age_domain
                else:
                    age_domain += [('age_range', '=', 8)]

            ######### More Than 59 ##############
            if 9 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('age_range', '=', 9)] + age_domain
                else:
                    age_domain += [('age_range', '=', 9)]

            ######### A ##############
            if 1 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'A')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'A')]

            ######### B ##############
            if 2 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'B')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'B')]

            ######### C1 ##############
            if 3 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'C1')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'C1')]

            ######### C2 ##############
            if 4 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'C2')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'C2')]

            ######### DE ##############
            if 5 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'DE')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'DE')]
            filtered_domain = ['&'] + gender_domain + ['&'] + region_domain + ['&'] + age_domain + \
                              ['&'] + sec_domain
            # print(filtered_domain)
            return self.env['a.data.processing'].search(filtered_domain + date_domain +
                                                        [('channel_lines', '!=', False),
                                                         ('stage_id', '=', 'approved')])
        else:
            return self.env['a.data.processing'].search(date_domain + [('channel_lines', '!=', False),
                                                                       ('stage_id', '=', 'approved')])

    def get_total_sample_count(self, date_domain, filtered):
        gender_domain = []
        region_domain = []
        age_domain = []
        sec_domain = []
        if filtered:
            ######## Male ##############
            if 1 in self.gender.ids or 3 in self.gender.ids:
                if gender_domain:
                    gender_domain = ['|', ('s4', '=', 'male')] + gender_domain
                else:
                    gender_domain += [('s4', '=', 'male')]

            ######## Female ##############
            if 2 in self.gender.ids or 3 in self.gender.ids:
                if gender_domain:
                    gender_domain = ['|', ('s4', '=', 'female')] + gender_domain
                else:
                    gender_domain += [('s4', '=', 'female')]

            ######## Cairo ##############
            if 1 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 1)] + region_domain
                else:
                    region_domain += [('sec6', '=', 1)]

            ######## Alex ##############
            if 2 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 2)] + region_domain
                else:
                    region_domain += [('sec6', '=', 2)]

            ######## Delta ##############
            if 3 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 3)] + region_domain
                else:
                    region_domain += [('sec6', '=', 3)]

            ######## UE ##############
            if 4 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 4)] + region_domain
                else:
                    region_domain += [('sec6', '=', 4)]

            ######## CR ##############
            if 5 in self.region.ids or 6 in self.region.ids:
                if region_domain:
                    region_domain = ['|', ('sec6', '=', 5)] + region_domain
                else:
                    region_domain += [('sec6', '=', 5)]

            ######### 15 - 19 ##############
            if 1 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 2)] + age_domain
                else:
                    age_domain += [('s3', '=', 2)]

            ######### 20 - 24 ##############
            if 2 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 3)] + age_domain
                else:
                    age_domain += [('s3', '=', 3)]

            ######### 25 - 29 ##############
            if 3 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 4)] + age_domain
                else:
                    age_domain += [('s3', '=', 4)]

            ######### 30 - 34 ##############
            if 4 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 5)] + age_domain
                else:
                    age_domain += [('s3', '=', 5)]

            ######### 35 - 39 ##############
            if 5 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 6)] + age_domain
                else:
                    age_domain += [('s3', '=', 6)]

            ######### 40 - 44 ##############
            if 6 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 7)] + age_domain
                else:
                    age_domain += [('s3', '=', 7)]

            ######### 45 - 49 ##############
            if 7 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 8)] + age_domain
                else:
                    age_domain += [('s3', '=', 8)]

            ######### 50 - 59 ##############
            if 8 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 9)] + age_domain
                else:
                    age_domain += [('s3', '=', 9)]

            ######### More Than 59 ##############
            if 9 in self.age.ids or 10 in self.age.ids:
                if age_domain:
                    age_domain = ['|', ('s3', '=', 10)] + age_domain
                else:
                    age_domain += [('s3', '=', 10)]

            ######### A ##############
            if 1 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'A')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'A')]

            ######### B ##############
            if 2 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'B')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'B')]

            ######### C1 ##############
            if 3 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'C1')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'C1')]

            ######### C2 ##############
            if 4 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'C2')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'C2')]

            ######### DE ##############
            if 5 in self.sec.ids or 6 in self.sec.ids:
                if sec_domain:
                    sec_domain = ['|', ('sec', '=', 'DE')] + sec_domain
                else:
                    sec_domain += [('sec', '=', 'DE')]
            filtered_domain = ['&'] + gender_domain + region_domain + ['&'] + age_domain + sec_domain
            # print(filtered_domain)
            return self.env['a.questionnaire'].search_count(filtered_domain + date_domain +
                                                            [('stage_id', '=', 'approved')])
        else:
            return self.env['a.questionnaire'].search_count(date_domain + [('stage_id', '=', 'approved')])

    def generate_quarter_report(self):
        date_domain = []
        if self.date_format == 'from_to':
            date_domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to)]
        elif self.date_format == 'days':
            date_domain.append(('date', 'in', self.dates_ids.mapped('date')))
        else:
            date_domain.append(('month', 'in', self.month_ids.mapped('code')))

        filtered = self.env.context.get('filtered', False)

        self.total_sample = self.get_total_sample_count(date_domain, filtered)

        self.wizard_date = self.get_report_name()

        data_processing_base = self.get_data_processing_base(date_domain, filtered)
        questionnaire_ids = data_processing_base.mapped('name')
        questionnaire_ids = questionnaire_ids.mapped('id')

        if data_processing_base:
            samples_per_day = ''' 
                select count(*) from a_questionnaire where id IN %s
            ''' % str(tuple(questionnaire_ids))

            self._cr.execute(samples_per_day)
            number_of_total_quest = self._cr.dictfetchall()
            number_of_total_quest = number_of_total_quest[0]['count'] if number_of_total_quest else 0

            self._cr.execute('DELETE FROM a_quarter_total_sample')

        if data_processing_base:
            channel_lines = data_processing_base.mapped('channel_lines').mapped('id')
            query = '''
                    SELECT period,program,time_from,time_to,header,
                    array_agg(id) as ids
                    FROM a_channel_lines 
                    WHERE id IN %s
                    GROUP BY period,program,time_from,time_to,header
                    ''' % str(tuple(channel_lines))

            self._cr.execute(query)
            groups = self._cr.dictfetchall()
            groups_ids = []
            for group in groups:
                groups_ids.append(group['ids'])
            line_groups = self.split_channel_lines(groups_ids, 10)
            created_threads = []
            start = time.time()
            for line_group in line_groups:
                self._thread_quarter_report(line_group, data_processing_base, number_of_total_quest)
            while any(x.is_alive() for x in created_threads):
                time.sleep(1)
            total_records = self.get_total_sample()
            self.create_total_report(total_records)
            end = time.time()
            print(f"Runtime of the program is {end - start}")
            return {
                'name': self.get_report_name(),
                'view_mode': 'tree,pivot',
                'res_model': 'a.quarter.total.sample',
                'view_ids': [(self.env.ref('media_tracking.quarter_list').id, 'list'),
                             (self.env.ref('media_tracking.quarter_view_pivot').id, 'pivot')],
                'target': 'current',
                'type': 'ir.actions.act_window', }
        else:
            raise UserError(
                _("No Records")
            )

    def get_total_sample(self) -> int:
        if self.env['a.wizard.quarter.total.sample'].search([]):
            total_sample = self.env['a.wizard.quarter.total.sample'].search([])[-1].total_sample
        else:
            return 0
        return total_sample

    def get_wizard_date(self):
        if self.env['a.wizard.quarter.total.sample'].search([]):
            wizard_date = self.env['a.wizard.quarter.total.sample'].search([])[-1].wizard_date
        else:
            return 'x'
        return wizard_date
