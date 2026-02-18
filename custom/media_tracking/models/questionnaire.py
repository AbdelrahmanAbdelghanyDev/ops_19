# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from typing import Any


class Questionnaire(models.Model):
    _name = 'a.questionnaire'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "Questionnaire"

    name = fields.Char(string="Sequence Number", readonly=True, required=True, copy=False, default='New', tracking=True)
    stage_id = fields.Selection(
        [('new', 'New'), ('cati', 'CATI supervisor'), ('qc', 'QC'), ('approved', 'Approved'), ('cancel', 'Cancel')],
        default='new', tracking=True)
    check_q3 = fields.Boolean(store=False)
    is_q3_editor = fields.Boolean(string="Is Q3 Editor", compute="_compute_is_q3_editor", store=False)

    def _compute_is_q3_editor(self):
        """Compute whether the current user is part of the Q3 Editor group."""
        q3_editor_group = 'media_tracking.group_q3_editor'
        for rec in self:
            if self.env.user.has_group(q3_editor_group):
                rec.is_q3_editor = True
            else:
                rec.is_q3_editor = False

    # def _check_empty(self):
    #     print(self.q3.ids)
    #     if len(self.q3.ids) > 0:
    #         self.check_q3 =True
    #     else:
    #         self.check_q3 = False

    def validate_tv(self) -> Any:
        self.ensure_one()
        tv_lines = self.q3

        if not tv_lines:
            raise ValidationError(_("No TV lines to validate."))

        program_not_found = False
        missing_program_name = ""

        for line in tv_lines:
            programs = line.channel_id.channel_lines.filtered(lambda l: l.program.id == line.programs_id.id)
            program = programs.filtered(lambda l: (
                    l.program.id == line.programs_id.id and
                    l.time_from.id == line.time_from.id and
                    l.time_to.id == line.time_to.id and
                    l.header == line.header
            ))

            if not program:
                program_not_found = True
                missing_program_name = line.programs_id.name
                break  # Exit loop as soon as a missing program is found

        if program_not_found:
            raise ValidationError(_("Wrong data in TV channel program %s does not exist" % missing_program_name))

        return True

    def action_approve_1(self):
        self.stage_id = 'qc'

    def action_approve_2(self):
        if self.validate_tv():
            if self.q3:
                self.stage_id = 'approved'
            else:
                raise ValidationError('Cannot approved becouse their is no data in tv section')
            self.stage_id = 'approved'
        return True

    def action_approve_3(self):
        self.stage_id = 'qc'

    def action_cancel(self):
        self.stage_id = 'cancel'

    def action_new(self):
        self.stage_id = 'new'

    def submit_to_cati(self):
        self.stage_id = 'cati'

    @api.model
    def create(self, vals):
        print(vals)
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'a.questionnaire.seq') or 'New'
        if vals['s1_continue']:
            if not vals['s2']:
                raise ValidationError(_("Please Select choice in S2"))
            if vals['s2'] == '1':
                if vals['s3'] != '1':
                    if not vals['s4']:
                        raise ValidationError(_("Please Select choice in S4"))
                    if not vals['s3']:
                        raise ValidationError(_("Please Select choice in S3"))
                    if not vals['s4']:
                        raise ValidationError(_("Please Select choice in S4"))

                    if not vals['s5a']:
                        raise ValidationError(_("Please Select choice in S5a"))
                    if vals['s5a'] == '2':
                        if not vals['s6']:
                            raise ValidationError(_("Please Select choice in S6"))

                        if vals['s6'] == '2':
                            if not vals['s7']:
                                raise ValidationError(_("Please Select choice in S7"))
                            if vals['s7'] == '1':
                                if not vals['sec3'] and self.show_demographics:
                                    raise ValidationError(_("Please Select choice in SEC3"))
                                if vals['sec3'] == '2':
                                    if not vals['sec4a']:
                                        raise ValidationError(_("Please Select choice in SEC4a"))
                                if vals['sec6'] != '1':
                                    if not vals['sec6b'] and self.show_demographics:
                                        raise ValidationError(_("Please Select choice in SEC6b"))
                                if not vals['q2']:
                                    raise ValidationError(_("Please Select choice in Q2"))

        result = super(Questionnaire, self).create(vals)
        return result

    date = fields.Date('Today Date', default=lambda self: fields.Date.today())
    day_name = fields.Char(default=lambda self: fields.Date.today().strftime("%A"), string='Day')
    respondent_id = fields.Many2one('res.partner', string='Respondent name', tracking=True, required=True)

    @api.depends('date')
    def _get_month(self):
        for rec in self:
            rec.month = rec.date.month

    month = fields.Integer(string="Month", compute='_get_month', store=True)

    # @api.model
    # @api.onchange('respondent_id')
    # def _get_employee_id_domain(self):
    #     last_six_months_questionnaire = self.env['a.questionnaire'].search(
    #         [('date', '>=', fields.Date.today() - relativedelta(months=6))]).mapped('respondent_id')
    #     return [('id', 'not in', last_six_months_questionnaire.ids)]

    telephone = fields.Char('Tel.', tracking=True, required=True, )
    address = fields.Char('Address', tracking=True, required=True, )

    @api.onchange('respondent_id')
    def onchange_respondent(self):
        if self.respondent_id:
            self.telephone = self.respondent_id.mobile
            self.address = self.respondent_id.street
        last_six_months_questionnaire = self.env['a.questionnaire'].search(
            [('date', '>=', fields.Date.today() - relativedelta(months=6))]).mapped('respondent_id')
        return {'domain': {'respondent_id': [('id', 'not in', last_six_months_questionnaire.ids)]}}

    @api.constrains('telephone')
    def constrains_telephone(self):
        if self.telephone[0:2] != '+2':
            self.telephone = '+2' + self.telephone
        self.respondent_id.write({'mobile': self.telephone})

    interviewer_id = fields.Many2one('res.users', default=lambda self: self.env.user, string="Interviewer Name",
                                     tracking=True)
    interviewer_code = fields.Char(string="Interviewer Code", tracking=True, required=True)
    call_date = fields.Date('Recall Date', tracking=True,
                            default=lambda self: fields.Date.today() - relativedelta(days=1))
    sec = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C1', 'C1'),
        ('C2', 'C2'),
        ('DE', 'DE'),
    ], string='SEC', default='DE')
    ######################## Tab 1 ###############################
    s1 = fields.Many2many('a.s1', 'rel_s1_questionnaire')
    s1_continue = fields.Boolean(default=False)

    @api.onchange('s1')
    def onchange_s1(self):
        if self.s1:
            for rec in self.s1:
                if rec.continue_questionnaire:
                    self.s1_continue = True
                else:
                    self.s1_continue = False
                    break
        else:
            self.s1_continue = True

    s2 = fields.Selection([('1', 'لا'), ('2', 'نعم')])
    s3 = fields.Selection([
        ('1', 'أقل من 15 سنة'),
        ('2', '15 - 19'),
        ('3', '20 - 24'),
        ('4', '25 - 29'),
        ('5', '30 - 34'),
        ('6', '35 - 39'),
        ('7', '40 - 44'),
        ('8', '45 - 49'),
        ('9', '50 - 59'),
        ('10', 'أكثر من 59'),
    ], string='Age Range')
    age = fields.Integer('Age')

    @api.onchange('age')
    def _onchange_age(self):
        if self.age:
            if self.age < 15:
                self.s3 = '1'
            if 15 <= self.age <= 19:
                self.s3 = '2'
            if 20 <= self.age <= 24:
                self.s3 = '3'
            if 25 <= self.age <= 29:
                self.s3 = '4'
            if 30 <= self.age <= 34:
                self.s3 = '5'
            if 35 <= self.age <= 39:
                self.s3 = '6'
            if 40 <= self.age <= 44:
                self.s3 = '7'
            if 45 <= self.age <= 49:
                self.s3 = '8'
            if 50 <= self.age <= 59:
                self.s3 = '9'
            if 59 <= self.age:
                self.s3 = '10'

    s4 = fields.Selection([('male', 'ذكر'), ('female', 'انثى')], string='Gender')
    s5 = fields.Integer(compute='get_score')
    s5a = fields.Selection([('1', 'لا'), ('2', 'نعم')])
    s6 = fields.Selection([('1', 'لا'), ('2', 'نعم')])
    s7 = fields.Selection([('1', '‫حضر‬'), ('2', '‫ريف‬')])

    ######################## Tab 2 ###############################
    sec1_a = fields.Selection([
        ('1', 'بدون عمل / ربات البيوت‬'),
        ('2',
         'عمالة مؤقتة غير ماهرة، خدم، حارس أمن، جنود، باعة متجولون، شحادون، مزارعون / صيادو سمك بالأجرة، سعاة مكاتب‬'),
        ('3', 'عمالة ماهرة (سباك، ميكانيكي، وما شابه ذلك)، مساعد في متجر'),
        ('4', 'فنيون معتمدون، موظفون إداريون ومشرفون، موظفون في مكاتب (القطاع العام)، سائقو سيارات الأجرة'),
        ('5',
         'موظفو الإدارة الدنيا (القطاع الخاص)، موظفو خدمة مدنية متوسطي الدرجة، ملاك متاجر صغيرة، مدرسون، موظف بنك مبتدئ'),
        ('6', 'إدارة متوسطة/متخصصون/تجار/موظفو خدمة مدنية كبار، ملاك شركات صغيرة'),
        ('7', 'إدارة عليا / ملاك شركات كبيرة'),
        ('0', 'رفض الإجابة Exclusive')
    ])
    sec1_b = fields.Selection([
        ('1', 'بدون عمل / ربات البيوت‬'),
        ('2',
         'عمالة مؤقتة غير ماهرة، خدم، حارس أمن، جنود، باعة متجولون، شحادون، مزارعون / صيادو سمك بالأجرة، سعاة مكاتب‬'),
        ('3', 'عمالة ماهرة (سباك، ميكانيكي، وما شابه ذلك)، مساعد في متجر'),
        ('4', 'فنيون معتمدون، موظفون إداريون ومشرفون، موظفون في مكاتب (القطاع العام)، سائقو سيارات الأجرة'),
        ('5',
         'موظفو الإدارة الدنيا (القطاع الخاص)، موظفو خدمة مدنية متوسطي الدرجة، ملاك متاجر صغيرة، مدرسون، موظف بنك مبتدئ'),
        ('6', 'إدارة متوسطة/متخصصون/تجار/موظفو خدمة مدنية كبار، ملاك شركات صغيرة'),
        ('7', 'إدارة عليا / ملاك شركات كبيرة'),
        ('0', 'رفض الإجابة Exclusive')
    ])

    sec2_a = fields.Selection([
        ('1', 'يجهل القراءة والكتابة‬'),
        ('2', 'يمكنه القراءة والكتابة لكن بدون تعليم رسمي / يمكنه الحصول على شهادة محو الأمية‬'),
        ('3', 'بلغ مستوى التعليم الأساسي / الإعدادي'),
        ('4', 'بلغ مستوى التعليم الثانوي'),
        ('5', 'شهادة البكالوريوس'),
        ('6', 'شهادة جامعية من جامعة محلية'),
        ('0', 'رفض الإجابة Exclusive'),

    ])
    sec2_b = fields.Selection([
        ('1', 'يجهل القراءة والكتابة‬'),
        ('2', 'يمكنه القراءة والكتابة لكن بدون تعليم رسمي / يمكنه الحصول على شهادة محو الأمية‬'),
        ('3', 'بلغ مستوى التعليم الأساسي / الإعدادي'),
        ('4', 'بلغ مستوى التعليم الثانوي'),
        ('5', 'شهادة البكالوريوس'),
        ('6', 'شهادة جامعية من جامعة محلية'),
        ('0', 'رفض الإجابة Exclusive'),

    ])

    sec3 = fields.Selection([('2', 'لا'), ('1', 'نعم')])
    sec4 = fields.Many2many('a.sec4', 'rel_sec4_m2m_questionnaire')

    # sec4 = fields.Selection([
    #     ('1','أندية المدن الصغيرة (مراكز الشباب)‬'),
    #     ('2','أندية الشركات (المقاولون العرب - السكة الحديد - البترول - أي ناد مرتبط بمؤسسة أو شركة)'),
    #     ('3','أندية الطبقة المتوسطة (نادي الغابة - نادي التوفيقية - نادي النصر)'),
    #     ('4','أندية الطبقة الثانية (النادي الأهلي - الزمالك - الزهور - الترسانة - مدينة نصر – الشمس,نادى وادى دجلة)'),
    #     ('5','أندية الطبقة الأولى (نادي الصيد المصري - نادي الجزيرة - نادي هليوبوليس - نادي القطامية)'),
    #     ('0','رفض الإجابة')
    # ])
    sec4a = fields.Selection([('0', 'لا'), ('2', 'نعم')])
    # sec4b = fields.Selection([
    #     ('4','التعليم‬'),
    #     ('3','السياحة'),
    #     ('2','العمل'),
    #     ('1','الحج / العمرة'),
    #     ('0','رفض الإجابة Exclusive'),
    # ])
    sec4b_m2m = fields.Many2many('a.sec4b', 'rel_sec4b_m2m_questionnaire')
    sec4c_m2m = fields.Many2many('a.sec4c', 'rel_sec4c_m2m_questionnaire')

    sec5 = fields.Selection([
        ('00', 'لا نمتلك سيارة‬'),
        ('1', 'سيارة واحدة'),
        ('2', 'سيارتان'),
        ('3', 'أكثر من سيارتين'),
        ('0', 'رفض الإجابة Exclusive')
    ])
    sec6 = fields.Selection([
        ('1', 'القاهرة'),
        ('2', 'الاسكندرية'),
        ('3', 'الدلتا'),
        ('4', 'الصعيد'),
        ('5', 'القناة و البحر الاحمر'),
    ], string='Region')
    sec6a = fields.Selection([
        ('5', 'العجوزة - الدقى - النزهة - مصر الجديدة - المعادى - المنيل - المهندسين - مدينة نصر - الزمالك'),
        ('3', 'العباسية - عابدين - المقطم - الجيزة - حدائق القبة - الهرم & فيصل - شبرا - الزيتون'),
        ('2',
         'عين شمس - العمرانية - الضاهر - حلوان - قصر النيل - المطرية - مصر القديمة - الساحل - شبرا الخيمة - الوايلى'),
        ('1',
         'المرج - البساتين - بولاق ابوالعلا - بولاق الدكرور - دار السلام - الدرب الاحمر - عزبة النخل -الجمالية - امبابة-مدينة السلام - منشية ناصر - روض الفرج - السيدة زينب - الشرابية - الزاوية الحمراء'),
        ('0', 'رفض الإجابة')
    ])
    sec6b = fields.Selection([
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('5', '5'),
    ])
    sec7 = fields.Selection([
        ('1', 'منزل مبني بالطوب'),
        ('2', 'عمارات الطبقة الدنيا'),
        ('3', 'عمارات الطبقة المتوسطة'),
        ('4', 'برج / عمارات الطبقة الراقية'),
        ('5', 'فيلا منفصلة'),
	('0','رفض الاجابة')
    ])

    sec8 = fields.Selection([
        ('1', '1,000 أو أقل'),
        ('2', '1,001-2,000'),
        ('3', '2,001-4,000'),
        ('4', '4,001-8,000'),
        ('5', '8,001-15,000'),
        ('6', '15,001-20,000'),
        ('7', '20,001-30,000'),
        ('8', '40,000‎-30,001'),
        ('9', 'أكثر من 40,000'),
        ('0', 'رفض الإجابة EXCLUSIVE'),
    ])

    ######################## Tab 3 ###############################

    q1 = fields.Selection([
        ('1', 'اقل من ساعة'),
        ('2', 'من  ساعة لساعتين'),
        ('3', 'من  ساعتين ل 3'),
        ('4', 'أكتر من 3 ساعات'),
    ])
    q2 = fields.Selection([('1', 'لا'), ('2', 'نعم')], default='1')

    q3 = fields.One2many('a.data.processing', 'name')

    show_internet_questions = fields.Boolean(string="أسئلة الانترنت", )
    show_demographics = fields.Boolean(string="الديموغرافيا", )

    ######################## Tab 4 ###############################

    # n1 = fields.Selection([
    #     ('1','نعم بتفرج ومتابع'),
    #     ('2','نعم بتفرج بس مش متابع باستمرار'),
    #     ('3','لا,بس بدخل على الانترنت عادي'),
    #     ('4','لا أنا مبدخلش على الانترنت'),
    # ])
    n1 = fields.Many2one('a.n1', string='N1')
    n1_id = fields.Integer(related='n1.id', store=True)
    n1_name = fields.Char(related='n1.name', store=True)
    n2 = fields.Many2many('a.n2', 'rel_n2_questionnaire')

    @api.onchange('n1')
    def onchange_n1(self):
        if self.n1_id not in ['1', '2']:
            self.n2 = False
            self.n2_other = False
        if self.n1_id == 4:
            self.n4 = False

    # n2 = fields.Selection([
    #     ('1','فيديوهات على الفيس بوك'),
    #     ('2','فيديوهات على تيك توك'),
    #     ('3','فيديوهات على انستاجرام'),
    #     ('4','فيديوهات على يوتيوب'),
    #     ('5','مسلسلات'),
    #     ('6','افلام'),
    #     ('7','افلام وثائقية'),
    #     ('8','برامج'),
    #     ('9','ماتشات كورة'),
    #     ('10','كرتون'),
    #     ('11','Others Specify'),
    # ])
    open_n2_other = fields.Boolean(default=False)
    show_n3 = fields.Boolean(default=False)
    report_n3 = fields.Boolean(default=False)

    @api.onchange('n2')
    def show_n2_other(self):
        if self.n2:
            n2_other_list = []
            show_n3_list = []
            report_n3_list = []
            for rec in self.n2:
                n2_other_list.append(rec.other)
                show_n3_list.append(rec.show_n3)
                report_n3_list.append(rec.report_n3)
                if True in n2_other_list:
                    self.open_n2_other = True
                else:
                    self.open_n2_other = False
                    self.n2_other = False
                if True in show_n3_list:
                    self.show_n3 = True
                else:
                    self.show_n3 = False
                if True in report_n3_list:
                    self.report_n3 = True
                else:
                    self.report_n3 = False
        else:
            self.open_n2_other = False
            self.show_n3 = False
            self.report_n3 = False
            self.n3 = False
            self.n3_other = False

    def cron_show_n2_other(self):
        for record in self.env['a.questionnaire'].search([]):
            if record.n2:
                n2_other_list = []
                show_n3_list = []
                report_n3_list = []
                for rec in record.n2:
                    n2_other_list.append(rec.other)
                    show_n3_list.append(rec.show_n3)
                    report_n3_list.append(rec.report_n3)
                    if True in n2_other_list:
                        record.open_n2_other = True
                    else:
                        record.open_n2_other = False
                        record.n2_other = False
                    if True in show_n3_list:
                        record.show_n3 = True
                    else:
                        record.show_n3 = False
                    if True in report_n3_list:
                        record.report_n3 = True
                    else:
                        record.report_n3 = False
            else:
                record.open_n2_other = False
                record.show_n3 = False
                record.report_n3 = False
                record.n3 = False
                record.n3_other = False

    n2_other = fields.Char('Other')

    # n3 = fields.Selection([
    #     ('1','يوتيوب'),
    #     ('2','سينما فور يو'),
    #     ('3','شاهد.نت'),
    #     ('4','ديلى موشن'),
    #     ('5','شاهد فور يو'),
    #     ('6','سى بى سى.كوم'),
    #     ('7','تيلى.كوم'),
    #     ('8','واتش ات'),
    #     ('9','نيتفليكس'),
    #     ('10','او اس ان ستريمنج (OSN)'),
    #     ('11','امازون'),
    #     ('12','وافو (WAVO)'),
    #     ('13','فيو'),
    #     ('14','فيديوهات مبعوتة على تيليجرام'),
    #     ('15','اتصالات تي في'),
    #     ('16','ايجي بيست'),
    #     ('17','اف موفيز'),
    #     ('18','بوب كورن تايم'),
    #     ('19','بنزلهم على الكومبيوتر'),
    #     ('20','اخرى من فضلك حدد....'),
    # ])
    n3 = fields.Many2many('a.n3', 'rel_n3_questionnaire')

    open_n3_other = fields.Boolean(default=False)

    @api.onchange('n3')
    def show_n3_other(self):
        n3_other_list = []
        if self.n3:
            for rec in self.n3:
                n3_other_list.append(rec.other)
                if True in n3_other_list:
                    self.open_n3_other = True
                    break
                else:
                    self.open_n3_other = False
        else:
            self.open_n3_other = False

    n3_other = fields.Char('Other')
    n4 = fields.Many2one('a.n4')
    n4_id = fields.Integer(related='n4.id', store=True)
    n4_name = fields.Char(related='n4.name', store=True)

    #     ('1','9-11 AM'),
    #     ('2','11:05-1 PM'),
    #     ('3','1:05-3 PM'),
    #     ('4','3:05-5 PM'),
    #     ('5','5:05-7 PM'),
    #     ('6','7:05-9 PM'),
    #     ('7','9:05-11 PM'),
    #     ('8','11:05-1 AM'),
    #     ('9','1:05-3 AM'),
    #     ('10','3:05-5 AM'),
    #     ('11','5:05-7 AM'),
    #     ('12','7:05-9 AM'),
    # ])

    #####################################################

    def get_score(self):
        for rec in self.sudo():
            score = []
            # score.append(int(rec.sec1_a) or 0)
            score.append(int(rec.sec1_b) or 0)
            score.append(int(rec.sec2_a) or 0)
            # score.append(int(rec.sec2_b) or 0)
            # score.append(int(rec.sec3) or 0)
            # score.append(int(rec.sec4a) or 0)
            # score.append(int(rec.sec6) or 0)
            score.append(int(rec.sec6a) or 0)
            score.append(int(rec.sec6b) or 0)
            score.append(int(rec.sec5) or 0)
            score.append(int(rec.sec7) or 0)
            score.append(int(rec.sec8) or 0)
            line_sec4 = []
            line_sec4b = []
            line_sec4c = []

            if rec.sec4:
                for record in rec.sec4:
                    line_sec4.append(record.score)
                score.append(int(max(line_sec4)) or 0)
            if rec.sec4b_m2m:
                for recordb in rec.sec4b_m2m:
                    line_sec4b.append(recordb.score)
                score.append(int(max(line_sec4b)) or 0)
            if rec.sec4c_m2m:
                for recordc in rec.sec4c_m2m:
                    line_sec4c.append(recordc.score)
                score.append(int(max(line_sec4c)) or 0)
            rec.s5 = sum(score)
            if 1 <= sum(score) <= 15:
                rec.sec = 'DE'
            if 16 <= sum(score) <= 23:
                rec.sec = 'C2'
            if 24 <= sum(score) <= 31:
                rec.sec = 'C1'
            if 32 <= sum(score) <= 40:
                rec.sec = 'B'
            if 40 <= sum(score):
                rec.sec = 'A'
            else:
                pass

    def open_wizard(self):
        return {
            'name': 'Add Line',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'a.add.line',
            'target': 'new',
            'context': {
                'default_name': self.id,
                'default_questionnaire_date': self.call_date,
            },
            'type': 'ir.actions.act_window',
        }

    def write(self, vals):
        res = super(Questionnaire, self).write(vals)
        if self.s1_continue:
            if not self.s2:
                raise ValidationError(_("Please Select choice in S2"))
            if self.s2 == '1':
                if not self.s3:
                    raise ValidationError(_("Please Select choice in S3"))
                if self.s3 != '1':
                    if not self.s4:
                        raise ValidationError(_("Please Select choice in S4"))

                    if not self.s5a:
                        raise ValidationError(_("Please Select choice in S5a"))
                    if self.s5a == '2':
                        if not self.s6:
                            raise ValidationError(_("Please Select choice in S6"))

                        if self.s6 == '2':
                            if not self.s7:
                                raise ValidationError(_("Please Select choice in S7"))
                            if self.s7 == '1':
                                if not self.sec3 and self.show_demographics:
                                    raise ValidationError(_("Please Select choice in SEC3"))
                                if self.sec3 == '2':
                                    if not self.sec4a:
                                        raise ValidationError(_("Please Select choice in SEC4a"))
                                if self.sec6 != '1':
                                    if not self.sec6b and self.show_demographics:
                                        raise ValidationError(_("Please Select choice in SEC6b"))
                                if not self.q2:
                                    raise ValidationError(_("Please Select choice in Q2"))
        return res
