from odoo import models, fields, api


class ReachReportLine(models.Model):
    _name = 'reach.report.line'
    _description = 'Reach Report Line'

    channel_id = fields.Many2one(comodel_name="media.channel", string="Channel", required=False)
    program_id = fields.Many2one(comodel_name="a.programs", string="Program", required=False)
    time_from_id = fields.Many2one(comodel_name="a.time_from", string="From", required=False)
    time_to_id = fields.Many2one(comodel_name="a.time_from", string="To", required=False)
    report_id = fields.Many2one(comodel_name="reach.report", string="Report", required=False)
    frequency = fields.Float(string="Frequency")
    brand = fields.Char(string="Brand")

    def get_avg_rating(self):
        for rec in self:
            total_rec = self.env['a.full'].search([('programs_id', '=', rec.program_id.id),
                                                   ('media_channel_id', '=', rec.channel_id.id),
                                                   ('time_from', '=', rec.time_from_id.id),
                                                   ('time_to', '=', rec.time_to_id.id)], limit=1)
            avg_rating = total_rec.avg_rate if total_rec else 0
            rec.avg_rating = avg_rating

    avg_rating = fields.Float(string='AVG Rating', default=0)

    @api.depends('frequency', 'avg_rating')
    def get_line_grp(self):
        for rec in self:
            rec.grp = rec.frequency * rec.avg_rating

    grp = fields.Float(string="GRP", compute='get_line_grp')

    @api.depends('channel_id', 'program_id', 'time_from_id', 'time_to_id',
                 'report_id.age_ids', 'report_id.gender_ids', 'report_id.sec_ids', 'report_id.region_ids')
    def get_line_reach(self):
        for rec in self:
            gender_ids = rec.report_id.gender_ids.ids
            age_ids = rec.report_id.age_ids.ids
            sec_ids = rec.report_id.sec_ids.ids
            region_ids = rec.report_id.region_ids.ids
            filtered_domain = rec.report_id.get_total_sample_domain(gender_ids, region_ids, age_ids, sec_ids)
            # domain = filtered_domain + [('date', '>=', rec.report_id.date_from),
            #                             ('date', '<=', rec.report_id.date_to),
            #                             ('stage_id', '<=', 'approved')]

            domain = filtered_domain + [('date', '>=', rec.report_id.date_from),
                                        ('date', '<=', rec.report_id.date_to),
                                        ('media_channel_id', '=', rec.channel_id.id),
                                        ('programs_id', '=', rec.program_id.id),
                                        ('time_from.seq', '>=', rec.time_from_id.seq),
                                        # ('time_from.seq', '<=', rec.time_to_id.seq),
                                        # ('time_to.seq', '>=', rec.time_from_id.seq),
                                        ('time_to.seq', '<=', rec.time_to_id.seq),
                                        ('stage_id', '<=', 'approved'),
                                        ]
            dates_program_mentioned = list(set(self.env['a.data.processing'].search(domain).mapped('date')))
            print(len(dates_program_mentioned))
            total_sample = len(self.env['a.data.processing'].read_group([
                ('date', 'in', dates_program_mentioned)], ['name'], ['name']))
            # total_sample = self.env['a.questionnaire'].search_count([('call_date', 'in', dates_program_mentioned)])
            # questionnaires = self.env['a.data.processing'].read_group(domain, ['date'], ['date:day'])
            # total_sample = len(questionnaires)
            # total_sample = 0
            # for quest in questionnaires:
            #     total_sample += quest.get('date_count', 0)
            print('Sample Domain', domain)
            sample = len(self.env['a.data.processing'].read_group(domain, ['name'], ['name']))
            # print('total_sample', total_sample)
            # print('sample', len(sample))

            rec.sample = sample
            rec.total_sample = total_sample
            rec.reach = sample / total_sample * 100 if total_sample != 0 else 0

    reach = fields.Float(string="Reach", compute='get_line_reach')
    sample = fields.Float(string="Sample", compute='get_line_reach')
    total_sample = fields.Float(string="Total Sample", compute='get_line_reach')

    @api.onchange('channel_id')
    def _onchange_channel_id(self):
        program_lines = self.env['a.program.line'].search([('media_channel_id', '=', self.channel_id.id)])
        program_ids = program_lines.mapped('program_id').ids
        return {'domain': {'program_id': [('id', 'in', program_ids)]}}

    @api.onchange('program_id')
    def _onchange_program_id(self):
        program_lines = self.env['a.program.line'].search([('program_id', '=', self.program_id.id)])
        time_from_ids = program_lines.mapped('date_from_id').ids
        time_to_ids = program_lines.mapped('date_to_id').ids
        return {'domain': {'time_from_id': [('id', 'in', time_from_ids)],
                           'time_to_id': [('id', 'in', time_to_ids)]
                           }
                }


