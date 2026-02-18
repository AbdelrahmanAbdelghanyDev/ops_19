from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError


class WizardInternet(models.TransientModel):
    _name = 'a.wizard.internet'
    _description = 'Internet Wizard'

    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')

    def generate_internet_report(self):
        # query = '''
        # select n1,count(*)::float  as base,
        #
        # count(case s4 when 'male' then 1 else null end)::float  as male_base,
        # ROUND((count(case s4 when 'male' then 1 else null end)::float/count(*)::float)*100) as male_precent,
        #
        # count(case s4 when 'female' then 1 else null end)::float  as female_base,
        # ROUND((count(case s4 when 'female' then 1 else null end)::float/count(*)::float)*100) as female_percent,
        #
        # count(case sec6 when '1' then 1 else null end)::float  as cairo_base,
        # ROUND((count(case sec6 when '1' then 1 else null end)::float/count(*)::float)*100) as alex_percent,
        #
        # count(case sec6 when '2' then 1 else null end)::float  as alex_base,
        # ROUND((count(case sec6 when '3' then 1 else null end)::float/count(*)::float)*100) as alex_percent,
        #
        # count(case sec6 when '3' then 1 else null end)::float  as delta_base,
        # ROUND((count(case sec6 when '3' then 1 else null end)::float/count(*)::float)*100) as delta_percent,
        #
        # count(case sec6 when '4' then 1 else null end)::float  as ue_base,
        # ROUND((count(case sec6 when '4' then 1 else null end)::float/count(*)::float)*100) as ue_percent,
        #
        # count(case sec6 when '5' then 1 else null end)::float  as c_r_base,
        # ROUND((count(case sec6 when '5' then 1 else null end)::float/count(*)::float)*100) as c_r_percent
        #
        # from a_questionnaire Group By n1;
        # '''
        questionnaire = self.env['a.questionnaire']
        internet = self.env['a.internet.n1']
        internet_n2 = self.env['a.internet.n2']
        internet_n3 = self.env['a.internet.n3']
        internet_n4 = self.env['a.internet.n4']
        internet.search([]).unlink()
        internet_n2.search([]).unlink()
        internet_n3.search([]).unlink()
        internet_n4.search([]).unlink()
        if questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to)]):
            internet_base = internet.create({
                'n1': 'Base',
                'base': len(questionnaire.search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_percent': 100,
                'base_male': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s4', '=', 'male')])),
                'base_male_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('s4', '=', 'male')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_female': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s4', '=', 'female')])),
                'base_female_percent': round(100 * len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s4', '=', 'female')])) / len(
                    questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                          ('stage_id', '=', 'approved')]))),

                'base_2': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '2')])),
                'base_2_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('s3', '=', '2')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_3': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '3')])),
                'base_3_percent': round(100 * len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '3')])) / len(
                    questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                          ('stage_id', '=', 'approved')]))),
                'base_4': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '4')])),
                'base_4_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('s3', '=', '4')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_5': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '5')])),
                'base_5_percent': round(100 * len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '5')])) / len(
                    questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                          ('stage_id', '=', 'approved')]))),
                'base_6': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '6')])),
                'base_6_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('s3', '=', '6')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_7': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '7')])),
                'base_7_percent': round(100 * len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '7')])) / len(
                    questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                          ('stage_id', '=', 'approved')]))),
                'base_8': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '8')])),
                'base_8_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('s3', '=', '8')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_9': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '9')])),
                'base_9_percent': round(100 * len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '9')])) / len(
                    questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                          ('stage_id', '=', 'approved')]))),
                'base_10': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('s3', '=', '10')])),
                'base_10_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('s3', '=', '10')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),

                'base_cairo': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec6', '=', '1')])),
                'base_cairo_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec6', '=', '1')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_alex': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec6', '=', '2')])),
                'base_alex_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec6', '=', '2')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_delta': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec6', '=', '3')])),
                'base_delta_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec6', '=', '3')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_ue': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec6', '=', '4')])),
                'base_ue_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec6', '=', '4')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),
                'base_c_r': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec6', '=', '5')])),
                'base_c_r_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec6', '=', '5')])) / len(questionnaire.search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to),
                         ('stage_id', '=', 'approved')]))),

                'base_a': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec', '=', 'A')])),
                'base_a_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec', '=', 'A')])) / len(
                        questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                              ('stage_id', '=', 'approved')]))),
                'base_b': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec', '=', 'B')])),
                'base_b_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec', '=', 'B')])) / len(
                        questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                              ('stage_id', '=', 'approved')]))),
                'base_c1': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec', '=', 'C1')])),
                'base_c1_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec', '=', 'C1')])) / len(
                        questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                              ('stage_id', '=', 'approved')]))),
                'base_c2': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec', '=', 'C2')])),
                'base_c2_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec', '=', 'C2')])) / len(
                        questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                              ('stage_id', '=', 'approved')]))),
                'base_de': len(self.env['a.questionnaire'].search(
                    [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                     ('sec', '=', 'DE')])),
                'base_de_percent': round(
                    100 * len(self.env['a.questionnaire'].search(
                        [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved'),
                         ('sec', '=', 'DE')])) / len(
                        questionnaire.search([('date', '>=', self.date_from), ('date', '<=', self.date_to),
                                              ('stage_id', '=', 'approved')]))),

            })

            query = '''
            INSERT INTO a_internet_n1 (n1,base,base_percent,base_male,base_male_percent,base_female,base_female_percent
            
            ,base_2,base_2_percent,base_3,base_3_percent,base_4,base_4_percent,base_5,base_5_percent
            ,base_6,base_6_percent,base_7,base_7_percent,base_8,base_8_percent,base_9,base_9_percent
            ,base_10,base_10_percent,
            
            base_cairo,base_cairo_percent,base_alex,base_alex_percent,base_delta,base_delta_percent,base_ue,base_ue_percent
            ,base_c_r,base_c_r_percent,
            
            base_a,base_a_percent,base_b,base_b_percent,base_c1,base_c1_percent,base_c2,base_c2_percent,base_de,base_de_percent) 
            
            select n1_name,
            count(*)::float,
            ROUND(100 * count(*)::float/%s),
            
            count(case a_questionnaire.s4 when 'male' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s4 when 'male' then 1 else null end)::float/%s)*100),
            count(case a_questionnaire.s4 when 'female' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s4 when 'female' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.s3 when '2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '3' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '3' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '4' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '4' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '5' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '5' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '6' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '6' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '7' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '7' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '8' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '8' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '9' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '9' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '10' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '10' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.sec6 when '1' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '1' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '3' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '3' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '4' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '4' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '5' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '5' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.sec when 'A' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'A' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'B' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'B' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'C1' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'C1' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'C2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'C2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'DE' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'DE' then 1 else null end)::float/%s::float)*100)
    
            from a_questionnaire where (('%s' <= date) AND (date <= '%s') AND (stage_id = 'approved')) Group By n1_name ;
            ''' % (len(questionnaire.search(
                [('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                   internet_base.base_male if internet_base.base_male != 0 else 1,
                   internet_base.base_female if internet_base.base_female != 0 else 1,

                   internet_base.base_2 if internet_base.base_2 != 0 else 1,
                   internet_base.base_3 if internet_base.base_3 != 0 else 1,
                   internet_base.base_4 if internet_base.base_4 != 0 else 1,
                   internet_base.base_5 if internet_base.base_5 != 0 else 1,
                   internet_base.base_6 if internet_base.base_6 != 0 else 1,
                   internet_base.base_7 if internet_base.base_7 != 0 else 1,
                   internet_base.base_8 if internet_base.base_8 != 0 else 1,
                   internet_base.base_9 if internet_base.base_9 != 0 else 1,
                   internet_base.base_10 if internet_base.base_10 != 0 else 1,

                   internet_base.base_cairo if internet_base.base_cairo != 0 else 1,
                   internet_base.base_alex if internet_base.base_alex != 0 else 1,
                   internet_base.base_delta if internet_base.base_delta != 0 else 1,
                   internet_base.base_ue if internet_base.base_ue != 0 else 1,
                   internet_base.base_c_r if internet_base.base_c_r != 0 else 1,

                   internet_base.base_a if internet_base.base_a != 0 else 1,
                   internet_base.base_b if internet_base.base_b != 0 else 1,
                   internet_base.base_c1 if internet_base.base_c1 != 0 else 1,
                   internet_base.base_c2 if internet_base.base_c2 != 0 else 1,
                   internet_base.base_de if internet_base.base_de != 0 else 1,
                   self.date_from, self.date_to)

            internet_base_n2 = internet_n2.create({
                'n2': 'Base',
                'base': len(questionnaire.search(
                    [('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
                     ('stage_id', '=', 'approved')])),
                'base_percent': 100,
                'base_male': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s4', '=', 'male'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_male_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s4', '=', 'male'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                     len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                               ('date', '<=', self.date_to),
                                                               ('stage_id', '=', 'approved')])),
                'base_female': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s4', '=', 'female'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_female_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s4', '=', 'female'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                       len(questionnaire.search(
                                           [('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                            ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),

                'base_2': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_2_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_3': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '3'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_3_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '3'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_4': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '4'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_4_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '4'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_5': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '5'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_5_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '5'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_6': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '6'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_6_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '6'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_7': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '7'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_7_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '7'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_8': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '8'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_8_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '8'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_9': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '9'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_9_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '9'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_10': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '10'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_10_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('s3', '=', '10'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                   len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                             ('date', '<=', self.date_to),
                                                             ('stage_id', '=', 'approved')])),

                'base_cairo': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '1'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_cairo_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '1'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                      len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                                ('date', '<=', self.date_to),
                                                                ('stage_id', '=', 'approved')])),
                'base_alex': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_alex_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                     len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                               ('date', '<=', self.date_to),
                                                               ('stage_id', '=', 'approved')])),
                'base_delta': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '3'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_delta_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '3'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                      len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                                ('date', '<=', self.date_to),
                                                                ('stage_id', '=', 'approved')])),
                'base_ue': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '4'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_ue_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '4'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                   len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                             ('date', '<=', self.date_to),
                                                             ('stage_id', '=', 'approved')])),
                'base_c_r': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '5'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c_r_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec6', '=', '5'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                    len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                              ('date', '<=', self.date_to),
                                                              ('stage_id', '=', 'approved')])),

                'base_a': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'A'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_a_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'A'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_b': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'B'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_b_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'B'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                  len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                            ('date', '<=', self.date_to),
                                                            ('stage_id', '=', 'approved')])),
                'base_c1': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'C1'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c1_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'C1'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                   len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                             ('date', '<=', self.date_to),
                                                             ('stage_id', '=', 'approved')])),
                'base_c2': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'C2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c2_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'C2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                   len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                             ('date', '<=', self.date_to),
                                                             ('stage_id', '=', 'approved')])),
                'base_de': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'DE'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_de_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2]), ('sec', '=', 'DE'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                   len(questionnaire.search([('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from),
                                                             ('date', '<=', self.date_to),
                                                             ('stage_id', '=', 'approved')])),

            })
            query_2 = '''
            INSERT INTO a_internet_n2 (
             n2_id,n2,base,base_percent,base_male,base_male_percent,base_female,base_female_percent
            ,base_2,base_2_percent,base_3,base_3_percent,base_4,base_4_percent,base_5,base_5_percent
            ,base_6,base_6_percent,base_7,base_7_percent,base_8,base_8_percent,base_9,base_9_percent
            ,base_10,base_10_percent,
            
            base_cairo,base_cairo_percent,base_alex,base_alex_percent,base_delta,base_delta_percent,base_ue,base_ue_percent
            ,base_c_r,base_c_r_percent,
            
            base_a,base_a_percent,base_b,base_b_percent,base_c1,base_c1_percent,base_c2,base_c2_percent,base_de,base_de_percent)
            
            
            select a_n2_id, (select name from a_n2 where id=a_n2_id),
            count(*)::float,
            ROUND(100 * count(*)::float/%s),
            count(case a_questionnaire.s4 when 'male' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s4 when 'male' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s4 when 'female' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s4 when 'female' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.s3 when '2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '3' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '3' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '4' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '4' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '5' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '5' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '6' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '6' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '7' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '7' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '8' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '8' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '9' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '9' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '10' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '10' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.sec6 when '1' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '1' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '3' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '3' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '4' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '4' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '5' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '5' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.sec when 'A' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'A' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'B' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'B' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'C1' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'C1' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'C2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'C2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'DE' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'DE' then 1 else null end)::float/%s::float)*100)

            from rel_n2_questionnaire
            INNER Join a_questionnaire
            ON rel_n2_questionnaire.a_questionnaire_id=a_questionnaire.id where (('%s' <= date) AND (date <= '%s') AND (stage_id = 'approved'))
            Group By a_n2_id;    
            ''' % (len(questionnaire.search(
                [('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
                 ('stage_id', '=', 'approved')])),
                   internet_base_n2.base_male if internet_base_n2.base_male != 0 else 1,
                   internet_base_n2.base_female if internet_base_n2.base_female != 0 else 1,

                   internet_base_n2.base_2 if internet_base_n2.base_2 != 0 else 1,
                   internet_base_n2.base_3 if internet_base_n2.base_3 != 0 else 1,
                   internet_base_n2.base_4 if internet_base_n2.base_4 != 0 else 1,
                   internet_base_n2.base_5 if internet_base_n2.base_5 != 0 else 1,
                   internet_base_n2.base_6 if internet_base_n2.base_6 != 0 else 1,
                   internet_base_n2.base_7 if internet_base_n2.base_7 != 0 else 1,
                   internet_base_n2.base_8 if internet_base_n2.base_8 != 0 else 1,
                   internet_base_n2.base_9 if internet_base_n2.base_9 != 0 else 1,
                   internet_base_n2.base_10 if internet_base_n2.base_10 != 0 else 1,

                   internet_base_n2.base_cairo if internet_base_n2.base_cairo != 0 else 1,
                   internet_base_n2.base_alex if internet_base_n2.base_alex != 0 else 1,
                   internet_base_n2.base_delta if internet_base_n2.base_delta != 0 else 1,
                   internet_base_n2.base_ue if internet_base_n2.base_ue != 0 else 1,
                   internet_base_n2.base_c_r if internet_base_n2.base_c_r != 0 else 1,

                   internet_base_n2.base_a if internet_base_n2.base_a != 0 else 1,
                   internet_base_n2.base_b if internet_base_n2.base_b != 0 else 1,
                   internet_base_n2.base_c1 if internet_base_n2.base_c1 != 0 else 1,
                   internet_base_n2.base_c2 if internet_base_n2.base_c2 != 0 else 1,
                   internet_base_n2.base_de if internet_base_n2.base_de != 0 else 1,
                   self.date_from, self.date_to)
            self._cr.execute(query_2)

            query_2_other = '''
                        INSERT INTO a_internet_n2 (
                         n2,base,base_percent,base_male,base_male_percent,base_female,base_female_percent
                        ,base_2,base_2_percent,base_3,base_3_percent,base_4,base_4_percent,base_5,base_5_percent
                        ,base_6,base_6_percent,base_7,base_7_percent,base_8,base_8_percent,base_9,base_9_percent
                        ,base_10,base_10_percent,

                        base_cairo,base_cairo_percent,base_alex,base_alex_percent,base_delta,base_delta_percent,base_ue,base_ue_percent
                        ,base_c_r,base_c_r_percent,

                        base_a,base_a_percent,base_b,base_b_percent,base_c1,base_c1_percent,base_c2,base_c2_percent,base_de,base_de_percent)


                        select n2_other,
                        count(*)::float,
                        ROUND(100 * count(*)::float/%s),
                        count(case a_questionnaire.s4 when 'male' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s4 when 'male' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s4 when 'female' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s4 when 'female' then 1 else null end)::float/%s::float)*100),

                        count(case a_questionnaire.s3 when '2' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '2' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '3' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '3' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '4' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '4' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '5' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '5' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '6' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '6' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '7' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '7' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '8' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '8' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '9' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '9' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '10' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '10' then 1 else null end)::float/%s::float)*100),

                        count(case a_questionnaire.sec6 when '1' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '1' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec6 when '2' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '2' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec6 when '3' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '3' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec6 when '4' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '4' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec6 when '5' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '5' then 1 else null end)::float/%s::float)*100),

                        count(case a_questionnaire.sec when 'A' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'A' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec when 'B' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'B' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec when 'C1' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'C1' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec when 'C2' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'C2' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec when 'DE' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'DE' then 1 else null end)::float/%s::float)*100)

                        from a_questionnaire where (('%s' <= date) AND (date <= '%s') AND (stage_id = 'approved')AND (n2_other IS NOT Null))
                        Group By n2_other;    
                        ''' % (len(questionnaire.search(
                [('n1_id', 'in', [1, 2]), ('date', '>=', self.date_from), ('date', '<=', self.date_to),
                 ('stage_id', '=', 'approved')])),
                               internet_base_n2.base_male if internet_base_n2.base_male != 0 else 1,
                               internet_base_n2.base_female if internet_base_n2.base_female != 0 else 1,

                               internet_base_n2.base_2 if internet_base_n2.base_2 != 0 else 1,
                               internet_base_n2.base_3 if internet_base_n2.base_3 != 0 else 1,
                               internet_base_n2.base_4 if internet_base_n2.base_4 != 0 else 1,
                               internet_base_n2.base_5 if internet_base_n2.base_5 != 0 else 1,
                               internet_base_n2.base_6 if internet_base_n2.base_6 != 0 else 1,
                               internet_base_n2.base_7 if internet_base_n2.base_7 != 0 else 1,
                               internet_base_n2.base_8 if internet_base_n2.base_8 != 0 else 1,
                               internet_base_n2.base_9 if internet_base_n2.base_9 != 0 else 1,
                               internet_base_n2.base_10 if internet_base_n2.base_10 != 0 else 1,

                               internet_base_n2.base_cairo if internet_base_n2.base_cairo != 0 else 1,
                               internet_base_n2.base_alex if internet_base_n2.base_alex != 0 else 1,
                               internet_base_n2.base_delta if internet_base_n2.base_delta != 0 else 1,
                               internet_base_n2.base_ue if internet_base_n2.base_ue != 0 else 1,
                               internet_base_n2.base_c_r if internet_base_n2.base_c_r != 0 else 1,

                               internet_base_n2.base_a if internet_base_n2.base_a != 0 else 1,
                               internet_base_n2.base_b if internet_base_n2.base_b != 0 else 1,
                               internet_base_n2.base_c1 if internet_base_n2.base_c1 != 0 else 1,
                               internet_base_n2.base_c2 if internet_base_n2.base_c2 != 0 else 1,
                               internet_base_n2.base_de if internet_base_n2.base_de != 0 else 1,
                               self.date_from, self.date_to)
            self._cr.execute(query_2_other)
            internet_base_n3 = internet_n3.create({
                'n3': 'Base',
                'base': sum(internet_n2.search([('n3_report', '=', True)]).mapped('base')),
                'base_percent': 100,
                'base_male': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s4', '=', 'male'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_male_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s4', '=', 'male'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_female': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s4', '=', 'female'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_female_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s4', '=', 'female'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),

                'base_2': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_2_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '2'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_3': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '3'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_3_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '3'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_4': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '4'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_4_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '4'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_5': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '5'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_5_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '5'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_6': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '6'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_6_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '6'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_7': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '7'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_7_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '7'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_8': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '8'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_8_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '8'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_9': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '9'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_9_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '9'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_10': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('s3', '=', '10'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_10_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('s3', '=', '10'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),

                'base_cairo': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec6', '=', '1'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_cairo_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec6', '=', '1'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_alex': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec6', '=', '2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_alex_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec6', '=', '2'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_delta': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec6', '=', '3'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_delta_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec6', '=', '3'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_ue': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec6', '=', '4'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_ue_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec6', '=', '4'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_c_r': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec6', '=', '5'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c_r_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec6', '=', '5'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),

                'base_a': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec', '=', 'A'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_a_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec', '=', 'A'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_b': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec', '=', 'B'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_b_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec', '=', 'B'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_c1': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec', '=', 'C1'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c1_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec', '=', 'C1'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_c2': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec', '=', 'C2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c2_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec', '=', 'C2'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),
                'base_de': len(self.env['a.questionnaire'].search(
                    [('show_n3', '=', True), ('sec', '=', 'DE'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_de_percent': 0 if not sum(
                    internet_n2.search([('n3_report', '=', True)]).mapped('base')) else 100 * len(
                    self.env['a.questionnaire'].search(
                        [('show_n3', '=', True), ('sec', '=', 'DE'), ('date', '>=', self.date_from),
                         ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) /
                                                                                        sum(internet_n2.search([(
                                                                                            'n3_report',
                                                                                            '=',
                                                                                            True)]).mapped(
                                                                                            'base')),

            })
            query_3 = '''
            INSERT INTO a_internet_n3 (
            n3,base,base_percent,base_male,base_male_percent,base_female,base_female_percent
            ,base_2,base_2_percent,base_3,base_3_percent,base_4,base_4_percent,base_5,base_5_percent
            ,base_6,base_6_percent,base_7,base_7_percent,base_8,base_8_percent,base_9,base_9_percent
            ,base_10,base_10_percent,
            
            base_cairo,base_cairo_percent,base_alex,base_alex_percent,base_delta,base_delta_percent,base_ue,base_ue_percent
            ,base_c_r,base_c_r_percent,
            
            base_a,base_a_percent,base_b,base_b_percent,base_c1,base_c1_percent,base_c2,base_c2_percent,base_de,base_de_percent)
            
            select (select name from a_n3 where id=a_n3_id),
            count(*)::float,
            ROUND(100 * count(*)::float/%s),
            count(case a_questionnaire.s4 when 'male' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s4 when 'male' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s4 when 'female' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s4 when 'female' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.s3 when '2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '3' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '3' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '4' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '4' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '5' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '5' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '6' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '6' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '7' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '7' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '8' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '8' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '9' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '9' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '10' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '10' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.sec6 when '1' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '1' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '3' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '3' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '4' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '4' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '5' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '5' then 1 else null end)::float/%s::float)*100),
            
            count(case a_questionnaire.sec when 'A' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'A' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'B' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'B' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'C1' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'C1' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'C2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'C2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'DE' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'DE' then 1 else null end)::float/%s::float)*100)

            from rel_n3_questionnaire
            INNER Join a_questionnaire
            ON rel_n3_questionnaire.a_questionnaire_id=a_questionnaire.id where (('%s' <= date) AND (date <= '%s') AND (stage_id = 'approved'))
            Group By a_n3_id;    
            ''' % (sum(internet_n2.search([('n3_report', '=', True)]).mapped('base')),
                   internet_base_n3.base_male if internet_base_n3.base_male != 0 else 1,
                   internet_base_n3.base_female if internet_base_n3.base_female != 0 else 1,

                   internet_base_n3.base_2 if internet_base_n3.base_2 != 0 else 1,
                   internet_base_n3.base_3 if internet_base_n3.base_3 != 0 else 1,
                   internet_base_n3.base_4 if internet_base_n3.base_4 != 0 else 1,
                   internet_base_n3.base_5 if internet_base_n3.base_5 != 0 else 1,
                   internet_base_n3.base_6 if internet_base_n3.base_6 != 0 else 1,
                   internet_base_n3.base_7 if internet_base_n3.base_7 != 0 else 1,
                   internet_base_n3.base_8 if internet_base_n3.base_8 != 0 else 1,
                   internet_base_n3.base_9 if internet_base_n3.base_9 != 0 else 1,
                   internet_base_n3.base_10 if internet_base_n3.base_10 != 0 else 1,

                   internet_base_n3.base_cairo if internet_base_n3.base_cairo != 0 else 1,
                   internet_base_n3.base_alex if internet_base_n3.base_alex != 0 else 1,
                   internet_base_n3.base_delta if internet_base_n3.base_delta != 0 else 1,
                   internet_base_n3.base_ue if internet_base_n3.base_ue != 0 else 1,
                   internet_base_n3.base_c_r if internet_base_n3.base_c_r != 0 else 1,

                   internet_base_n3.base_a if internet_base_n3.base_a != 0 else 1,
                   internet_base_n3.base_b if internet_base_n3.base_b != 0 else 1,
                   internet_base_n3.base_c1 if internet_base_n3.base_c1 != 0 else 1,
                   internet_base_n3.base_c2 if internet_base_n3.base_c2 != 0 else 1,
                   internet_base_n3.base_de if internet_base_n3.base_de != 0 else 1,
                   self.date_from, self.date_to)

            query_3_other = '''
                        INSERT INTO a_internet_n3 (
                        n3,base,base_percent,base_male,base_male_percent,base_female,base_female_percent
                        ,base_2,base_2_percent,base_3,base_3_percent,base_4,base_4_percent,base_5,base_5_percent
                        ,base_6,base_6_percent,base_7,base_7_percent,base_8,base_8_percent,base_9,base_9_percent
                        ,base_10,base_10_percent,

                        base_cairo,base_cairo_percent,base_alex,base_alex_percent,base_delta,base_delta_percent,base_ue,base_ue_percent
                        ,base_c_r,base_c_r_percent,

                        base_a,base_a_percent,base_b,base_b_percent,base_c1,base_c1_percent,base_c2,base_c2_percent,base_de,base_de_percent)

                        select n3_other,
                        count(*)::float,
                        ROUND(100 * count(*)::float/%s),
                        count(case a_questionnaire.s4 when 'male' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s4 when 'male' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s4 when 'female' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s4 when 'female' then 1 else null end)::float/%s::float)*100),

                        count(case a_questionnaire.s3 when '2' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '2' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '3' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '3' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '4' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '4' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '5' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '5' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '6' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '6' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '7' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '7' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '8' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '8' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '9' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '9' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.s3 when '10' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.s3 when '10' then 1 else null end)::float/%s::float)*100),

                        count(case a_questionnaire.sec6 when '1' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '1' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec6 when '2' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '2' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec6 when '3' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '3' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec6 when '4' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '4' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec6 when '5' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec6 when '5' then 1 else null end)::float/%s::float)*100),

                        count(case a_questionnaire.sec when 'A' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'A' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec when 'B' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'B' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec when 'C1' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'C1' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec when 'C2' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'C2' then 1 else null end)::float/%s::float)*100),
                        count(case a_questionnaire.sec when 'DE' then 1 else null end)::float,
                        ROUND((count(case a_questionnaire.sec when 'DE' then 1 else null end)::float/%s::float)*100)

                        from a_questionnaire
                        where (('%s' <= date) AND (date <= '%s') AND (stage_id = 'approved') AND (n3_other IS Not Null))
                        Group By n3_other;    
                        ''' % (sum(internet_n2.search([('n3_report', '=', True)]).mapped('base')),
                               internet_base_n3.base_male if internet_base_n3.base_male != 0 else 1,
                               internet_base_n3.base_female if internet_base_n3.base_female != 0 else 1,

                               internet_base_n3.base_2 if internet_base_n3.base_2 != 0 else 1,
                               internet_base_n3.base_3 if internet_base_n3.base_3 != 0 else 1,
                               internet_base_n3.base_4 if internet_base_n3.base_4 != 0 else 1,
                               internet_base_n3.base_5 if internet_base_n3.base_5 != 0 else 1,
                               internet_base_n3.base_6 if internet_base_n3.base_6 != 0 else 1,
                               internet_base_n3.base_7 if internet_base_n3.base_7 != 0 else 1,
                               internet_base_n3.base_8 if internet_base_n3.base_8 != 0 else 1,
                               internet_base_n3.base_9 if internet_base_n3.base_9 != 0 else 1,
                               internet_base_n3.base_10 if internet_base_n3.base_10 != 0 else 1,

                               internet_base_n3.base_cairo if internet_base_n3.base_cairo != 0 else 1,
                               internet_base_n3.base_alex if internet_base_n3.base_alex != 0 else 1,
                               internet_base_n3.base_delta if internet_base_n3.base_delta != 0 else 1,
                               internet_base_n3.base_ue if internet_base_n3.base_ue != 0 else 1,
                               internet_base_n3.base_c_r if internet_base_n3.base_c_r != 0 else 1,

                               internet_base_n3.base_a if internet_base_n3.base_a != 0 else 1,
                               internet_base_n3.base_b if internet_base_n3.base_b != 0 else 1,
                               internet_base_n3.base_c1 if internet_base_n3.base_c1 != 0 else 1,
                               internet_base_n3.base_c2 if internet_base_n3.base_c2 != 0 else 1,
                               internet_base_n3.base_de if internet_base_n3.base_de != 0 else 1,
                               self.date_from, self.date_to)
            internet_base_n4 = internet_n4.create({
                'n4': 'Base',
                'base': len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_percent': 100,
                'base_male': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s4', '=', 'male'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_male_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s4', '=', 'male'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_female': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s4', '=', 'female'),
                     ('date', '>=', self.date_from), ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_female_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s4', '=', 'female'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),

                'base_2': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_2_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '2'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_3': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '3'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_3_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '3'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_4': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '4'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_4_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '4'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_5': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '5'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_5_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '5'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_6': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '6'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_6_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '6'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_7': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '7'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_7_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '7'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_8': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '8'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_8_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '8'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_9': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '9'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_9_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '9'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_10': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '10'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_10_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('s3', '=', '10'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),

                'base_cairo': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '1'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_cairo_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '1'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_alex': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '2'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_alex_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '2'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_delta': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '3'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_delta_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '3'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_ue': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '4'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_ue_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '4'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c_r': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '5'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c_r_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec6', '=', '5'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),

                'base_a': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'A'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_a_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'A'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_b': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'B'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_b_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'B'), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c1': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'C1'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c1_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'C1'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c2': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'C2'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_c2_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'C2'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_de': len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'DE'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                'base_de_percent': 100 * len(self.env['a.questionnaire'].search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('sec', '=', 'DE'),
                     ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])) / len(questionnaire.search(
                    [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                     ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),

            })
            query_4 = '''
            INSERT INTO a_internet_n4 (n4,base,base_percent,base_male,base_male_percent,base_female,base_female_percent

            ,base_2,base_2_percent,base_3,base_3_percent,base_4,base_4_percent,base_5,base_5_percent
            ,base_6,base_6_percent,base_7,base_7_percent,base_8,base_8_percent,base_9,base_9_percent
            ,base_10,base_10_percent,

            base_cairo,base_cairo_percent,base_alex,base_alex_percent,base_delta,base_delta_percent,base_ue,base_ue_percent
            ,base_c_r,base_c_r_percent,

            base_a,base_a_percent,base_b,base_b_percent,base_c1,base_c1_percent,base_c2,base_c2_percent,base_de,base_de_percent) 

            select n4_name,
            count(*)::float,
            ROUND(100 * count(*)::float/%s),

            count(case a_questionnaire.s4 when 'male' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s4 when 'male' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s4 when 'female' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s4 when 'female' then 1 else null end)::float/%s::float)*100),

            count(case a_questionnaire.s3 when '2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '3' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '3' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '4' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '4' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '5' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '5' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '6' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '6' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '7' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '7' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '8' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '8' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '9' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '9' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.s3 when '10' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.s3 when '10' then 1 else null end)::float/%s::float)*100),

            count(case a_questionnaire.sec6 when '1' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '1' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '3' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '3' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '4' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '4' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec6 when '5' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec6 when '5' then 1 else null end)::float/%s::float)*100),

            count(case a_questionnaire.sec when 'A' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'A' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'B' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'B' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'C1' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'C1' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'C2' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'C2' then 1 else null end)::float/%s::float)*100),
            count(case a_questionnaire.sec when 'DE' then 1 else null end)::float,
            ROUND((count(case a_questionnaire.sec when 'DE' then 1 else null end)::float/%s::float)*100)

            from a_questionnaire where (('%s' <= date) AND (date <= '%s') AND (stage_id = 'approved')) Group By n4_name ;
            ''' % (len(questionnaire.search(
                [('n1_id', 'in', [1, 2, 3]), ('n4', '!=', False), ('date', '>=', self.date_from),
                 ('date', '<=', self.date_to), ('stage_id', '=', 'approved')])),
                   internet_base_n4.base_male if internet_base_n4.base_male != 0 else 1,
                   internet_base_n4.base_female if internet_base_n4.base_female != 0 else 1,
                   internet_base_n4.base_2 if internet_base_n4.base_2 != 0 else 1,
                   internet_base_n4.base_3 if internet_base_n4.base_3 != 0 else 1,
                   internet_base_n4.base_4 if internet_base_n4.base_4 != 0 else 1,
                   internet_base_n4.base_5 if internet_base_n4.base_5 != 0 else 1,
                   internet_base_n4.base_6 if internet_base_n4.base_6 != 0 else 1,
                   internet_base_n4.base_7 if internet_base_n4.base_7 != 0 else 1,
                   internet_base_n4.base_8 if internet_base_n4.base_8 != 0 else 1,
                   internet_base_n4.base_9 if internet_base_n4.base_9 != 0 else 1,
                   internet_base_n4.base_10 if internet_base_n4.base_10 != 0 else 1,

                   internet_base_n4.base_cairo if internet_base_n4.base_cairo != 0 else 1,
                   internet_base_n4.base_alex if internet_base_n4.base_alex != 0 else 1,
                   internet_base_n4.base_delta if internet_base_n4.base_delta != 0 else 1,
                   internet_base_n4.base_ue if internet_base_n4.base_ue != 0 else 1,
                   internet_base_n4.base_c_r if internet_base_n4.base_c_r != 0 else 1,

                   internet_base_n4.base_a if internet_base_n4.base_a != 0 else 1,
                   internet_base_n4.base_b if internet_base_n4.base_b != 0 else 1,
                   internet_base_n4.base_c1 if internet_base_n4.base_c1 != 0 else 1,
                   internet_base_n4.base_c2 if internet_base_n4.base_c2 != 0 else 1,
                   internet_base_n4.base_de if internet_base_n4.base_de != 0 else 1,
                   self.date_from, self.date_to)

            self._cr.execute(query)
            self._cr.execute(query_3)
            self._cr.execute(query_3_other)
            self._cr.execute(query_4)

        return {
            'name': _("Internet Report N1"),
            'view_mode': 'tree',
            'res_model': 'a.internet.n1',
            'view_ids': [(self.env.ref('media_tracking.internet_n1_list').id, 'list'),
                         (self.env.ref('media_tracking.internet_n1_view_pivot').id, 'pivot')],
            'target': 'current',
            'type': 'ir.actions.act_window', }
