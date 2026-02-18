odoo.define('media_tracking.required', function (require) {
    'use strict';

    var core = require('web.core');
    var FormController = require('web.FormController');
    var ListController = require('web.ListController');
    var FormRenderer = require('web.FormRenderer');
    var _t = core._t;


    ListController.include({
		renderButtons: function() {
			this._super.apply(this, arguments);
            var total_sample = this.$buttons.find('#total_sample');
            var wizard_date = this.$buttons.find('#wizard_date');
            console.log(total_sample,this);
            if (this.modelName =='a.quarter' || this.modelName =='a.full'){
            total_sample[0].textContent="x";
            total_sample[0].style.background='#adff2f';
            total_sample[0].style.color='#000000';
            total_sample[0].style.height='30px';
            total_sample[0].style.fontWeight = 'bold';
            total_sample[0].disabled = true;
            this._rpc({
                    model: 'a.wizard.quarter',
                    method: 'get_total_sample',
                    args: [[1]],
                    }).then(function (result) {
                    total_sample[0].textContent= "Total Sample = " + result;
                    });
            wizard_date[0].textContent="x";
            wizard_date[0].style.background='#adff2f';
            wizard_date[0].style.color='#000000';
            wizard_date[0].style.height='30px';
            wizard_date[0].style.fontWeight = 'bold';
            wizard_date[0].disabled = true;
            this._rpc({
                    model: 'a.wizard.quarter',
                    method: 'get_wizard_date',
                    args: [[1]],
                    }).then(function (result) {
                    wizard_date[0].textContent= result;
                    });
            }
            else if (this.modelName == 'a.quarter.total.sample' || this.modelName == 'a.full.total.sample'){
            total_sample[0].textContent="x";
            total_sample[0].style.background='#adff2f';
            total_sample[0].style.color='#000000';
            total_sample[0].style.height='30px';
            total_sample[0].style.fontWeight = 'bold';
            total_sample[0].disabled = true;
            this._rpc({
                    model: 'a.wizard.quarter.total.sample',
                    method: 'get_total_sample',
                    args: [[1]],
                    }).then(function (result) {
                    total_sample[0].textContent= "Total Sample = " + result;
                    });
            wizard_date[0].textContent="x";
            wizard_date[0].style.background='#adff2f';
            wizard_date[0].style.color='#000000';
            wizard_date[0].style.height='30px';
            wizard_date[0].style.fontWeight = 'bold';
            wizard_date[0].disabled = true;
            this._rpc({
                    model: 'a.wizard.quarter.total.sample',
                    method: 'get_wizard_date',
                    args: [[1]],
                    }).then(function (result) {
                    wizard_date[0].textContent= result;
                    });
            }
            else{
            if(total_sample[0]){
            total_sample[0].style.display = "none";
            }
            if(wizard_date[0]){
            wizard_date[0].style.display = "none";
            }
            }

    }
});
});