class ReachReport(models.Model):
    _name = 'reach.report'
    _rec_name = 'name'
    _description = 'Reach Report'

    ################################################################################
    @api.model
    def get_total_sample_domain(self, genders, regions, ages, secs):
        gender_domain = []
        region_domain = []
        age_domain = []
        sec_domain = []

        ######## Male ##############
        if 1 in genders or 3 in genders:
            if gender_domain:
                gender_domain = ['|', ('gender', '=', 'male')] + gender_domain
            else:
                gender_domain += [('gender', '=', 'male')]

        ######## Female ##############
        if 2 in genders or 3 in genders:
            if gender_domain:
                gender_domain = ['|', ('gender', '=', 'female')] + gender_domain
            else:
                gender_domain += [('gender', '=', 'female')]

        ######## Cairo ##############
        if 1 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 1)] + region_domain
            else:
                region_domain += [('region', '=', 1)]

        ######## Alex ##############
        if 2 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 2)] + region_domain
            else:
                region_domain += [('region', '=', 2)]

        ######## Delta ##############
        if 3 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 3)] + region_domain
            else:
                region_domain += [('region', '=', 3)]

        ######## UE ##############
        if 4 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 4)] + region_domain
            else:
                region_domain += [('region', '=', 4)]

        ######## CR ##############
        if 5 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 5)] + region_domain
            else:
                region_domain += [('region', '=', 5)]

        ######### 15 - 19 ##############
        if 1 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 2)] + age_domain
            else:
                age_domain += [('age_range', '=', 2)]

        ######### 20 - 24 ##############
        if 2 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 3)] + age_domain
            else:
                age_domain += [('age_range', '=', 3)]

        ######### 25 - 29 ##############
        if 3 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 4)] + age_domain
            else:
                age_domain += [('age_range', '=', 4)]

        ######### 30 - 34 ##############
        if 4 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 5)] + age_domain
            else:
                age_domain += [('age_range', '=', 5)]

        ######### 35 - 39 ##############
        if 5 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 6)] + age_domain
            else:
                age_domain += [('age_range', '=', 6)]

        ######### 40 - 44 ##############
        if 6 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 7)] + age_domain
            else:
                age_domain += [('age_range', '=', 7)]

        ######### 45 - 49 ##############
        if 7 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 8)] + age_domain
            else:
                age_domain += [('age_range', '=', 8)]

        ######### 50 - 59 ##############
        if 8 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 9)] + age_domain
            else:
                age_domain += [('age_range', '=', 9)]

        ######### More Than 59 ##############
        if 9 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 10)] + age_domain
            else:
                age_domain += [('age_range', '=', 10)]

        ######### A ##############
        if 1 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'A')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'A')]

        ######### B ##############
        if 2 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'B')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'B')]

        ######### C1 ##############
        if 3 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'C1')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'C1')]

        ######### C2 ##############
        if 4 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'C2')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'C2')]

        ######### DE ##############
        if 5 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'DE')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'DE')]
        filtered_domain = ['&'] + gender_domain + region_domain + ['&'] + age_domain + sec_domain
        # filtered_domain = gender_domain + region_domain + age_domain + sec_domain
        # print(filtered_domain)
        return filtered_domain

    ########################################################################

    def compute_line_avg_rating(self):
        for rec in self:
            for line in rec.report_line_ids:
                line.get_avg_rating()

    @api.depends('date_from', 'date_to')
    def get_report_name(self):
        for rec in self:
            rec.name = str(rec.date_from) + ' - ' + str(rec.date_to)

    name = fields.Char(compute='get_report_name')
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    report_line_ids = fields.One2many(comodel_name="reach.report.line", inverse_name="report_id", string="Report Lines",
                                      required=False)

    age_ids = fields.Many2many(comodel_name="age.data", string='Ages')
    gender_ids = fields.Many2many(comodel_name="gender.data", string='Genders')
    sec_ids = fields.Many2many(comodel_name="sec.data", string='Sections')
    region_ids = fields.Many2many(comodel_name="region.data", string='Regions')

    #TODO:fixed issue
    # @api.depends('date_from', 'date_to', 'report_line_ids')
    # def get_reach_percentage(self):
    #     for rec in self:
    #         gender_ids = rec.gender_ids.ids
    #         age_ids = rec.age_ids.ids
    #         sec_ids = rec.sec_ids.ids
    #         region_ids = rec.region_ids.ids
    #         filtered_domain = rec.get_total_sample_domain(gender_ids, region_ids, age_ids, sec_ids)
    #         domain = filtered_domain + [('date', '>=', rec.date_from),
    #                                     ('date', '<=', rec.date_to),
    #                                     ('stage_id', '<=', 'approved')]
    #         questionnaires = self.env['a.data.processing'].read_group(domain, ['name'], ['name'])
    #         # print(len(questionnaires))
    #         total_sample = len(questionnaires)
    #         reach_sample = 0
    #         for line in rec.report_line_ids:
    #             domain = filtered_domain + [
    #                 # ('date', '>=', rec.date_from),
    #                 # ('date', '<=', rec.date_to),
    #                 ('media_channel_id', '=', line.channel_id.id),
    #                 ('programs_id', '=', line.program_id.id),
    #                 ('time_from.seq', '>=', line.time_from_id.seq),
    #                 ('time_from.seq', '<=', line.time_to_id.seq),
    #                 ('time_to.seq', '>=', line.time_from_id.seq),
    #                 ('time_to.seq', '<=', line.time_to_id.seq),
    #                 ('stage_id', '<=', 'approved'),
    #             ]
    #             sample = self.env['a.data.processing'].read_group(domain, ['name'], ['name'])
    #             reach_sample += len(sample)
    #             # print(sample)
    #         # print(reach_sample)
    #         rec.reach_percentage = reach_sample / total_sample * 100 if total_sample != 0 else 0

    @api.depends('report_line_ids')
    def get_reach_percentage(self):
        def get_line_domain(domain, line):
            line_domain = ['&', '&', '&',
                           ('media_channel_id', '=', line.channel_id.id),
                           ('programs_id', '=', line.program_id.id),
                           ('time_from.seq', '>=', line.time_from_id.seq),
                           ('time_to.seq', '<=', line.time_to_id.seq)
                           ]
            if domain != []:
                domain.insert(0, '|')
            domain += line_domain
            return domain
        for rec in self:
            gender_ids = rec.gender_ids.ids
            age_ids = rec.age_ids.ids
            sec_ids = rec.sec_ids.ids
            region_ids = rec.region_ids.ids
            filtered_domain = rec.get_total_sample_domain(gender_ids, region_ids, age_ids, sec_ids)
            filtered_domain += [
                ('stage_id', '<=', 'approved'),
                ('date', '>=', rec.date_from),
                ('date', '<=', rec.date_to)
            ]
            # filtered_domain += report_domain
            domain = []
            # questionnaires = self.env['a.data.processing'].read_group(report_domain, ['name'], ['name'])
            # total_sample = len(questionnaires)
            for line in rec.report_line_ids:
                domain = get_line_domain(domain, line)
            print('Domain', domain)
            domain += filtered_domain
            dates_program_mentioned = list(set(self.env['a.data.processing'].search(domain).mapped('date')))
            total_sample = len(self.env['a.data.processing'].read_group([
                ('date', 'in', dates_program_mentioned)], ['name'], ['name']))
            print('Report Sample Domain', domain)
            sample = len(self.env['a.data.processing'].read_group(domain, ['name'], ['name']))
            print('sample', sample, 'total_sample', total_sample)
            rec.reach_percentage = sample / total_sample * 100 if total_sample != 0 else 0

        # def get_line_reach(rec, line):
        #     gender_ids = rec.gender_ids.ids
        #     age_ids = rec.age_ids.ids
        #     sec_ids = rec.sec_ids.ids
        #     region_ids = rec.region_ids.ids
        #     filtered_domain = rec.get_total_sample_domain(gender_ids, region_ids, age_ids, sec_ids)
        #     domain = filtered_domain + [('date', '>=', rec.date_from),
        #                                 ('date', '<=', rec.date_to),
        #                                 ('media_channel_id', '=', line.channel_id.id),
        #                                 ('programs_id', '=', line.program_id.id),
        #                                 ('time_from.seq', '>=', line.time_from_id.seq),
        #                                 ('time_to.seq', '<=', line.time_to_id.seq),
        #                                 ('stage_id', '<=', 'approved'),
        #                                 ]
        #     dates_program_mentioned = list(set(rec.env['a.data.processing'].search(domain).mapped('date')))
        #     print(len(dates_program_mentioned))
        #     total_sample = len(rec.env['a.data.processing'].read_group([
        #         ('date', 'in', dates_program_mentioned)], ['name'], ['name']))
        #
        #     sample = len(rec.env['a.data.processing'].read_group(domain, ['name'], ['name']))
        #     return sample / total_sample * 100 if total_sample != 0 else 0

        # for rec in self:
        #     reach_percentage = 0
        #     for line in rec.report_line_ids:
        #         reach_percentage += get_line_reach(rec, line)
        #     rec.reach_percentage = reach_percentage

    reach_percentage = fields.Float(string="Reach Percentage %", compute='get_reach_percentage')


class TotalSampleReachReportLine(models.Model):
    _name = 'total.sample.reach.report.line'
    _description = 'Total Sample Reach Report Line'

    channel_id = fields.Many2one(comodel_name="media.channel", string="Channel", required=False)
    program_id = fields.Many2one(comodel_name="a.programs", string="Program", required=False)
    time_from_id = fields.Many2one(comodel_name="a.time_from", string="From", required=False)
    time_to_id = fields.Many2one(comodel_name="a.time_from", string="To", required=False)
    report_id = fields.Many2one(comodel_name="total.sample.reach.report", string="Report", required=False)
    frequency = fields.Float(string="Frequency")
    brand = fields.Char(string="Brand")

    def get_avg_rating(self):
        for rec in self:
            total_rec = self.env['a.full.total.sample'].search([('programs_id', '=', rec.program_id.id),
                                                                ('media_channel_id', '=', rec.channel_id.id),
                                                                ('time_from', '=', rec.time_from_id.id),
                                                                ('time_to', '=', rec.time_to_id.id)], limit=1)
            avg_rating = total_rec.avg_rate if total_rec else 0
            rec.avg_rating = avg_rating

    avg_rating = fields.Float(string='AVG Rating', default=0)

    @api.depends('frequency', 'avg_rating')
    def get_line_grp(self):
        for rec in self:
            rec.grp = rec.frequency * rec.avg_rating

    grp = fields.Float(string="GRP", compute='get_line_grp')

    @api.depends('channel_id', 'program_id', 'time_from_id', 'time_to_id',
                 'report_id.age_ids', 'report_id.gender_ids', 'report_id.sec_ids', 'report_id.region_ids')
    def get_line_reach(self):
        for rec in self:
            gender_ids = rec.report_id.gender_ids.ids
            age_ids = rec.report_id.age_ids.ids
            sec_ids = rec.report_id.sec_ids.ids
            region_ids = rec.report_id.region_ids.ids
            filtered_domain = rec.report_id.get_total_sample_domain(gender_ids, region_ids, age_ids, sec_ids)
            # domain = filtered_domain + [('date', '>=', rec.report_id.date_from),
            #                             ('date', '<=', rec.report_id.date_to),
            #                             ('stage_id', '<=', 'approved')]

            domain = filtered_domain + [('date', '>=', rec.report_id.date_from),
                                        ('date', '<=', rec.report_id.date_to),
                                        ('media_channel_id', '=', rec.channel_id.id),
                                        ('programs_id', '=', rec.program_id.id),
                                        ('time_from.seq', '>=', rec.time_from_id.seq),
                                        # ('time_from.seq', '<=', rec.time_to_id.seq),
                                        # ('time_to.seq', '>=', rec.time_from_id.seq),
                                        ('time_to.seq', '<=', rec.time_to_id.seq),
                                        ('stage_id', '<=', 'approved'),
                                        ]
            dates_program_mentioned = list(set(self.env['a.data.processing'].search(domain).mapped('date')))
            print(len(dates_program_mentioned))
            total_sample = len(self.env['a.data.processing'].read_group([
                ('date', 'in', dates_program_mentioned)], ['name'], ['name']))
            # total_sample = self.env['a.questionnaire'].search_count([('call_date', 'in', dates_program_mentioned)])
            # questionnaires = self.env['a.data.processing'].read_group(domain, ['date'], ['date:day'])
            # total_sample = len(questionnaires)
            # total_sample = 0
            # for quest in questionnaires:
            #     total_sample += quest.get('date_count', 0)
            print('Sample Domain', domain)
            sample = len(self.env['a.data.processing'].read_group(domain, ['name'], ['name']))
            # print('total_sample', total_sample)
            # print('sample', len(sample))

            rec.sample = sample
            rec.total_sample = total_sample
            rec.reach = sample / total_sample * 100 if total_sample != 0 else 0

    reach = fields.Float(string="Reach", compute='get_line_reach')
    sample = fields.Float(string="Sample", compute='get_line_reach')
    total_sample = fields.Float(string="Total Sample", compute='get_line_reach')

    @api.onchange('channel_id')
    def _onchange_channel_id(self):
        program_lines = self.env['a.program.line'].search([('media_channel_id', '=', self.channel_id.id)])
        program_ids = program_lines.mapped('program_id').ids
        return {'domain': {'program_id': [('id', 'in', program_ids)]}}

    @api.onchange('program_id')
    def _onchange_program_id(self):
        program_lines = self.env['a.program.line'].search([('program_id', '=', self.program_id.id)])
        time_from_ids = program_lines.mapped('date_from_id').ids
        time_to_ids = program_lines.mapped('date_to_id').ids
        return {'domain': {'time_from_id': [('id', 'in', time_from_ids)],
                           'time_to_id': [('id', 'in', time_to_ids)]
                           }
                }


class TotalSampleReachReport(models.Model):
    _name = 'total.sample.reach.report'
    _rec_name = 'name'
    _description = 'Total Sample Reach Report'

    ################################################################################
    @api.model
    def get_total_sample_domain(self, genders, regions, ages, secs):
        gender_domain = []
        region_domain = []
        age_domain = []
        sec_domain = []

        ######## Male ##############
        if 1 in genders or 3 in genders:
            if gender_domain:
                gender_domain = ['|', ('gender', '=', 'male')] + gender_domain
            else:
                gender_domain += [('gender', '=', 'male')]

        ######## Female ##############
        if 2 in genders or 3 in genders:
            if gender_domain:
                gender_domain = ['|', ('gender', '=', 'female')] + gender_domain
            else:
                gender_domain += [('gender', '=', 'female')]

        ######## Cairo ##############
        if 1 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 1)] + region_domain
            else:
                region_domain += [('region', '=', 1)]

        ######## Alex ##############
        if 2 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 2)] + region_domain
            else:
                region_domain += [('region', '=', 2)]

        ######## Delta ##############
        if 3 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 3)] + region_domain
            else:
                region_domain += [('region', '=', 3)]

        ######## UE ##############
        if 4 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 4)] + region_domain
            else:
                region_domain += [('region', '=', 4)]

        ######## CR ##############
        if 5 in regions or 6 in regions:
            if region_domain:
                region_domain = ['|', ('region', '=', 5)] + region_domain
            else:
                region_domain += [('region', '=', 5)]

        ######### 15 - 19 ##############
        if 1 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 2)] + age_domain
            else:
                age_domain += [('age_range', '=', 2)]

        ######### 20 - 24 ##############
        if 2 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 3)] + age_domain
            else:
                age_domain += [('age_range', '=', 3)]

        ######### 25 - 29 ##############
        if 3 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 4)] + age_domain
            else:
                age_domain += [('age_range', '=', 4)]

        ######### 30 - 34 ##############
        if 4 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 5)] + age_domain
            else:
                age_domain += [('age_range', '=', 5)]

        ######### 35 - 39 ##############
        if 5 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 6)] + age_domain
            else:
                age_domain += [('age_range', '=', 6)]

        ######### 40 - 44 ##############
        if 6 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 7)] + age_domain
            else:
                age_domain += [('age_range', '=', 7)]

        ######### 45 - 49 ##############
        if 7 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 8)] + age_domain
            else:
                age_domain += [('age_range', '=', 8)]

        ######### 50 - 59 ##############
        if 8 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 9)] + age_domain
            else:
                age_domain += [('age_range', '=', 9)]

        ######### More Than 59 ##############
        if 9 in ages or 10 in ages:
            if age_domain:
                age_domain = ['|', ('age_range', '=', 10)] + age_domain
            else:
                age_domain += [('age_range', '=', 10)]

        ######### A ##############
        if 1 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'A')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'A')]

        ######### B ##############
        if 2 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'B')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'B')]

        ######### C1 ##############
        if 3 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'C1')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'C1')]

        ######### C2 ##############
        if 4 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'C2')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'C2')]

        ######### DE ##############
        if 5 in secs or 6 in secs:
            if sec_domain:
                sec_domain = ['|', ('sec', '=', 'DE')] + sec_domain
            else:
                sec_domain += [('sec', '=', 'DE')]
        filtered_domain = ['&'] + gender_domain + region_domain + ['&'] + age_domain + sec_domain
        # filtered_domain = gender_domain + region_domain + age_domain + sec_domain
        # print(filtered_domain)
        return filtered_domain

    ########################################################################

    def compute_line_avg_rating(self):
        for rec in self:
            for line in rec.report_line_ids:
                line.get_avg_rating()

    @api.depends('date_from', 'date_to')
    def get_report_name(self):
        for rec in self:
            rec.name = str(rec.date_from) + ' - ' + str(rec.date_to)

    name = fields.Char(compute='get_report_name')
    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    report_line_ids = fields.One2many(comodel_name="total.sample.reach.report.line",
                                      inverse_name="report_id", string="Report Lines",
                                      required=False)

    age_ids = fields.Many2many(comodel_name="age.data", string='Ages')
    gender_ids = fields.Many2many(comodel_name="gender.data", string='Genders')
    sec_ids = fields.Many2many(comodel_name="sec.data", string='Sections')
    region_ids = fields.Many2many(comodel_name="region.data", string='Regions')

    #TODO:fixed issue
    # @api.depends('date_from', 'date_to', 'report_line_ids')
    # def get_reach_percentage(self):
    #     for rec in self:
    #         gender_ids = rec.gender_ids.ids
    #         age_ids = rec.age_ids.ids
    #         sec_ids = rec.sec_ids.ids
    #         region_ids = rec.region_ids.ids
    #         filtered_domain = rec.get_total_sample_domain(gender_ids, region_ids, age_ids, sec_ids)
    #         domain = filtered_domain + [('date', '>=', rec.date_from),
    #                                     ('date', '<=', rec.date_to),
    #                                     ('stage_id', '<=', 'approved')]
    #         questionnaires = self.env['a.data.processing'].read_group(domain, ['name'], ['name'])
    #         # print(len(questionnaires))
    #         total_sample = len(questionnaires)
    #         reach_sample = 0
    #         for line in rec.report_line_ids:
    #             domain = filtered_domain + [
    #                 # ('date', '>=', rec.date_from),
    #                 # ('date', '<=', rec.date_to),
    #                 ('media_channel_id', '=', line.channel_id.id),
    #                 ('programs_id', '=', line.program_id.id),
    #                 ('time_from.seq', '>=', line.time_from_id.seq),
    #                 ('time_from.seq', '<=', line.time_to_id.seq),
    #                 ('time_to.seq', '>=', line.time_from_id.seq),
    #                 ('time_to.seq', '<=', line.time_to_id.seq),
    #                 ('stage_id', '<=', 'approved'),
    #             ]
    #             sample = self.env['a.data.processing'].read_group(domain, ['name'], ['name'])
    #             reach_sample += len(sample)
    #             # print(sample)
    #         # print(reach_sample)
    #         rec.reach_percentage = reach_sample / total_sample * 100 if total_sample != 0 else 0

    @api.depends('report_line_ids')
    def get_reach_percentage(self):
        def get_line_domain(domain, line):
            line_domain = ['&', '&', '&',
                           ('media_channel_id', '=', line.channel_id.id),
                           ('programs_id', '=', line.program_id.id),
                           ('time_from.seq', '>=', line.time_from_id.seq),
                           ('time_to.seq', '<=', line.time_to_id.seq)
                           ]
            if domain != []:
                domain.insert(0, '|')
            domain += line_domain
            return domain
        for rec in self:
            gender_ids = rec.gender_ids.ids
            age_ids = rec.age_ids.ids
            sec_ids = rec.sec_ids.ids
            region_ids = rec.region_ids.ids
            filtered_domain = rec.get_total_sample_domain(gender_ids, region_ids, age_ids, sec_ids)
            filtered_domain += [
                ('stage_id', '<=', 'approved'),
                ('date', '>=', rec.date_from),
                ('date', '<=', rec.date_to)
            ]
            # filtered_domain += report_domain
            domain = []
            # questionnaires = self.env['a.data.processing'].read_group(report_domain, ['name'], ['name'])
            # total_sample = len(questionnaires)
            for line in rec.report_line_ids:
                domain = get_line_domain(domain, line)
            print('Domain', domain)
            domain += filtered_domain
            dates_program_mentioned = list(set(self.env['a.data.processing'].search(domain).mapped('date')))
            total_sample = len(self.env['a.data.processing'].read_group([
                ('date', 'in', dates_program_mentioned)], ['name'], ['name']))
            print('Report Sample Domain', domain)
            sample = len(self.env['a.data.processing'].read_group(domain, ['name'], ['name']))
            print('sample', sample, 'total_sample', total_sample)
            rec.reach_percentage = sample / total_sample * 100 if total_sample != 0 else 0

        # def get_line_reach(rec, line):
        #     gender_ids = rec.gender_ids.ids
        #     age_ids = rec.age_ids.ids
        #     sec_ids = rec.sec_ids.ids
        #     region_ids = rec.region_ids.ids
        #     filtered_domain = rec.get_total_sample_domain(gender_ids, region_ids, age_ids, sec_ids)
        #     domain = filtered_domain + [('date', '>=', rec.date_from),
        #                                 ('date', '<=', rec.date_to),
        #                                 ('media_channel_id', '=', line.channel_id.id),
        #                                 ('programs_id', '=', line.program_id.id),
        #                                 ('time_from.seq', '>=', line.time_from_id.seq),
        #                                 ('time_to.seq', '<=', line.time_to_id.seq),
        #                                 ('stage_id', '<=', 'approved'),
        #                                 ]
        #     dates_program_mentioned = list(set(rec.env['a.data.processing'].search(domain).mapped('date')))
        #     print(len(dates_program_mentioned))
        #     total_sample = len(rec.env['a.data.processing'].read_group([
        #         ('date', 'in', dates_program_mentioned)], ['name'], ['name']))
        #
        #     sample = len(rec.env['a.data.processing'].read_group(domain, ['name'], ['name']))
        #     return sample / total_sample * 100 if total_sample != 0 else 0

        # for rec in self:
        #     reach_percentage = 0
        #     for line in rec.report_line_ids:
        #         reach_percentage += get_line_reach(rec, line)
        #     rec.reach_percentage = reach_percentage

    reach_percentage = fields.Float(string="Reach Percentage %", compute='get_reach_percentage')


